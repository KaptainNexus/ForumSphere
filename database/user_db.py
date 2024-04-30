from typing import Any
from database.db import get_connection
from werkzeug.security import generate_password_hash
from psycopg2 import extras
import psycopg2.extras
import datetime

def create_user(username: str, email:str, password: str) -> int:
    conn = get_connection()
    try:
        registration_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current timestamp
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO Users (username, email, password, registration_date)
                        VALUES (%s, %s, %s, %s)
                        RETURNING user_id
                        ''', (username, email, password, registration_date))
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
#test