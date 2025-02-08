import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def create_db_connection(dbname=None):

    if dbname:
        dbconn = psycopg2.connect(dbname=dbname,
                                  user=os.getenv("USER"),
                                  password=os.getenv("PASSWORD"),
                                  host=os.getenv("HOST"),
                                  port=os.getenv("PORT"))
    else:
        dbconn = psycopg2.connect(user=os.getenv("USER"),
                                  password=os.getenv("PASSWORD"),
                                  host=os.getenv("HOST"),
                                  port=os.getenv("PORT"))

    dbconn.autocommit = True
    # cursor = dbconn.cursor()
    return dbconn


def create_database(dbname):

    dbconn = create_db_connection()
    cur = dbconn.cursor()
    # SQL query to create a new database
    create_db_query = f"CREATE DATABASE {dbaname};"

    # Execute the query
    cur.execute(create_db_query)
    print(f"Database {dbname} created successfully.")

    # Commit the transaction
    dbconn.commit()
    dbconn.close()


def create_table(tablename, dbname):
    # SQL query to create a table
    create_table_query = f'''
    CREATE TABLE {tablename} (
        user_id VARCHAR(50) PRIMARY KEY,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        username VARCHAR(20) UNIQUE,
        password VARCHAR(100),
        phone VARCHAR(12),  -- Phone number format: XXX-XXX-XXXX
        address VARCHAR(255),
        user_type VARCHAR(50),  -- Could be an ENUM if predefined types exist
        dob TIMESTAMP,  -- Date of birth as timestamp
        membership_status VARCHAR(50),  -- Could be an ENUM as well
        user_expiration TIMESTAMP  -- Renewal date as timestamp
    );
    '''
    dbconn = create_db_connection(dbname)
    cur = dbconn.cursor()
    # Execute the query
    cur.execute(create_table_query)
    print(f"Table {tablename} created successfully.")

    # Commit the transaction (not necessary for 'CREATE TABLE' but good practice)
    dbconn.commit()
    cur.close()
    dbconn.close()


def write_to_table(data, table_name, db=None):

    # Prepare the insert query with named placeholders
    insert_query = f'''
    INSERT INTO {table_name} (user_id, first_name, last_name, email, username, password, phone, address, user_type, 
    dob, membership_status, user_expiration)
    VALUES (%(user_id)s, %(first_name)s, %(last_name)s, %(email)s, %(username)s, %(password)s, %(phone)s, %(address)s, 
    %(user_type)s, %(dob)s, %(membership_status)s, %(user_expiration)s);
    '''

    # Connect to the PostgreSQL database
    try:
        # Establish connection
        connection = create_db_connection(db)
        cursor = connection.cursor()

        # Execute the insert query with the data
        cursor.execute(insert_query, data)

        # Commit the changes to the database
        connection.commit()

        print("Data inserted successfully!")

    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def list_all_databases():
    # Connect to the RDS instance
    dbconn = create_db_connection()

    # Create a cursor object to interact with the database
    cursor = dbconn.cursor()

    # List all databases
    cursor.execute("SELECT datname FROM pg_database;")
    databases = cursor.fetchall()
    print("Databases:", databases)

    # Drop the database
    # cursor.execute("DROP DATABASE lms2026;"

    cursor.close()
    dbconn.close()


def list_tables_in_database(dbname):

    connection = create_db_connection(dbname)
    try:
        # Create a cursor object to interact with the database
        with connection.cursor() as cursor:
            # Query to list all tables in the public schema
            query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
            """

            # Execute the query
            cursor.execute(query)

            # Fetch all rows from the executed query
            tables = cursor.fetchall()

            # Print the list of tables
            print("Tables in the 'public' schema:")
            for table in tables:
                print(table[0])  # table[0] because each entry is a tuple with one item (table name)

    finally:
        # Close the connection to the database
        connection.close()


def list_data_in_table(dbname, table_name):

    connection = create_db_connection(dbname)
    try:
        # Create a cursor object to interact with the database
        with connection.cursor() as cursor:
            # Example query to read data from a table (replace 'your_table_name' with your actual table)
            query = (f"SELECT * FROM {table_name};")

            cursor.execute(query)

            # Fetch all rows from the executed query
            rows = cursor.fetchall()
            print(rows)

            # Print the data
            for row in rows:
                print(row) # Each 'row' is a tuple of column values from the table

    finally:
        # Close the connection to the database
        connection.close()


if __name__ == "__main__":
    # Creating the dictionary
    user_data = {
        "user_id": "12345678",  # String of length 8
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",  # Valid email format
        "username": "john1234",  # Max length of 8 characters
        "password": "securePassword123",  # Any string (typically encrypted in real scenarios)
        "phone": "123-456-7890",  # Valid phone number format (XXX-XXX-XXXX)
        "address": "123 Main St, Anytown, USA",  # Example address string
        "user_type": "student",  # Enum for User_type
        "dob": datetime(1990, 5, 15),  # Example date of birth
        "membership_status": "Active",  # Optional, defaults to 'active' if not provided
        "user_expiration": datetime(2025, 12, 31),  # Example expiration date
    }
    # list all databases
    list_all_databases()
    # create a table **ENTER NEW TABLE NAME**
    create_table("Users_Table2", os.getenv("DBNAME"))
    # list all table in lms2026 database
    list_tables_in_database(os.getenv("DBNAME"))
    # write data to table in database **ENTER TABLE NAME**
    write_to_table(user_data, "Users_Table2", os.getenv("DBNAME"))
    # list data in table **ENTER TABLE NAME**
    list_data_in_table(os.getenv("DBNAME"), "Users_Table2")
