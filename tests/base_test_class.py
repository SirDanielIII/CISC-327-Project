import unittest
from werkzeug.security import generate_password_hash
from uuid import uuid4
import os

from app.app import create_app
from app.database import db
from app.models import User
from app.enums.AccountType import AccountType

class BaseTestClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        db_name_prefix = f'{uuid4()}_account_tests_'
        cls.app = create_app(db_name_prefix)
        cls.app.config['TESTING'] = True

        cls.user_first_name = 'Property'
        cls.user_last_name = 'Owner'
        cls.user_email = 'propertyowner@example.com'
        cls.user_password = 'propertyowner'

        with cls.app.app_context():
            cls.test_user = User(first_name=cls.user_first_name, last_name=cls.user_last_name, email=cls.user_email, 
                            password=cls.user_password, account_type=AccountType.PROPERTY_OWNER)
            db.session.add(cls.test_user)
            db.session.commit()
            db.session.refresh(cls.test_user)
    
    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()
            os.remove(db.db_path)

    def setUp(self) -> None:
        with self.app.app_context():
            # Disable any 2FA that may have been setup in a test case
            self.test_user = db.session.get(User, self.test_user.id)
            self.test_user.is_2fa_auth_enabled = False
            db.session.commit()
        self.client = self.app.test_client()
        return super().setUp()
    
    def enableTestUser2fa(self) -> str:
        with self.app.app_context():
            # Enable 2FA and return the 2FA secret token
            test_user = db.session.query(User).filter_by(email=self.user_email).scalar()
            test_user.is_2fa_auth_enabled = True
            db.session.commit()
            return test_user.token_2fa
    
    def loginTestUser(self):
        response = self.client.post('/login', data=dict(
            email=self.user_email,
            password=self.user_password
        ), follow_redirects=True)
        self.assertIn(b'Welcome', response.data)
        self.assertNotIn(b'LOGIN', response.data)
        self.assertNotIn(b'REGISTER', response.data)
        self.assertIn(str.encode(self.user_first_name), response.data)
        self.assertIn(str.encode(self.user_last_name), response.data)

    def logoutUser(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
        self.assertIn(b'Login', response.data)