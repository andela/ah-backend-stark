from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    ResetPasswordSerializer 
)
from .serializers import (LoginSerializer, RegistrationSerializer,
                          UserSerializer)
from .validation import validate

from .send_email import send_mail
from .backends import JWTAuthentication


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        validate(user)

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipient = serializer.data['email']
        subject = 'Activate Authors Haven Account'
        host = 'http://' + request.get_host()
        url = '/api/users/activate_account/'
        token = serializer.data['token']
        content = "Thank you for registering with Authors Haven.\
        Follow this link to activate your account {}{}{}/".format(host, url, token)
        
        send_mail(recipient, subject, content)
        user_data = serializer.data
        user_data.update({
            "message": "User successfully registered. Check your email to activate account"
        })
    
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
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
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class ResetPasswordView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


    def retrieve(self, request, token, *args, **kwargs):
        """this allows one to retrive the token from the end point
        """
        msg = {'message': 'a link has been sent to your email', 'token': token}
        return Response(msg, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {'message': 'Your password has been updated'}
        return Response(msg, status=status.HTTP_200_OK)

class VerifyAccountAPIView(APIView, JWTAuthentication):
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    # function to retrieve user info from the token
    def get(self, request, token):
        try:
            user, token = self.get_verification_credencials(request, token)
            
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    "message": "Your account has been successfully activated. Complete profile" ,
                    "token": token 
                }, status=status.HTTP_200_OK)
            
            return Response({
                "message": "Account already activated. Please login"
            }, status=status.HTTP_200_OK)
        
        except:
            return Response({
                "message": "Sorry. Activation link either expired or is invalid"
            }, status=status.HTTP_400_BAD_REQUEST)

