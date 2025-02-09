import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

class RDSOperations:
    def __init__(self):
        load_dotenv()
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")

    def get_connection(self, dbname=None):
        """Get a database connection."""
        connection_params = {
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port
        }

        if dbname:
            connection_params["dbname"] = dbname

        connection = psycopg2.connect(**connection_params)
        connection.autocommit = True
        return connection

    def create_database(self, dbname):
        """Create a new database."""
        try:
            # Establish a connection
            connection = psycopg2.connect(
                user=self.user, password=self.password, host=self.host, port=self.port
            )
            connection.autocommit = True  # Ensure we don't run into transaction blocks
            with connection.cursor() as cursor:
                create_db_query = f"CREATE DATABASE {dbname};"
                cursor.execute(create_db_query)
                print(f"Database {dbname} created successfully.")
            connection.close()  # Close the connection after creating the database
        except Exception as e:
            print(f"Error creating database: {e}")

    def create_table(self, tablename, dbname):
        """Create a new table in the specified database."""
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
        try:
            with self.get_connection(dbname) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_table_query)
                    print(f"Table {tablename} created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def write_to_table(self, data, table_name, db=None):
        """Write data to the specified table."""
        insert_query = f'''
        INSERT INTO {table_name} (
            user_id, first_name, last_name, email, username, password, phone, 
            address, user_type, dob, membership_status, user_expiration
        )
        VALUES (
            %(user_id)s, %(first_name)s, %(last_name)s, %(email)s, %(username)s, 
            %(password)s, %(phone)s, %(address)s, %(user_type)s, %(dob)s, 
            %(membership_status)s, %(user_expiration)s
        );
        '''
        try:
            with self.get_connection(db) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(insert_query, data)
                    print("Data inserted successfully!")
        except Exception as e:
            print(f"Error inserting data: {e}")

'''
Main Check:
To test, assign the name you want to give your database to 'database_name' and name for the table to 'table_name'.
'''
if __name__ == "__main__":
    # assign name to your database
    database_name = "db_test"
    # assign name for your table
    table_name = "table_test"
    #initialise class
    rds_operations = RDSOperations()

    # Create database
    rds_operations.create_database(database_name)

    # Create a new table in the new database
    rds_operations.create_table(table_name, database_name)

    # Insert data into the new table
    data = {
        "user_id": "123456789",
        "first_name": "Nene",
        "last_name": "Ayo",
        "email": "nene@example.com",
        "username": "Ayo123",
        "password": "password$2004",
        "phone": "333-444-7777",
        "address": "123 Main St",
        "user_type": "student",
        "dob": datetime(1990, 1, 1),
        "membership_status": "active",
        "user_expiration": datetime(2025, 1, 1)
    }
    rds_operations.write_to_table(data, table_name, database_name)

    # Step 4: List all databases
    try:
        with rds_operations.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
                databases = cursor.fetchall()
                print("Databases:")
                for db in databases:
                    print(db[0])
    except Exception as e:
        print(f"Error listing databases: {e}")

    # Step 5: List tables in the newly created database
    try:
        with rds_operations.get_connection(database_name) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                tables = cursor.fetchall()
                print("Tables in test_db:")
                for table in tables:
                    print(table[0])
    except Exception as e:
        print(f"Error listing tables in {database_name}: {e}")

    # Step 6: Fetch all data from the 'users' table
    try:
        with rds_operations.get_connection(database_name) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()
                print(f"Data in {table_name} table:")
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"Error fetching data from 'users': {e}")