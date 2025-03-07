import pandas as pd
import psycopg2 as psy
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns


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

def assign_customer_level(cluster):
    if cluster == 3:
        return "inactive"
    elif cluster == 0:
        return "loyal gold"
    elif cluster == 1:
        return "loyal platinum"
    elif cluster == 2:
        return "new customer"
    elif cluster == 4:
        return "loyal silver"


def barplot(df: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(df, x="customer_level", y="purch_months", palette='viridis')
    ax.bar_label(ax.containers[0])
    plt.ylabel('num of customers')
    plt.title("Customer numbers by Category")
    plt.show()


def scatterplot(df: pd.DataFrame):
    centroids = df.groupby("customer_level").mean().reset_index()
    # print(centroids)
    centroid_coor = centroids[['PC1', 'PC2']]

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df['PC1'], y=df['PC2'], hue=df['customer_level'], palette='viridis')
    plt.scatter(centroid_coor['PC1'], centroid_coor['PC2'],
                color='red', marker='*', s=150, label='Centroids')
    plt.title("Customer Cluster (PCA reduced)")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("Customer Clustering by PCA axis")
    plt.legend()
    plt.show()


def main():
    try:
        # connect to DB
        conn = get_connection()
        print("Connected to Postgres DB")

        # 1. retrieve data using RFM model: Recency, Frequency, Monetary
        query = """
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
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall(), columns=columns)
        
        # change object types to numeric
        for column in df.columns:
            if pd.api.types.is_object_dtype(df[column]):
                df[column] = pd.to_numeric(df[column], errors='coerce')

        # 2. normalize the data to prevent scaling error
        df = df[['purch_months', 'recency_days', 'frequency', 'avg_sales']]
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df)
        df_scaled = pd.DataFrame(scaled_data, columns=df.columns)

        # 3. K-means elbow method
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        df_scaled['cluster'] = kmeans.fit_predict(df_scaled)
        print("\n------ Scaled data ------\n")
        print(df_scaled)
        
        # # use pair plot directly
        # plt.figure(figsize=(10, 6))
        # sns.pairplot(df_scaled, hue='cluster', palette='viridis')
        # plt.show()

        # Apply PCA to reduce to 2 dimensions
        pca = PCA(n_components=2)
        df_scaled[['PC1', 'PC2']] = pca.fit_transform(df_scaled.iloc[:, :-1])
        print("\n------ Adding PCA columns ------\n")
        df_scaled['customer_level'] = df_scaled['cluster'].apply(assign_customer_level)
        print(df_scaled)

        # add cluster back to unscaled data to see how it is clustered
        df['customer_level'] = df_scaled['customer_level']
        print("\n------ Adding cluster category names and show the mean value of each feature ------\n")
        print(df.groupby("customer_level").mean())

        # Draw bar plot using amount of customer per each category
        df_customer_level = df.groupby("customer_level").count().reset_index()
        barplot(df_customer_level)

        # Draw Scatter plot
        scatterplot(df_scaled)


    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
