import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psycopg2 as psy
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


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

def scatter_chart(df: pd.DataFrame):
    """Draw scatter plot showing customer categories respect to recency and frequency"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(
        df['avg_recency'],
        df['avg_frequency'],
        s=df['size'] / 150,
        c='blue',
        alpha=0.6,
        edgecolors='black')
    for i, txt in enumerate(df['custom_level']):
        ax.annotate(f"{txt}: {df['size'][i]}", (df['avg_recency'][i] - 0.2, df['avg_frequency'][i] + 0.2),
                    fontsize=10, xytext=(5,5), textcoords='offset points')
    plt.xlabel("Average Recency (Month)")
    plt.xlim(-0.5, 4.0)
    plt.ylim(0, 12)
    plt.ylabel("Average Frequency")
    plt.grid(True)
    plt.show()

def main():
    try:
        # connect to DB
        conn = get_connection()
        print("Connected to Postgres DB")

        # 1st use recency and frequncy to determine number of clusters

        # retrieve data
        query1 = """
SELECT
	CASE
		WHEN NOT (last_purch_month = 1 OR last_purch_month = 2 OR last_purch_month = 12) THEN 'inactive'
		WHEN purchased_months = 5 THEN 'loyal platinum'
		WHEN purchased_months = 4 THEN 'loyal gold'
		WHEN purchased_months = 3 THEN 'loyal silver'
		WHEN purchased_months = 2 THEN 'active'
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
            df = pd.DataFrame(cursor.fetchall(), columns=columns)
        print(df)
        barh_chart(df)
        scalar = StandardScaler()
        scaled_data = scalar.fit_transform(df['customer_count'].to_numpy().reshape(-1, 1))
        # print(scaled_data)
        num_clusters = 6
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(scaled_data)

        cluster_average = []



        query2 = """
SELECT
	customer_category,
	AVG(recency) AS avg_recency,
	AVG(frequency) AS avg_frequency,
    COUNT(*) AS counts
FROM (
	SELECT
		CASE
			WHEN NOT (last_purch_month = 1 OR last_purch_month = 2 OR last_purch_month = 12) THEN 'inactive'
			WHEN purchased_months = 5 THEN 'loyal platinum'
			WHEN purchased_months = 4 THEN 'loyal gold'
			WHEN purchased_months = 3 THEN 'loyal silver'
			WHEN purchased_months = 2 THEN 'active'
			WHEN purchased_months = 1 AND purchase_times = 1 THEN 'new customer'
			WHEN purchased_months = 1 AND purchase_times > 1 THEN 'active'
		END AS customer_category,
		CASE
			WHEN last_purch_month = 2 THEN 0
			WHEN last_purch_month = 1 THEN 1
			WHEN last_purch_month = 12 THEN 2
			WHEN last_purch_month = 11 THEN 3
			WHEN last_purch_month = 10 THEN 4
		END AS recency,
		purchase_times AS frequency,
		purchased_months
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
)
GROUP BY customer_category
"""
        # columns2 = ['custom_level', 'avg_recency', 'avg_frequency', 'size']
        # with conn.cursor() as cursor:
        #     cursor.execute(query2)
        #     df2 = pd.DataFrame(cursor.fetchall(), columns=columns2)
        # df2['avg_recency'] = pd.to_numeric(df2['avg_recency'], errors='coerce')
        # df2['avg_frequency'] = pd.to_numeric(df2['avg_frequency'], errors='coerce')
        # print(df2)
        # scatter_chart(df2)

    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
