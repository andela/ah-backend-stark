from rest_framework import status
from authors.apps.authentication.tests import BaseTest


class TestUser(BaseTest):
    """This class tests activities concerning user model"""

    def test_creating_user(self):
        """"This method tests creating a new user"""
        response = self.client.post("/api/users/", self.reg_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.user_data['email'],response.data['email'])
        self.assertIn(self.user_data['username'],response.data['username'])
        assert "token" in response.data

    def test_logging_in(self):
        """"This method tests logging in a user"""
        response = self.client.post("/api/users/login/", self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.login_data['user']['email'],response.data['email'])
        assert "token" in response.data    
