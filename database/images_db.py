from psycopg_pool import ConnectionPool
from typing import Any
from database.db import get_pool
from psycopg.rows import dict_row


def get_all_images_db() -> list[dict[str, Any]]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT 
                    image_id,
                    image_link,
                    timestamp
                FROM Images
            ''')
            return cur.fetchall()

def get_image_by_id(image_id: int) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            image_id,
                            image_link,
                            timestamp
                        FROM
                            Images
                        WHERE image_id = %s
                        ''', [image_id])
            image = cur.fetchone()
            return image
        
def create_image(image_link: str) -> int:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        INSERT INTO Images (image_link)
                        VALUES (%s)
                        RETURNING image_id
                        ''', [image_link])
            image_id = cur.fetchone().get('image_id') 
            # may need to update get(image_id)
            return image_id
        
"""add true false for return type
how to test is query was successful pscyopg"""
def update_image_link(image_id: int, image_link: str) -> None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        UPDATE Images
                        SET image_link = %s
                        WHERE image_id = %s
                        ''', [image_link, image_id])
            
def delete_image(image_id: int) -> None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        DELETE FROM Images
                        WHERE image_id = %s
                        ''', [image_id])

