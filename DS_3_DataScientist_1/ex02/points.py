import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# from Correlation import corr_generate


def boxplots(df: pd.DataFrame):
    """draw boxplots for each feature"""
    num_columns = len(df.columns)
    rows = num_columns // 5
    fig, axs = plt.subplots(rows, 5, figsize=(12, 10))
    axs = axs.flatten()

    for i, column in enumerate(df.columns):
        if i < 30:
            sns.boxenplot(df, x=column, ax=axs[i])
            axs[i].set_title(column, fontsize=10)
            axs[i].grid(False)
    plt.tight_layout()
    plt.show()
    plt.close()

def scatterplot(df: pd.DataFrame, x, y, hue=None, legend_pos="upper left"):
    plt.figure(figsize=(10,6))
    sns.scatterplot(df, x=x, y=y, hue=hue)
    if hue:
        legend = plt.legend(loc=legend_pos)
        legend.set_title("")
    else:
        plt.legend(['knight'], loc=legend_pos)
    plt.show()
    plt.close()


def main():
    try:
        df = pd.read_csv('../Train_knight.csv')
        df2 = pd.read_csv('../Test_knight.csv')
        # print(df.isnull().sum())
        # print(df.shape)

        # Try to find out the right scatter plots as subject 
        # df['knight'] = df['knight'].astype('category').cat.codes
        # corr_dict = corr_generate(df, 'knight')
        # top_10_corr = [feature for feature, (corr, p_value) in corr_dict.items()][:10]
        # print(df[top_10_corr].describe())
        # df_top10 = df[top_10_corr].copy()
        # df_top10['knight'] = df['knight']
        # plt.figure(figsize=(12,6))
        # sns.pairplot(df_top10, hue='knight')
        # plt.tight_layout()
        # plt.show()

        # 1st graph Empowered vs Stims
        scatterplot(df, 'Empowered', 'Stims', 'knight')
        scatterplot(df2, 'Empowered', 'Stims', None)
        # 2nd graph push vs Deflection
        scatterplot(df, 'Push', 'Deflection', 'knight', legend_pos="upper right")
        scatterplot(df2, 'Push', 'Deflection', None, legend_pos="upper right")


    except Exception as e:
        print("Error", e)


if __name__ == "__main__":
    main()
