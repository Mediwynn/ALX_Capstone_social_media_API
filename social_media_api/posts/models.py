from django.db import models

# Create your models here.

from users.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media = models.ImageField(upload_to='posts_media/', null=True, blank=True)

    def __str__(self):
        return self.content[:20]
