from psycopg_pool import ConnectionPool
from typing import Any
from database.db import get_pool
from psycopg.rows import dict_row

def get_all_posts_db() -> list[dict[str, Any]]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT 
                    post_id,
                    title,
                    body,
                    user_id,
                    timestamp
                FROM Posts
            ''')
            return cur.fetchall()
        
def get_post_by_id(post_id: int) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            post_id,
                            title,
                            body,
                            user_id,
                            timestamp
                        FROM
                            Posts
                        WHERE post_id = %s
                        ''', [post_id])
            post = cur.fetchone()
            return post
        
def create_post(title: str, body: str, user_id: int, difficulty: int) -> int:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        INSERT INTO Posts (title, body, user_id, difficulty)
                        VALUES (%s, %s, %s, %s)
                        RETURNING post_id
                        ''', [title, body, user_id, difficulty])
            post_id = cur.fetchone().get('post_id')
            # may need to change get statement
            return post_id
        
def update_post(post_id: int, title: str, body: str) -> None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        UPDATE Posts
                        SET title = %s, body = %s
                        WHERE post_id = %s
                        ''', [title, body, post_id])
            
def delete_post(post_id: int) -> None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        DELETE FROM Posts
                        WHERE post_id = %s
                        ''', [post_id])
            
