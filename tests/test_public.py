import unittest

from app.app import create_app

class PublicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_app(True)
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def test_home(self):
        """Test the home page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)