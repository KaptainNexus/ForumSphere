from flask import Flask, flash, redirect, render_template, request, url_for, session
from dotenv import load_dotenv
from repositories import user_repo
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt 
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
bcrypt=Bcrypt(app)

@app.get('/')
def index():
    return render_template('new_index.html')

@app.get('/signup')
def signup():
    all_users = user_repo.get_all_users()
    print(all_users)
    return render_template('new_signup.html', users=all_users)

@app.get('/signin')
def signin():
    return render_template('new_signin.html')
@app.get('/search')
def search():
    return render_template('new_search.html') 

@app.get('/create_post')
def create_post():
    return render_template('new_createpost.html')

@app.get('/profile')
def see_profile():
    return render_template('new_profilepage.html')

@app.get('/<int:user_id>')
def see_user(user_id):
    user = user_repo.get_user_by_id(user_id)
    return render_template('new_user.html', user=user)

@app.post('/signup')
def create_user():
    first_name = request.form['firstName'].strip()
    last_name = request.form['lastName'].strip()
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    if not (first_name and last_name and email and password):
        flash('All fields are required.')
        return redirect(url_for('signup'))

    # Encrypt password
    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check if user already exists
    user = user_repo.find_user_by_email(email)
    if user:
        flash('Email already in use.')
        return redirect(url_for('signup'))

    # Create new user
    user_repo.create_user(first_name, last_name, email, encrypted_password)
    flash('Account created successfully, please log in.')
    return redirect(url_for('signin'))


    # find user by email, BY SQL FIND "USER" WHERE....
    # if user exists and password matches, redirect to index compare form password to user.password
@app.post('/signin')
def signin_user():
    email = request.form['email'].strip()
    password = request.form['password'].strip()
    # Validation: check if not empty
    if not email or not password:
        flash('Email and password are required.')
        return redirect(url_for('signin'))

    # Find user by email
    user = user_repo.find_user_by_email(email)
    if user and check_password_hash(user['password'], password):
    # If user exists and password matches
        session['user_id'] = user['id']  # Assuming there's a user ID field
        flash('You are successfully logged in.')
        return redirect(url_for('index'))  # Redirect to the homepage or dashboard
    else:
    # If no user or password doesn't match
        flash('Invalid email or password.')
        return redirect(url_for('signin'))










'''def signin():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = get_user_by_email(email)
    if not user:
        msg = 'Incorrect Email or Email does not exist. Try again.'
    isValid = bcrypt.check_password_hash(user.password, password)
    if not isValid:
        msg = 'Incorrect Password. Try again.'
    if msg:
        return render_template('pages/loginoage.html', msg = msg)
    session['user'] = {'first_name': user.first_name,}

    return redirect('/') '''
