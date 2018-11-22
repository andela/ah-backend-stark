from django.shortcuts import get_object_or_404
from rest_framework import status, serializers, exceptions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated, AllowAny)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (UpdateAPIView, CreateAPIView,
                                     RetrieveAPIView, ListAPIView)
from .renderers import ArticleJSONRenderer, LikesJSONRenderer
from .serializers import (ArticlesSerializer, CommentSerializer,
                          CommentDetailSerializer, LikeSerializer,
                          ArticlesReadSerializer)
from .models import Article, Comment, Likes, ArticlesRead
from authors.apps.profiles.serializers import ProfileSerializer
from authors.apps.profiles.models import Profile
from authors.apps.authentication.backends import JWTAuthentication
from .mixins import AhPaginationMixin


class ArticleCreationAPIView(APIView, AhPaginationMixin):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = ArticlesSerializer
    pagination_class = LimitOffsetPagination
    profile_serializer_class = ProfileSerializer

    def get(self, request):
        article = Article.objects.all().order_by('-id')
        page = self.paginate_queryset(article)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            res_data = Article.format_data_for_display(serializer.data)
            new_data = self.get_paginated_response(res_data)
            return new_data

    def post(self, request):
        article = request.data.get('article')
        user = get_user_from_auth(request)
        article['author'] = user.id

        if Article.title_exists(user.id, article['title']):
            raise serializers.ValidationError(
                'You already have an article with the same title', 409)

        article = ArticlesSerializer.convert_tagList_to_str(article)
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        action = "increment"
        Profile.update_write_stats(request, self.profile_serializer_class,
                                   action)
        res_data = Article.format_data_for_display(serializer.data)
        return Response(res_data, status=status.HTTP_201_CREATED)


class GetSingleArticleAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (ArticleJSONRenderer, )
    serializer_class = ArticlesSerializer
    articles_read_serializer_class = ArticlesReadSerializer
    profile_serializer_class = ProfileSerializer

    def check_authenticated(self, request, user, slug, author):
        if user:
            if ArticlesRead.already_read(user, slug) or user == author:
                pass
            else:
                self.update_read_stats(user, request, slug)

    def update_read_stats(self, user, request, slug):
        """
        This method increments the articles_read field
        when a user reads an article
        """
        serializer_data = {"user": user, "slug": slug}
        read_serializer = self.articles_read_serializer_class(
            data=serializer_data)
        read_serializer.is_valid(raise_exception=True)
        read_serializer.save()
        field_str = "articles_read"
        user_id = request.user.id
        instance = Profile.objects.filter(user_id=user_id)
        username = instance.first()
        profile = Profile.objects.select_related('user').get(
            user__username=username)
        action = "increment"
        Profile.update_profile_stats(request, self.profile_serializer_class,
                                     profile.articles_read, field_str, action)

    def get(self, request, slug):
        article = Article.get_article(slug)
        if not article:
            raise exceptions.NotFound('The selected article was not found.')
        serializer = self.serializer_class(article)
        res_data = Article.format_data_for_display(serializer.data)
        user = request.user.id
        author = Article.get_single_article(slug)[0].author_id

        self.check_authenticated(request, user, slug, author)

        return Response({"article": res_data}, status.HTTP_200_OK)

    def put(self, request, slug):
        user = get_user_from_auth(request)
        new_article = request.data.get('article')
        status = Article.update_article(user.id, slug, new_article)

        if status[1] == 202:
            serializer = self.serializer_class(status[0])
            res_data = Article.format_data_for_display(serializer.data)
            return Response(res_data, 202)
        return Response({'message': status[0]}, status[1])

    def delete(self, request, slug):
        user = get_user_from_auth(request)
        status = Article.delete_article(user.id, slug)
        action = "decrement"
        Profile.update_write_stats(request, self.profile_serializer_class,
                                   action)
        return Response({'message': status[0]}, status[1])


class RateArticleAPIView(APIView):
    """
    This class contains the views regarding the article
    rating feature
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = ArticlesSerializer

    def get_values(self, queryset):
        """
        This method takes in the article queryset and
        returns a dictionary of the article's data
        """
        return queryset.values()[0]

    def validate_rating(self, rating):
        if rating not in list(range(1, 6)):
            raise exceptions.ParseError(
                "Sorry, only a rating in the 1-5 range can be given.")

    def put(self, request, slug):
        """
        This method rates an article and saves the updated
        rating and ratingsCount in the database
        """
        queryset = Article.objects.filter(slug=slug)
        article = self.get_values(queryset)
        if not queryset:
            raise exceptions.NotFound('The selected article was not found.')
        elif article.get("author_id") == get_user_from_auth(request).id:
            raise exceptions.ParseError(
                "Sorry, you cannot rate your own article.")

        serializer_instance = queryset.first()
        serializer_data = request.data.get('article', {})
        self.validate_rating(serializer_data.get("rating"))
        current_rating = article['rating']
        current_rating_count = article['ratingsCount']
        user_rating = serializer_data.get('rating')
        new_rating = Article.calculate_rating(
            current_rating, current_rating_count, user_rating)
        serializer_data["rating"] = new_rating["rating"]
        serializer_data["ratingsCount"] = new_rating["ratingsCount"]
        serializer = self.serializer_class(
            serializer_instance, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "article": serializer.data
        },
                        status=status.HTTP_202_ACCEPTED)


def get_user_from_auth(request):
    """
    This helper function returns an instance of the authenticated
    user and their token from the authentication class
    """
    auth = JWTAuthentication()
    user = auth.authenticate(request)[0]
    return user


class LikeView(CreateAPIView, UpdateAPIView):
    """like view class"""
    permission_classes = (IsAuthenticated, )
    renderer_classes = (LikesJSONRenderer, )
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        article = self.kwargs["slug"]
        self.article1 = get_object_or_404(Article, slug=article)
        if Likes.objects.filter(
                action_by=request.user, article=self.article1).exists():
            raise serializers.ValidationError(
                'you can only like or dislike an article once', 400)
        else:
            action = request.data.get('like', {})
            serializer = self.serializer_class(data=action)
            serializer.is_valid(raise_exception=True)
            serializer.save(action_by=self.request.user, article=self.article1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        article1 = self.kwargs["slug"]
        article = get_object_or_404(Article, slug=article1)
        try:
            instance = Likes.objects.get(
                action_by=request.user.id, article=article.id)
            action = request.data.get('like', {})
            serializer = self.serializer_class(
                instance, data=action, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            raise serializers.ValidationError(
                'cannot update'
                'like or dislike article', 400)


class PostCommentApiView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = CommentSerializer

    def get(self, request, slug):
        instance = get_object_or_404(Article, slug=slug)
        article = instance.id
        comment = Comment.objects.all().filter(article_id=article)
        serializer = self.serializer_class(comment, many=True)
        return Response({"comments": serializer.data}, status.HTTP_200_OK)

    def post(self, request, slug):
        comment = request.data.get("comment")
        instance = get_object_or_404(Article, slug=slug)
        user = get_user_from_auth(request)
        comment["user"] = user.id
        comment["article"] = instance.id
        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailApiView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = CommentDetailSerializer

    def get(self, request, slug, id):
        comment = Comment.objects.all().filter(id=id)
        serializer = self.serializer_class(comment, many=True)
        new_data = serializer.data
        for item in new_data:
            new_comment = self.format_dictionary(item)
        return Response({"comment": new_comment}, status.HTTP_200_OK)

    def format_dictionary(self, item):
        new_comment = dict(
            id=item["id"],
            body=item["body"],
            user=item["user"],
            timestamp=item["timestamp"],
            reply=item["replies"])
        return new_comment

    def post(self, request, slug, id):
        comment = request.data.get("reply")
        instance = get_object_or_404(Article, slug=slug)
        user = get_user_from_auth(request)
        comment["user"] = user.id
        comment["article"] = instance.id
        comment["parent_comment"] = id
        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        new_data = serializer.data
        new_comment = self.format_dictionary(new_data)
        return Response(new_comment, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete(request, slug, id):
        comment = Comment.objects.get(pk=id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchArticleView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ArticlesSerializer

    def get(self, request):
        search_params = request.query_params
        query_set = Article.objects.all()

        author = search_params.get('author', None)
        title = search_params.get('title', None)
        tag = search_params.get('tag', None)
        keywords = search_params.get('keywords', None)

        if author:
            query_set = query_set.filter(author__username=author)
        if title:
            query_set = query_set.filter(title__icontains=title)
        if tag:
            query_set = query_set.filter(tagList__icontains=tag)
        if keywords:
            words = str(keywords).split(',')
            final_queryset = ''
            for word in words:
                final_queryset = query_set.filter(title__icontains=word)
            query_set = final_queryset

        serializer = self.serializer_class(query_set, many=True)
        res_data = serializer.data
        if res_data:
            res_data = Article.format_data_for_display(res_data)

        return Response({"search results": res_data}, status.HTTP_200_OK)
