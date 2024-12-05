import os
import threading
import unittest
from typing import Any
from uuid import uuid4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.app import create_app
from app.database import db
from app.enums.AccountType import AccountType
from app.models import User

WEB_SERVER_PORT = 8080


class BaseTestClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        db_name_prefix = f'{uuid4()}_account_tests_'
        cls.app = create_app(db_name_prefix)
        cls.app.config['TESTING'] = True

        cls.user_first_name = 'Property'
        cls.user_last_name = 'Owner'
        cls.user_email = 'propertyowner@example.com'
        cls.user_password = 'Propertyowner1'

        cls.user_logged_out_welcome_msg = "Welcome to the Rental Management System"
        cls.user_logged_in_welcome_msg = f"Welcome {cls.user_first_name}, to the Rental Management System"

        with cls.app.app_context():
            cls.test_user = User(first_name=cls.user_first_name, last_name=cls.user_last_name, email=cls.user_email,
                                 password=cls.user_password, account_type=AccountType.PROPERTY_OWNER)
            db.session.add(cls.test_user)
            db.session.commit()
            db.session.refresh(cls.test_user)

        # Start the web app in a separate thread
        from werkzeug.serving import make_server
        cls.server = make_server('localhost', WEB_SERVER_PORT, cls.app)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.start()

        # Setting up selenium
        cls.driver = webdriver.Chrome(options=webdriver.ChromeOptions())

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

        # Stop the web app
        cls.server.shutdown()

        with cls.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()
            os.remove(db.db_path)

    def setUp(self) -> None:
        # Reset driver state
        self.driver.delete_all_cookies()
        self.driver.get(f'http://localhost:{WEB_SERVER_PORT}')

        with self.app.app_context():
            # Disable any 2FA that may have been setup in a test case
            self.test_user = db.session.get(User, self.test_user.id)
            self.test_user.is_2fa_auth_enabled = False
            db.session.commit()
        self.client = self.app.test_client()
        self.test_user_2fa_token = None
        return super().setUp()

    def enableTestUser2fa(self) -> Any | None:
        if self.test_user_2fa_token:
            return
        with self.app.app_context():
            # Enable 2FA and return the 2FA secret token
            test_user = db.session.query(User).filter_by(email=self.user_email).scalar()
            test_user.is_2fa_auth_enabled = True
            db.session.commit()
            self.test_user_2fa_token = test_user.token_2fa
            return test_user.token_2fa

    def getFullWebPath(self, path: str) -> str:
        return f'http://localhost:{WEB_SERVER_PORT}{path}'
    
    def pageFlashesContain(self, expectedStr: str) -> bool:
        flashesContainer = self.driver.find_element(By.ID, 'flashes')
        if not flashesContainer:
            return False
        flashes = flashesContainer.find_elements(By.TAG_NAME, 'li')
        for flash in flashes:
            if expectedStr in flash.text:
                return True
        return False
    
    def loginTestUser(self):
        login_full_path = self.getFullWebPath('/login')
        original_url = self.driver.current_url
        self.driver.get(login_full_path)

        wait = WebDriverWait(self.driver, 10).until(
            EC.url_changes(original_url)
        )

        self.assertEqual(login_full_path, self.driver.current_url)

        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'login-submit'))
        )

        email_input = self.driver.find_element(By.NAME, 'email')
        email_input.send_keys(self.user_email)

        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.send_keys(self.user_password)

        login_button.click()

        # Check that the user is logged in
        nav_fullname = self.driver.find_element(By.ID, 'nav-user-fullname')
        self.assertEqual(f'{self.user_first_name} {self.user_last_name}', nav_fullname.text)

        self.assertTrue(self.pageFlashesContain("Logged in successfully!"))
