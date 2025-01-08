from celery import shared_task
from django.core.exceptions import ValidationError

from Bitpin.celery import app
from models.Post import Post
from models.Rating import Rating
from django.db import transaction
from django.core.cache import cache

from models.serializers.RatingSerializer import RatingSerializer

VOTE_THRESHOLD = 1000  # Could be added to the projects meta data file
DISCOUNT_FACTOR = 0.5  # Could be added to the projects meta data file
SIGNIFICANCE_THRESHOLD = 2  # Could be added to the projects meta data file


def validate_data(rating_data):
    serializer = RatingSerializer(data=rating_data)
    if serializer.is_valid():
        serializer.save()
    else:
        raise ValidationError(serializer.errors)


@shared_task
def process_rating(rating_data):
    validate_data(rating_data)
    post_id = rating_data['post_id']
    user_id = rating_data['user_id']
    rating_value = rating_data['rating']

    try:
        # Store the latest rating per user in cache to act as a buffer
        cache_key = f'post_{post_id}_user_{user_id}'
        cache.set(cache_key, rating_value, timeout=300)  # Buffer for 5 minutes

        # Optionally, maintain a separate cache key for buffered ratings
    except Exception as e:
        # Handle exceptions
        pass


def get_post_ratings(post_id):
    pattern = f'post_{post_id}_user_*'
    keys = cache.keys(pattern)
    user_ratings = {}
    for key in keys:
        user_id = key.decode().split('_')[-1]
        rating = cache.get(key)
        if rating is not None:
            user_ratings[user_id] = rating
    return user_ratings


def get_rating_avg(user_ratings):
    rating_sum = 0
    count_rates = max(len(user_ratings.items()), 1)
    for _, rating in user_ratings.items():
        rating_sum += rating
    return rating_sum / count_rates


def are_ratings_corrupted(user_ratings, post):
    if post.rating_count > VOTE_THRESHOLD:
        new_votes_avg = get_rating_avg(user_ratings)
        return (post.average_rating - new_votes_avg) > SIGNIFICANCE_THRESHOLD
    return False


def handle_rating(post, user_id, new_rating, alpha, corrupted):
    try:
        rating_obj = Rating.objects.get(post_id=post.post_id, user_id=user_id)
        beta = 1 if not rating_obj.corrupted else DISCOUNT_FACTOR

        old_rating = rating_obj.rating
        rating_obj.rating = new_rating
        rating_obj.corrupted = corrupted
        rating_obj.save()
        new_rating_sum = post.average_rating * post.rating_count - beta * old_rating + alpha * new_rating
        post.average_rating = new_rating_sum / post.rating_count
    except Rating.DoesNotExist:
        Rating.objects.create(post_id=post.id, user_id=user_id, rating=new_rating, corrupted=corrupted)
        post.rating_count += 1
        post.average_rating = ((post.average_rating * post.rating_count) + alpha * new_rating) / (post.rating_count + 1)


@shared_task
def update_post_aggregates(post_id):
    user_ratings = get_post_ratings(post_id)

    try:
        with transaction.atomic():
            post = Post.objects.select_for_update().get(id=post_id)
            corrupted = are_ratings_corrupted(user_ratings, post)
            alpha = 1 if not corrupted else DISCOUNT_FACTOR

            for user_id, new_rating in user_ratings.items():
                handle_rating(post, user_id, new_rating, alpha, corrupted)
            post.save()

            # Invalidate cache
            cache.delete_pattern(f'post_{post_id}_user_*')

    except Post.DoesNotExist:
        # Handle Error!
        pass


@shared_task
def update_post_aggregates_task():
    posts = Post.objects.all()
    for post in posts:
        update_post_aggregates.delay(str(post.id))
