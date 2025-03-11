import sys
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.tree import export_graphviz
import graphviz


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

        # Create Decision tree model
        clf = DecisionTreeClassifier(criterion='entropy')
        # Train Descision Tree model with training set
        clf = clf.fit(X_train, y_train)
        # Prediect result on validating set
        y_pred = clf.predict(X_test)
        # Evaluating model y_pred and y_test
        print("f1-score:", metrics.f1_score(y_test, y_pred))
        # print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
        # print("Confusion Metrics:\n", metrics.confusion_matrix(y_test, y_pred))

        # Visualize Decision Tree
        dot_data = export_graphviz(clf, out_file=None,
                        filled=True, rounded=True,
                        special_characters=True, feature_names=df_test.columns)
        graph = graphviz.Source(dot_data)
        graph.render("decision_tree")
        graph.view()

        # Predict on Test_knight.csv
        test_pred = clf.predict(df_test)
        print(test_pred)
        decoded_test_pred = np.where(test_pred == 1, 'Sith', 'Jedi')

        with open("Tree.txt", "w") as file:
            file.write("\n".join(decoded_test_pred))

    except AssertionError as e:
        print("AssertionError:", e)
    except FileNotFoundError as e:
        print("FileNotFound:", e)
    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    main()
