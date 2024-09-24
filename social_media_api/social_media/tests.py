from django.test import TestCase

# Create your tests here.

# social_media/tests.py
from django.test import TestCase
from .models import User, Post, Follower

class UserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')

class PostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(content='Hello World!', user=self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.content, 'Hello World!')
        self.assertEqual(self.post.user, self.user)
