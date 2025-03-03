import psycopg2 as psy


# Database connection details
DB_USER = "tsuchen"
DB_PASSWORD = "mysecretpassword"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "piscineds"


def get_connection():
    """return connecting object to Postgres DB"""
    return psy.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def table_exists(conn, table_name):
    # with keyword automatically close object that needs to close
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = %s
            );
        """, (table_name,))
        return cursor.fetchone()[0]


def get_column_names(conn, table_name) -> list[str]:
    """return a list of column names of a table"""
    with conn.cursor() as cursor:
        query = f"""SELECT * FROM {table_name}"""
        cursor.execute(query)
        return [desc[0] for desc in cursor.description]



def remove_duplicate(conn, table: str):
    """remove all duplicate rows in table"""
    columns = get_column_names(conn, table)
    column_str = ', '.join(columns)
    query = f"""
DELETE FROM {table}
WHERE ctid NOT IN (
    SELECT MIN(ctid)
    FROM {table}
    GROUP BY {column_str}
);
"""
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()
    print(f"Table {table} has removed duplicated rows!")


def main():
    try:
        # Connect to DB
        conn = get_connection()
        print("Connection to PostgreSQL!")

        # check table exists
        if not table_exists(conn, 'customers'):
            raise AssertionError("table customers not exists")
        
        # handle duplication
        remove_duplicate(conn, 'customers')

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
