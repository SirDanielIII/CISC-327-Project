import re
from pyotp import TOTP
from base_test_class import BaseTestClass


class IntegrationTests(BaseTestClass):

    def test_register_and_2fa_setup(self):
        """Test the integration of the registration and 2FA setup process"""
        test_first_name = 'Integration'
        test_last_name = 'Test'
        # Register a new user
        response = self.client.post('/register', data=dict(
            first_name=test_first_name,
            last_name=test_last_name,
            email='integration@test.com',
            password='Integrationtest1',
            confirm_password='Integrationtest1',
        ), follow_redirects=True)
        # Ensure the registration was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(test_first_name), response.data)
        self.assertIn(str.encode(test_last_name), response.data)
        # Ensure user redirected to 2FA setup page
        self.assertIn(b'Setup 2FA', response.data)
        # Extract the 2FA secret token from the response
        token_2fa_search = re.search(r'2FA Secret Token: ([\w\d]{32})', response.text, re.IGNORECASE)
        self.assertIsNotNone(token_2fa_search)
        token_2fa = token_2fa_search.group(1)
        totp = TOTP(token_2fa)
        # Enable 2FA for the user
        response = self.client.post('/setup_2fa', data=dict(
            verification_code=totp.now()
        ), follow_redirects=True)
        # Ensure the 2FA setup was successful
        self.assertEqual(response.status_code, 200)
        # Ensure user is redirected to the home page
        self.assertIn(f"Welcome {test_first_name}, to the Rental Management System", response.text)
        self.assertIn(str.encode(test_first_name), response.data)
        self.assertIn(str.encode(test_last_name), response.data)
