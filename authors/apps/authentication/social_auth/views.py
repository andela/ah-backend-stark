import os
import base64
from webbrowser import open as launch_browser
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse
from authors.apps.authentication.models import User
from django.http import HttpResponseRedirect
from authors.apps.authentication.models import User
from authors.apps.authentication.social_auth.helpers import (
    generate_unique_username, get_base64_str, add_user_to_queue,
    get_user_from_queue, pop_user_from_queue, set_redirect_url,
    get_redirect_url)


class LaunchSocialAuthAPIView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):

        protocol = request.scheme + '://'
        site_url = request.get_host()
        social_path = self.set_social_path(request)
        resolved_url = self.set_resolved_url(social_path)
        social_login_url = ''
        set_redirect_url(request)

        social_login_url = protocol + site_url + resolved_url

        return HttpResponseRedirect(social_login_url)

    def set_social_path(self, request):
        provider = request.query_params.get('Provider')
        redirect_url = get_redirect_url()
        social_path = str(request.path).lower()
        if redirect_url:
            social_path = provider.lower()

        return social_path

    def set_resolved_url(self, social_path):
        resolved_url = ''

        if social_path in ('/api/auth/google/', 'google'):
            resolved_url = reverse('social:begin', args=['google-oauth2'])

        elif social_path in ('/api/auth/facebook/', 'facebook'):
            resolved_url = reverse('social:begin', args=['facebook'])

        else:
            if social_path in ('/api/auth/twitter/', 'twitter'):
                resolved_url = reverse('social:begin', args=['twitter'])

        return resolved_url


class AuthenticateSocialLogin(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        token = get_user_from_queue().get('token', '')
        email = get_user_from_queue().get('email', '')
        username = get_user_from_queue().get('username', '')

        resp_data = {
            'message': 'Your social authentication was successful',
            'username': username,
            'email': email,
            'Token': token
        }

        return self.redirect_if_true() or Response(resp_data,
                                                   status.HTTP_200_OK)

    def redirect_if_true(self):
        encoded_data = self.get_redirection_data()
        redirect_url = get_redirect_url()
        pop_user_from_queue()

        if redirect_url:
            return HttpResponseRedirect(redirect_url + encoded_data)

    def get_redirection_data(self):
        token = get_user_from_queue().get('token', '')
        email = get_user_from_queue().get('email', '')
        username = get_user_from_queue().get('username', '')

        param_string = "?t=" + get_base64_str(token)
        param_string += "&e=" + get_base64_str(email)
        param_string += "&u=" + get_base64_str(username)
        param_string += "&end="

        return param_string


def create_social_user(*args, **kwargs):
    """
    This function is called within the social django pipeline
    to create users
    """
    details = kwargs['details']

    email = details['email']
    username = generate_unique_username(details['username'])
    password = email + 'Ah' + str(len(email))
    token = ''

    user = User.objects.filter(email=email).first()
    if user:
        token = user.token()
        username = user.username

    else:

        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.is_verified = True
        user.save()

        token = user.token()

    add_user_to_queue(username, email, token)
