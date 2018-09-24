from authors.apps.authentication.models import User
from django.test import TestCase,Client
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
        response = self.client.post("/api/users/", self.reg_data, format="json")
        return self.assertEqual(response.status_code, status.HTTP_201_CREATED)