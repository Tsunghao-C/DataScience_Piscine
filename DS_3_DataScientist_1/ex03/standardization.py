import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_standardization(df: pd.DataFrame) -> pd.DataFrame:
    """return a stadardizaed df"""
    df_std = df.copy()
    for column in df_std.columns:
        df_std[column] = (df_std[column] - df_std[column].mean()) / df_std[column].std()
    return df_std


def boxplot(df: pd.DataFrame):
    """draw boxplot to see that all data after standardization have mean = 0"""
    df_melt = pd.melt(df)
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='variable', y='value', data=df_melt)
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
        df = pd.read_csv("../Train_knight.csv")
        print("Data before standardization:\n")
        print(df.iloc[:, :-1])
        df2 = pd.read_csv("../Test_knight.csv")

        # do stadardization: all data minus the mean and divided by std
        df_std = get_standardization(df.iloc[:, :-1])
        print("\nData after standardization:\n")
        print(df_std)
        df2_std = get_standardization(df2)
        # we can do a boxplot to see the mean of each feature is now zero
        # boxplot(df_std)

        df_std['knight'] = df['knight']
        scatterplot(df_std, 'Empowered', 'Stims', 'knight')
        scatterplot(df2_std, 'Empowered', 'Stims', None)

    except Exception as e:
        print("Error", e)


if __name__ == "__main__":
    main()
