import os

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    """
    一些参数
    """
    toUse = 'Acceleration'
    # toUse = 'Velocity'

    # 数据集
    df = pd.read_csv("in2.csv", encoding="utf-8")

    data = df.groupby('Case')
    for i in range(len(data)):
        try:
            data1 = data.get_group(i+1).reset_index()
        except KeyError:
            print("case", i+1, "被完全去除了")
        plt.plot(data1[[toUse]], label='data' + str(i+1))

    df = pd.read_csv("middle2.csv", encoding="utf-8")
    data = df.groupby('Case')
    for i in range(len(data)):
        try:
            data1 = data.get_group(i + 1).reset_index()
        except KeyError:
            print("case", i + 1, "被完全去除了")
        plt.plot(data1[[toUse]], label='data' + str(i + 1))

    df = pd.read_csv("out2.csv", encoding="utf-8")
    data = df.groupby('Case')
    for i in range(len(data)):
        try:
            data1 = data.get_group(i + 1).reset_index()
        except KeyError:
            print("case", i + 1, "被完全去除了")
        plt.plot(data1[[toUse]], label='data' + str(i + 1))

    # # 多少次后截断
    # standard = 3
    # """
    # 数据处理开始
    # """
    # cut = 0
    # inList = []
    # outList = []
    # largerTimes = 0
    #
    # inCount = 0
    # outCount = 0
    # inCut = []
    # # 切割手指进入
    # for i in range(dataStart, dataEnd):
    #     try:
    #         data1 = data.get_group(i).reset_index()
    #     except KeyError:
    #         print("case", i, "被完全去除了")
    #     data2 = np.array(data1[['Case', toUse]]).tolist()
    #     data3 = np.array(data1).tolist()
    #     # 去除有问题的数据
    #     if len(data2) < 150:
    #         inCut.append(-1)
    #         print("出现错误数据，已忽略")
    #         continue
    #     for j in range(len(data2)):
    #         if (abs(data2[j][1]) - threshold) < 0:
    #             largerTimes += 1
    #             if largerTimes == standard:
    #                 cut = j-2
    #                 largerTimes = 0
    #                 plt.plot(cut, data2[cut][1], 'bs', label='data' + str(i))
    #                 z = data3[:cut]
    #                 for zrow in z:
    #                     inList.append(abs(zrow[1]))
    #                 inCount += 1
    #                 inCut.append(cut)
    #                 break
    #         else:
    #             largerTimes = 0
    #     print("进入切割点", cut)
    #     cut = 0
    #     plt.plot(data1[[toUse]], label='data' + str(i))
    # print("进入时的平均", toUse, "为:", np.mean(inList))
    # print("进入截点个数", inCount)
    # print(inCut)
    # print(len(inCut))
    # # 切割手指出去
    # for i in range(dataStart, dataEnd):
    #     try:
    #         data1 = data.get_group(i).reset_index()
    #     except KeyError:
    #         print("case", i, "被完全去除了")
    #     data2 = np.array(data1[['Case', toUse]]).tolist()
    #     data3 = np.array(data1).tolist()
    #     # 去除有问题的数据
    #     if len(data2) < 150:
    #         print("出现错误数据，已忽略")
    #         continue
    #     for j in range(len(data2)-1, -1, -1):
    #         if (abs(data2[j][1]) - threshold) < 0:
    #             largerTimes += 1
    #             if largerTimes == standard:
    #                 cut = j+2
    #                 largerTimes = 0
    #                 plt.plot(cut, data2[cut][1], 'bs', label='data' + str(i))
    #                 z = data3[cut:]
    #
    #                 for zrow in z:
    #                     outList.append(abs(zrow[1]))
    #                 outCount += 1
    #
    #
    #                 break
    #         else:
    #             largerTimes = 0
    #     print("出去切割点", cut)
    #     cut = 0
    #     plt.plot(data1[[toUse]], label='data' + str(i))
    #
    # print("出去时的平均", toUse, "为:", np.mean(outList))
    # print("出去截点个数", outCount)
    plt.show()


