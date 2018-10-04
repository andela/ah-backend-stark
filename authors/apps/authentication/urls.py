from django.urls import path
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ResetPasswordView, ResetPasswordView, ChangePasswordView,
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, VerifyAccountAPIView
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('password-reset/', ResetPasswordView.as_view()),
    path('password-reset/<str:token>/', ResetPasswordView.as_view()),
    path('password/reset/done/', ChangePasswordView.as_view()),
    path('users/activate_account/<str:token>/', VerifyAccountAPIView.as_view())
]
