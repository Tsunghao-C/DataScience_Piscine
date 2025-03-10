import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_normalization(df: pd.DataFrame) -> pd.DataFrame:
    """return a normalized df using Max-Min method"""
    df_nml = df.copy()
    for column in df_nml.columns:
        dist = df_nml[column].max() - df_nml[column].min()
        if dist == 0:
            pass
        df_nml[column] = (df_nml[column] - df_nml[column].min()) / dist
    return df_nml


def boxplot(df: pd.DataFrame):
    """draw boxplot to see that all data after standardization have mean = 0"""
    # melt if a built-in function to aggregate all data into two columns with first column to be 
    # original column name (variable)
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
        print("Data before normalization:\n")
        print(df.iloc[:, :-1])
        df2 = pd.read_csv("../Test_knight.csv")

        # do Normalization: all data minus the min and divided by (max - min)
        df_nml = get_normalization(df.iloc[:, :-1])
        print("\nData after normalization:\n")
        print(df_nml)
        df2_nml = get_normalization(df2)
        # we can do a boxplot to see the mean of each feature is now zero
        # boxplot(df_nml)

        df_nml['knight'] = df['knight']
        scatterplot(df_nml, 'Push', 'Deflection', 'knight', legend_pos="upper right")
        scatterplot(df2_nml, 'Push', 'Deflection', None, legend_pos="upper right")

    except Exception as e:
        print("Error", e)


if __name__ == "__main__":
    main()


### Notes:
# Normalization changes the shape of original distribution of data
# and thus is very sensitive to outliers
# Best used for data that are not normally distributed or
# has known fixed boundaries