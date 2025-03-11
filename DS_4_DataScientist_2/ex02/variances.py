import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def main():
    try:
        df = pd.read_csv("../Train_knight.csv")

        # replace string with 0 and 1, and then replace the column
        df['knight'] = df['knight'].astype('category').cat.codes
        # print(df)

        # Standardize data
        scaler = StandardScaler()
        scaled = scaler.fit_transform(df)
        # print(scaled)

        # Apply PCA with all components
        pca = PCA(n_components=len(df.columns))
        pca.fit(scaled)

        # Compute explanined variance ratio
        explained_var_ratio = pca.explained_variance_ratio_
        a = pca.explained_variance_
        # b = pca.feature_names_in_
        print("\npca explained_variance:\n", a)
        first_elem = a[0] / a.sum()
        print("\nfirst elem:", first_elem)
        # print("\npca feature names in:\n", b)
        print("Variances (Percentage):")
        print(explained_var_ratio)
        cumulative_var = np.cumsum(explained_var_ratio)
        print("\nCumulative Variances (Percentage):")
        print(cumulative_var * 100)


        # find the optimal number of components (Elbow method)
        optimal_k = np.argmax(cumulative_var >= 0.90) + 1
        print(f"\nOptimal number of components: {optimal_k}")

        fig, ax = plt.subplots(1, 2, figsize=(14, 6))
        ax[0].plot(range(1, len(explained_var_ratio)), cumulative_var[:-1], marker='o', linestyle='-')
        ax[0].set_xlabel("Number of components")
        ax[0].set_ylabel("Explained variance (%)")
        ax[0].set_title("Cumulative Variance Plot")
        ax[0].grid()

        ax[1].plot(range(1, len(explained_var_ratio)), explained_var_ratio[:-1], marker='o', linestyle='-', label="Explained Variance per Component")
        ax[1].set_xlabel("Number of components")
        ax[1].set_ylabel("Explained variance ratio")
        ax[1].set_title("Scree Plot")
        ax[1].grid()

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()


# The benefit of using PCA is 
# 1. used for dimensinality reduction
# 2. leave only Uncorrelated features

# PCA finds the most "efficient" axes that captures the most variance in order
# to explain variaces.
# Use original fieatures doesn't remove correlation, so high-variance features
# might still be redundant.