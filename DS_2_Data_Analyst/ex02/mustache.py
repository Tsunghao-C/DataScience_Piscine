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
    

def ft_describe(df: pd.DataFrame):
    """mimic decribe function"""
    print(f"count\t {df['price'].count()}")
    print(f"mean\t {df['price'].mean()}")
    print(f"std\t {df['price'].std()}")
    print(f"min\t {df['price'].min()}")
    print(f"25%\t {df['price'].quantile(.25)}")
    print(f"50%\t {df['price'].quantile(.5)}")
    print(f"75%\t {df['price'].quantile(.75)}")
    print(f"max\t {df['price'].max()}")

def chart1(df: pd.DataFrame):
    """Draw a plot chart showing the num of customers"""
    fig = plt.figure(figsize=(10, 7))
    plt.boxplot(df['price'], orientation='horizontal')
    plt.xlabel('price')
    plt.show()

def chart2(df: pd.DataFrame):
    """Draw a plot chart showing the num of customers"""
    fig = plt.figure(figsize=(10, 7))
    plt.boxplot(df['price'], orientation='horizontal')
    plt.xlabel('price')
    plt.xlim(26, 46)
    plt.show()


def main():
    try:
        # connect to DB
        conn = get_connection()
        print("Connected to Postgres DB")

        # retrieve data
        query1 = """
SELECT price FROM customers
WHERE event_type='purchase'
"""
        with conn.cursor() as cursor:
            cursor.execute(query1)
            df1 = pd.DataFrame(cursor.fetchall(), columns=['price'])
        df1['price'] = pd.to_numeric(df1['price'])
        ft_describe(df1)
        # print(df1.describe())
        chart1(df1)

        # retrieve data 2
        query2 = """
SELECT total_price / baskets AS avg_basket_price
FROM(
	SELECT 
		user_id,
		COUNT(DISTINCT user_session) AS baskets,
		SUM(price) AS total_price
	FROM(
		SELECT user_id, price, user_session
		FROM customers
		WHERE event_type='purchase'
	)
	GROUP BY user_id
)
"""
        with conn.cursor() as cursor:
            cursor.execute(query2)
            df2 = pd.DataFrame(cursor.fetchall(), columns=['price'])
        df2['price'] = pd.to_numeric(df2['price'])
        ft_describe(df2)
        chart1(df2)

    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
