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


def get_tables(conn) -> list[tuple]:
    """return all tables in pulbic schema"""
    with conn.cursor() as cursor:
        query = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name LIKE 'data_202%_%';
"""
        cursor.execute(query)
        return cursor.fetchall()


def get_column_names(conn, table_name) -> list[str]:
    """return a list of column names of a table"""
    with conn.cursor() as cursor:
        query = f"""SELECT * FROM {table_name}"""
        cursor.execute(query)
        return [desc[0] for desc in cursor.description]


def create_table_if_not_exists(conn, table_name):
    with conn.cursor() as cursor:
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            event_time TIMESTAMP WITH TIME ZONE,
            event_type VARCHAR(255),
            product_id INTEGER,
            price NUMERIC(10,2),
            user_id BIGINT,
            user_session UUID
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
    print(f"Table '{table_name}' is ready!")


def append_data(conn, source_table: str, dest_table: str):
    """Append table from source to dest using conn obj"""
    columns = get_column_names(conn, source_table)
    column_str = ', '.join(columns)
    query = f"""
INSERT INTO {dest_table} ({column_str})
SELECT {column_str} FROM {source_table}
"""
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()
    print(f"Data from {source_table} appended to {dest_table} successfully!")


def main():
    try:
        # Build connection to DB
        conn = get_connection()
        print("Connnection to PostgreSQL!")

        # Create a table called "customers"
        if not table_exists(conn, 'customers'):
            create_table_if_not_exists(conn, 'customers')

        # get all the table_names like "data_202*_***"
        tables = [x[0] for x in get_tables(conn)]
        # print(tables)

        # iterate through tables and append data to 'customers'
        for table in tables:
            append_data(conn, table, 'customers')

    except Exception as e:
        print("Error loading data:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
