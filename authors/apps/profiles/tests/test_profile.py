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

    def test_follow_a_user_no_auth(self):
        """"This method tests following a user without logging in"""
        client = APIClient()
        client.credentials(HTTP_TOKEN="not-a-token")
        response = client.post("/api/profile/test1234/follow/",
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get("detail"), "The token is invalid")

    def test_follow_a_user(self):
        """"This method tests following a user"""
        response = self.client.post("/api/profile/test1234/follow/",
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("message"), "You're now following test1234! You will receive notifications about their posts")
 
    def test_unfollow_a_user(self):
        """"This method tests unfollowing a user"""
        self.client.post("/api/profile/test1234/follow/",
                                    format="json")
        response = self.client.delete("/api/profile/test1234/unfollow/",
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "You have unfollowed test1234")
 
    def test_unfollow_a_user_not_following(self):
        """This method tests unfollowing a user who is not being followed"""
        response = self.client.delete("/api/profile/test1234/unfollow/",
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "You are currently not following test1234")
   
    def test_user_follows_themselves(self):
        """"This method tests response for a user following themselves"""
        response = self.client.post("/api/profile/test123/follow/",
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "As awesome as you may be, you cannot follow yourself!")
   
    def test_follow_a_user_who_doesnt_exist(self):
        """This method tests following a user that doesnt exist"""
        response = self.client.post("/api/profile/someuser/follow/",
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
   
    def test_get_follower_list(self):
        """This method tests checking follower list"""
        self.client.post("/api/profile/test1234/follow/",
                        format="json")
        self.mock_login(self.reg_data2)
        response = self.client.get("/api/profile/test1234/followers/",
                        format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_other_user_follower_list(self):
        """This method tests checking follower list"""
        self.client.post("/api/profile/test1234/follow/",
                        format="json")
        response = self.client.get("/api/profile/test1234/followers/",
                        format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_following_list(self):
        """This method tests checking following list"""
        self.client.post("/api/profile/test1234/follow/",
                        format="json")
        response = self.client.get("/api/profile/test123/following/",
                        format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_empty_follower_list(self):
        """This method tests getting an empty follower list"""
        response = self.client.get("/api/profile/test1234/followers/",
                        format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("followers"), "test1234 currently has no followers")
   
    def test_get_empty_following_list(self):
        """This method tests getting an empty following list"""
        response = self.client.get("/api/profile/test123/following/",
                        format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("following"), "You are currently not following anyone")
