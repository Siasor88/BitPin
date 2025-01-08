import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from models.Post import Post


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_id = models.ForeignKey(Post, related_name='ratings', on_delete=models.CASCADE)
    user_id = models.UUIDField()  # Assuming user identification is handled externally
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    corrupted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('post_id', 'user_id')
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user_id']),
        ]

    def __str__(self):
        return f'Rating {self.rating} for Post {self.post_id.title} by User {self.user_id}'