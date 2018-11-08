from rest_framework import serializers
from .models import Article, Likes, Comment, Favourite
from authors.apps.authentication.backends import JWTAuthentication
from ast import literal_eval


class ArticlesSerializer(serializers.ModelSerializer):
    """
    Handles the serialization and deserialization of Article objects
    """

    def create(self, validated_data):
        """
        Create and return a new article instance given the validated data
        """
        return Article.objects.create(**validated_data)

    class Meta:
        model = Article
        fields = ("slug", "title", "description", "body", "image", "tagList",
                  "createdAt", "updatedAt", "favoritesCount", "rating",
                  "ratingsCount", "author", "likes", "dislikes")

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


class LikeSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='action_by.username')
    article = serializers.ReadOnlyField(source='article.slug')

    class Meta:
        model = Likes
        fields = ("username", "action", "article")


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ("id", "user", "body", "article",
                  "timestamp", "username")


class ChildCommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ("id", "body", "timestamp", "username")


class CommentDetailSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "user", "body", "article",
                  "timestamp", "replies", "parent_comment", "username")

    @staticmethod
    def get_replies(obj):
        if obj.is_parent:
            return ChildCommentSerializer(obj.children(), many=True).data
        return None


class FavouriteSerializer(serializers.ModelSerializer):
    """This serializer class handles favourites """

    username = serializers.ReadOnlyField(source='user.username')
    article = serializers.ReadOnlyField(source='article.slug')

    class Meta:
        """Favourite serializer meta class"""
        model = Favourite
        fields = ("username", "article")


class GetFavouriteSerializer(serializers.ModelSerializer):
    """This serializer class handles getting favourites"""

    title = serializers.CharField(source='article.title')
    slug = serializers.CharField(source='article.slug')
    description = serializers.CharField(source='article.description')

    class Meta:
        """get favourite serializer meta class"""
        model = Favourite
        fields = ("title", "slug", "description")
