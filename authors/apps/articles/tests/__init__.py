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
        self.sample_login_credencials ={"user": {
            "email":"userx@gmail.com",
            "password":"thispassword"}
        }
        self.article_1 = {"article": {
            "title": "Titlely",
            "description": "Now, how do you describe this?",
            "body": "This is my article",
            "tagList":["Health","Safety"]
               } 
        }


    def mock_login(self):
        self.client.post("/api/users/", self.sample_user, format="json")
        login_response = self.client.post("/api/users/login/",
         self.sample_login_credencials, format="json")

        data = login_response.data
        token = data['token']
        self.set_headers(token)

    def set_headers(self,token):
        self.client.credentials(HTTP_TOKEN=token)

        