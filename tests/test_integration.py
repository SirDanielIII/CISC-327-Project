import re
from flask import Flask
from pyotp import TOTP
from tests.base_test_class import BaseTestClass
from app.models import Property
from app.database import db
from app.app import create_app

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

    # THIS IS MEANT TO WORK WITH REGISTER ONCE COMBINED
    def test_login_with_2fa(self):
        """Test the integration of the login process with 2FA"""
        test_email = 'integration@test.com'
        test_password = 'Integrationtest1'

        # Login
        response = self.client.post('/login', data=dict(
            email=test_email,
            password=test_password,
        ), follow_redirects=True)

        # Ensure user is asked for 2FA
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Verify 2FA', response.data)

        # Get 2FA secret token
        token_2fa_search = re.search(r'2FA Secret Token: ([\w\d]{32})', response.text, re.IGNORECASE)
        self.assertIsNotNone(token_2fa_search)
        token_2fa = token_2fa_search.group(1)
        totp = TOTP(token_2fa)

        # Verify 2FA code
        response = self.client.post('/verify_2fa', data=dict(
            verification_code=totp.now()
        ), follow_redirects=True)

        # Ensure login is successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"Welcome {self.test_first_name}, to the Rental Management System", response.text)
        self.assertIn(str.encode(self.test_first_name), response.data)
        self.assertIn(str.encode(self.test_last_name), response.data)

    def test_new_property(self):
        """Test the property addition process"""
        with self.app.app_context():
            response = self.client.post('/add_property', data=dict(
                streetAddress='3434 Integration Blvd',
                ptype='House',
                sqft='2100',
                bdr='4',
                btr='2',
                price='1850',
                availability='available'
            ), follow_redirects=True)

            # Verify the response
            self.assertEqual(response.status_code, 200)
            # self.assertIn(b"Property added successfully", response.data)

            # Ensure the property exists in the database
            property_in_db = db.session.query(Property).filter_by(address='3434 Integration Blvd').first()
            self.assertIsNotNone(property_in_db)
            self.assertEqual(property_in_db.property_type, 'House')
            self.assertEqual(property_in_db.square_footage, 2100)
            self.assertEqual(property_in_db.bedrooms, 4)
            self.assertEqual(property_in_db.bathrooms, 2)
            self.assertEqual(property_in_db.rent_per_month, 1850)
            self.assertTrue(property_in_db.available)