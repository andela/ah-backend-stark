from django.urls import path

from .views import (
    ArticleCreationAPIView, GetSingleArticleAPIView,
    PostCommentApiView, CommentDetailApiView, RateArticleAPIView, LikeView
)
urlpatterns = [
    path('articles/', ArticleCreationAPIView.as_view()),
    path('articles/<str:slug>', GetSingleArticleAPIView.as_view()),
    path('articles/<str:slug>/comments/', PostCommentApiView.as_view()),
    path('articles/<str:slug>/comments/<int:id>/',
         CommentDetailApiView.as_view()),
    path('articles/<str:slug>/rate_article/', RateArticleAPIView.as_view()),
    path('articles/<str:slug>/like/', LikeView.as_view()),

]
