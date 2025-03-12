import sys
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn import metrics


def main():
    try:
        # Input check and create splitting data_sets
        if len(sys.argv) != 3:
            raise AssertionError("incorrect input arguments")
        path_train, path_test = (sys.argv[1], sys.argv[2])
        if not (os.path.exists(path_train) and os.path.exists(path_test)):
            raise FileNotFoundError("File not found")
        # 1. Load data
        df_train = pd.read_csv(path_train)
        df_train['knight'] = df_train['knight'].astype('category').cat.codes
        df_test = pd.read_csv(path_test)

        # 2 Feature selection
        X = df_train.drop(columns=['knight'])
        y = df_train['knight']

        # Splitting data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y, shuffle=True)

        # 3. Scaled data with standard scaler (fit_transform on train, transform on test)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # 4. Apply PCA (fit_transform on train, transform on test)
        pca = PCA(n_components=7)
        X_train_pca = pca.fit_transform(X_train_scaled)
        X_test_pca = pca.transform(X_test_scaled)

        # 5. Defines models for assembly
        knn = KNeighborsClassifier(n_neighbors=19)
        dt = DecisionTreeClassifier(random_state=42, criterion='entropy')
        logreg = LogisticRegression(random_state=42)
        voting_clf = VotingClassifier(
            estimators=[('knn', knn), ('dt', dt), ('lr', logreg)],
            voting='hard'
        )

        # train the model using training dataset
        voting_clf.fit(X_train_pca, y_train)
        y_pred = voting_clf.predict(X_test_pca)
        # Evaluating model y_pred and y_test
        print("f1-score:", metrics.f1_score(y_test, y_pred))
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
        print("Explained Variance Ratio:", pca.explained_variance_ratio_.sum())
        # Visualize KNN by numbers of neighbors (k)

        # Predict on Test_knight.csv
        test_pred = voting_clf.predict(pca.transform(scaler.transform(df_test)))
        print(test_pred)
        decoded_test_pred = np.where(test_pred == 1, 'Sith', 'Jedi')

        with open("Voting.txt", "w") as file:
            file.write("\n".join(decoded_test_pred))

    except AssertionError as e:
        print("AssertionError:", e)
    except FileNotFoundError as e:
        print("FileNotFound:", e)
    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    main()


# if you directly use the raw data of all 30 features, LogReg will have problem
# converge within 100 reps. Even after Stadardization, the f1-score is unbelieveabliy high
# at 0.9919, which is very likely to have overfitting.
# solution -> either use PCA or VIF for Feature selection