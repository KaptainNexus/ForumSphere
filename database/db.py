import os
import psycopg2
from psycopg2 import pool

pool = None

def get_pool():
    database = 'forumsphere'
    user = 'postgres'
    password = 'Grad2024!'
    host = 'localhost'
    port = '5432'

    try:
        global pool
        pool = psycopg2.pool.SimpleConnectionPool(1, 10, database=database, user=user, password=password, host=host, port=port)
        return pool
    except Exception as e:
        print(f"Error creating connection pool: {e}")
        return None

def get_connection():
    try:
        if pool is None:
            get_pool()
        conn = pool.getconn()  # Corrected line
        return conn
    except Exception as e:
        print(f"Error retrieving connection: {e}")
        return None
