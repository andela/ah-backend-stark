"""profile app serializer file"""
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """profile app serializer class"""

    username = serializers.CharField(source='user.username')
    bio = serializers.CharField(allow_blank=True, required=False)
    location = serializers.CharField(allow_blank=True, required=False)
    fun_fact = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        """profile app serializer meta class"""
        model = Profile
        fields = ('username', 'bio', 'location', 'fun_fact', 'image')
        read_only_fields = ('username',)


class FollowingSerializer(serializers.ModelSerializer):
    """follower serializer class"""

    user = serializers.CharField(source='user')
    followed_by = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        """profile app serializer meta class"""
        model = Profile
        fields = ('user_id', 'follower_id')
