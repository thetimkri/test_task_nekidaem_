from celery import shared_task
from django.db.models import Prefetch
from .models import Post, Subscription

@shared_task
def print_latest_posts():
    posts = Post.objects.order_by('-created_at')[:5]
    for post in posts:
        print(f"{post.title}: {post.text[:50]}...")
