import sys
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import matplotlib.pyplot as plt


def main():
    try:
        # Input check and create splitting data_sets
        if len(sys.argv) != 3:
            raise AssertionError("incorrect input arguments")
        path_train, path_test = (sys.argv[1], sys.argv[2])
        if not (os.path.exists(path_train) and os.path.exists(path_test)):
            raise FileNotFoundError("File not found")
        df_train = pd.read_csv(path_train)
        # codes method will codes by ascii acscending order
        df_train['knight'] = df_train['knight'].astype('category').cat.codes
        df_test = pd.read_csv(path_test)

        # Feature selection
        X = df_train.drop(columns=['knight'])
        y = df_train['knight']

        # Splitting data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y, shuffle=True)

        neighbors = range(1, 30)
        train_accuracy = np.empty(len(neighbors))
        test_accuracy = np.empty(len(neighbors))
        f1_score = np.empty(len(neighbors))
        for i, k in enumerate(neighbors):
            # Create Decision tree model
            knn = KNeighborsClassifier(n_neighbors=k)
            # Train Descision Tree model with training set
            knn = knn.fit(X_train, y_train)
            # Prediect result on validating set
            train_accuracy[i] = knn.score(X_train, y_train)
            test_accuracy[i] = knn.score(X_test, y_test)
            f1_score[i] = metrics.f1_score(y_test, knn.predict(X_test))

        # Visualize KNN by numbers of neighbors (k)
        plt.plot(neighbors, test_accuracy, label='Validating dataset')
        plt.plot(neighbors, train_accuracy, label='Training dataset')
        plt.plot(neighbors, f1_score, label='Validating f1-score')

        plt.legend()
        plt.xlabel('k_values')
        plt.ylabel('accuracy')
        plt.show()
        # Predict on Test_knight.csv
        optimal_k = np.argmax(f1_score) + 1
        print(f"Optimal K value from KNN: {optimal_k}")
        knn = KNeighborsClassifier(n_neighbors=optimal_k)
        knn = knn.fit(X_train, y_train)
        print(f"f1_score of KNN with {optimal_k} neighbors: {metrics.f1_score(y_test, knn.predict(X_test))}")
        test_pred = knn.predict(df_test)
        print(test_pred)
        decoded_test_pred = np.where(test_pred == 1, 'Sith', 'Jedi')

        with open("KNN.txt", "w") as file:
            file.write("\n".join(decoded_test_pred))

    except AssertionError as e:
        print("AssertionError:", e)
    except FileNotFoundError as e:
        print("FileNotFound:", e)
    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    main()
