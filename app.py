from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.get('/layout')
def layout():
    return render_template('new_index.html')

@app.get('/signup')
def signup():
    return render_template('new_signup.html')

@app.get('/signin')
def signin():
    return render_template('new_signin.html')
@app.get('/search')
def search():
    return render_template('new_search.html') 
@app.get('/create_post')
def create_post():
    return render_template('new_createpost.html')