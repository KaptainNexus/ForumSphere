from flask import Flask, flash, redirect, render_template, request, url_for, request, url_for, session
from dotenv import load_dotenv
from repositories import user_repo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import os
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mailman import Mail, EmailMessage
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'a_default_secret_key_for_dev')
bcrypt=Bcrypt(app)

app.config['MAIL_SERVER'] = 'smtp.fastmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'oav2008@fastmail.com'
app.config['MAIL_PASSWORD'] = 'sxgjpvwktjmqeduu'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

hashed_password = generate_password_hash('your_plain_text_password', method='pbkdf2:sha256')
def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email, salt='email-confirm')


@app.get('/')
def fetch_all_posts():
    try:
        logging.debug("Attempting to fetch all posts from the database.")
        posts = user_repo.find_all_posts()
        if not posts:
            logging.debug('No posts found')
        else:
            logging.debug(f'Number of posts retrieved: {len(posts)}')
        return render_template('new_index.html', posts=posts)
    except Exception as e:
        logging.error(f'Failed to fetch posts: {e}', exc_info=True)
        return "Error fetching posts", 500

@app.get('/signup')
def signup():
    all_users = user_repo.get_all_users()
    return render_template('new_signup.html', users=all_users)

@app.get('/signin')
def signin():
    return render_template('new_signin.html')


@app.get('/create_post')
def show_create_post_form():
    return render_template('new_createpost.html')

@app.get('/profile')
def see_profile():
    return render_template('new_profilepage.html')

@app.get('/message')
def send_message():
    return render_template('new_message.html')


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

@app.get('/signin')
def show_signin_form():
    return render_template('signin.html')

@app.post('/signin')
def signin_user():
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    print("Attempting to sign in with:", email, password)
    # Find user by email
    user = user_repo.find_user_by_email(email)
    print("User found:", user)
    
    # Check if user is None before trying to access its properties
    if user is None:
        print("No user found with that email.")
        flash('Invalid email or password.')
        return redirect(url_for('signin'))

    # Since user is not None, it's safe to access its properties
    print("Stored hash:", user.get('password', 'No password found'))

    if bcrypt.check_password_hash(user['password'], password):
        session['user_id'] = user['user_id']
        session['username'] = user['username'] 

        flash('You are successfully logged in.')
        return redirect(url_for('fetch_all_posts'))  
    else:
        flash('Invalid email or password.')
        return redirect(url_for('signin'))
@app.post('/logout')
def logout():
    # Remove user info from the session
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have successfully logged out.')
    return redirect(url_for('signin'))


@app.get('/forgot_password')
def show_forgot_password_form():
    return render_template('forgot_password.html')


@app.post('/forgot_password')
def submit_forgot_password_form():
    email = request.form['email'].strip()
    user = user_repo.find_user_by_email(email)
    if not user:
        flash('No account associated with that email. Please try another email or <a href="/signup">sign up</a>.', 'error')
        return redirect(url_for('show_forgot_password_form'))
    
    if user:

        user_repo.update_password_change_flag(email)
        token = generate_reset_token(email)
        reset_url = url_for('reset_password', token=token, _external=True)

        msg = EmailMessage(
        subject="Password Reset Link",
        body= f"Here is your password reset link. Follow this link to reset your password: {reset_url}",
        from_email="oav2008@fastmail.com",
        to=[email]
            )
        try:
            msg.send()
            flash('Password reset link has been sent to your email.')
        except Exception as e:
            flash('An error occurred while sending the email. Please try again later.', 'error')
            app.logger.error(f"Failed to send email: {e}")
        return redirect(url_for('fetch_all_posts'))

@app.get('/reset_password/<token>')
def show_reset_password_form(token):
    try:
        serializer = URLSafeTimedSerializer(app.secret_key)
        email = serializer.loads(token, salt='email-confirm', max_age=3600)  # 1 hour expiration
    except SignatureExpired:
        flash('Your password reset link has expired.', 'error')
        return redirect(url_for('forgot_password'))
    except BadSignature:
        flash('Invalid password reset link.', 'error')
        return redirect(url_for('forgot_password'))

    return render_template('reset_password.html', token=token)

@app.post('/reset_password/<token>')
def reset_password(token):
    try:
        serializer = URLSafeTimedSerializer(app.secret_key)
        email = serializer.loads(token, salt='email-confirm', max_age=3600)  # 1 hour expiration
    except SignatureExpired:
        flash('Your password reset link has expired.', 'error')
        return redirect(url_for('forgot_password'))
    except BadSignature:
        flash('Invalid password reset link.', 'error')
        return redirect(url_for('forgot_password'))

    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if new_password != confirm_password:
        flash('Passwords do not match.', 'error')
        return redirect(url_for('reset_password', token=token))

    if len(new_password) < 8:  # Assuming you want at least 8 characters
        flash('Password must be at least 8 characters long.', 'error')
        return redirect(url_for('reset_password', token=token))

    # Assuming user_repo.update_user_password(email, new_password) exists and properly hashes the password before storing it
    if user_repo.update_user_password(email, new_password):
        flash('Your password has been updated successfully.', 'success')
        return redirect(url_for('signin'))
    else:
        flash('An error occurred while updating your password. Please try again.', 'error')
        return redirect(url_for('reset_password', token=token))

@app.post('/create_post')
def submit_create_post():
    title = request.form['title'].strip()
    content = request.form['content'].strip()

    if not (title and content):
        flash('Both title and content are required.')
        return redirect(url_for('create_post_form'))  # Assuming you have a form at this route

    # Assuming user_id is retrieved from session after user logs in
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to create a post.')
        return redirect(url_for('signin'))

    # Create new post in the database
    post_id = user_repo.create_post(user_id, title, content)
    if post_id:
        flash('Post created successfully!')
        return redirect(url_for('fetch_all_posts'))  # Redirect to the homepage or another appropriate page
    else:
        flash('An error occurred while creating the post.')
        return redirect(url_for('create_post_form'))

@app.post('/delete_post')
def delete_post():
    post_id = request.form['post_id']
    if post_id:
        user_repo.delete_post_from_db(post_id)
        flash('Post deleted successfully!')
    else:
        flash('Failed to delete the post.')
    return redirect(url_for('fetch_all_posts'))

@app.get('/search')
def search():
    query = request.args.get('q', '').strip()
    if query:
        user_results = user_repo.search_users(query)
        post_results = user_repo.search_posts_title(query)
        results = {
            'users': user_results,
            'posts': post_results
        }
    else:
        results = None
    return render_template('new_search.html', results=results)


if __name__ == "__main__":
    print("FLASK_ENV:", os.environ.get("FLASK_ENV"))
    print("Debug mode:", app.debug)
    app.run(port=5003)