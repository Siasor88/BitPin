# posts/views.py
from rest_framework import generics, status
from rest_framework.response import Response

from models.Post import Post
from models.serializers.RatingSerializer import RatingSerializer
from kafka_agents.producer import send_rating


class SubmitRatingView(generics.GenericAPIView):
    serializer_class = RatingSerializer

    def post(self, request, post_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_value = serializer.validated_data['rating']
        user_id = request.headers.get('X-User-ID')  # For simplicity; adjust as needed

        if not user_id:
            return Response({'error': 'User ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Post.objects.filter(post_id=post_id).exists():
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        rating_data = {
            'post_id': str(post_id),
            'user_id': str(user_id),
            'rating': rating_value
        }

        send_rating(rating_data)

        return Response({'status': 'Rating submitted successfully.'}, status=status.HTTP_202_ACCEPTED)
