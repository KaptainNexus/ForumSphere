from psycopg_pool import ConnectionPool
from typing import Any
from database.db import get_pool
from psycopg2 import extras

def get_all_posts_db() -> list[tuple]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT 
                    post_id,
                    title,
                    content,
                    user_id,
                    last_modified_data,
                    difficulty_level,
                    image_id
                FROM Posts
            ''')
            return cur.fetchall()
        
def get_post_by_id(post_id: int) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=extras.DictCursor) as cur:
            cur.execute('''
                        SELECT
                            post_id,
                            title,
                            content,
                            user_id,
                            last_modified_data,
                            difficulty_level,
                            image_id
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
                        INSERT INTO Posts (title, content, user_id, difficulty_level)
                        VALUES (%s, %s, %s, %s)
                        RETURNING post_id
                        ''', [title, body, user_id])
            post_id = cur.fetchone()[0]
            return post_id
        
            
def delete_post(post_id: int) -> None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        DELETE FROM Posts
                        WHERE post_id = %s
                        ''', [post_id])
            
