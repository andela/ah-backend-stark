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
            "password":"testpassword"}
        }
       
        self.login_data= {"user": {
            "email":"test@test.com",
            "password":"testpassword"}
        }