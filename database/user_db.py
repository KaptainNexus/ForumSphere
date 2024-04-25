from psycopg_pool import ConnectionPool
from typing import Any
from database.db import get_pool
from psycopg.rows import dict_row


def get_user_by_username(username: str) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            user_id,
                            username,
                            password AS hashed_password
                        FROM
                            Users
                        WHERE username = %s
                        ''', [username])
            user = cur.fetchone()
            return user
        
def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            user_id,
                            username,
                            password AS hashed_password
                        FROM
                            Users
                        WHERE user_id = %s
                        ''', [user_id])
            user = cur.fetchone()
            return user
        
def create_user(username: str, hashed_password: str) -> int:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO Users (username or email, password)
                        VALUES (%s, %s)
                        RETURNING user_id
                        ''', [username, hashed_password])
            user_id = cur.fetchone()[0]
            return user_id
        
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
                        DELETE FROM Users
                        WHERE user_id = %s
                        ''', [user_id])