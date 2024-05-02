import os
import psycopg2

def test_database_connection():
    try:
        # Get the DB_CONNECTION environment variable
        connection_string = os.getenv('DB_CONNECTION')
        
        # Establish a connection to the database
        connection = psycopg2.connect(connection_string)
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # Execute a test query
        cursor.execute("SELECT version()")
        
        # Fetch the result
        db_version = cursor.fetchone()
        
        print("Connected to PostgreSQL successfully")
        print("PostgreSQL version:", db_version[0])
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error connecting to PostgreSQL:", e)

# Call the function to test the database connection
test_database_connection()
