import psycopg2
from psycopg2 import OperationalError

def connect_to_database():
    """Establish a connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="Grad2024!",
            host="localhost",
            port="5432",
            database="forumsphere"
        )
        return connection
    except OperationalError as e:
        print(f"The error '{e}' occurred.")

def create_user_table(connection):
    """Create a table for users in PostgreSQL."""
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            firstname VARCHAR(255) NOT NULL,
            lastname VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            registration_date TIMESTAMP
        )
    '''
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
        connection.commit()
        print("Users table created successfully!")
    except psycopg2.Error as error:
        print("Error while creating users table:", error)

def create_post_table(connection):
    """Create a table for posts in PostgreSQL."""
    create_table_query = """
        CREATE TABLE IF NOT EXISTS posts (
            post_id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP,
            user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE
        );
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
        connection.commit()
        print("Posts table created successfully!")
    except psycopg2.Error as error:
        print("Error while creating posts table:", error)

def main():
    # Connect to the PostgreSQL database
    connection = connect_to_database()
    if connection is not None:
        # Create the users table
        create_user_table(connection)
        # Create the posts table
        create_post_table(connection)
        # Close the database connection
        connection.close()
        print("PostgreSQL connection is closed.")

if __name__ == "__main__":
    main()
