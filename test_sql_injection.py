import importlib.util
import sys
import unittest
from unittest.mock import patch

# Load the module manually
spec = importlib.util.spec_from_file_location("app", "C:/Users/Malu/PycharmProjects/CodeAlpha_cybersecurity/.venv/app,py.py")
app_module = importlib.util.module_from_spec(spec)
sys.modules["app"] = app_module
spec.loader.exec_module(app_module)
app = app_module.app  # Assuming your Flask app is named `app` inside that file

class SQLInjectionTest(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_sql_injection(self, mock_connect):
        # Mock the cursor and the fetchone method
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = None  # Simulating no user found

        username = "' OR '1'='1"
        password = "' OR '1'='1"

        # Call the login function with SQL injection
        with app.test_client() as client:
            response = client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)

            # Check if the response contains the flash message in the session
            with client.session_transaction() as session:
                self.assertIn('_flashes', session)
                # Check that the first flash message is a string and matches the expected message
                self.assertIn('Invalid credentials!', [msg[1] for msg in session['_flashes']])

if __name__ == '__main__':
    unittest.main()
