"""authentication tests file"""

from rest_framework import status
from authors.apps.authentication.tests import BaseTest
from authors.apps.authentication.models import User
from rest_framework.test import APIClient

class TestUser(BaseTest):
    """This class tests activities concerning user model"""

    def test_creating_user(self):
        """"This method tests creating a new user"""
        response = self.client.post("/api/users/", self.reg_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert "username" in response.data
        assert "token" in response.data

    def test_get_full_name(self):
        """method to get user's full name"""
        self.assertEquals("test5", self.user.get_full_name)

    def test_get_short_name(self):
        """method to get user's short name"""
        self.assertEquals("test5", self.user.get_short_name())
 
    def test_user_model(self):
        """method to test User model"""
        user=User.objects.create_superuser("test9", "test9@test.com", password="123456789")
        user.save()
        self.assertEqual(str(user.email), "test9@test.com")
        self.assertEqual(str(user.username), "test9")

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

    def test_reset_user_password_status_code_returns_200(self):
        self.client.post("/api/users/", self.reg_data, format="json")
        self.client.post("/api/users/login/", self.login_data, format="json")
        response = self.client.post("/api/password-reset/",
                                    data={"user": {
                                            "email":"test@test.com",
                                            }
                                        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_confirm_reset_user_password_status_code(self):
        response = self.client.get(
            "/api/password-reset/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
            ".eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTUzODU2OTI4M"
            "30.PP8TfDmrEA5oDXLkoePqw5zS9Bw6nzhtJVLhWm76GUc"
            "/",
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_confirm_reset_without_token_status_code(self):
        client = APIClient()
        response = client.put("/api/password/reset/done/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        assert "detail" in response.data

    def test_confirm_reset(self):
        """"This method tests creating a new user"""
        client = APIClient()
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
        ".eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTUzODU2OTI4M"
        "30.PP8TfDmrEA5oDXLkoePqw5zS9Bw6nzhtJVLhWm76GUc"
        client.credentials(HTTP_TOKEN=token)
        response = self.client.put("/api/password/reset/done/", data=self.password_update, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)