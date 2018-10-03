"""profile app url file"""
from django.urls import path
from .views import  UserProfile

urlpatterns = [
    path('profiles/<str:username>/', UserProfile.as_view()),
    path('profile/update/', UserProfile.as_view()),
]
