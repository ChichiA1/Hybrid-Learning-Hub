import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def create_db_connection(dbname=None):
    if dbname:
        dbconn = psycopg2.connect(dbanme=dbname,
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

# # Execute the query
    cur.execute(create_db_query)
    print(f"Database {dbname} created successfully.")
#
# # Commit the transaction
    dbconn.commit()
    dbconn.close()


def create_table(tablename, dbname):
    # SQL query to create a table
    create_table_query = f'''
    CREATE TABLE {tablename} (
        student_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        email VARCHAR(100),
        usertype VARCHAR(10),
        enrolled_date DATE
    );
    '''
    dbconn = get_db_connection(dbname)
    cur = dbconn.cursor()
    # Execute the query
    cur.execute(create_table_query)
    print("Table 'students' created successfully.")

    # Commit the transaction (not necessary for 'CREATE TABLE' but good practice)
    dbconn.commit()
    dbconn.close()


if __name__ == "__main__":
    create_table("Users")


