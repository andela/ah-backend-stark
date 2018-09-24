from authors.apps.authentication.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
class TestUser(TestCase):

    def setUp(self):
        """test class set up method"""
        self.client=APIClient()
        self.reg_data= {"user": {
            "username":"kenneth051",
            "email":"ken@ken.com",
            "password":"12345678"}
        }

    def test_creating_user(self):
        """"This method tests creating a new user"""
        data={'email':'ken@ken.com','username':'kenneth051'}
        response = self.client.post("/api/users/", self.reg_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(data['email'],response.data['email'])
        self.assertIn(data['username'],response.data['username'])