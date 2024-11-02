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
        
#this are the new test cases
    @patch('flask.Flask.test_client')
    def test_fetch_tasks(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        response = mock_test_client().get('/fetchTasks')
        self.assertEqual(response.status_code, 200)

    @patch('flask.Flask.test_client')
    def test_gpt_endpoint(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        mock_test_client().get.return_value.data = b'GPT Response'
        response = mock_test_client().get('/gpt')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GPT Response', response.data)

    @patch('flask.Flask.test_client')
    def test_activity_log(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        response = mock_test_client().get('/activity')
        self.assertEqual(response.status_code, 200)

    @patch('flask.Flask.test_client')
    def test_settings_page(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        response = mock_test_client().get('/settings')
        self.assertEqual(response.status_code, 200)

    @patch('flask.Flask.test_client')
    def test_contact_submission(self, mock_test_client):
        mock_test_client().post.return_value.status_code = 200
        mock_test_client().post.return_value.data = b'Contact Submitted'
        response = mock_test_client().post('/contact', data={'message': 'Help needed'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact Submitted', response.data)

    @patch('flask.Flask.test_client')
    def test_reminders_scheduled(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        response = mock_test_client().get('/reminderscheduled')
        self.assertEqual(response.status_code, 200)

    @patch('flask.Flask.test_client')
    def test_profile_update(self, mock_test_client):
        mock_test_client().post.return_value.status_code = 200
        response = mock_test_client().post('/profile', data={'name': 'New Name'})
        self.assertEqual(response.status_code, 200)

    @patch('flask.Flask.test_client')
    def test_post_submission(self, mock_test_client):
        mock_test_client().post.return_value.status_code = 201
        response = mock_test_client().post('/post', data={'content': 'New post content'})
        self.assertEqual(response.status_code, 201)

    @patch('flask.Flask.test_client')
    def test_update_task_status(self, mock_test_client):
        mock_test_client().post.return_value.status_code = 200
        response = mock_test_client().post('/update_task_status', data={'task_id': '123', 'status': 'completed'})
        self.assertEqual(response.status_code, 200)

    @patch('flask.Flask.test_client')
    def test_recommendations_page(self, mock_test_client):
        mock_test_client().get.return_value.status_code = 200
        response = mock_test_client().get('/recommend')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
