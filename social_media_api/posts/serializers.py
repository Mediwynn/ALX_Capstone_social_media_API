from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'updated_at', 'media']
        read_only_fields = ['author', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'user', 'created_at']
        read_only_fields = ['post', 'user']
