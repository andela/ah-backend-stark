"""views for profile app"""
from rest_framework import status, exceptions
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer
from .exceptions import ProfileDoesNotExist

# from authors.apps.articles.views import get_user_from_auth


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

        user_data = request.data.get('profile', {})

        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'bio': user_data.get('bio', request.user.profile.bio),
            'location': user_data.get('location', request.user.profile.location),
            'fun_fact': user_data.get('fun_fact', request.user.profile.fun_fact),
            'image': user_data.get('image', request.user.profile.image)
        }

        serializer = self.serializer_class(
            request.user.profile, data=serializer_data, context={'request': request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user.profile, serializer_data)

        try:
            serializer.update(request.user, serializer_data)
        except:
            return Response({"error": "Username or email already exist, create a unique one"},
                            status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFollowing(RetrieveUpdateAPIView):
    """Profile views class"""
    permission_classes = (IsAuthenticated,)
    # renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def follow_user(request, username):
        following_id = username
        user_id = request.user.id
        if check_following(user_id, follower_id):
            message = "You're already following this user."
            status = status.HTTP_200_OK
            return (message, status)
        else:
            serializer_instance = 
            serializer_data = {
                        "user_id" = 
                        "follower_id" = follower_id
            }
            serializer = self.serializer_class

        pass
    
    def unfollow_user(username):
        pass
    
    def retrieve(self, request, username):
        pass

    def update(self, request, username, follow, *args, **kwargs):
        if follow == "follow":
            follow_user(request, username)
        elif follow == "unfollow":
            unfollow_user(username)
        else:
            raise exceptions.NotFound(
                "Sorry, page not found."
            )