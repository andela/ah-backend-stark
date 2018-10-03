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

        self.missing_username= {
            "user": {
            "username":"",
            "email":"test@test.com",
            "password":"test_password"
            }
        }

        self.missing_email= {
            "user": {
            "username":"test",
            "email":"",
            "password":"test_password"
            }
        }

        self.invalid_email= {
            "user": {
            "username":"test",
            "email":"test",
            "password":"test_password"
            }
        }

        self.short_password= {
            "user": {
            "username":"test",
            "email":"test@test.com",
            "password":"test"
            }
        }

        self.non_alphanumeric_password= {
            "user": {
            "username":"test",
            "email":"test@test.com",
            "password":"@$* p#$%"
            }
        }   