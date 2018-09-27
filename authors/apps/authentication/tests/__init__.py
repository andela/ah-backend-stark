"""base test file"""

from django.test import TestCase
from rest_framework.test import APIClient
class BaseTest(TestCase):

    def setUp(self):
        """test class set up method"""
        self.client=APIClient()
        self.reg_data= {"user": {
            "username":"test",
            "email":"test@test.com",
            "password":"test_password"}
        }
        self.reg_data2= {"user": {
            "username":"test1",
            "email":"test1@test.com",
            "password":"test_password"}
        }
        self.login_data= {"user": {
            "email":"test1@test.com",
            "password":"test_password"}
        }
        self.client.post("/api/users/", self.reg_data2, format="json")
        self.user_data={'email':'test@test.com','username':'test'}