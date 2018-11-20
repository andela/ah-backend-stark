from authors.apps.authentication.models import User
from authors.apps.authentication.helpers import (
    get_env_variable, set_social_env_variable, generate_unique_username,
    get_base64_str)

social_users = []
def create_social_user(*args, **kwargs):
    details = kwargs['details']

    email = details['email']
    username = generate_unique_username(details['username'])
    password = email + 'Ah' + str(len(email))

    set_social_env_variable('user_email', email)
    set_social_env_variable('user_username', username)

    user = User.objects.filter(email=email).first()
    if user:
        token = user.token()
        set_social_env_variable('user_username', user.username)
        set_social_env_variable('user_token', token)

    else:

        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.is_verified = True
        user.save()

        token = user.token()
        set_social_env_variable('user_token', token)
