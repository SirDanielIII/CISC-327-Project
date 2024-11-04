import unittest
import re
from pyotp import TOTP
from base_test_class import BaseTestClass

class AccountTests(BaseTestClass):
    current_user_index = 0

    def test_register_visible(self):
        """Test the register page"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_visible(self):
        """Test the login page visibility"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'LOGIN', response.data)

    def test_setup_2fa_visible(self):
        """Test the 2fa setup page visibility"""
        self.loginTestUser()
        response = self.client.get('/setup_2fa')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Setup 2FA', response.data)
        self.assertIn(b'Skip', response.data)

    def test_verify_2fa_visible(self):
        """Test the 2fa verficiation page visibility"""
        self.loginTestUser()
        self.enableTestUser2fa()
        response = self.client.get('/verify_2fa')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Verify 2FA', response.data)

    def test_register_success(self):
        """Test a successful registration"""
        AccountTests.current_user_index+=1
        test_email = f'testemail{AccountTests.current_user_index}@example.com'
        test_first_name = 'Test'
        test_last_name = 'Name'
        response = self.client.post('/register', data=dict(
            first_name=test_first_name,
            last_name=test_last_name,
            email=test_email,
            password='testingpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Setup 2FA', response.data)
        self.assertIn(str.encode(test_first_name), response.data)
        self.assertIn(str.encode(test_last_name), response.data)

    def test_setup_2fa(self):
        """Test setup 2FA authentication"""
        self.loginTestUser()

        # Get the setup 2fa page to retrieve 2FA secret token
        response = self.client.get('/setup_2fa')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Setup 2FA', response.data)
        self.assertIn(b'Skip', response.data)

        token_2fa_search = re.search('2FA Secret Token: ([\w\d]{32})', response.text, re.IGNORECASE)
        self.assertIsNotNone(token_2fa_search)
        token_2fa = token_2fa_search.group(1)
        totp = TOTP(token_2fa)

        response = self.client.post('/setup_2fa', data=dict(
            verification_code=totp.now()
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_logged_in_welcome_msg, response.data)
        self.assertIn(str.encode(self.user_first_name), response.data)
        self.assertIn(str.encode(self.user_last_name), response.data)

    def test_verify_2fa(self):
        """Test verify 2FA authentication"""
        self.loginTestUser()

        token_2fa = self.enableTestUser2fa()
        totp = TOTP(token_2fa)

        response = self.client.post('/verify_2fa', data=dict(
            verification_code=totp.now()
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_logged_in_welcome_msg, response.data)
        self.assertIn(str.encode(self.user_first_name), response.data)
        self.assertIn(str.encode(self.user_last_name), response.data)

    def test_register_fail(self):
        """Test a unsuccessful registration"""
        response = self.client.post('/register', data=dict(
            first_name=self.user_first_name,
            last_name=self.user_last_name,
            email=self.user_email,
            password=self.user_password
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The email provided is already registered for an account!', response.data)
        self.assertIn(b'Register', response.data)

    def test_valid_login(self):
        """Test Valid login"""
        response = self.client.post('/login', data=dict(
            email=self.user_email,
            password=self.user_password
        ), follow_redirects=True)
        self.assertIn(self.user_logged_in_welcome_msg, response.data)
        self.assertNotIn(b'LOGIN', response.data)
        self.assertNotIn(b'LOGIN', response.data)
        self.assertIn(str.encode(self.user_first_name), response.data)
        self.assertIn(str.encode(self.user_last_name), response.data)

    def test_invalid_login(self):
        """Test Invalid login"""
        response = self.client.post('/login', data=dict(
            email='nonexistent@example.com',
            password='boguspassword'
        ), follow_redirects=True)
        self.assertIn(b'LOGIN', response.data)
        self.assertIn(b'The email or password provided is invalid!', response.data)

    def test_logout(self):
        """Test logout"""
        self.loginTestUser()
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_logged_out_welcome_msg, response.data)
        self.assertIn(b'LOGIN', response.data)

if __name__ == "__main__":
    unittest.main()