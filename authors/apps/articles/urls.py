from django.urls import path
from django.conf.urls import include

from .views import ArticleCreationAPIView

urlpatterns = [
    path('articles/',ArticleCreationAPIView.as_view()),
    #path('articles/<str:slug>')
]
