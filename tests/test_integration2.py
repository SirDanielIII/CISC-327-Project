import re
import pytest
from pyotp import TOTP
from base_test_class import BaseTestClass
from app.models import Property
from app import create_app, db

class IntegrationTests(BaseTestClass):

    # THIS IS MEANT TO WORK WITH REGISTER ONCE COMBINED
    def test_login_with_2fa(self):
        """Test the integration of the login process with 2FA"""
        response = self.client.post('/login', data=dict(
            email=self.test_email,
            password=self.test_password,
        ), follow_redirects=True)

        # Ensure user is asked for 2FA
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enter 2FA Code', response.data)

        # Verify 2FA code
        response = self.client.post('/verify_2fa', data=dict(
            verification_code=self.totp.now()
        ), follow_redirects=True)

        # Ensure login is successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"Welcome {self.test_first_name}, to the Rental Management System", response.text)
        self.assertIn(str.encode(self.test_first_name), response.data)
        self.assertIn(str.encode(self.test_last_name), response.data)

    # def client():
    #     """Set up test client and data for integration testing"""
    #     app = create_app('TESTER')
    #     with app.test_client() as client:
    #         with app.app_context():
    #             db.create_all()         # Create necessary table prior to each test
    #             yield client            # Yield test client to test case
    #             db.session.remove()     # Remove session after test
    #             db.drop_all()           # Drop all tables to clean up

    # Add client to parameters WHEN YOU FIGURE IT OUT
    def test_new_property(self):
        """Test the property addition process"""
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
        self.assertIn(b"Property added successfully", response.data)

        # Ensure the property exists in the database
        property_in_db = self.db.session.query(Property).filter_by(address='3434 Integration Blvd').first()
        self.assertIsNotNone(property_in_db)
        self.assertEqual(property_in_db.property_type, 'House')
        self.assertEqual(property_in_db.square_footage, 2100)
        self.assertEqual(property_in_db.bedrooms, 4)
        self.assertEqual(property_in_db.bathrooms, 2)
        self.assertEqual(property_in_db.rent_per_month, 1850)
        self.assertTrue(property_in_db.available)