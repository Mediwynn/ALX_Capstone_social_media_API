from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

class UserTests(APITestCase):
    
    def setUp(self):
        """Set up a user for tests."""
        self.user_data = {
            'username': 'TestUser',
            'email': 'testuser@example.com',
            'password': 'password123',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
    
    def test_create_user(self):
        url = reverse('user-register')  # Adjust the URL name if necessary
        
        # Create valid data for user registration
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'bio': 'This is a bio',
            # Include other fields if necessary
        }
        
        # Send a POST request to create a user
        response = self.client.post(url, data, format='json')
        
        # Check that the status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_deletion(self):
        """Test user deletion via API."""
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        url = f'/api/users/delete/{self.user.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
