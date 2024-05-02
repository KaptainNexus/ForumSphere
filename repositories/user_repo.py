from datetime import datetime
from repositories.db import get_pool
from psycopg.rows import dict_row
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
            cur.execute('SELECT * FROM "User" WHERE user_id = %s;', [user_id,])
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
            
def update_password_change_flag(email):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('UPDATE "User" SET want_to_change_password = TRUE WHERE email = %s;', [email])
            conn.commit()

def update_user_password(user_id: int, hashed_password: str) -> None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE users
                        SET password = %s
                        WHERE user_id = %s
                        ''', [hashed_password, user_id])
            
def delete_user(user_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        DELETE FROM "Users"
                        WHERE user_id = %s
                        ''', [user_id])
            conn.commit()
            
def update_user(user_id, username):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE "User"
                SET username = %s
                WHERE user_id = %s
                ''', (username, user_id))
            conn.commit()

# _______________________________________________________________________________________________

def find_all_posts(limit=15, offset=0):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT * FROM Post ORDER BY post_id LIMIT %s OFFSET %s;', (limit, offset))
            results = cur.fetchall()
            return results
        
def create_post(user_id, title, content, difficulty_level):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            now = datetime.now()
            cur.execute('''
                INSERT INTO Post (user_id, title, content, post_data, last_modified_data, difficulty_level)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING post_id
            ''', (user_id, title, content, now, now, difficulty_level))
            post_id = cur.fetchone()[0]
            return post_id

def delete_post_from_db(post_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM Post WHERE post_id = %s;', [post_id])
            conn.commit()

def search_users(query: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT * FROM "User" WHERE username ILIKE %s', ['%' + query + '%'])
            return cur.fetchall()

def search_posts_title(query: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT * FROM Post WHERE title ILIKE %s', ['%' + query + '%'])
            results = cur.fetchall()
            return results
        
def search_posts_by_username(username: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Find the user_id associated with the username
            cur.execute('SELECT user_id FROM "User" WHERE username ILIKE %s', ['%' + username + '%'])
            user = cur.fetchone()
            if user:
                user_id = user['user_id']
                # Search for posts by user_id
                cur.execute('SELECT * FROM Post WHERE user_id = %s', [user_id])
                results = cur.fetchall()
                return results
            else:
                return []
