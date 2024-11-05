from base_test_class import BaseTestClass

class PublicTests(BaseTestClass):
    def test_home(self):
        """Test the home page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_logged_out_welcome_msg, response.data)

    def test_custom_not_found(self):
        """Test the custom not found page is used"""
        response = self.client.get('/not-found')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"We couldn't find the page you are looking for", response.data)

        response = self.client.get('/other-not-found')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"We couldn't find the page you are looking for", response.data)
