from repositories.db import get_pool
from psycopg.rows import dict_row



def get_all_users():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT * FROM "User";')
            return cur.fetchall()
        
def get_user_by_id(user_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT * FROM "User" WHERE id = %s;', [user_id,])
            return cur.fetchone()
        
def find_user_by_email(email):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT user_id, email,  password, username FROM "User" WHERE email = %s;', [email])
            return cur.fetchone()


def create_user(first_name, last_name, email, password):
    pool = get_pool()
    username = f'{first_name}{last_name}'
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO "User" (username, email, password) VALUES ( %s, %s, %s);',
                (username, email, password)
            )
            conn.commit() 


'''def get_user_by_email():
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute('SELECT * FROM 'Users' WHERE email=%s, (email))
                return cursor.fetchone()'''





















'''def signin_user():
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
        return redirect(url_for('signin'))'''