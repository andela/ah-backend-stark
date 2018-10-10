"""profile app url file"""
from django.urls import path
from .views import  UserProfile,ListProfiles

urlpatterns = [
    path('profile/<str:username>/', UserProfile.as_view()),
    path('profiles/', ListProfiles.as_view()),
]
