import psycopg2
import os

def connect_to_database():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            dbname=os.environ.get('DN_NAME', 'movies'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', '31082013bA'),
            port=os.environ.get('DB_PORT', '5433')
        )

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        return conn, cur

    except psycopg2.Error as e:
        print(f"Unable to connect to the database {e}")
        return None, None


def disconnect_from_database(conn, cur):
    if cur is not None:
        cur.close()

    if conn is not None:
        conn.commit()
        conn.close()