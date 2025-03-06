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
 

def boxplot(df: pd.DataFrame):
    """
    draw boxplots per column to see distribution
    """

    # Draw 1 row and 2 columns of subplots in one output
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))

    # First hist: Frequency
    axs[0].grid(True, zorder=-1)
    axs[0].hist(frequency, bins=5, edgecolor='w')
    axs[0].set_ylabel('customers')
    axs[0].set_xlabel('frequency')
    axs[0].set_xticks(range(0, 39, 10))
    axs[0].set_ylim(0, 70000)


def main():
    try:
        # connect to DB
        conn = get_connection()
        print("Connected to Postgres DB")

        # retrieve data
        query1 = """
SELECT
	user_id,
	SUM(price) as sales,
	COUNT(*) as item_purchased,
	COUNT(DISTINCT event_time) as trans,
	SUM(price) / COUNT(*) as avg_item_sales,
	SUM(price) / COUNT(DISTINCT event_time) as avg_trans_sales
FROM customers
WHERE event_type='purchase'
GROUP BY user_id
ORDER BY trans, avg_trans_sales DESC;
"""
        columns = ['user_id', 'tol_sales', 'item_purchased', 'num_trans', 'sales_per_item', 'sales_per_trans']
        with conn.cursor() as cursor:
            cursor.execute(query1)
            df1 = pd.DataFrame(cursor.fetchall(), columns=columns)
        
        for column in df1.columns:
            if pd.api.types.is_object_dtype(df1[column]):
                df1[column] = pd.to_numeric(df1[column], errors='coerce')
        # print(df1)
        # print(df1.columns)
        # print(df1.describe)
        print(df1.dtypes)
        # boxplot(df1)

    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
