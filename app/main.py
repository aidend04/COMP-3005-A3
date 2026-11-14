import psycopg2
from psycopg2 import errors


def main():
    conn = sql_connection()


def sql_connection():
    try:
        # Connect to postgres DB
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="temp",
            user="postgres",
            password="secret",
        )
        return conn
    except errors.ConnectionFailure as e:
        print(f"Failed to connect to the database: {e}")
