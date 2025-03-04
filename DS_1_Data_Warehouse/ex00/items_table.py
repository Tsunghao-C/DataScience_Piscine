import pandas as pd
import psycopg2 as psy
import os


# # For quicky check data status
# df = pd.read_csv("/tmp/DS_Piscine/subject/item/item.csv")
# print(df.shape)
# # See all the column nams
# print(df.columns)
# # See last 10 rows
# print(df.iloc[-10:, :])
# # See unique values of a column
# print(df['category_code'].unique())
# print("----------------------")
# print(df.describe())


# Database connection details
DB_USER = "tsuchen"
DB_PASSWORD = "mysecretpassword"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "piscineds"

# Path to data
path_prefix = "/tmp/subject/item/"
data_to_load = [
    "item.csv",
]

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


def create_table_if_not_exists(conn, table_name):
    with conn.cursor() as cursor:
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            product_id INTEGER,
            category_id BIGINT,
            category_code TEXT,
            brand VARCHAR(255)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
    print(f"Table '{table_name}' is ready!")


# Function to load csv using COPY (bulk insert)
def copy_csv_to_db(file_path, table_name, conn):
    with conn.cursor() as cursor:
        with open(file_path, "r") as file:
            next(file)
            cursor.copy_expert(
                f"COPY {table_name} FROM STDIN WITH CSV HEADER",
                file)
        conn.commit()
    print(f"{table_name} loaded successfully!")


if __name__ == "__main__":
    try:
        # Build connection to DB
        conn = get_connection()
        print("Connnection to PostgreSQL!")

        # iterate through all CSV files
        for data in data_to_load:
            table_name = data.split('.')[0]
            full_path = os.path.join(path_prefix, data)
            # Check if table already exists, create new one if not
            if not table_exists(conn, table_name):
                create_table_if_not_exists(conn, table_name)

            # Copy csv to DB table (bulk import)
            copy_csv_to_db(full_path, table_name, conn)

        print("All CSV files loaded successfully")

    except Exception as e:
        print("Error loading data:", e)
    finally:
        conn.close()
