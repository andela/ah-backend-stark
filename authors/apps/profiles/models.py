"""profile model file"""
from django.db import models


class Profile(models.Model):
    """user profile model"""
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    fun_fact = models.TextField(blank=True)
    location = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
