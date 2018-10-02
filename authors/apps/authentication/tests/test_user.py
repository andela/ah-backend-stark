from rest_framework import status
from authors.apps.authentication.tests import BaseTest


class TestUser(BaseTest):
    """This class tests activities concerning user model"""

    def test_creating_user(self):
        """"This method tests creating a new user"""
        response = self.client.post("/api/users/", self.reg_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert "username" in response.data
        assert "token" in response.data

    def test_logging_in(self):
        """"This method tests logging in a user"""
        self.client.post("/api/users/", self.reg_data, format="json")
        response = self.client.post("/api/users/login/", self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.login_data['user']['email'],response.data['email'])
        assert "token" in response.data    

    def test_registration_without_username(self):
        """This method tests that a user receives a descriptive error message 
        when they attempt to signup without a username"""
        response = self.client.post("/api/users/", self.missing_username, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('A username is required to signup', response.json()['errors']['username'])

    def test_registration_with_existing_user_email(self):
        """This method tests that a user receives a descriptive error message 
        when they attempt to signup with an existing email address"""
        self.client.post("/api/users/", self.reg_data, format="json")
        response = self.client.post("/api/users/", self.reg_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user with this email already exists.', response.json()['errors']['email'])

    def test_registration_with_invalid_email(self):
        """This method tests that a user receives a descriptive error message 
        when they attempt to signup with an invalid email address"""
        response = self.client.post("/api/users/", self.invalid_email, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('A valid email address is required to signup', response.json()['errors']['email'])

    def test_registration_without_email(self):
        """This method tests that a user receives a descriptive error message 
        when they attempt to signup with an invalid email address"""
        response = self.client.post("/api/users/", self.missing_email, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('An email address is required to signup', response.json()['errors']['email'])

    def test_registration_with_short_password(self):
        """This method tests that a user receives a descriptive error message 
        when they attempt to signup with a password of length less than 8"""
        response = self.client.post("/api/users/", self.short_password, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Password should be atleast 8 characters long', response.json()['errors']['password'])

    def test_registration_with_non_alphanumeric_password(self):
        """This method tests that a user receives a descriptive error message 
        when they attempt to signup with a non-alphanumeric password"""
        response = self.client.post("/api/users/", self.non_alphanumeric_password, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Password should only contain numbers and letters', response.json()['errors']['password'])
