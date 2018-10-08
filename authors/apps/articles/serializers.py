from rest_framework import serializers
from .models import Article
from authors.apps.authentication.backends import JWTAuthentication
from ast import literal_eval

    
class ArticlesSerializer(serializers.ModelSerializer):
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
        fields = ("slug","title", "description", "body",
         "tagList","createdAt","updatedAt","favorited","favoritesCount", "rating", "ratingsCount", "author")

    @staticmethod
    def convert_tagList_to_str(request_data={}):
        modified_data = request_data
        if modified_data.get('tagList', None):
           modified_data['tagList'] = str(request_data['tagList'])
           
        return modified_data
    
    def update(self, instance, validated_data):
        """
        This method assigns the data in `validated_data` to
        the instance of the Article.
        """
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
