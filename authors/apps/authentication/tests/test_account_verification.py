"""account verification test file"""

from authors.apps.authentication.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authors.apps.authentication.tests import BaseTest


class TestVerification(BaseTest):
    def test_send_email_on_successful_registration(self):
        """
        This method tests if an email with the account verification
        link is sent to a user upon registration
        """

        response = self.client.post(
            "/api/users/", self.reg_data, format="json")
        self.assertIn(
            'User successfully registered. ' +
            'Check your email to activate account',
            response.json()['user']['message'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_successful_acccount_verification(self):
        """
        This method tests that a user can successfully
        activate their account
        """

        res = self.client.post("/api/users/", self.reg_data, format="json")
        token = res.data['token']
        response = self.client.get(
            "/api/users/activate_account/{}/".format(token))
        self.assertIn(
            'Your account has been successfully activated. Complete profile',
            response.json()['user']['message'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verification_with_invalid_or_expired_link(self):
        """
        This method tests that a user cannot activate their account
        with an invalid or expired link
        """

        self.token = 'token'
        response = self.client.get("/api/users/activate_account/{}/".format(
            self.token))
        self.assertIn('Sorry. Activation link either expired or is invalid',
                      response.json()['user']['message'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_account_already_activated(self):
        """
        This method tests that a user can only activate their account once
        """

        res = self.client.post("/api/users/", self.reg_data, format="json")
        token = res.data['token']
        self.client.get("/api/users/activate_account/{}/".format(token))
        response = self.client.get(
            "/api/users/activate_account/{}/".format(token))
        self.assertIn('Account already activated. Please login',
                      response.json()['user']['message'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
