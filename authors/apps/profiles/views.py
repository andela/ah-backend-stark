"""views for profile app"""
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer
from .exceptions import ProfileDoesNotExist


class UserProfile(RetrieveUpdateAPIView):
    """Profile views class"""
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):

        """ function to retrieve user profile information """
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username)

        except:
            raise ProfileDoesNotExist

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """User profile update information """
        param_name = self.kwargs["username"]
        active_user = request.user.username
        if param_name == active_user:
            user_data = request.data.get('profile', {})

            serializer_data = {
                'username': user_data.get('username', request.user.username),
                'bio': user_data.get('bio', request.user.profile.bio),
                'location': user_data.get(
                    'location', request.user.profile.location),
                'fun_fact': user_data.get(
                    'fun_fact', request.user.profile.fun_fact),
                'image': user_data.get('image', request.user.profile.image)
            }

            serializer = self.serializer_class(
                request.user.profile, data=serializer_data,
                context={'request': request}, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.update(request.user.profile, serializer_data)

            try:
                serializer.update(request.user, serializer_data)
            except:
                return Response(
                    {"error": "Username or email already exist, " +
                        "create a unique one"},
                    status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "You can only update your own profile"},
                status.HTTP_400_BAD_REQUEST)


class ListProfiles(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):

        """ function to retrieve user profile information """

        users = Profile.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(
            {"Authors": serializer.data},
            status=status.HTTP_200_OK)
