from django.urls import path

from .views import ArticleCreationAPIView, GetSingleArticleAPIView

urlpatterns = [
    path('articles/',ArticleCreationAPIView.as_view()),
    path('articles/<str:slug>',GetSingleArticleAPIView.as_view())
]
