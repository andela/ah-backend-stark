from authors.apps.authentication.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import json
class TestUser(TestCase):

    def setUp(self):
        """test class set up method"""
        self.client=APIClient()
        self.reg_data= {"user": {
            "username":"test",
            "email":"test@test.com",
            "password":"test_password"}
        }
        self.user_data={'email':'test@test.com','username':'test'}

    def test_creating_user(self):
        """"This method tests creating a new user"""
        response = self.client.post("/api/users/", self.reg_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.user_data['email'],response.data['email'])
        self.assertIn(self.user_data['username'],response.data['username'])