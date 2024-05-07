from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", related_name="followers")
    liked_posts = models.ManyToManyField("Post", related_name="likes")


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    content = models.TextField(max_length=1024)
    timestamp = models.DateTimeField()
