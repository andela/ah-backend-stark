"""profile app tests file"""
from rest_framework import status
from rest_framework.test import APIClient
from authors.apps.profiles.tests import BaseTest
from authors.apps.profiles.models import Profile


class ProfileUser(BaseTest):
    """This class tests activities concerning user model"""

    def test_fetching_profile(self):
        """"This method tests creating a new user"""
        response = self.client.get("/api/profiles/test123/",
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert "username" in response.data

    def test_fetching_missing_profile(self):
        """"This method tests creating a new user"""
        response = self.client.get("/api/profiles/testuuuu/",
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        assert "errors" in response.data

    def test_editing_profile(self):
        """"This method tests updating in a user profile"""
        response = self.client.put("/api/profile/update/",
                                   self.profile_update,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.profile_update['profile']['username'], response.data['username'])
        self.assertIn(self.profile_update['profile']['bio'], response.data['bio'])

    def test_invalid_token(self):
        """"This method tests updating in a user profile"""
        client = APIClient()
        client.credentials(HTTP_TOKEN="uuyytttt")
        response = client.put("/api/profile/update/",
                              self.profile_update,
                              format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_model(self):
        """method to test profile model"""
        entry = Profile(bio="i love me", location="mbuya", fun_fact="food")
        self.assertEqual(str(entry.bio), "i love me")
        self.assertEqual(str(entry.location), "mbuya")
        self.assertEqual(str(entry.fun_fact), "food")
