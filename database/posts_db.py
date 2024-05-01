from typing import Any
from database.db import get_connection
from psycopg2 import extras
import psycopg2.extras
import datetime

def create_post(title: str, body: str, user_id: int) -> int:
    conn = get_connection()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO Posts (title, content, user_id, timestamp)
                        VALUES (%s, %s, %s, %s)
                        RETURNING post_id
                        ''', (title, body, user_id, timestamp))
            post_id = cur.fetchone()[0]
            conn.commit()
            return post_id
    finally:
        conn.close()

def get_all_posts() -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('''
                SELECT 
                    post_id,
                    title,
                    content,
                    user_id,
                    timestamp
                FROM Posts
            ''')
            posts = cur.fetchall()
            return [dict(post) for post in posts]
    finally:
        conn.close()

def get_post_by_id(post_id: int) -> dict[str, Any] | None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.row_factory = psycopg2.extras.DictCursor
            cur.execute('''
                        SELECT
                            post_id,
                            title,
                            content,
                            user_id,
                            timestamp
                        FROM
                            Posts
                        WHERE post_id = %s
                        ''', [post_id])
            post = cur.fetchone()
            return post
    finally:
        conn.close()

def update_post(post_id: int, title: str, body: str) -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE Posts
                        SET title = %s, content = %s
                        WHERE post_id = %s
                        ''', [title, body, post_id])
            conn.commit()
    finally:
        conn.close()

def delete_post(post_id: int) -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('''
                        DELETE FROM Posts
                        WHERE post_id = %s
                        ''', [post_id])
            conn.commit()
    finally:
        conn.close()

def search_posts_title(title: str) -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.row_factory = psycopg2.extras.DictCursor
            cur.execute('''
                        SELECT
                            post_id,
                            title,
                            content,
                            user_id,
                            timestamp
                        FROM
                            Posts
                        WHERE title ILIKE %s
                        ''', ['%' + title + '%'])
            posts = cur.fetchall()
            return [dict(post) for post in posts]
    except Exception as e:
        print(f"Error in search_posts_title: {e}")
        return []
    finally:
        conn.close()
