import unittest

from app.app import create_app
from app.database import db

class AccountTests(unittest.TestCase):
    current_user_index = 0

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
    
    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            db.drop_all()

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
        response = self.client.get('/setup_2fa')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Setup 2FA', response.data)
        self.assertIn(b'Skip', response.data)

    def test_register_success(self):
        """Test a successful registration"""
        AccountTests.current_user_index+=1
        test_email = f'testemail{AccountTests.current_user_index}@example.com'
        response = self.client.post('/register', data=dict(
            email=test_email,
            password='testingpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(test_email), response.data)
        self.assertIn(b'Setup 2FA', response.data)

    def test_setup_2fa(self):
        """Test setup 2FA authentication"""
        AccountTests.current_user_index+=1
        test_email = f'testemail{AccountTests.current_user_index}@example.com'
        response = self.client.post('/register', data=dict(
            email=test_email,
            password='testingpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(test_email), response.data)
        self.assertIn(b'Setup 2FA', response.data)

        response = self.client.post('/setup_2fa', data=dict(
            verification_code='123456'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
        self.assertIn(str.encode(test_email), response.data)

    def test_register_fail(self):
        """Test a unsuccessful registration"""
        AccountTests.current_user_index+=1
        test_email = f'testemail{AccountTests.current_user_index}@example.com'
        response = self.client.post('/register', data=dict(
            email=test_email,
            password='testingpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(test_email), response.data)
        self.assertIn(b'Setup 2FA', response.data)

        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
        self.assertIn(b'Login', response.data)

        response = self.client.post('/register', data=dict(
            email=test_email,
            password='testingpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The email provided is already registed for an account!', response.data)
        self.assertIn(b'Register', response.data)

    def test_valid_login(self):
        """Test Valid login"""
        AccountTests.current_user_index+=1
        test_email = f'testemail{AccountTests.current_user_index}@example.com'
        test_password = 'testingpassword'
        response = self.client.post('/register', data=dict(
            email=test_email,
            password=test_password
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(test_email), response.data)
        self.assertIn(b'Setup 2FA', response.data)

        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
        self.assertIn(b'Login', response.data)

        response = self.client.post('/login', data=dict(
            email=test_email,
            password=test_password
        ), follow_redirects=True)
        self.assertIn(b'Welcome', response.data)
        self.assertIn(str.encode(test_email), response.data)

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
        AccountTests.current_user_index+=1
        test_email = f'testemail{AccountTests.current_user_index}@example.com'
        response = self.client.post('/register', data=dict(
            email=test_email,
            password='testingpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(test_email), response.data)
        self.assertIn(b'Setup 2FA', response.data)

        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
        self.assertIn(b'Login', response.data)

if __name__ == "__main__":
    unittest.main()