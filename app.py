from os import abort
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.get('/secret')
def secret():
    return render_template('pages/secret.html')

@app.post('/signup')
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        abort (400)
    existing_user = ...
    if existing_user is not None:
        return redirect('/')
    return 'signup'