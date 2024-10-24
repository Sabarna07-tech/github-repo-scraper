from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
from scraper.scraper import fetch_github_repo_content
from werkzeug.security import check_password_hash
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure secret key and database
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_fallback_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for homepage
@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

# Route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please login.', 'error')
            return redirect(url_for('login'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('index'))

    return render_template('signup.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your email and password.', 'error')

    return render_template('login.html')

# Route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Scrape GitHub repository (only if logged in)
@app.route('/scrape', methods=['POST'])
@login_required
def scrape_repo():
    data = request.get_json()
    repo_url = data.get('url')

    # Call your scraping function
    scraped_data = fetch_github_repo_content(repo_url)

    # Return the scraped data as JSON
    return jsonify(scraped_data)

if __name__ == '__main__':
    app.run(debug=True)

