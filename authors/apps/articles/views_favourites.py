from rest_framework import status, serializers, exceptions
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, RetrieveAPIView)
from .renderers import LikesJSONRenderer
from .serializers import (FavouriteSerializer, GetFavouriteSerializer)
from django.shortcuts import get_object_or_404
from .models import Article, Comment, Likes, Favourite


class GetFavouriteView(RetrieveAPIView):
    """This class handles getting favourite articles"""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (LikesJSONRenderer, )
    serializer_class = GetFavouriteSerializer

    def retrieve(self, request, *args, **kwargs):
        data1 = Favourite.objects.all().prefetch_related('article').filter(
            user=request.user.id)
        serializer = self.serializer_class(data1, many=True)
        return Response({
            "favourites": serializer.data
        },
                        status=status.HTTP_200_OK)


class FavouriteView(APIView):
    """This class handles favourating and unfavourating articles"""

    permission_classes = (IsAuthenticated, )
    renderer_classes = (LikesJSONRenderer, )
    serializer_class = FavouriteSerializer

    def post(self, request, slug):
        """This method adds an article to favourites"""
        article = get_object_or_404(Article, slug=slug)
        if Favourite.objects.filter(
                user=request.user, article=article).exists():
            raise serializers.ValidationError(
                "You have already favourited " + "this article", 400)
        else:
            request.data["user"] = request.user.id
            request.data["article"] = article
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user, article=article)
            return Response(
                {
                    "message": "Article successfully " + "added to favorites"
                },
                status=status.HTTP_201_CREATED)

    def delete(self, request, slug):
        """This method deletes an article from favourites"""
        article = get_object_or_404(Article, slug=slug)
        try:
            instance = Favourite.objects.get(
                user=request.user.id, article=article.id)
            instance.delete()
            return Response({
                "status": "successfully removed from favourites"
            },
                            status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "error": "Article not in favourite list"
            },
                            status=status.HTTP_400_BAD_REQUEST)
