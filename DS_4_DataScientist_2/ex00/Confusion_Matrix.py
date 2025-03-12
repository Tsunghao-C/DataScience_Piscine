import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os


def format_float(func):
    def wrapper(self, *args, **kwargs):
        res= func(self, *args, **kwargs)
        return round(res, 2)
    return wrapper


@format_float
def get_accuracy(cm: dict) -> float:
    return (cm['TP'] + cm['TN']) / (cm['TP'] + cm['TN'] + cm['FP'] + cm['FN'])


@format_float
def get_precision(cm: dict, flag: bool=True) -> float:
    if flag:
        return cm['TP'] / (cm['TP'] + cm['FP'])
    return cm['TN'] / (cm['TN'] + cm['FN'])


@format_float
def get_recall(cm: dict, flag: bool=True) -> float:
    if flag:
        return cm['TP'] / (cm['TP'] + cm['FN'])
    return cm['TN'] / (cm['TN'] + cm['FP'])


@format_float
def get_f1score(cm: dict, flag: bool=True) -> float:
    if flag:
        return (2 * get_precision(cm) * get_recall(cm)) / (get_precision(cm) + get_recall(cm))
    return (2 * get_precision(cm, False) * get_recall(cm, False)) / (get_precision(cm, False) + get_recall(cm, False))


@format_float
def get_specificity(cm: dict, flag: bool=True) -> float:
    if flag:
        return cm['TN'] / (cm['TN'] + cm['FP'])
    return cm['TP'] / (cm['TP'] + cm['FN'])


def display_cm(cm: dict):
    # positive scores
    Jedi_score = np.array([
        get_precision(cm),
        get_recall(cm),
        get_f1score(cm),
        cm['TP'] + cm['FN']])
    # negative scores
    Sith_score = np.array([
        get_precision(cm, False),
        get_recall(cm, False),
        get_f1score(cm, False),
        cm['FP'] + cm['TN']])
    # accruacy and total
    total = np.array([x for x in cm.values()]).sum()
    Accuracy = np.array([get_accuracy(cm), total])

    # display scores in table format
    columns = ['precision', 'recall', 'f1-score', 'total']
    df_cm2 = pd.DataFrame([Jedi_score, Sith_score], columns=columns, index=['Jedi', 'Sith'])
    df_cm2 = df_cm2.astype({'total': int})
    print(df_cm2)
    print(f"\naccuracy                     {Accuracy[0]}    {Accuracy[1]:.0f}")

    # diplay confusion matrix
    cm_matrix = np.array([
        [cm['TP'], cm['FN']],
        [cm['FP'], cm['TN']]
    ])
    print(f"\n{cm_matrix}")

    # plt.figure(figsize=(12, 8))
    sns.heatmap(cm_matrix, annot=True)
    plt.show()
    plt.close()


def main():
    try:
        # input check
        if len(sys.argv) != 3:
            raise AssertionError("incorrect input arguments")
        path_pre, path_truth = (sys.argv[1], sys.argv[2])
        if not (os.path.exists(path_pre) and os.path.exists(path_truth)):
            raise FileNotFoundError("file not found")

        # Load data into lists
        with open(path_pre, 'r') as file:
            pred = [line.strip() for line in file]
        # print(pred)
        with open(path_truth, 'r') as file:
            truth = [line.strip() for line in file]
        # print(truth)

        # Add a column to check the results in TP, TN, FP, FN
        df = pd.DataFrame({'Prediction': pred, 'Truth': truth})
        conditions = [
            (df['Truth'] == 'Jedi') & (df['Prediction'] == 'Jedi'),
            (df['Truth'] == 'Sith') & (df['Prediction'] == 'Sith'),
            (df['Truth'] == 'Sith') & (df['Prediction'] == 'Jedi'),
            (df['Truth'] == 'Jedi') & (df['Prediction'] == 'Sith')
        ]
        labels = ['TP', 'TN', 'FP', 'FN']
        df['result'] = np.select(condlist=conditions, choicelist=labels, default='other')
        # print(df)

        # Add default value 0 to all keys to make sure all 4 keys are created
        cm = {label: 0 for label in labels}  # Ensure all labels are included
        df_cm = df.groupby('result').size().to_dict()  # Convert grouped counts to dict
        cm.update(df_cm)  # Update only existing values while keeping others at 0
        # print(cm)
        # print("confusion matrix:\n")
        display_cm(cm)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
