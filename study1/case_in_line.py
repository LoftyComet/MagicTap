import pandas as pd
import csv
import numpy as np
import xlsxwriter as xw
with open("dataRemoved.csv", "w", encoding="utf-8", newline="") as f:
    # df = pd.read_csv("inVelocity2.csv", encoding="utf-8")
    df = pd.read_csv("data.csv", encoding="utf-8")
    toOutput = []
    df_by_case = df.groupby('Case')
    for i in range(1, len(df_by_case) + 1):
        try:
            data1 = df_by_case.get_group(i).reset_index()
        except KeyError:
            print("case", i, "被完全去除了")
        toInput = np.array(data1[["Velocity"]]).tolist()
        toInput2 = []
        for temp in toInput:
            toInput2.append(temp[0])

        toOutput.append(toInput2)
        print(toInput)
    df = pd.DataFrame(toOutput).T  # 创建DataFrame
    df.to_excel("dataRemoved.xlsx", index=False)  # 存表，去除原始索引列（0,1,2...）
    f.close()