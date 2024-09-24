from django.contrib import admin

# Register your models here.

from .models import User, Post, Follower

# Customizing the admin interface for the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

# Customizing the admin interface for the Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')
    search_fields = ('content',)
    list_filter = ('user', 'timestamp')
    ordering = ('-timestamp',)

# Customizing the admin interface for the Follower model
@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('follower', 'following')
    ordering = ('-created_at',)

# Optional: Sample data for testing purposes
def create_sample_data():
    # Create sample users
    user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password123', bio='This is user 1.')
    user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password123', bio='This is user 2.')
    user3 = User.objects.create_user(username='user3', email='user3@example.com', password='password123', bio='This is user 3.')

    # Create sample posts
    Post.objects.create(content='Hello from user 1!', user=user1)
    Post.objects.create(content='Hello from user 2!', user=user2)
    Post.objects.create(content='Hello from user 3!', user=user3)

    # Create sample follower relationships
    Follower.objects.create(follower=user1, following=user2)
    Follower.objects.create(follower=user1, following=user3)
    Follower.objects.create(follower=user2, following=user3)

# Uncomment the following line to create sample data when the admin is loaded
# create_sample_data()
