import pandas as pd
import scipy.stats as stat


def corr_generate(df: pd.DataFrame, target: str) -> dict:
    """
    return a dictionary {feature_name: (corr, p_value)} to target column
    """
    results = {}
    for feature in df.columns:
        corr, p_value = stat.pearsonr(df[feature], df[target])
        results[feature] = (abs(corr), p_value)
    
    # sort by absolute correlation value (strongest to weakest)
    sorted_result = dict(sorted(results.items(), key=lambda x: abs(x[1][0]), reverse=True))
    return sorted_result


def main():
    try:
        df = pd.read_csv("../Train_knight.csv")

        # 1: replace string with 0 and 1, and then replace the column
        # df['target'] = df['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
        # df.drop(['knight'], axis=1, inplace=True)
        # df.rename(columns={'target':'knight'}, inplace=True)
        df['knight'] = df['knight'].astype('category').cat.codes
        # print(df)

        pearson_corr = corr_generate(df, 'knight')
        # print(pearson_corr)
        for feature, (corr, p_value) in pearson_corr.items():
            print(f"{feature:<15}{corr:.6f}")

    except Exception as e:
        print("Error", e)

if __name__ == "__main__":
    main()
