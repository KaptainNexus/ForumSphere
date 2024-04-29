import psycopg2
from psycopg2 import OperationalError

def create_user_table():
    """Create a table in PostgreSQL."""
    try:
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            user="postgres",
            password="Grad2024!",
            host="localhost",
            port="5432",
            database="forumsphere"
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Define the SQL command to create the table
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                registration_date TIMESTAMP
            )
        '''

        # Execute the SQL command to create the table
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully!")

    except OperationalError as e:
        print(f"The error '{e}' occurred.")

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")

# Call the function to create the table
def create_post_table():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            user="postgres",
            password="Grad2024!",
            host="localhost",
            port="5432",
            database="forumsphere"
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Define the SQL query to create the posts table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS posts (
            post_id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP,
            user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE
        );
        """

        # Execute the SQL query to create the posts table
        cursor.execute(create_table_query)

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        print("Posts table created successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while creating posts table:", error)

# Call the functions to create the tables
create_user_table()
create_post_table()
