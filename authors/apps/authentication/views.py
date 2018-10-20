from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .backends import JWTAuthentication
from .renderers import UserJSONRenderer
from .send_email import send_email
from .serializers import (LoginSerializer, RegistrationSerializer,
                          UserSerializer, ResetPasswordSerializer)
from .models import User
from .validation import validate
from django.http import HttpResponseRedirect
import base64


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        redirect_url = request.META.get('HTTP_REDIRECTTO', '')
        validate(user)

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipient = serializer.data['email']
        subject = 'Activate Authors Haven Account'

        protocol = request.scheme + '://'
        host = protocol + request.get_host()
        url = '/api/users/activate_account/'
        token = serializer.data['token']

        encoded_url = str(base64.b64encode(bytes(redirect_url, 'utf-8')))
        encoded_url = encoded_url[2:-1]  # remove b''
        redirect_str = token + "$" + str(encoded_url)
        content = "Thank you for registering with Authors Haven.\
        Follow this link to activate your account {}{}{}/".format(
            host, url, token)

        if redirect_url:
            content = "Thank you for registering with Authors Haven.\
            Follow this link to activate your account {}{}{}/".format(
                host, url, redirect_str)

        send_email(recipient, subject, content)
        user_data = serializer.data
        user_data.update({
            "message":
            "User successfully registered. " +
            "Check your email to activate account"
        })

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = User.serialize(request, self.serializer_class)

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('profile', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        recipient = serializer.data['email']
        subject = 'Password For Authors Haven Account'
        host = 'https://ah-frontend-stark.herokuapp.com'
        url = '/password-reset/done/'
        content = "Follow this link to Reset\
        your account password {}{}".format(
            host, url
        )
        print(content)
        send_email(recipient, subject, content)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def retrieve(self, request, token, *args, **kwargs):
        """this allows one to retrive the token from the end point
        """
        msg = {
            'message': 'this token is valid for a small amount of time',
            'token': token
        }
        return Response(msg, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {'message': 'Your password has been updated'}
        return Response(msg, status=status.HTTP_200_OK)


class VerifyAccountAPIView(APIView, JWTAuthentication):
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer

    # function to retrieve user info from the token
    def get(self, request, token):
        redirect_url = ''
        cleantoken = token
        if '$' in str(token):
            redirect_url = str(base64.b64decode((token.rsplit('$', 1)[1])))
            redirect_url = redirect_url[2:-1]
            cleantoken = str((token.rsplit('$')[0]))
        try:

            user, token = self.get_verification_credencials(
                request, cleantoken)

            if not user.is_verified:
                user.is_verified = True
                user.save()

                if redirect_url:
                    return HttpResponseRedirect(redirect_url)

                return Response({
                    "message":
                    "Your account has been successfully " +
                    "activated. Complete profile",
                    "token":
                    token
                },
                    status=status.HTTP_200_OK)

            if redirect_url:
                return HttpResponseRedirect(redirect_url)

            return Response(
                {
                    "message": "Account already activated. Please login"
                },
                status=status.HTTP_200_OK)

        except Exception as e:
            if redirect_url:
                return HttpResponseRedirect(redirect_url)

            return Response({
                "message":
                "Sorry. Activation link " + "either expired or is invalid"
            },
                status=status.HTTP_400_BAD_REQUEST)
