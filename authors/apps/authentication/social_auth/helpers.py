import os
import base64
from authors.apps.authentication.models import User

temp_user_queue = []
redirect_url = None


def add_user_to_queue(username, email, token):
    temp_user_queue.append({
        "username": username,
        "email": email,
        "token": token
    })


def get_user_from_queue():
    """
    Returns the first user from the social queue
    """
    user_data = ''
    if temp_user_queue:
        user_data = temp_user_queue[get_queue_count()]
    return user_data or {}


def pop_user_from_queue():
    if temp_user_queue:
        temp_user_queue.pop(get_queue_count())


def get_queue_count():
    return len(temp_user_queue) - 1


def set_redirect_url(request):
    global redirect_url
    social_url = request.query_params.get('RedirectTo', None)
    redirect_url = request.META.get('HTTP_REDIRECTTO', social_url)



def get_redirect_url():
    return redirect_url



def generate_unique_username(current_name):
    unique_name = current_name.replace(" ", "")
    count = 0
    while User.objects.filter(username=unique_name).exists():
        unique_name = f'{unique_name}{count}'
        count += 1
    return unique_name


def get_base64_str(data):
    value = str(base64.b64encode(bytes(str(data), 'utf-8')))
    value = value[2:-1]
    return value
