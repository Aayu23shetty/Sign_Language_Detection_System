import sys
print("Python executable:", sys.executable)
print("Python path:", sys.path)
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, template_folder='template')  # Use 'template' folder for HTML files
app.secret_key = 'your_secret_key'  # Set a secret key for session and flash messages

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dummy credentials for testing
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Load user callback
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Route for the Home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate the username and password
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            user = User(id=username)
            login_user(user)
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Route for the Dashboard page
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Route for the Get Started page
@app.route('/get_started')
def get_started():
    return render_template('get_started.html')

if __name__ == '__main__':
    app.run(debug=True)


