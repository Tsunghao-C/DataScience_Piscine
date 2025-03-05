import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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


def pie(data: pd.DataFrame, label: str, size: str):
    """Draw a pie chart using input DataFrame"""
    labels = data[label]
    y = data[size]
    plt.pie(
        y, labels=labels, autopct='%1.1f%%',
        colors=['orange', 'red', 'green', 'blue'],
        startangle=180,
        wedgeprops={'edgecolor': 'white'}
    )
    plt.title("Event_Type Distribution")
    plt.show()


def main():
    try:
        # connect to DB
        conn = get_connection()
        print("Connected to Postgres DB")

        # retrieve data
        query = """
SELECT event_type, count(*) as counts
FROM customers
GROUP BY event_type
"""
        with conn.cursor() as cursor:
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall(), columns=['event_type', 'counts'])
        # Other method (but it is recommended to use SQLAlchemy)
        # chunks = pd.read_sql_query(query, conn, chunksize=10000)
        # df2 = pd.concat(chunks)
        pie(df, 'event_type', 'counts')
    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
