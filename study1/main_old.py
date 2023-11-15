import os

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

def getThreshold(use):
    df = pd.read_csv("data.csv", encoding="utf-8")
    data = df.groupby('Case')
    for i in range(1, len(data) - 1):
        try:
            data1 = data.get_group(i).reset_index()
        except KeyError:
            print("case", i, "被完全去除了")
        data2 = np.array(data1[[use]]).tolist()
        if len(data2) < 150:
            print("出现错误数据，已忽略")
            continue
        mid = int(len(data2) / 2)
        # 截取中间1s，0.02s为一帧
        data3 = data2[mid - 25:mid + 25]
        data4 = []
        # for j in range(len(data3) - 1):
        #     data4.append(abs(data3[j+1][0]) + abs(data3[j][0]))
        # print(use, np.mean(data4))
        # print(np.mean(abs(data3)))
        for temp in data3:
            data4.append(abs(temp[0]))
        print(np.max(data4))
        # return np.mean(data4)
        return np.max(data4)


def cut(difference, threshold ,use):
    """
    一些参数
    """
    # 数据集
    df = pd.read_csv("data.csv", encoding="utf-8")

    # threshold = 2.5
    dataStart = 1
    dataEnd = 171

    # 多少次后截断
    standard = 3
    """
    数据处理开始
    """
    cut = 0
    inList = []
    outList = []
    if os.path.exists("in" + use + ".csv"):
        os.remove("in" + use + ".csv")
        os.remove("middle" + use + ".csv")
        os.remove("out" + use + ".csv")
    largerTimes = 0
    data = df.groupby('Case')
    inCount = 0
    outCount = 0
    inCut = []

    with open("in" + use + ".csv", "w", encoding="utf-8", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(
            ["Case", "RunTime", "Object", "EnterTime", "Velocity", "Acceleration", "Condition", "PrepTime"])
        f.close()
    with open("middle" + use + ".csv", "w", encoding="utf-8", newline="") as f2:
        csv_writer = csv.writer(f2)
        csv_writer.writerow(
            ["Case", "RunTime", "Object", "EnterTime", "Velocity", "Acceleration", "Condition", "PrepTime"])
        f2.close()
    with open("out" + use + ".csv", "w", encoding="utf-8", newline="") as f3:
        csv_writer = csv.writer(f3)
        csv_writer.writerow(
            ["Case", "RunTime", "Object", "EnterTime", "Velocity", "Acceleration", "Condition", "PrepTime"])
        f3.close()

    # 切割手指进入
    for i in range(dataStart, dataEnd):
        try:
            data1 = data.get_group(i).reset_index()
        except KeyError:
            print("case", i, "被完全去除了")
        data2 = np.array(data1[['Case', use]]).tolist()
        isCut = False
        if difference:
            data4 = []
            # for j in range(len(data2) - 1):
            #     data4.append((abs(data2[j + 1][1]) + abs(data2[j][1])) / 2)
            for temp in data2:
                data4.append(abs(temp[1]))
            data2 = data4
        data3 = np.array(data1).tolist()
        data5 = np.array(data1[['Case', use]]).tolist()
        # 去除有问题的数据
        if len(data2) < 150:
            inCut.append(-1)
            print("出现错误数据，已忽略")
            continue

        for j in range(len(data2)):
            if (abs(data2[j]) - threshold) < 0:
                largerTimes += 1
                if largerTimes == standard:
                    cut = j - (standard - 1)
                    print("cut", cut)
                    largerTimes = 0
                    plt.plot(cut, data5[cut][1], 'bs', label='data' + str(i))
                    z = data3[:cut]
                    for zrow in z:
                        inList.append(abs(zrow[1]))
                    inCount += 1
                    inCut.append(cut)
                    isCut = True
                    break
            else:
                largerTimes = 0
        print("进入切割点", cut)
        cut = 0
        plt.plot(data1[[use]], label='data' + str(i))
        if not isCut:
            inCut.append(-1)
    # print("进入时的平均", use, "为:", np.mean(inList))
    print("进入截点个数", inCount)
    # 切割手指出去
    for i in range(dataStart, dataEnd):
        # if i==len(inCut):
        #     break
        try:
            data1 = data.get_group(i).reset_index()
        except KeyError:
            print("case", i, "被完全去除了")
        data2 = np.array(data1[['Case', use]]).tolist()
        if difference:
            data4 = []
            for j in range(len(data2) - 1):
                data4.append(abs(data2[j + 1][1] - data2[j][1]))
            data2 = data4
        data3 = np.array(data1).tolist()
        data5 = np.array(data1[['Case', use]]).tolist()
        # 去除有问题的数据
        if len(data2) < 150:
            print("出现错误数据，已忽略")
            continue
        for j in range(len(data2)-1, -1, -1):
            if (abs(data2[j]) - threshold) < 0:
                largerTimes += 1
                if largerTimes == standard:
                    cut = j + standard
                    largerTimes = 0
                    plt.plot(cut, data5[cut][1], 'bs', label='data' + str(i))
                    z = data3[cut:]

                    for zrow in z:
                        outList.append(abs(zrow[1]))
                    outCount += 1
                    # 写入csv
                    # 1. 创建文件对象（指定文件名，模式，编码方式）a模式 为 下次写入在这次的下一行
                    with open("in" + use + ".csv", "a", encoding="utf-8", newline="") as f:
                        # 2. 基于文件对象构建 csv写入对象
                        csv_writer = csv.writer(f)
                        z = data3[:inCut[i-1]]
                        for zrow in z:
                            csv_writer.writerow(zrow)
                        # 5. 关闭文件
                        f.close()
                    with open("middle" + use + ".csv", "a", encoding="utf-8", newline="") as f2:
                        # 2. 基于文件对象构建 csv写入对象
                        csv_writer = csv.writer(f2)

                        z = data3[inCut[i-1]:cut]
                        for zrow in z:
                            csv_writer.writerow(zrow)

                        # 5. 关闭文件
                        f2.close()
                    with open("out" + use + ".csv", "a", encoding="utf-8", newline="") as f3:
                        # 2. 基于文件对象构建 csv写入对象
                        csv_writer = csv.writer(f3)
                        z = data3[cut+1:]
                        for zrow in z:
                            csv_writer.writerow(zrow)
                        # 5. 关闭文件
                        f3.close()
                    break
            else:
                largerTimes = 0
        print("出去切割点", cut)
        cut = 0
        plt.plot(data1[[use]], label='data' + str(i))
    print("出去截点个数", outCount)
    plt.show()


if __name__ == '__main__':
    threshold = getThreshold('Acceleration')
    cut(difference=True, threshold=3, use='Acceleration')
    threshold = getThreshold('Velocity')
    cut(difference=True, threshold=0.1, use='Velocity')
