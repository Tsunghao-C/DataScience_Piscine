import pandas as pd
import matplotlib.pyplot as plt
import psycopg2 as psy
import matplotlib.ticker as mticker


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


def month_formatter(dates) -> list[str]:
    """return simple mon string in MMM format"""
    month_map = {
        '01': 'Jan',
        '02': 'Feb',
        '03': 'Mar',
        '04': 'Apr',
        '05': 'May',
        '06': 'Jun',
        '07': 'Jul',
        '08': 'Aug',
        '09': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec'
    }
    mon = str(x).split('-')
    return month_map[mon]
    

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
    print(months)
    plt.bar(months, df['sales'])
    plt.ylabel("total sales in million of ₳")
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
	ORDER BY event_time
)
GROUP BY date
ORDER BY date;
"""
        with conn.cursor() as cursor:
            cursor.execute(query1)
            df1 = pd.DataFrame(cursor.fetchall(), columns=['date', 'num_customers'])
        # Need to change the data type from obj to datetime!!!
        df1['date'] = pd.to_datetime(df1['date'])
        print(df1.dtypes)
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
        df2['month'] = pd.to_datetime(df2['month'])
        print(df2.dtypes)
        print(df2.describe)
        chart2(df2)
    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
