from rest_framework import serializers
from .models import Article
from authors.apps.authentication.models import User
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
         "tagList","createdAt","updatedAt","favorited","favoritesCount", "author")

    @staticmethod
    def convert_tagList_to_str(request_data={}):
        modified_data = request_data
        if modified_data.get('tagList', None):
           modified_data['tagList'] = str(request_data['tagList'])
        return modified_data

    # @staticmethod
    # def convert_tagList_str_to_list(data={}):
    #     modified_data = data
    #     if modified_data.get('tagList', None): 
    #        modified_data['tagList'] = literal_eval(data['tagList'])
    #     return modified_data

    
        

