import re
from rest_framework import serializers

def validate(data):
    """This method validates username and password"""
    username = str(data.get('username', None)).strip()
    email = data.get('email', None)
    password = data.get('password', None)
        
    if not username:
        raise serializers.ValidationError({'username': 'A username is required to signup'})

    if not email:
        raise serializers.ValidationError({'email': 'An email address is required to signup'})

    if not re.search("^[a-z0-9_.+-]+@[a-z]+\\.[a-z]+$",email):
        raise serializers.ValidationError({'email': 'A valid email address is required to signup'})

    if not password:
        raise serializers.ValidationError({'password': 'A password is required to signup'})

    if not re.match("^[A-Za-z0-9]*$", password):
        raise serializers.ValidationError({'password': 'Password should only contain numbers and letters'})

    if len(password) < 8 :
        raise serializers.ValidationError({'password': 'Password should be atleast 8 characters long'})

    return {
            "username" : username,
            "email" : email,
            "password": password
        }
