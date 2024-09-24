from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    user_id = models.PositiveIntegerField(unique=True, null=True, blank=True)  # New user_id field

    def save(self, *args, **kwargs):
        if not self.user_id:  # Check if the user_id is not already assigned
            self.user_id = self._generate_unique_user_id()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_unique_user_id():
        # Find the smallest available user_id starting from 1
        existing_ids = set(User.objects.values_list('user_id', flat=True))
        new_id = 1
        while new_id in existing_ids:
            new_id += 1
        return new_id

    def __str__(self):
        return self.username
