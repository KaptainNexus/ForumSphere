from flask import Flask, flash, redirect, render_template, request, url_for, request, url_for, session, current_app
from dotenv import load_dotenv
from database import user_db, posts_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import os
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mailman import Mail, EmailMessage



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

# Function to set the logged-in user in the session
def set_logged_in_user(user_id):
    session['user_id'] = user_id
    session['logged_in'] = True

# Function to check if the user is logged in
def is_logged_in():
    return session.get('logged_in', False)

@app.get('/')
def index():
    posts = posts_db.get_all_posts()

    # Log the content of each post for debugging
    return render_template('new_index.html', posts=posts, is_logged_in=is_logged_in())


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

@app.route('/create_post', methods=['GET'])
def render_create_post_form():
    return render_template('new_createpost.html')

@app.route('/create_post', methods=['POST'])
def create_post():
    if not is_logged_in():  # Check if the user is not logged in
        flash('Please sign in to create a post.')
        return redirect(url_for('signin'))

    title = request.form['title']
    content = request.form['content']
    user_id = session.get('user_id')

    if not title or not content:
        flash('Title and content are required for creating a post.')
        return redirect(url_for('create_post'))

    # Create the post
    post_id = posts_db.create_post(title, content, user_id)

    if post_id:
        flash('Post created successfully.')
    else:
        flash('Failed to create post. Please try again.')

    # Redirect to index page
    return redirect(url_for('index'))

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


@app.get('/<int:user_id>')
def see_user(user_id):
    user = user_db.get_user_by_id(user_id)
    return render_template('new_user.html', user=user)

@app.route('/signup', methods=['GET'])
def render_signup():
    return render_template('new_signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    first_name = request.form['firstName'].strip()
    last_name = request.form['lastName'].strip()
    email = request.form['email'].strip()
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    confirm_password = request.form['confirm_password'].strip()

    if not first_name or not last_name or not email or not username or not password or not confirm_password:
        flash('All fields are required.')
        return redirect(url_for('render_signup'))

    if password != confirm_password:
        flash('Passwords do not match.')
        return redirect(url_for('render_signup'))

    # Check if user already exists
    existing_user = user_db.get_user_by_email(email)
    if existing_user:
        flash('Email already in use.')
        return redirect(url_for('render_signup'))

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create new user
    user_id = user_db.create_user(first_name, last_name, email, username, hashed_password)
    if user_id:
        flash('Account created successfully. Please log in.')
        return redirect(url_for('signin_user'))
    else:
        flash('Failed to create account. Please try again.')
        return redirect(url_for('render_signup'))


@app.get('/signin')
def show_signin_form():
    return render_template('new_signin.html')

@app.post('/signin')
def signin_user():
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    if not email or not password:
        flash('Email and password are required.')
        return redirect(url_for('signin'))

    user = user_db.get_user_by_email(email)
    print("User retrieved from the database:", user)  # Add this debugging statement

    if user:
        hashed_password_from_db = user['password']
        print("Hashed password from the database:", hashed_password_from_db)  # Add this debugging statement
        if check_password_hash(hashed_password_from_db, password):
            set_logged_in_user(user['user_id'])  # Set user_id and logged_in flag in session
            flash('You are successfully logged in.')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('signin_user'))
    else:
        flash('Invalid email or password.')
        return redirect(url_for('signin_user'))
    
@app.post('/logout')
def logout():
    # Remove user info from the session
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have successfully logged out.')
    return redirect(url_for('signin_user'))


@app.get('/forgot_password')
def show_forgot_password_form():
    return render_template('forgot_password.html')


@app.post('/forgot_password')
def submit_forgot_password_form():
    email = request.form['email'].strip()
    user = user_db.get_user_by_email(email)
    if not user:
        flash('No account associated with that email. Please try another email or <a href="/signup">sign up</a>.', 'error')
        return redirect(url_for('show_forgot_password_form'))
    
    if user:

        user_db.update_password_change_flag(email)
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
        return redirect(url_for('index'))

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
    if user_db.update_user_password(email, new_password):
        flash('Your password has been updated successfully.', 'success')
        return redirect(url_for('signin'))
    else:
        flash('An error occurred while updating your password. Please try again.', 'error')
        return redirect(url_for('reset_password', token=token))
    




if __name__ == "__main__":
    print("FLASK_ENV:", os.environ.get("FLASK_ENV"))
    print("Debug mode:", app.debug)
    app.run(port=5003)