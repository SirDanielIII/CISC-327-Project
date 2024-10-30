import unittest
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
        self.assertIn(b'Login', response.data)

    def test_setup_2fa_visible(self):
        """Test the 2fa setup page visibility"""
        self.loginTestUser()
        response = self.client.get('/setup_2fa')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Setup 2FA', response.data)
        self.assertIn(b'Skip', response.data)

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
        response = self.client.post('/setup_2fa', data=dict(
            verification_code='123456'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
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
        self.assertIn(b'Welcome', response.data)
        self.assertNotIn(b'Login', response.data)
        self.assertNotIn(b'Register', response.data)
        self.assertIn(str.encode(self.user_first_name), response.data)
        self.assertIn(str.encode(self.user_last_name), response.data)

    def test_invalid_login(self):
        """Test Invalid login"""
        response = self.client.post('/login', data=dict(
            email='nonexistent@example.com',
            password='boguspassword'
        ), follow_redirects=True)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'The email or password provided is invalid!', response.data)

    def test_logout(self):
        """Test logout"""
        self.loginTestUser()
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
        self.assertIn(b'Login', response.data)

if __name__ == "__main__":
    unittest.main()