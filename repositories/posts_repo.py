from datetime import datetime
from repositories.db import get_pool
from psycopg.rows import dict_row
import logging
from typing import Dict, Any, Optional


def find_all_posts(limit=15, offset=0):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT * FROM Post ORDER BY post_id LIMIT %s OFFSET %s;', (limit, offset))
            results = cur.fetchall()
            return results
        
def create_post(user_id, title, content, difficulty_level='easy'):
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

def update_post(post_id, title, content):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            now = datetime.now()
            cur.execute('''
                UPDATE Post
                SET title = %s, content = %s, last_modified_data = %s
                WHERE post_id = %s
            ''', (title, content, now, post_id))
            conn.commit()

def get_post_by_id(post_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            post_id,
                            title,
                            content,
                            user_id,
                            last_modified_data
                        FROM
                            Post
                        WHERE post_id = %s
                        ''', [post_id])
            post = cur.fetchone()
            return post
        
