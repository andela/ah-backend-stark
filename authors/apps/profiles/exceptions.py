"""profile exception file"""
from rest_framework.exceptions import APIException


class ProfileDoesNotExist(APIException):
    """profile exception class"""
    status_code = 404
    default_detail = "The profile does not exist"
