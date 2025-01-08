from rest_framework import serializers
from rating_app.models.Rating import Rating


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=0, max_value=5)

    class Meta:
        model = Rating
        fields = ['id', 'post_id', 'user_id', 'rating', 'created_at', 'updated_at', 'corrupted']
        read_only_fields = ['id', 'created_at', 'updated_at']

