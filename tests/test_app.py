import sys
import os
sys.path.append(os.path.join(os.path.curdir, 'app'))

import unittest

from app.app import create_app

class AppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def test_home(self):
        """Test the home page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_register_success(self):
        pass

    def test_register_fail(self):
        pass

    def test_login(self):
        pass

if __name__ == "__main__":
    unittest.main()