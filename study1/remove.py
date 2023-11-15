import pandas as pd
import csv
import numpy as np


def get_quantile_and_iqr(df) -> list:
    [q1, q3] = df.quantile([.25, .75]).squeeze()
    iqr = q3-q1
    return [q1, q3, iqr]


def remove_outliers(df, col_name, by_case) -> pd.DataFrame:
    """
    Input: df, target variable's column name, if the removement is by case
    Output: df without outlier data
    Outliers Calculation: data points < (q1-1.5*IQR) or data points > (q3 + 1.5*IQR)
    """
    if by_case:
        df_by_case = df.groupby('Case')
        df_out = pd.DataFrame(columns=df.columns)
        for key, key_df in df_by_case:
            [q1, q3, iqr] = get_quantile_and_iqr(key_df[col_name])
            temp = key_df[(key_df[col_name] >= q1 - 1.5 * iqr) & (key_df[col_name] <= q3 + 1.5 * iqr)]
            df_out = pd.concat([df_out, temp])
        return df_out
    else:
        [q1, q3, iqr] = get_quantile_and_iqr(df[col_name])
        return df[(df[col_name] >= q1 - 1.5 * iqr) & (df[col_name] <= q3 + 1.5 * iqr)]


# 去除异常值
toUse = "Acceleration"
suffix = ".csv"
fileList = ["in", "middle", "out"]
for filename in fileList:
    with open(filename + toUse + "2" + suffix, "w", encoding="utf-8", newline="") as f:
        df = pd.read_csv(filename + toUse + suffix, encoding="utf-8")
        by_case = False
        print("before cut", len(df))
        data = remove_outliers(df, toUse, by_case)
        print("after cut", len(data))
        toInput = np.array(data).tolist()

        csv_writer = csv.writer(f)
        csv_writer.writerow(["Case", "RunTime", "Object", "EnterTime", "Velocity", "Acceleration", "Condition", "PrepTime"])
        for zrow in toInput:
            csv_writer.writerow(zrow)
        f.close()

toUse = 'Velocity'
for filename in fileList:
    with open(filename + toUse + "2" + suffix, "w", encoding="utf-8", newline="") as f:
        df = pd.read_csv(filename + toUse + suffix, encoding="utf-8")

        by_case = False
        print("before cut", len(df))
        data = remove_outliers(df, toUse, by_case)
        print("after cut", len(data))
        toInput = np.array(data).tolist()

        csv_writer = csv.writer(f)
        csv_writer.writerow(["Case", "RunTime", "Object", "EnterTime", "Velocity", "Acceleration", "Condition", "PrepTime"])
        for zrow in toInput:
            csv_writer.writerow(zrow)
        f.close()

# with open("dataRemoved.csv", "w", encoding="utf-8", newline="") as f:
#     df = pd.read_csv("data.csv", encoding="utf-8")
#     by_case = False
#     data = remove_outliers(df, "Acceleration", by_case)
#     data = remove_outliers(data, 'Velocity', by_case)
#     toInput = np.array(data).tolist()
#
#     csv_writer = csv.writer(f)
#     csv_writer.writerow(["Case", "RunTime", "Object", "EnterTime", "Velocity", "Acceleration", "Condition", "PrepTime"])
#     for zrow in toInput:
#         csv_writer.writerow(zrow)
#     f.close()