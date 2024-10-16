from django.db import models
from users.models import User
from django.contrib.auth import get_user_model

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media = models.ImageField(upload_to='posts_media/', null=True, blank=True)
    
    # New fields for likes and comments
    likes_count = models.PositiveIntegerField(default=0)  # Tracks the number of likes
    comments_count = models.PositiveIntegerField(default=0)  # Tracks the number of comments

    def __str__(self):
        return self.content[:20]

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    