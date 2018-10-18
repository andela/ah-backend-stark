"""profile app url file"""
from django.urls import path
from .views import UserProfile, ListProfiles, UserFollow, UserUnfollow, UserFollowers, UserFollowing

urlpatterns = [
    path('profile/<str:username>/', UserProfile.as_view()),
    path('profiles/', ListProfiles.as_view()),
    path('profile/<str:username>/followers/', UserFollowers.as_view()),
    path('profile/<str:username>/following/', UserFollowing.as_view()),
    path('profile/<str:username>/follow/', UserFollow.as_view()),
    path('profile/<str:username>/unfollow/', UserUnfollow.as_view())
]
