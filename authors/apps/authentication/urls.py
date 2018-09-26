from django.urls import path
from django.conf.urls import include
from authors.apps.articles.views import ArticleCreationAPIView
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('articles/',ArticleCreationAPIView.as_view()),
]
