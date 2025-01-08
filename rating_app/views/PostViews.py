from rest_framework import generics
from rating_app.models.Post import Post
from rating_app.models.serializers.PostSerializer import PostSerializer
from rest_framework.pagination import PageNumberPagination


class PostPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')  # Adjust ordering as necessary
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Assuming user ID is passed via headers for simplicity
        context['user_id'] = self.request.headers.get('X-User-ID')
        return context
