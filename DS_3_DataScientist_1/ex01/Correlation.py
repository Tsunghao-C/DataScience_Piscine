import numpy as np
import pandas as pd
import scipy.stats


def main():
    try:
        df = pd.read_csv("Train_knight.csv")
        # replace string with 0 and 1, and then replace the column
        df['target'] = df['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
        df.drop(['knight'], axis=1, inplace=True)
        df.rename(columns={'target':'knight'}, inplace=True)
        # print(df)

        # iterate and print all correlation coefficient
        correlations = []
        for column in df.columns:
            correlations.append(scipy.stats.pearsonr(df[column], df['knight'])[0])
        # print(correlations)
        df_corr = pd.DataFrame(zip(df.columns, correlations), columns=['feature', 'corr'])
        df_corr.set_index('feature', inplace=True)
        print(df_corr.sort_values(by='corr', ascending=False))
            
    except Exception as e:
        print("Error", e)

if __name__ == "__main__":
    main()
