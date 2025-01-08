from rest_framework import serializers
from rating_app.models.Post import Post
from rating_app.models.Rating import Rating


class PostSerializer(serializers.ModelSerializer):
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'rating_count', 'average_rating']

    def get_user_rating(self, obj):
        user_id = self.context.get('user_id')
        if user_id:
            try:
                rating = obj.ratings.get(user_id=user_id)
                return rating.rating
            except Rating.DoesNotExist:
                return None
        return None
