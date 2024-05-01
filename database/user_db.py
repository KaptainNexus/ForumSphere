from typing import Any
from database.db import get_connection
from psycopg2 import extras
import psycopg2.extras
import datetime

def create_user(firstname: str, lastname: str, email:str, username: str, password: str) -> int:
    conn = get_connection()
    try:
        registration_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current timestamp
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO users (firstname, lastname, email, username, password, registration_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING user_id
                        ''', (firstname, lastname, email, username, password, registration_date))
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id
    finally:
        conn.close()

def get_user_by_username(username: str) -> dict[str, Any] | None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.row_factory = psycopg2.extras.DictCursor  # Set row_factory on the cursor
            cur.execute('''
                        SELECT *
                        FROM users
                        WHERE username = %s
                        ''', [username])
            user = cur.fetchone()
            return user
    finally:
        conn.close()

def get_user_by_email(email: str) -> dict[str, Any] | None:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # Set row_factory on the cursor
            cur.execute('''
                        SELECT *
                        FROM users
                        WHERE email = %s
                        ''', [email])
            user = cur.fetchone()
            if user is None:
                print(f"No user found with email: {email}")
            else:
                print(f"User found: {user}")
            return user
    finally:
        conn.close()

def get_user_by_id(user_id: str) -> dict[str, Any] | None:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur: # Set row_factory on the cursor
            cur.execute('''
                        SELECT *
                        FROM users
                        WHERE user_id = %s
                        ''', [user_id])
            user = cur.fetchone()
            return user
    finally:
        conn.close()

def search_users(query: str) -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('''
                        SELECT *
                        FROM users
                        WHERE username ILIKE %s
                        ''', ['%' + query + '%'])
            users = cur.fetchall()
            return users
    finally:
        conn.close()

def update_password_change_flag(email):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('UPDATE "user" SET want_to_change_password = TRUE WHERE email = %s;', [email])
            conn.commit()
    finally:
        conn.close()

def update_user_password(user_id: int, hashed_password: str) -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE users
                        SET password = %s
                        WHERE user_id = %s
                        ''', [hashed_password, user_id])
            conn.commit()
    finally:
        conn.close()
            
def get_all_users():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('SELECT * FROM users')
            users = cur.fetchall()
            return users
    finally:
        conn.close()