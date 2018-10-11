"""profile model file"""
from django.db import models
from rest_framework.exceptions import NotFound
from authors.apps.authentication.models import User


class Profile(models.Model):
    """user profile model"""
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    fun_fact = models.TextField(blank=True)
    location = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
    @staticmethod
    def get_user(username):
        return Profile.objects.filter(username=username).values()[0]

class Following(models.Model):
    """
    user followers model
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    following_id = models.TextField()
    
    def __str__(self):
        return self.user
    
    @staticmethod
    def already_following(user_id, following_id):
        queryset = Following.objects.filter(
                    user=user_id, 
                    following_id=following_id)
        return queryset.exists()
    
    @staticmethod
    def unfollow(user_id, following_id, username):
        queryset = Following.objects.filter(
                    user=user_id,
                    following_id=following_id)
        queryset.delete()
        message = "You have unfollowed %s" % (username,)    
        return message
    
    @staticmethod
    def get_followers(user_id):
        queryset = Following.objects.filter(
                    following_id=user_id)
        return queryset
    
    @staticmethod
    def get_following(user_id):
        queryset = Following.objects.filter(
                    user=user_id)
        return queryset
    
    @staticmethod
    def get_profile_list(input_list, serializer_class, list_id):
        return_list = []
        for i in range(len(input_list)):

            try:
                item = Profile.objects.select_related('user').get(
                                    user__id=input_list[i][list_id])
            except NotFound:
                raise ProfileDoesNotExist

            serializer = serializer_class(item)
            return_list.append(serializer.data)
        return return_list
    
    @staticmethod
    def get_list(request, username, query, serializer_class):
        follow_details = Following.get_id_from_username(username, Following.get_following)
        check_id = follow_details[0]
        follow_list = follow_details[1]
        user_id = request.user.id
        if len(follow_list) == 0: 
            query_response = Following.empty_list(
                            query, 
                            check_id, 
                            user_id,
                            username)
        else:
            list_id = "following_id"
            query_response = Following.get_profile_list(
                                follow_list,
                                serializer_class, 
                                list_id)
        return query_response

    @staticmethod
    def get_id_from_username(username, function):
        check_id = Following.check_exists(username)
        queryset = function(check_id)
        return_list = queryset.values()
        return (check_id, return_list)

    @staticmethod
    def check_exists(username):
        queryset = User.get_user_queryset(username)
        if not queryset:
            raise NotFound("Sorry, there's no user with the username, '%s'." % (username,))
        user = User.get_user(queryset)
        user_id = user[0].get("id")
        return user_id
    
    @staticmethod
    def empty_list(query, check_id, user_id, username):
        if query == "following":
            query_response = Following.empty_following(
                            query, 
                            check_id, 
                            user_id, 
                            username)
        elif query == "followers":
            query_response = Following.empty_followers(
                            query, 
                            check_id, 
                            user_id, 
                            username)
        return query_response
    
    @staticmethod
    def empty_following(query, check_id, user_id, username):
        if check_id == user_id:
            query_response = "You are currently not following anyone"
        else:
            query_response = "%s is currently not following anyone" % (username,)
        return query_response
    
    @staticmethod
    def empty_followers(query, check_id, user_id, username):
        if check_id != user_id:
            query_response = "%s currently has no followers" % (username,)
            return query_response
        elif check_id == user_id:
            query_response = "You currently have no followers"
            return query_response