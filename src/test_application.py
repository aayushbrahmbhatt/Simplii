import unittest
from flask import session
from application import app

class ApplicationTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_home_redirect(self):
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_dashboard_access_denied_without_login(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Expect redirect to login

    def test_about_page(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About', response.data)

    def test_registration_page(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_dummy_page(self):
        response = self.app.get('/dummy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Page Under Maintenance', response.data)

    def test_contact_post_message(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['email'] = 'test@example.com'
            response = client.post('/contact', data={'message': 'Test message'}, follow_redirects=True)
            self.assertIn(b'Your message has been sent to support!', response.data)

    def test_reset_password_invalid_token(self):
        response = self.app.get('/resetPassword/invalidtoken', follow_redirects=True)
        self.assertIn(b'Invalid password reset link.', response.data)

    def test_recommend_redirect(self):
        response = self.app.get('/recommend')
        self.assertEqual(response.status_code, 302)  # Redirects to home if not logged in

    def test_kanban_board_redirect(self):
        response = self.app.get('/kanbanBoard')
        self.assertEqual(response.status_code, 302)  # Redirects to home if not logged in

if __name__ == '__main__':
    unittest.main()
