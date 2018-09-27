from django.contrib.auth import authenticate
from django.template.defaultfilters import slugify

from rest_framework import serializers

from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    """ 
    Handles the serialization and deserialization of Article objects
    """

    def create(self,validated_data):
        """
        Create and return a new article instance given the validated data 
        """
        return Article.objects.create(**validated_data)
 
    class Meta:
        model = Article
        fields = ("title", "description", "body", "tagList", "author")
