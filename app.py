from flask import Flask, flash, redirect, render_template, request, url_for, session, jsonify
from dotenv import load_dotenv
from database import user_db
from database import posts_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt 
import psycopg2
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "12345"
bcrypt=Bcrypt(app)

# Function to set the logged-in user in the session
def set_logged_in_user(user_id):
    session['user_id'] = user_id
    session['logged_in'] = True

# Function to check if the user is logged in
def is_logged_in():
    return session.get('logged_in', False)

@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    return redirect(url_for('index'))

@app.get('/')
def index():
    return render_template('new_index.html', is_logged_in=is_logged_in())

@app.route('/signup', methods=['GET'])
def render_signup():
    return render_template('new_signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email'].strip()
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    confirm_password = request.form['confirm_password'].strip()

    if not username or not password or not confirm_password:
        flash('All fields are required.')
        return redirect(url_for('render_signup'))

    if password != confirm_password:
        flash('Passwords do not match.')
        return redirect(url_for('render_signup'))

    existing_user = user_db.get_user_by_username(username)
    if existing_user:
        flash('Username already exists. Please choose a different one.')
        return redirect(url_for('render_signup'))
    
    existing_email = user_db.get_user_by_email(email)
    if existing_email:
        flash('email is already in use. Please choose a different one.')
        return redirect(url_for('render_signup'))

    hashed_password = generate_password_hash(password)

    try:
        user_id = user_db.create_user(username, email, hashed_password)
        if user_id:
            flash('User successfully created. Please sign in.')
            return redirect(url_for('signin'))
        else:
            flash('Failed to create user.')
            return redirect(url_for('render_signup'))
    except Exception as e:
        flash('An error occurred. Please try again later.')
        app.logger.error(f"Error during signup: {e}")
        return redirect(url_for('render_signup'))

@app.get('/signin')
def signin():
    return render_template('new_signin.html')

@app.post('/signin')
def signin_user():
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    if not email or not password:
        flash('Email and password are required.')
        return redirect(url_for('signin'))

    user = user_db.get_user_by_email(email)
    if user and check_password_hash(user['password'], password):
        set_logged_in_user(user['user_id'])  # Set user_id and logged_in flag in session
        flash('You are successfully logged in.')
        return redirect(url_for('index'))
    else:
        flash('Invalid email or password.')
        return redirect(url_for('signin'))

@app.get('/search')
def search():
    query = request.args.get('q', '').strip()
    if query:
        user_results = user_db.search_users(query)
        post_results = posts_db.search_posts_title(query)
        results = {
            'users': user_results,
            'posts': post_results
        }
    else:
        results = None
    return render_template('new_search.html', results=results)
    
def generate_suggestions(query):
    # Query the database for users and post names that match the query
    users = user_db.search_users(query)
    posts = posts_db.search_posts_title(query)
    
    # Combine user and post suggestions
    suggestions = users + posts
    
    if not suggestions:
        suggestions.append("No results found")
    
    return suggestions

@app.get('/create_post')
def create_post():
    return render_template('new_createpost.html')

@app.get('/profile')
def see_profile():
    if not is_logged_in():  # Check if the user is not logged in
        flash('Please sign in to view your profile.')
        return redirect(url_for('signin'))

    user_id = session.get('user_id', None)  # Retrieve user_id from session
    if user_id is None:
        flash('User ID is required.')
        return redirect(url_for('index'))
    
    # Convert user_id to string if it's an integer
    user_id = str(user_id)

    user = user_db.get_user_by_id(user_id)
    
    if not user:
        flash('User not found.')
        return redirect(url_for('index'))
    
    return render_template('new_profilepage.html', user=user)


