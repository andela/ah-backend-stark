from django.urls import path

from .views import (ArticleCreationAPIView, GetSingleArticleAPIView,
                    PostCommentApiView, CommentDetailApiView,
                    RateArticleAPIView, LikeView, SearchArticleView)
from .views_favourites import (FavouriteView, GetFavouriteView)
urlpatterns = [
    path('articles/', ArticleCreationAPIView.as_view()),
    path('articles/<str:slug>', GetSingleArticleAPIView.as_view()),
    path('articles/<str:slug>/comments/', PostCommentApiView.as_view()),
    path('articles/<str:slug>/comments/<int:id>/',
         CommentDetailApiView.as_view()),
    path('articles/<str:slug>/rate_article/', RateArticleAPIView.as_view()),
    path('articles/<str:slug>/like/', LikeView.as_view()),
    path('articles/<str:slug>/favourite/', FavouriteView.as_view()),
    path('articles/favourites/', GetFavouriteView.as_view()),
    path('articles/search/', SearchArticleView.as_view()),
]
