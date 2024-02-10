from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Blog
import faker

class Command(BaseCommand):
    help = 'Generates a large number of blog posts'

    def handle(self, *args, **kwargs):
        fake = faker.Faker()
        users = User.objects.all()
        if not users:
            print("No users found. Please create some users first.")
            return
        for user in users:
            blog, created = Blog.objects.get_or_create(owner=user)
            for _ in range(100):
                Post.objects.create(
                    blog=blog,
                    title=fake.sentence(),
                    text=fake.text(max_nb_chars=140),
                )
        print("Posts generated successfully.")
