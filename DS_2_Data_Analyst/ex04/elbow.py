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
 

def boxplot(df: pd.DataFrame):
    """
    draw boxplots per column to see distribution
    """

    # Draw 1 row and 2 columns of subplots in one output
    num_cols = len(df.columns)
    rows = (num_cols // 2) + (num_cols % 2)

    fig, axs = plt.subplots(rows, 2, figsize=(15, rows * 5))

    axs = axs.flatten()  # convert 2D array of subplots into 1D for easier iteration

    for i, column in enumerate(df.columns):
        axs[i].boxplot(df[column], vert=False)
        axs[i].set_title(column)

    # Hide unused subplots (if any)
    # for j in range(i + 1, len(axs)):
    #     fig.delaxes(axs[j])

    plt.tight_layout()
    plt.show()


def hist_plot(df: pd.DataFrame):
    """
    draw boxplots per column to see distribution
    """

    # Draw 1 row and 2 columns of subplots in one output
    num_cols = len(df.columns)
    rows = (num_cols // 2) + (num_cols % 2)

    fig, axs = plt.subplots(rows, 2, figsize=(15, rows * 5))

    axs = axs.flatten()  # convert 2D array of subplots into 1D for easier iteration

    for i, column in enumerate(df.columns):
        iqr = df[column].quantile(.75) - df[column].quantile(.25)
        bar = df[column].quantile(.75) + (1.5 * iqr)
        data = [x for x in df[column] if x <= bar]
        axs[i].hist(data, bins=5, edgecolor='w')
        axs[i].set_title(column)

    plt.tight_layout()
    plt.show()


def main():
    try:
        # connect to DB
        conn = get_connection()
        print("Connected to Postgres DB")

        # retrieve data
        query1 = """
SELECT
	user_id,
	COUNT (DISTINCT EXTRACT(MONTH FROM event_time)) AS purchased_months,
	DATE '2023-03-01' - MAX(event_time)::DATE AS recency_days,
	COUNT(DISTINCT event_time) as purchased_times,
	SUM(price) / COUNT(DISTINCT event_time) as avg_trans_sales
FROM customers
WHERE event_type='purchase'
GROUP BY user_id;
"""
        columns = ['user_id', 'purch_months', 'recency_days', 'frequency', 'avg_sales']
        with conn.cursor() as cursor:
            cursor.execute(query1)
            df = pd.DataFrame(cursor.fetchall(), columns=columns)
        
        # change object types to numeric
        for column in df.columns:
            if pd.api.types.is_object_dtype(df[column]):
                df[column] = pd.to_numeric(df[column], errors='coerce')
        # Use boxplot and hist to see data distribution
        # boxplot(df1)
        # hist_plot(df1)

        # 2. normalize the data to prevent scaling error
        df = df[['purch_months', 'recency_days', 'frequency', 'avg_sales']]
        print(df)
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df)
        print(scaled_data)
        # df_scaled = pd.DataFrame(scaled_data, columns=df.columns)


        # 3. K-means elbow method
        wcss = []
        # centroids = []
        # print(data)
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10).fit(scaled_data)
            wcss.append(kmeans.inertia_)
            # centroids.append(kmeans.cluster_centers_)
        
        print(wcss)
        # print(centroids)

        fig, axs = plt.subplots(1, 1, figsize=(12, 6))

        # Elbow plot        
        axs.plot(range(1, 11), wcss)
        axs.grid(True, linestyle='-', alpha=0.5)
        axs.set_xlabel("Number of clusters")
        axs.set_ylabel("WCSS")
        axs.set_title("The Elbow Method")
        plt.show()

    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
