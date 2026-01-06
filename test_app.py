import importlib.util
import sys
import unittest
import sqlite3  # Make sure to import sqlite3

# Load the module manually
spec = importlib.util.spec_from_file_location("app", "C:/Users/Malu/PycharmProjects/CodeAlpha_cybersecurity/.venv/app,py.py")
app_module = importlib.util.module_from_spec(spec)
sys.modules["app"] = app_module
spec.loader.exec_module(app_module)
app = app_module.app  # Assuming your Flask app is named `app` inside that file

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.init_db()  # Initialize the database before each test

    def init_db(self):
        # Create a test database for the tests
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        conn.commit()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('test', 'test'))
        conn.commit()
        conn.close()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the App!', response.data)  # Updated to match the actual output

    def test_login(self):
        response = self.app.post('/login', data={'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully!', response.data)  # Updated to match the actual output

if __name__ == '__main__':
    unittest.main()
