import pandas as pd
import csv
import numpy as np
# 2为加速度分割，3为速度分割

suffix = ".csv"
fileList = ["in", "middle", "out"]
cutWays = ['Acceleration', 'Velocity']
for cutWay in cutWays:
    for filename in fileList:
        toUse = 'Acceleration'
        # 数据集
        df = pd.read_csv(filename + cutWay + "2" + suffix, encoding="utf-8")
        # df = pd.read_csv(filename + cutWay + suffix, encoding="utf-8")
        # toUse = 'Velocity'
        by_case = False
        data = df.groupby('Case')
        tempPeak = []
        tempTrough = []
        # 分开算每个case
        for i in range(1, len(data) + 1):
            # 前面数据预处理可能已经干掉了一些case
            try:
                data1 = data.get_group(i).reset_index()
            except KeyError:
                # print("case", i, "被完全去除了")
                pass
                # continue
            # 每个case的数据
            data2 = np.array(data1[toUse]).tolist()
            # 找出波峰波谷
            pre = data2[0]
            nextNum = float(0)

            for j in range(1, len(data2) - 1):
                nextNum = data2[j + 1]
                # 波峰
                if data2[j] > pre and data2[j] > nextNum:
                    tempPeak.append(data2[j])
                # 波谷
                elif data2[j] < pre and data2[j] < nextNum:
                    tempTrough.append(data2[j])
                pre = data2[j]
        # print("使用", cutWay, "截断的波峰的", filename, toUse, "平均值为", np.mean(tempPeak))
        # print("使用", cutWay, "截断的波谷的", filename, toUse, "平均值为", np.mean(tempTrough))
        print(tempTrough)
        for temp in tempTrough:
            if temp >= 0:
                print(temp, ">0")
        # print("使用", cutWay, "截断的波峰的", filename, toUse, "标准差为", np.std(tempPeak))
        # print("使用", cutWay, "截断的波谷的", filename, toUse, "标准差为", np.std(tempTrough))

    for filename in fileList:
        toUse = 'Velocity'
        # 数据集
        df = pd.read_csv(filename + cutWay + "2" + suffix, encoding="utf-8")
        # df = pd.read_csv(filename + cutWay + suffix, encoding="utf-8")
        by_case = False
        data = df.groupby('Case')
        tempPeak = []
        tempTrough = []
        # 分开算每个case
        for i in range(1, len(data) + 1):
            # 前面数据预处理可能已经干掉了一些case
            try:
                data1 = data.get_group(i).reset_index()
            except KeyError:
                # print("case", i, "被完全去除了")
                pass
            # 每个case的数据
            data2 = np.array(data1[toUse]).tolist()
            # 找出波峰波谷
            pre = data2[0]
            nextNum = float(0)

            for j in range(1, len(data2) - 1):
                nextNum = data2[j + 1]
                # 波峰
                if data2[j] > pre and data2[j] > nextNum:
                    tempPeak.append(data2[j])
                # 波谷
                elif data2[j] < pre and data2[j] < nextNum:
                    tempTrough.append(data2[j])
                pre = data2[j]
        # print("使用", cutWay, "截断的波峰的", filename, toUse, "平均值为", np.mean(tempPeak))
        # print("使用", cutWay, "截断的波谷的", filename, toUse, "平均值为", np.mean(tempTrough))
        # for temp in tempTrough:
        #     if temp >= 0:
        #         print(">0")
        # print("使用", cutWay, "截断的波峰的", filename, toUse, "标准差为", np.std(tempPeak))
        # print("使用", cutWay, "截断的波谷的", filename, toUse, "标准差为", np.std(tempTrough))
        print("end")
