from rest_framework import status
from authors.apps.authentication.tests import BaseTest
from authors.apps.authentication.social_auth import create_social_user


class TestSocialAuth(BaseTest):
    """
    This class runs tests on the social authentication api
    endpoints
    """

    def test_new_social_user_creation(self):
        create_social_user((), details=self.social_auth_dict)

    def test_existing_social_user_login(self):
        create_social_user((), details=self.social_auth_dict)
        create_social_user((), details=self.social_auth_dict)

    def test_social_auth_redirection(self):
        response = self.client.get('/api/auth/google/?RedirectTo=' +
                                   self.social_redirection_url)
        self.assertEqual(response.status_code, 302)
