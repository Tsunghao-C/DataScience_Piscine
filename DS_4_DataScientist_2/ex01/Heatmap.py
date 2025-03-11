import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stat
import seaborn as sns


def corr_generate(df: pd.DataFrame) -> np.ndarray:
    """
    return a dictionary {feature_name: (corr, p_value)} to target column
    """

    num_features = len(df.columns)
    corr_list = []
    for target in df.columns:
        tmp_list = []
        for feature in df.columns:
            corr, p_value = stat.pearsonr(df[feature], df[target])
            tmp_list.append(corr)
        corr_list.append(tmp_list)
    
    result = np.array(corr_list)
    # print(result)
    # print(result.shape)
    return corr_list


def main():
    try:
        df = pd.read_csv("../Train_knight.csv")

        # 1: replace string with 0 and 1, and then replace the column
        df['knight'] = df['knight'].astype('category').cat.codes
        # print(df)

        pearson_corr = corr_generate(df)
        # print(pearson_corr)
        sns.heatmap(pearson_corr, xticklabels=df.columns, yticklabels=df.columns)
        plt.show()

    except Exception as e:
        print("Error", e)
    finally:
        plt.close()

if __name__ == "__main__":
    main()
