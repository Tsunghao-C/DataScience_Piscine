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


def main():
    try:
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
        df['result'] = np.select(condlist=conditions, choicelist=labels)
        # print(df)

        # Create a table of confusion matrix
        df_cm = df.groupby('result').size().reset_index(name='count')
        # print(df_cm)
        # print(type(df_cm.set_index('result')))
        # print(type(df_cm.set_index('result')['count']))
        cm = df_cm.set_index('result')['count'].to_dict()
        print("confusion matrix:\n")
        cm_array = np.array([
            [cm['TP'], cm['FN']],
            [cm['FP'], cm['TN']]
        ])

        # calculate confusion matrix metrics

        Jedi_score = np.array([
            get_precision(cm),
            get_recall(cm),
            get_f1score(cm),
            cm['TP'] + cm['FN']])
        Sith_score = np.array([
            get_precision(cm, False),
            get_recall(cm, False),
            get_f1score(cm, False),
            cm['FP'] + cm['TN']])
        Accuracy = np.array([get_accuracy(cm), df_cm['count'].sum()])
        print(Jedi_score)
        print(Sith_score)
        print(Accuracy)

        print("\n", cm_array)


    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
