from django.contrib import admin
from .models import Post, Like, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at', 'likes_count', 'comments_count')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__content')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')  # Changed 'author' to 'user'
    search_fields = ('user__username', 'post__content')
    list_filter = ('created_at',)

# Register models with their respective admin classes
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
