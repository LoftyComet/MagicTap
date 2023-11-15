import os

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    """
    一些参数
    """
    # 数据集
    df = pd.read_csv("data.csv", encoding="utf-8")
    toUse = 'Acceleration'
    # toUse = 'Velocity'
    threshold = 2.5
    dataStart = 1
    dataEnd = 11

    # 多少次后截断
    standard = 3
    """
    数据处理开始
    """
    cut = 0
    inList = []
    outList = []
    largerTimes = 0
    data = df.groupby('Case')
    inCount = 0
    outCount = 0
    inCut = []

    with open("in" + toUse + ".csv", "w", encoding="utf-8", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(
            ["Case", "RunTime", "Object", "EnterTime", "Velocity", "Acceleration", "Condition", "PrepTime"])
        f.close()
    with open("middle" + toUse + ".csv", "w", encoding="utf-8", newline="") as f2:
        csv_writer = csv.writer(f2)
        csv_writer.writerow(
            ["Case", "RunTime", "Object", "EnterTime", "Velocity", "Acceleration", "Condition", "PrepTime"])
        f2.close()
    with open("out" + toUse + ".csv", "w", encoding="utf-8", newline="") as f3:
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
        data2 = np.array(data1[['Case', toUse]]).tolist()
        data3 = np.array(data1).tolist()
        # 去除有问题的数据
        if len(data2) < 150:
            inCut.append(-1)
            print("出现错误数据，已忽略")
            continue
        for j in range(len(data2)):
            if (abs(data2[j][1]) - threshold) < 0:
                largerTimes += 1
                if largerTimes == standard:
                    cut = j-2
                    largerTimes = 0
                    plt.plot(cut, data2[cut][1], 'bs', label='data' + str(i))
                    z = data3[:cut]
                    for zrow in z:
                        inList.append(abs(zrow[1]))
                    inCount += 1
                    inCut.append(cut)
                    break
            else:
                largerTimes = 0
        print("进入切割点", cut)
        cut = 0
        plt.plot(data1[[toUse]], label='data' + str(i))
    print("进入时的平均", toUse, "为:", np.mean(inList))
    print("进入截点个数", inCount)
    print(inCut)
    print(len(inCut))
    # 切割手指出去
    for i in range(dataStart, dataEnd):
        try:
            data1 = data.get_group(i).reset_index()
        except KeyError:
            print("case", i, "被完全去除了")
        data2 = np.array(data1[['Case', toUse]]).tolist()
        data3 = np.array(data1).tolist()
        # 去除有问题的数据
        if len(data2) < 150:
            print("出现错误数据，已忽略")
            continue
        for j in range(len(data2)-1, -1, -1):
            if (abs(data2[j][1]) - threshold) < 0:
                largerTimes += 1
                if largerTimes == standard:
                    cut = j+2
                    largerTimes = 0
                    plt.plot(cut, data2[cut][1], 'bs', label='data' + str(i))
                    z = data3[cut:]

                    for zrow in z:
                        outList.append(abs(zrow[1]))
                    outCount += 1
                    # 写入csv
                    # 1. 创建文件对象（指定文件名，模式，编码方式）a模式 为 下次写入在这次的下一行
                    with open("in.csv", "a", encoding="utf-8", newline="") as f:
                        # 2. 基于文件对象构建 csv写入对象
                        csv_writer = csv.writer(f)
                        # # 3. 构建列表头
                        # name = ['top', 'left']
                        # csv_writer.writerow(name)
                        # 4. 写入csv文件内容
                        print("i-1", i-1)
                        z = data3[:inCut[i-1]]
                        for zrow in z:
                            csv_writer.writerow(zrow)
                        # 5. 关闭文件
                        f.close()
                    with open("middle.csv", "a", encoding="utf-8", newline="") as f2:
                        # 2. 基于文件对象构建 csv写入对象
                        csv_writer = csv.writer(f2)
                        # # 3. 构建列表头
                        # name = ['top', 'left']
                        # csv_writer.writerow(name)
                        # 4. 写入csv文件内容
                        z = data3[inCut[i-1]:cut]
                        for zrow in z:
                            csv_writer.writerow(zrow)

                        # 5. 关闭文件
                        f2.close()
                    with open("out.csv", "a", encoding="utf-8", newline="") as f3:
                        # 2. 基于文件对象构建 csv写入对象
                        csv_writer = csv.writer(f3)
                        # # 3. 构建列表头
                        # name = ['top', 'left']
                        # csv_writer.writerow(name)
                        # 4. 写入csv文件内容
                        z = data3[cut:]
                        for zrow in z:
                            csv_writer.writerow(zrow)
                        # 5. 关闭文件
                        f3.close()
                    break
            else:
                largerTimes = 0
        print("出去切割点", cut)
        cut = 0
        plt.plot(data1[[toUse]], label='data' + str(i))

    print("出去时的平均", toUse, "为:", np.mean(outList))
    print("出去截点个数", outCount)
    plt.show()


