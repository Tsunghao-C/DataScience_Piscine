import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def main():
    try:
        df = pd.read_csv("../Train_knight.csv")
        df['knight'] = df['knight'].astype('category').cat.codes

        df_data = df.drop(columns=['knight'], errors='ignore')

        vif_manual = {}
        # iterate through each feature, and calculate the r_square
        # score of the feature to all other features
        for feature in df_data.columns:
            y = df_data[feature]
            X = df_data.drop(columns=[feature])

            # Check if X has at least one column
            if X.shape[1] == 0:
                vif_manual[feature] = np.inf
                continue

            # Fit linear regression model
            model = LinearRegression().fit(X, y)
            r_square = model.score(X, y)

            # Calculate VIF (and prevent division by zero)
            vif =  np.inf if r_square == 1 else 1 / (1 - r_square)
            vif_manual[feature] = vif
        
        # conver dict to pd.DataFrame
        vif_manual_df = pd.DataFrame(list(vif_manual.items()), columns=['Feature', 'VIF'])
        vif_manual_df['Tolerance'] = vif_manual_df['VIF'].apply(lambda x: 1 / x)
        vif_manual_df.set_index('Feature', inplace=True)
        vif_manual_df.index.name = None
        print(vif_manual_df)

        # select features with VIF < 5
        print("\nFeatures having VIF less than 5:\n")
        vif_filtered = vif_manual_df[vif_manual_df['VIF'] < 5]
        print(vif_filtered)


    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
