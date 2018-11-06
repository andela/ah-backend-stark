"""views for profile app"""
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Profile, Following
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, FollowingSerializer
from .exceptions import ProfileDoesNotExist
from authors.apps.authentication.models import User


class UserProfile(RetrieveUpdateAPIView):
    """Profile views class"""
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ProfileJSONRenderer, )
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        """ function to retrieve user profile information """
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username)

        except Exception as e:
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
                'username':
                user_data.get('username', request.user.username),
                'bio':
                user_data.get('bio', request.user.profile.bio),
                'location':
                user_data.get('location', request.user.profile.location),
                'fun_fact':
                user_data.get('fun_fact', request.user.profile.fun_fact),
                'image':
                user_data.get('image', request.user.profile.image)
            }

            serializer = self.serializer_class(
                request.user.profile,
                data=serializer_data,
                context={'request': request},
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.update(request.user.profile, serializer_data)

            try:
                serializer.update(request.user, serializer_data)
            except Exception as e:
                return Response({
                    "error":
                    "Username or email already exist, " + "create a unique one"
                }, status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "You can only update your own profile"
            }, status.HTTP_400_BAD_REQUEST)


class ListProfiles(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ProfileJSONRenderer, )
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        """ function to retrieve user profile information """

        users = Profile.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response({
            "Authors": serializer.data
        },
                        status=status.HTTP_200_OK)


class UserFollow(APIView):
    """
    View class for user to follow other users
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = FollowingSerializer

    def post(self, request, username):
        """
        This method allows users to follow others
        """
        following_id = Following.check_exists(username)
        user_id = request.user.id

        if user_id == following_id:
            message = "As awesome as you may be, you cannot follow yourself!"
            status_code = status.HTTP_400_BAD_REQUEST
        elif Following.already_following(user_id, following_id):
            message = "You're already following %s!" % (username, )
            status_code = status.HTTP_200_OK
        else:
            serializer_data = {"user": user_id, "following_id": following_id}
            serializer = self.serializer_class(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            string = ("You're now following %s! " +
                      "You will receive notifications about their posts")
            message = string % (username, )
            status_code = status.HTTP_201_CREATED
        return Response({"message": message}, status=status_code)


class UserUnfollow(APIView):
    """
    View class which allows users to unfollow other users
    """
    permission_classes = (IsAuthenticated, )

    def delete(self, request, username):
        """
        This method allows users to unfollow others
        """
        following_id = Following.check_exists(username)
        user_id = request.user.id

        if Following.already_following(user_id, following_id):
            message = Following.unfollow(user_id, following_id, username)
            status_code = status.HTTP_200_OK
        else:
            message = "You are currently not following %s" % (username, )
            status_code = status.HTTP_400_BAD_REQUEST
        return Response({"message": message}, status=status_code)


class UserFollowers(APIView):
    """
    View class for users to see who follows them
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileSerializer
    query = "followers"

    def get(self, request, username):
        follower_list = Following.get_list(request, username, self.query,
                                           self.serializer_class)
        return Response({self.query: follower_list}, status=status.HTTP_200_OK)


class UserFollowing(UserFollowers):
    """
    View class for users to see everyone they are following
    """
    query = "following"
