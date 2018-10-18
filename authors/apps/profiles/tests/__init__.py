"""profile base test file"""
from django.test import TestCase
from rest_framework.test import APIClient


class BaseTest(TestCase):
    """profile app basetest file"""

    def setUp(self):
        """test class set up method"""
        self.client = APIClient()
        self.reg_data = {
            "user": {
                "username": "test123",
                "email": "test1123@test.com",
                "password": "Testpassword1"
            }
        }

        self.reg_data2 = {
            "user": {
                "username": "test1234",
                "email": "test11234@test.com",
                "password": "Testpassword2"
            }
        }

        self.profile_update = {
            "profile": {
                "username": "test123",
                "email": "test6@test.com",
                "bio": "test",
                "location": "mbuya"
            }
        }

        self.profile_update1 = {
            "profile": {
                "username": "test1234",
                "email": "test6@test.com",
                "bio": "test",
                "location": "mbuya"
            }
        }

        self.register_user = self.client.post(
            "/api/users/", self.reg_data2, format="json")
        self.register_user = self.client.post(
            "/api/users/", self.reg_data, format="json")
        token1 = self.register_user.data["token"]
        self.client.get(
            "/api/users/activate_account/{}/".format(token1))
        self.client.credentials(HTTP_TOKEN=token1)
    
    def mock_login(self, reg_data):
        """
        This helper method creates a user, logs then in,
        gets their token and sets the 'Token' header to the
        token generated during login

        It helps in authenticating requests
        """
        self.client.post("/api/users/", self.reg_data, format="json")
        login_response = self.client.post("/api/users/login/",
                         self.reg_data, format="json")

        data = login_response.data
        token = data['token']
        self.client.credentials(HTTP_TOKEN=token)
    
    def mock_registration(self, reg_data):
        self.client.post("/api/users/", self.reg_data, format="json")
