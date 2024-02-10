from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Blog(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog')
    title = models.CharField(max_length=255, default="My Personal Blog")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} by {self.owner.username}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(owner=instance)


class Post(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
