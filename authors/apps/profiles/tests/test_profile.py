"""profile app tests file"""
from rest_framework import status
from rest_framework.test import APIClient
from authors.apps.profiles.tests import BaseTest
from authors.apps.profiles.models import Profile


class ProfileUser(BaseTest):
    """This class tests activities concerning user model"""

    def test_fetching_profile(self):
        """"This method tests fetching a user's profile"""
        response = self.client.get("/api/profile/test123/",
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert "username" in response.data
        assert "bio" in response.data
        assert "location" in response.data

    def test_fetching_missing_profile(self):
        """"This method tests fetching a profile that doesn't exists"""
        response = self.client.get("/api/profile/testuuuu/",
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        assert "errors" in response.data

    def test_editing_different_profile(self):
        """"This method tests updating a different user' profile"""
        response = self.client.put("/api/profile/test1234/",
                                   self.profile_update,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert "error" in response.data

    def test_editing_your_profile(self):
        """"This method tests updating a user profile"""
        response = self.client.put("/api/profile/test123/",
                                   self.profile_update,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.profile_update['profile']['username'], response.data['username'])
        self.assertIn(self.profile_update['profile']['bio'], response.data['bio'])

    def test_editing_with_another_users_name(self):
        """"This method tests updating a profile changing username to another user's username"""
        response = self.client.put("/api/profile/test123/",
                                   self.profile_update1,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert "error" in response.data  

    def test_invalid_token(self):
        """"This method tests updating a profile with an invalid token"""
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

    def test_fetching_all_profiles(self):
        """"This method tests getting all profiles"""
        response = self.client.get("/api/profiles/",
                                   format="json")                          
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert "Authors" in response.data   
