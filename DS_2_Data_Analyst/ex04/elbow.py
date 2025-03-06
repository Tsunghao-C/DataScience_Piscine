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


def scatter_plot(df: pd.DataFrame):
    plt.scatter(df[df.columns[0]], df[df.columns[1]])
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
            df = pd.DataFrame(cursor.fetchall(), columns=columns)
        
        # change object types to numeric
        for column in df.columns:
            if pd.api.types.is_object_dtype(df[column]):
                df[column] = pd.to_numeric(df[column], errors='coerce')
        # Use boxplot and hist to see data distribution
        # boxplot(df1)
        # hist_plot(df1)

        wcss = []
        centroids = []
        data = df[['tol_sales', 'item_purchased']]
        # scatter_plot(data)
        # print(data)
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10).fit(data.to_numpy())
            wcss.append(kmeans.inertia_)
            centroids.append(kmeans.cluster_centers_)
        
        print(wcss)
        print(centroids)

        fig, axs = plt.subplots(1, 2, figsize=(15, 6))

        # Elbow plot        
        axs[0].plot(range(1, 11), wcss)
        axs[0].grid(True, linestyle='-', alpha=0.5)
        axs[0].set_xlabel("Number of clusters")
        axs[0].set_ylabel("WCSS")
        axs[0].set_title("The Elbow Method")

        # Scatter plot
        final_centroids = np.array(centroids[4])
        axs[1].scatter(data[data.columns[0]], data[data.columns[1]], label="Data Points")
        axs[1].scatter(final_centroids[:, 0], final_centroids[:, 1],
                       color='red', marker='*', s=100, label='Centroids')
        axs[1].set_xlabel(data.columns[0])
        axs[1].set_ylabel(data.columns[1])
        axs[1].set_title("Cluster Scatter Plot with Centroids")
        axs[1].legend()

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
