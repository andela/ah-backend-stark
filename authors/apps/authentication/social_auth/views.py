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
from authors.apps.authentication.helpers import (
    get_env_variable, set_social_env_variable, generate_unique_username,
    get_base64_str, unset_social_variables)


class LaunchSocialAuthAPIView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):

        unset_social_variables()
        redirect_url = self.get_redirect_url(request)
        protocol = request.scheme + '://'
        site_url = request.get_host()
        social_path = self.set_social_path(request)
        resolved_url = self.set_resolved_url(social_path)
        social_login_url = ''

        social_login_url = protocol + site_url + resolved_url

        if redirect_url:
            set_social_env_variable('redirect_url', redirect_url)
        return HttpResponseRedirect(social_login_url)


    def set_social_path(self, request):
        provider = request.query_params.get('Provider', '')
        redirect_url = self.get_redirect_url(request)
        social_path = request.get_full_path().lower()
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

    def get_redirect_url(self, request):
        redirect_url = ''
        social_url = request.query_params.get('RedirectTo', '')
        redirect_url = request.META.get('HTTP_REDIRECTTO', social_url)

        return redirect_url


class AuthenticateSocialLogin(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        token = get_env_variable('social_user_token')
        email = get_env_variable('social_user_email')
        username = get_env_variable('social_user_username')

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
        redirect_url = get_env_variable('social_redirect_url').strip()
        if redirect_url:
            return HttpResponseRedirect(redirect_url + encoded_data)

    def get_redirection_data(self):
        token = get_env_variable('social_user_token')
        email = get_env_variable('social_user_email')
        username = get_env_variable('social_user_username')

        param_string = "?t=" + get_base64_str(token)
        param_string += "&e=" + get_base64_str(email)
        param_string += "&u=" + get_base64_str(username)
        param_string += "&end="

        return param_string
