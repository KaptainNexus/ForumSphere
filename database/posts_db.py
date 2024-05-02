from psycopg_pool import ConnectionPool
from typing import Any
from repositories.db import get_pool
from psycopg.rows import dict_row

def get_all_posts_db() -> list[tuple]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
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
        
def create_post(title: str, body: str, user_id: int) -> int:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO Posts (title, content, user_id, difficulty)
                        VALUES (%s, %s, %s, %s)
                        RETURNING post_id
                        ''', [title, body, user_id])
            post_id = cur.fetchone()[0]
            return post_id
        
def update_post(post_id: int, title: str, body: str) -> None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE Posts
                        SET title = %s, body = %s
                        WHERE post_id = %s
                        ''', [title, body, post_id])
            
def delete_post(post_id: int) -> None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        DELETE FROM Posts
                        WHERE post_id = %s
                        ''', [post_id])
            

def set_post_difficulty(post_id: int, difficulty: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE Post
                        SET difficulty_level = %s
                        WHERE post_id = %s
                        ''', [difficulty, post_id])
           ''' conn.commit()'''