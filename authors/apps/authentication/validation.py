import re
from rest_framework import serializers


def validate(data):
    """ This method validates username, email address
    and password  on registration """

    username = str(data.get('username', None)).strip()
    email = data.get('email', None)
    password = data.get('password', None)

    if (not username or
        not password or
            not email):
        raise serializers.ValidationError({
            'error': 'All fields are required for registration'
        })

    if len(username) < 5:
        raise serializers.ValidationError({
            'username': 'Username should be atleast 5 characters long'
        })

    if not re.match(r"^[A-Za-z]+[\d\w_]+", username):
        raise serializers.ValidationError({
            'username': 'Username should start with letters, ' +
            'and optionally include numbers and underscores'
        })

    if not re.search(r"^[a-z0-9_.+-]+@[a-z]+\.[a-z]+$", email):
        raise serializers.ValidationError({
            'email': 'A valid email address is required to signup'
        })

    strong_password(password)

    return {
        "username": username,
        "email": email,
        "password": password
    }


def strong_password(password):
    """ This method checks if a user password is strong """

    long_password = (len(password) > 7)
    capital_letter = re.search("[A-Z]", password)
    atleast_number = re.search("[0-9]", password)

    if (not long_password or
        not capital_letter or
            not atleast_number):

        raise serializers.ValidationError({
            'password': 'Weak password: Password should be ' +
            'atleast 8 characters long, ' +
            'include atleast a capital letter and a number'
        })
