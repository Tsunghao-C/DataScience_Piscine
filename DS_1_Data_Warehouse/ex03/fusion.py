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


def fusion(conn, table1: str, table2: str):
    """remove null values and group by primary key"""
    # First create new columns for the target table
    query1 = f"""
    ALTER TABLE {table1}
    ADD COLUMN category_id BIGINT,
    ADD COLUMN category_code TEXT,
    ADD COLUMN brand VARCHAR(255);
"""
    # Then, clean up item table by handling null values
    # and insert to customers table
    query2 = f"""
    CREATE TEMPORARY TABLE tmp AS
    SELECT
        product_id,
        COALESCE(MAX(category_id), NULL) AS category_id,
        COALESCE(MAX(category_code), NULL) AS category_code,
        COALESCE(MAX(brand), NULL) AS brand
    FROM {table2}
    GROUP BY product_id;

    UPDATE {table1} c
    SET
        category_id = i.category_id,
        category_code = i.category_code,
        brand = i.brand
    FROM tmp i
    WHERE c.product_id = i.product_id;
    DROP TABLE tmp
    """
    with conn.cursor() as cursor:
        cursor.execute(query1)
        print(f"Created new columns in {table1}")
    conn.commit()
    with conn.cursor() as cursor:
        cursor.execute(query2)
    conn.commit()
    print(f"Table {table2} has JOINED to {table1}!")


def main():
    try:
        # Connect to DB
        conn = get_connection()
        print("Connection to PostgreSQL!")

        # check table exists
        if not table_exists(conn, 'customers'):
            raise AssertionError("table customers not exists")
        
        # handle duplication
        fusion(conn, 'customers', 'item')

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
