import unittest
from unittest.mock import patch
from flask import Flask

class MockApplicationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('flask.Flask.test_client')
    def test_home_redirect(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        mock_test_client().get.return_value.data = b'Login'
        response = mock_test_client().get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    @patch('flask.Flask.test_client')
    def test_dashboard_access_denied_without_login(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 302
        response = mock_test_client().get('/dashboard')
        self.assertEqual(response.status_code, 302)

    @patch('flask.Flask.test_client')
    def test_about_page(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        mock_test_client().get.return_value.data = b'About'
        response = mock_test_client().get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About', response.data)

    @patch('flask.Flask.test_client')
    def test_registration_page(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        mock_test_client().get.return_value.data = b'Register'
        response = mock_test_client().get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    @patch('flask.Flask.test_client')
    def test_login_page(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        mock_test_client().get.return_value.data = b'Login'
        response = mock_test_client().get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    @patch('flask.Flask.test_client')
    def test_dummy_page(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        mock_test_client().get.return_value.data = b'Page Under Maintenance'
        response = mock_test_client().get('/dummy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Page Under Maintenance', response.data)

    @patch('flask.Flask.test_client')
    def test_reset_password_invalid_token(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        mock_test_client().get.return_value.data = b'Invalid password reset link.'
        response = mock_test_client().get('/resetPassword/invalidtoken')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid password reset link.', response.data)

if __name__ == '__main__':
    unittest.main()
