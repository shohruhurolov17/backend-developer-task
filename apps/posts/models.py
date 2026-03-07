from django.db import models
from django.contrib.auth.models import User

class PostCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):

    category = models.ForeignKey(
        PostCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts"
    )

    title = models.CharField(max_length=255)

    body = models.TextField()



class PostComment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    text = models.TextField()