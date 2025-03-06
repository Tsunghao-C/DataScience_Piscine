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
    

def chart1(df: pd.DataFrame):
    """Draw a plot chart showing the num of customers"""
    fig, ax = plt.subplots()

    ax.plot(df['date'], df['num_customers'])
    xticks = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='MS')
    xticks_labels = xticks.strftime('%b')
    plt.xticks(xticks, xticks_labels)
    plt.ylabel("Number of customers")
    plt.grid(True)
    plt.show()


def chart2(df: pd.DataFrame):
    """Draw a bar chart showing the monthly sales"""
    months = [x.strftime('%b') for x in df['month']]
    # print(months)
    plt.bar(months, df['sales'])
    plt.ylabel("total sales in million of ₳")
    plt.xlabel("month")
    plt.show()
    

def chart3(df: pd.DataFrame):
    """Draw a filled plot showing average spend per customer"""
    fig, ax = plt.subplots()

    ax.plot(df['date'], df['avg_spend'])
    ax.fill_between(df['date'], df['avg_spend'], alpha=0.6)
    xticks = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='MS')
    xticks_labels = xticks.strftime('%b')
    plt.xticks(xticks, xticks_labels)
    plt.ylabel("average spend/customers in ₳")
    plt.ylim(0, 60)
    plt.show()

def main():
    try:
        # connect to DB
        conn = get_connection()
        print("Connected to Postgres DB")

        # retrieve data
        query1 = """
SELECT 
	DATE(event_time) AS date,
	COUNT(DISTINCT user_id) AS unique_customers
FROM (
	SELECT event_time, user_id
	FROM customers
	WHERE event_type='purchase'
)
GROUP BY date
ORDER BY date;
"""
        with conn.cursor() as cursor:
            cursor.execute(query1)
            df1 = pd.DataFrame(cursor.fetchall(), columns=['date', 'num_customers'])
        # Need to change the data type from obj to datetime!!!
        df1['date'] = pd.to_datetime(df1['date'], errors='coerce')
        # print(df1.dtypes)
        chart1(df1)

        # retrieve 2nd data
        query2 = """
SELECT 
	DATE_TRUNC('month', event_time) AS month,
	SUM(price) / 1e6 AS sales_M
FROM (
	select event_time, price
	from customers
	where event_type='purchase'
)
GROUP BY month
ORDER BY month;
"""
        with conn.cursor() as cursor:
            cursor.execute(query2)
            df2 = pd.DataFrame(cursor.fetchall(), columns=['month', 'sales'])
        df2['month'] = pd.to_datetime(df2['month'], errors='coerce')
        # print(df2.dtypes)
        # print(df2.describe)
        chart2(df2)

        # retrieve 3rd data
        query3 = """
SELECT 
	DATE(event_time) AS date,
	SUM(price) / COUNT(DISTINCT user_id) AS avg_spend
FROM (
	select event_time, price, user_id
	from customers
	where event_type='purchase'
	order by event_time
)
GROUP BY date
ORDER BY date;
"""
        with conn.cursor() as cursor:
            cursor.execute(query3)
            df3 = pd.DataFrame(cursor.fetchall(), columns=['date', 'avg_spend'])
        df3['date'] = pd.to_datetime(df3['date'])
        # print(df3.dtypes)
        # print(df3.describe)
        chart3(df3)

    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
