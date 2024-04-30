from flask import Flask, flash, redirect, render_template, request, url_for, request, url_for, session
from dotenv import load_dotenv
from repositories import user_repo
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



@app.get('/')
def index():
    return render_template('new_index.html')

@app.get('/signup')
def signup():
    all_users = user_repo.get_all_users()
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
    print("Stored hash:", user.get('password', 'No password found'))
    

    if user and bcrypt.check_password_hash(user['password'], password):
        session['user_id'] = user['user_id']
        session['username'] = user['username'] 

        flash('You are successfully logged in.')
        return redirect(url_for('index'))  
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
    if user_repo.update_user_password(email, new_password):
        flash('Your password has been updated successfully.', 'success')
        return redirect(url_for('signin'))
    else:
        flash('An error occurred while updating your password. Please try again.', 'error')
        return redirect(url_for('reset_password', token=token))



if __name__ == "__main__":
    print("FLASK_ENV:", os.environ.get("FLASK_ENV"))
    print("Debug mode:", app.debug)
    app.run(port=5003)