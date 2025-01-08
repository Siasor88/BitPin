import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField()
    rating_count = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00,
                                         validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]

    def __str__(self):
        return self.title
