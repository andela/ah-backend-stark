from django.contrib.auth import authenticate
from django.template.defaultfilters import slugify

from rest_framework import serializers

from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    """ Handles the serialization and deserialization of Article objects"""
    id = serializers.IntegerField(read_only=True)
    title=serializers.CharField(required=True, max_length=255)
    #slug = serializers.SlugField()
    description = serializers.CharField(max_length=500)
    body = serializers.CharField()
    

    def create(self,validated_data):
        """
        Create and return a new article instance given the validated data 
        """
        return Article.objects.create(**validated_data)


    
    class Meta:
        model = Article
        fields = ("id","title","description","body","tagList","author")
