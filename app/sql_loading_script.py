import psycopg2
from psycopg2 import sql
from django.db import connection

def Run_SQL_Script(file_path):
    # Read SQL script content from file and split into individual statements
    with open(file_path, "r") as sql_file:
        sql_script = sql_file.read()
        sql_statements = sql_script.split(';')  # Split on semicolon

    # Connect to the database
    try:
        # connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Run SQL queries from the script
        for statement in sql_statements:
            if statement.strip():  # Avoid executing empty statements
                cursor.execute(sql.SQL(statement))

        # Commit the transaction
        connection.commit()

        print("SQL queries executed successfully.")

    except (Exception, psycopg2.Error) as error:
        print("Error:", error)
        return [error, 0]
    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed.")
            return ["SQL Script executed successfully.", 1]
