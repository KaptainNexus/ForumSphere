from repositories.db import get_pool
from psycopg.rows import dict_row



def get_all_users():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT * FROM "User";')
            return cur.fetchall()
        
def get_user_by_id(user_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT * FROM "User" WHERE id = %s;', [user_id,])
            return cur.fetchone()
        
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
