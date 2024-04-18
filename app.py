from os import abort
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('pages/index.html')


@app.get('/secret')
def secret():
    return render_template('pages/secret.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            abort(400)
        existing_user = ...  # Check if user already exists
        if existing_user is not None:
            return redirect('/')
        # Perform signup logic
        return 'signup successful'
    elif request.method == 'GET':
        # Render the signup form
        return render_template('pages/signuppage.html')

if __name__ == "__main__":
    app.run(debug=True)