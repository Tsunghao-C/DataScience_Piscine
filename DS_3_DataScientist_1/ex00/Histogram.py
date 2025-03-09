import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def display(df: pd.DataFrame):
    print(df.columns)
    print(len(df.columns))
    print(df.dtypes)
    print(df.describe())


def histplots(df: pd.DataFrame):
    num_columns = len(df.columns)
    rows = num_columns // 5
    if (num_columns % 5 > 0):
        rows += 1
    fig, axs = plt.subplots(rows, 5, figsize=(12, 10))
    axs = axs.flatten()

    for i, column in enumerate(df.columns):
        sns.histplot(df, x=column, ax=axs[i], bins=50, edgecolor=None, color='green')
        axs[i].set_title(column, fontsize=10)
        axs[i].set_xlabel("")
        axs[i].set_ylabel("")
        axs[i].grid(False)

    plt.subplots_adjust(hspace=0.5)
    plt.tight_layout()
    plt.show()
    # plt.savefig("histo_test.jpg")
    plt.close()


def set_legend_fontsize(axs, font_size: int):
    legend = axs.get_legend()
    if legend:
        legend.set_title("")
        for text in legend.get_texts():
            text.set_fontsize(font_size)


def histplots_hue(df: pd.DataFrame):
    num_columns = len(df.columns)
    rows = num_columns // 5
    fig, axs = plt.subplots(rows, 5, figsize=(12, 12))
    axs = axs.flatten()

    for i, column in enumerate(df.columns):
        if i < 30:
            sns.histplot(df, x=column, ax=axs[i], bins=50, hue='knight', edgecolor=None, color='green')
            axs[i].set_title(column, fontsize=10)
            axs[i].set_xlabel("")
            axs[i].set_ylabel("")
            axs[i].grid(False)
            # change legend fontsize
            set_legend_fontsize(axs[i], 6)

    plt.subplots_adjust(hspace=0.5)
    plt.tight_layout()
    plt.show()
    plt.close()


def main():
    try:
        # 1st plot
        df = pd.read_csv("../Test_knight.csv")
        # display(df)
        histplots(df)

        # 2nd plot
        df2 = pd.read_csv("../Train_knight.csv")
        # display(df2)
        histplots_hue(df2)
    except Exception as e:
        print("Error", e)

if __name__ == "__main__":
    main()