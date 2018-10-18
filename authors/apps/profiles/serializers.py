"""profile app serializer file"""
from rest_framework import serializers
from .models import Profile, Following


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
        read_only_fields = ('username', )


class FollowingSerializer(serializers.ModelSerializer):
    """
    serializer class for followers
    """

    class Meta:
        """profile app serializer meta class"""
        model = Following
        fields = ('user', 'following_id')

    def create(self, validated_data):
        """
        Create and return a new article instance given the validated data 
        """
        return Following.objects.create(**validated_data)
