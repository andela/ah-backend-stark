"""authentication tests file"""

from rest_framework import status
from authors.apps.authentication.tests import BaseTest
from authors.apps.authentication.models import User
from rest_framework.test import APIClient


class TestUser(BaseTest):
    """This class tests activities concerning user model"""

    def test_creating_user(self):
        """" Test creating a new user """
        response = self.client.post(
            "/api/users/", self.reg_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert "username" in response.data
        assert "token" in response.data

    def test_get_full_name(self):
        """ Test get user's full name"""
        self.assertEquals("test5", self.user.get_full_name)

    def test_get_short_name(self):
        """ Test get user's short name"""
        self.assertEquals("test5", self.user.get_short_name())

    def test_user_model(self):
        """ Test User model"""
        user = User.objects.create_superuser(
            "test9", "test9@test.com", password="123456789")
        user.save()
        self.assertEqual(str(user.email), "test9@test.com")
        self.assertEqual(str(user.username), "test9")

    def test_logging_in(self):
        """" Test logging in a user"""
        res = self.client.post("/api/users/", self.reg_data, format="json")
        token = res.data['token']
        self.client.get("/api/users/activate_account/{}/".format(token))
        response = self.client.post(
            "/api/users/login/", self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.login_data['user']['email'], response.data['email'])
        assert "token" in response.data

    def test_registration_without_username(self):
        """ Test signup without a username"""

        response = self.client.post(
            "/api/users/", self.missing_username, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ll fields are required for registration',
                      response.json()['errors']['error'])

    def test_registration_with_existing_user_email(self):
        """Test signup with an existing email address"""

        self.client.post("/api/users/", self.reg_data, format="json")
        response = self.client.post(
            "/api/users/", self.reg_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user with this email already exists.',
                      response.json()['errors']['email'])

    def test_registration_with_invalid_email(self):
        """ Test signup with an invalid email address """

        response = self.client.post(
            "/api/users/", self.invalid_email, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('A valid email address is required to signup',
                      response.json()['errors']['email'])

    def test_registration_without_email(self):
        """Test signup without an email address"""

        response = self.client.post(
            "/api/users/", self.missing_email, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('All fields are required for registration',
                      response.json()['errors']['error'])

    def test_registration_without_password(self):
        """Test signup without a password"""

        response = self.client.post(
            "/api/users/", self.missing_password, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('All fields are required for registration',
                      response.json()['errors']['error'])

    def test_registration_with_short_password(self):
        """Test signup with a password of length less than 8"""

        response = self.client.post(
            "/api/users/", self.short_password, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'Weak password: Password should be ' +
            'atleast 8 characters long, ' +
            'include atleast a capital letter and a number',
            response.json()['errors']['password'])

    def test_registration_with_password_that_has_no_caps(self):
        """Test signup with a password that has no capital letter"""

        response = self.client.post(
            "/api/users/", self.password_with_no_caps, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'Weak password: Password should be ' +
            'atleast 8 characters long, ' +
            'include atleast a capital letter and a number',
            response.json()['errors']['password'])

    def test_registration_with_password_that_has_no_number(self):
        """Test signup with a password that has no capital letter"""

        response = self.client.post(
            "/api/users/", self.pswd_no_number, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'Weak password: Password should be ' +
            'atleast 8 characters long, ' +
            'include atleast a capital letter and a number',
            response.json()['errors']['password'])

    def test_reset_user_password_status_code_returns_200(self):
        self.client.post("/api/users/", self.reg_data, format="json")
        self.client.post("/api/users/login/", self.login_data, format="json")
        response = self.client.post(
            "/api/password-reset/",
            data={"user": {
                "email": " test@test.com"
            }},
            format="json")
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
        """"This method tests successful resetting of a user password"""

        res = self.client.post("/api/users/", self.reg_data, format="json")
        token = res.data['token']
        self.client.get("/api/users/activate_account/{}/".format(token))
        resp = self.client.post(
            "/api/password-reset/", data=self.user_email, format="json")
        token = resp.data['token']
        x = self.client.get("/api/password-reset/{}/".format(token))
        token = x.data['token']
        self.client.credentials(HTTP_TOKEN=token)
        response = self.client.put(
            "/api/password/reset/done/",
            data=self.password_update,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
