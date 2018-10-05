from django.urls import path

from .views import ArticleCreationAPIView, GetSingleArticleAPIView, RateArticleAPIView

urlpatterns = [
    path('articles/',ArticleCreationAPIView.as_view()),
    path('articles/<str:slug>',GetSingleArticleAPIView.as_view()),
    path('articles/<str:slug>/rate_article/',RateArticleAPIView.as_view())
]