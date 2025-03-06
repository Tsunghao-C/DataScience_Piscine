import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psycopg2 as psy
from sklearn.cluster import KMeans


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


def barh_chart(df: pd.DataFrame):
    """Draw customer level barchart"""
    fig, ax = plt.subplots(figsize=(12, 5))
    hbars = ax.barh(
        y=df['custom_level'],
        width=df['customer_count'],
        align='center',
        color=['red', 'blue', 'green', 'silver', 'gold', 'pink'])
    ax.set_xlabel("number of customers")
    # Label with data
    ax.bar_label(hbars)
    plt.show()


def main():
    try:
        # connect to DB
        conn = get_connection()
        print("Connected to Postgres DB")

        # retrieve data
        query1 = """
SELECT
	CASE
		WHEN purchased_months = 5 THEN 'loyal platinum'
		WHEN purchased_months = 4 THEN 'loyal gold'
		WHEN purchased_months = 3 THEN 'loyal silver'
		WHEN purchased_months = 2 THEN 'active'
		WHEN purchased_months = 1 AND NOT (last_purch_month = 1 OR last_purch_month = 2) THEN 'inactive'
		WHEN purchased_months = 1 AND purchase_times = 1 THEN 'new customer'
		WHEN purchased_months = 1 AND purchase_times > 1 THEN 'active'
	END AS customer_category,
	COUNT(DISTINCT user_id) AS customer_count
FROM (
	SELECT
		user_id,
		COUNT (DISTINCT EXTRACT(MONTH FROM event_time)) AS purchased_months,
		EXTRACT(MONTH FROM MAX(event_time)) AS last_purch_month,
		COUNT (DISTINCT event_time) AS purchase_times
	FROM customers
	WHERE event_type='purchase'
	GROUP BY user_id
) AS purchase_counts
GROUP BY customer_category
ORDER BY customer_count DESC;
"""
        columns = ['custom_level', 'customer_count']
        with conn.cursor() as cursor:
            cursor.execute(query1)
            # data = cursor.fetchall()
            df = pd.DataFrame(cursor.fetchall(), columns=columns)
        print(df)
        barh_chart(df)




    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
