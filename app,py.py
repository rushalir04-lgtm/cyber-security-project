from flask import Flask, request, render_template_string, redirect, url_for, flash
import sqlite3
from markupsafe import escape

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key


# Database initialization
def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()


# Home Route
@app.route('/')
def home():
    return '''
        <h1>Welcome to the App!</h1>
        <a href="/login">Login</a>
        <a href="/hello">Say Hello</a>
    '''


# Secure Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Use parameterized queries to prevent SQL injection
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            return "Logged in successfully!"
        else:
            flash("Invalid credentials!")  # Flashing error message
            return redirect(url_for('login'))  # Redirect to login page on failure

    return '''
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f2f2f2;
            }
            form {
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            input[type="text"], input[type="password"] {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
        </style>
        <form method="post">
            <h2>Login</h2>
            <label for="username">Username:</label><br>
            <input type="text" name="username" required><br>
            <label for="password">Password:</label><br>
            <input type="password" name="password" required><br>
            <input type="submit" value="Login">
        </form>
    '''


# Secure Route to prevent XSS
@app.route('/hello')
def hello():
    name = request.args.get('name', 'World')
    safe_name = escape(name)  # Use escape to prevent XSS
    return render_template_string('<h1>Hello, {{ name }}</h1>', name=safe_name)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
