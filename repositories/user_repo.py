from repositories.db import get_pool
from psycopg.rows import dict_row # type: ignore
from typing import Any
from psycopg2 import extras # type: ignore

def get_all_users() -> list[dict[str, Any]]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=extras.DictCursor) as cur:
            cur.execute('''
                        SELECT
                            user_id,
                            username,
                            password AS hashed_password
                            email,
                            registration_date,
                            last_login_date
                        FROM
                            "Users"
                        ''')
            users = cur.fetchall()
            return users
        
def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=extras.DictCursor) as cur:
            cur.execute('''
                        SELECT
                            user_id,
                            username,
                            password AS hashed_password
                        FROM
                            "Users"
                        WHERE user_id = %s
                        ''', [user_id])
            user = cur.fetchone()
            return user
        
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

def update_user_password(user_id: int, hashed_password: str) -> None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE Users
                        SET password = %s
                        WHERE user_id = %s
                        ''', [hashed_password, user_id])
            
def delete_user(user_id: int) -> None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        DELETE FROM "Users"
                        WHERE user_id = %s
                        ''', [user_id])
