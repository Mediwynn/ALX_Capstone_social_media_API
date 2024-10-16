from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from posts.models import Post

class PostTests(APITestCase):

    def setUp(self):
        # Create a user and log in
        self.user = get_user_model().objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        
        # Create a post data for the tests
        self.post_data = {
            'author': self.user.id,
            'content': 'This is a test post',
        }
        
        # Create a post to use in other tests
        self.post = Post.objects.create(**self.post_data)

    def test_create_post(self):
        url = reverse('post-create')  # Adjust the URL name as needed
        response = self.client.post(url, self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_post(self):
        """Test reading a post via the API."""
        url = reverse('post_detail', args=[self.post.id])  # Corrected URL name for post detail
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        """Test post deletion via the API."""
        url = reverse('delete_post', args=[self.post.id])  # Corrected URL name for post deletion
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
