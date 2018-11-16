import os
import base64
from authors.apps.authentication.models import User


def set_social_env_variable(partialname, value):
    """
    Converts the provided environment variable name to uppercase
    before setting it as a social auth environment variable
    """
    variable_name = 'SOCIAL_' + str(partialname).upper()
    os.environ[variable_name] = value


def get_env_variable(varname):
    value = os.getenv(varname.upper(), '')

    return value


def unset_social_variables():
    set_social_env_variable('user_token', '')
    set_social_env_variable('user_email', '')
    set_social_env_variable('user_username', '')


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
