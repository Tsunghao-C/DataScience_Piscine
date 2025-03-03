import pandas as pd
import psycopg2 as psy
import os


# Database connection details
DB_USER = "tsuchen"
DB_PASSWORD = "mysecretpassword"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "piscineds"

# Path to data
path_prefix = "/tmp/subject/customer/"
data_to_load = [
    "data_2022_dec.csv",
    "data_2022_nov.csv",
    "data_2022_oct.csv",
    "data_2023_jan.csv"
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


# Not used because using sqlalchemy.tosql if uploading row by row
# which is too slow
def load_csv(path: str) -> pd.DataFrame:
    """
    Load csv file and return pd.Dataframe
    """
    try:
        if not path or not isinstance(path, str):
            raise AssertionError("bad input")
        if not path.lower().endswith(".csv"):
            raise AssertionError("bad input, only accept .csv")
        loaded_data = pd.read_csv(path, index_col=None)
        print(f"Loading dataset of dimensions {loaded_data.shape}")
        return loaded_data
    except AssertionError as e:
        print("AssertionError:", e)
    except FileNotFoundError as e:
        print("FileNotFound:", e)
    return None


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

        conn.close()
        print("All CSV files loaded successfully")

    except Exception as e:
        print("Error loading data:", e)


# Basic Workflow of "psycopg2"
# 1. Establish a connection to PostgreSQL DB
#       conn = psycopg2.connect()
# 2. Create a cursor (a temp workspace for Executing queries)
#       with conn.cursor() as cursor (or cursor = conn.cursor())
# 3. Execute queries using the cursor object
#       cursor.execute("SELECT * FROM my_table;")
# 4. commit transactions to apply changes
#       conn.commit()
# 5. Close the cursor and connection
#       cursor.close(); conn.close()

### IMPORTANT ###
# The SQL output is temporarily saved in cursor object of cursor.execut()
# You must call conn.commit() to apply the changes. If not, there will be no changes

# However, if the conn object is created using "with" like:

# with psycopg2.connect() as conn:
#       with conn.cursor() as cursor:
#           cursor.execute("INSERT INTO mytable(...)")

# This case, it will automatically commits when 'with' block ends
