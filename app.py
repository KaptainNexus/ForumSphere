from os import abort
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = Flask(__name__)

DB_NAME = "db_name"
DB_USER = "db_username"
DB_PASSWORD = "db_password"
DB_HOST = "localhost"
DB_PORT = "5432"

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/search')
def search():
    query = request.args.get('query')

    # Establish a connection to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Execute a SQL query to search for posts matching the query
    cursor.execute("SELECT * FROM Posts WHERE title LIKE %s OR content LIKE %s", ('%' + query + '%', '%' + query + '%'))
    post_results = cursor.fetchall()

    # Execute a SQL query to search for users matching the query
    cursor.execute("SELECT * FROM Users WHERE username LIKE %s", ('%' + query + '%',))
    user_results = cursor.fetchall()

    conn.close()

    return render_template('pages/components/_search_.html',post_results=post_results, user_results=user_results)

@app.get('/secret')
def secret():
    return render_template('pages/_secret_.html')

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

if __name__ == '__main__':
    app.run(debug=True)