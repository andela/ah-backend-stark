from django.db.models.signals import post_save
from django.dispatch import receiver
from authors.apps.profiles.models import Profile
from authors.apps.authentication.models import User


@receiver(post_save, sender=User)
def build_profile_on_user_creation(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
