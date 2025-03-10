import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def split_trained_data(df: pd.DataFrame, t_size: float):
    X = df.iloc[:, :-1]
    y = df['knight']

    # "stratify=y" to make sure both test and training data has the same ratio of output
    # "shuffle=True" to ramdonize the order of data rows
    # Best practice is to use these two options together
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, train_size=t_size, stratify=y, shuffle=True)

    # Save training set
    X_train['knight'] = y_train
    # print(X_train)
    X_train.to_csv('Training_knight.csv', index=False)

    # Save validation set
    X_test['knight'] = y_test
    X_test.to_csv('Validation_knight.csv', index=False)


def main():
    try:
        df = pd.read_csv("../Train_knight.csv")
        split_trained_data(df, 0.8)

    except Exception as e:
        print("Error", e)


if __name__ == "__main__":
    main()


# Note: train test split should be done BEFORE Scaling
# if we do scaling first, there will be information leek from test data to train data

# Size of train and test data portion
# 1. by default is 80% training and 20% validating
# 2. sometimes 90/10 when dataset is too small, need more data for training
# 3. sometimes 70/30 when more evaluation data is needed
# 4. There is "KFold" method for cross-validating split for example:
#   if k = 5 and testing is 20%, it will take turns to pick 20% of the data
#   to be testing set for 5 times, so every data will be treated for both
#   training and validating data. This help reduce the impact of data variability.
