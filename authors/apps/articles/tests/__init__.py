from django.test import TestCase
from rest_framework.test import APIClient

class BaseTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.sample_user ={"user": {
            "username":"userx",
            "email":"userx@gmail.com",
            "password":"thispassword"}
        }
        self.article_1 = {"article": {
            "title": "Titlely",
            "description": "Now, how do you describe this?",
            "body": "This is my article",
            "tagList":"Health,Safety",
            "author": 1
               } 
        }

    def register_user(self,user_data):
        self.client.post("/api/users/", user_data, format="json")
        