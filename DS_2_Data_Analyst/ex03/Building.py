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
 

def chart(df: pd.DataFrame, df2: pd.DataFrame):
    """
    Draw two histogram showing 
    the number of customers according to order frequency
    and the money spent
    """
    frequency = [x for x in df['num_orders'] if x <= 40]
    monetary = [x for x in df2['total_spend'] if x <= 250]
    # Draw 1 row and 2 columns of subplots in one output
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))

    # First hist: Frequency
    axs[0].grid(True, zorder=-1)
    axs[0].hist(frequency, bins=5, edgecolor='w')
    axs[0].set_ylabel('customers')
    axs[0].set_xlabel('frequency')
    axs[0].set_xticks(range(0, 39, 10))
    axs[0].set_ylim(0, 70000)

    # Second hist: Monetary
    axs[1].grid(True, zorder=-1)
    axs[1].hist(monetary, bins=5, edgecolor='w')
    axs[1].set_ylabel('customers')
    axs[1].set_xlabel('Monetary value in ₳')
    # Set grid transparant and behind histograms
    for ax in axs:
        ax.yaxis.grid(True, linestyle='-', alpha = 0.5)
        ax.set_axisbelow(True)

    plt.tight_layout()
    plt.show()


def main():
    try:
        # connect to DB
        conn = get_connection()
        print("Connected to Postgres DB")

        # retrieve data
        query1 = """
SELECT user_id, COUNT(*)
FROM customers
WHERE event_type='purchase'
GROUP BY user_id
"""
        query2 = """
SELECT user_id, SUM(price)
FROM customers
WHERE event_type='purchase'
GROUP BY user_id
"""
        with conn.cursor() as cursor:
            cursor.execute(query1)
            df1 = pd.DataFrame(cursor.fetchall(), columns=['customer', 'num_orders'])
            cursor.execute(query2)
            df2 = pd.DataFrame(cursor.fetchall(), columns=['customer', 'total_spend'])
        # print(df2.dtypes)
        # print(df2)
        chart(df1, df2)

    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
