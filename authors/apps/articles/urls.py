from django.urls import path
from django.conf.urls import include

from .views import ArticleAPIView

urlpatterns = [
    path('articles/',ArticleAPIView.as_view()),
]
