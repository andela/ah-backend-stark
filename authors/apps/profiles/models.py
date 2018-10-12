"""profile model file"""
from django.db import models
from authors.apps.authentication.models import User


class Profile(models.Model):
    """user profile model"""
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    fun_fact = models.TextField(blank=True)
    location = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Following(models.Model):
    """
    user followers model
    """
    user = models.ManyToManyField(User)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    following_id = models.TextField()
    
    def __str__(self):
        return self.user.username
    
    def check_following(user, following):
        queryset = Following.object.filter(
                    user=user_id, 
                    following_id=following)
        return queryset.exists()