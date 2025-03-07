import pandas as pd
import matplotlib.pyplot as plt
import psycopg2 as psy
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
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
    if cluster == 0:
        return "inactive"
    elif cluster == 1:
        return "loyal gold"
    elif cluster == 2:
        return "loyal platinum"
    elif cluster == 3:
        return "new customer"
    elif cluster == 4:
        return "loyal silver"
 

def main():
    try:
        # connect to DB
        conn = get_connection()
        print("Connected to Postgres DB")

        # 1. retrieve data
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
        print(df)
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df)
        df_scaled = pd.DataFrame(scaled_data, columns=df.columns)

        # 3. K-means elbow method
        kmeans = KMeans(n_clusters=5, random_state=42)
        df_scaled['cluster'] = kmeans.fit_predict(df_scaled)
        print(df_scaled)
        
        # # use pair plot directly
        # plt.figure(figsize=(10, 6))
        # sns.pairplot(df_scaled, hue='cluster', palette='viridis')
        # plt.show()

        # Apply PCA to reduce to 2 dimensions
        pca = PCA(n_components=2)
        df_scaled[['PC1', 'PC2']] = pca.fit_transform(df_scaled.iloc[:, :-1])
        print(df_scaled)

        df_scaled['customer_level'] = df_scaled['cluster'].apply(assign_customer_level)
        df['customer_level'] = df_scaled['customer_level']
        print(df.groupby("customer_level").mean())
        df_customer_level = df.groupby("customer_level").count()
        plt.figure(figsize=(10,6))
        sns.barplot(df_customer_level, x="customer_level", y="purch_months", palette='viridis')
        plt.show()
        print(df_customer_level)

        # # Scatter plot
        # plt.figure(figsize=(10, 6))
        # sns.scatterplot(x=df_scaled['PC1'], y=df_scaled['PC2'], hue=df_scaled['cluster'], palette='viridis')
        # plt.title("Customer Cluster (PCA reduced)")
        # plt.xlabel("Principal Component 1")
        # plt.ylabel("Principal Component 2")
        # plt.show()



    except Exception as e:
        print("Error", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
