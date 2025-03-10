import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    try:
        # Load data into lists
        with open('predictions.txt', 'r') as file:
            pred = [line.strip() for line in file]
        # print(pred)
        with open('truth.txt', 'r') as file:
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
        print(df)

        # Create a table of confusion matrix
        df_cm = df.groupby('result').size().reset_index(name='count')
        print(df_cm)
        # print(type(df_cm.set_index('result')))
        # print(type(df_cm.set_index('result')['count']))
        confusion_matrix = df_cm.set_index('result')['count'].to_dict()
        print("confusion_matrix:\n")
        cm_array = np.array([
            [confusion_matrix['TP'], confusion_matrix['FN']],
            [confusion_matrix['FP'], confusion_matrix['TN']]
        ])
        print(cm_array)
        


    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
