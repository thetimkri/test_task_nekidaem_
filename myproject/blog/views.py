from rest_framework import viewsets
from .models import Blog,Post,Subscription,ReadPost
from .serializers import BlogSerializer,PostSerializer,SubscriptionSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_as_read(self, request, pk=None):
        post = self.get_object()
        user = request.user
        ReadPost.objects.get_or_create(user=user, post=post)
        return Response({'status': 'post marked as read'}, status=status.HTTP_200_OK)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class UserFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get_queryset(self):
        user = self.request.user
        subscribed_blogs = Subscription.objects.filter(subscriber=user).values_list('blog', flat=True)
        queryset = Post.objects.filter(blog__in=subscribed_blogs).order_by('-created_at')[:500]
        return queryset
