import mysql.connector
from mysql.connector import Error
#import pandas as pd 

#server connection
def create_server_connection(hst, usr, pwd):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=hst,
            user=usr,
            password=pwd
        )
        print("server connection sucessful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection
connection=create_server_connection("localhost", "root", "")
 
pw = ""
#database name
db = "passwords_manager"

#create database
def create_database(connection, query):

    cursor= connection.cursor()
    try:
        cursor.execute(query)
        print("database created successfully")
    except Error as err:
        print(f"Error: '{err}'")
create_database_query = "CREATE database passwords_manager"
create_database(connection, create_database_query)

#create database connection
def create_db_connection(hst, usr, pwd, db_name):

    connection = None
    try:
        connection=mysql.connector.connect(
            host=hst,
            user=usr,
            password=pwd,
            database=db_name
        )
        print("database connection successfull")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

#execute query
def execute_query(connection, query):

    cursor= connection.cursor()
    try:
        cursor.execute(query)
        print("query executed successfully")
    except Error as err:
        print(f"Error: '{err}'")
#create table: users
create_table_users = """
                        CREATE TABLE users(
                            username VARCHAR(100) UNIQUE PRIMARY KEY NOT NULL,
                            email VARCHAR(100) NULL, 
                            password VARCHAR(100) NOT NULL);

                    """
connection = create_db_connection("localhost", "root", pw, db)
execute_query(connection, create_table_users)

#create table: passwords
create_table_accounts= """
                            CREATE TABLE accounts(
                                id INT UNIQUE PRIMARY KEY NOT NULL,
                                username VARCHAR(100),
                                site VARCHAR(100) NULL,
                                url VARCHAR(100) NULL,
                                acc_username VARCHAR(100) NULL,
                                acc_password VARCHAR(100) NOT NULL,
                                dateModified DATE NULL,
                                FOREIGN KEY (username) REFERENCES users(username)
                            );
                        """
connection = create_db_connection("localhost", "root", pw, db)
execute_query(connection, create_table_accounts)

#MODIFY id: auto increament ID
id_auto_increment = """
                    
                    ALTER TABLE accounts
                    MODIFY COLUMN id  INT UNIQUE NOT NULL AUTO_INCREMENT;
                    """
connection = create_db_connection("localhost", "root", pw, db)
execute_query(connection, id_auto_increment)

#add 2 columns: recovery question and recovery answer
add_column = """
            ALTER TABLE users
            ADD COLUMN recovery_question VARCHAR(100) NULL,
            ADD COLUMN recovery_answer VARCHAR(100) NULL;
            """
connection = create_db_connection("localhost", "root", pw, db)
execute_query(connection, add_column)

#delete dateModified column
delCol = """ALTER TABLE accounts
            DROP COLUMN dateModified;
            """
connection = create_db_connection("localhost", "root", pw, db)
execute_query(connection, delCol)

#modify site not NOT NULL
site_modify = """
                ALTER TABLE accounts
                MODIFY COLUMN site  VARCHAR(100) NOT NULL;
                """
connection = create_db_connection("localhost", "root", pw, db)
execute_query(connection, site_modify)

#re-adding the date column
add_date = """
            ALTER TABLE accounts
            ADD COLUMN dateModified DATE NULL;
            """
connection = create_db_connection("localhost", "root", pw, db)
execute_query(connection, add_date)
