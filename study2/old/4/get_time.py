import pandas as pd
import csv
import numpy as np
# 2为加速度分割，3为速度分割

suffix = ".csv"
fileList = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]

for fileIndex in range(len(fileList)):
    # toUse = 'Acceleration'
    # 数据集
    df = pd.read_csv(fileList[fileIndex] + suffix, encoding="utf-8")
    # df = pd.read_csv(filename + cutWay + suffix, encoding="utf-8")
    # toUse = 'Velocity'
    data = df.groupby('Case')
    # inTimes = [90, 60, 17, 27, 24, 32, 73, 51, 164]
    # inTimes = [15, 10, 52, 8, 15, 66, 19, 36, 36]
    inTimes = [21, 18, 18, 23, 28, 32, 25, 19, 28]
    inTimes2 = [87, 41, 34, 25, 21, 106, 54, 67, 88]
    triggerTime = []
    distriggerTime = []
    # 根据手动输入进入次数来划分轮次
    # 分开算每个case
    print(fileList[fileIndex])
    for i in range(1, inTimes[fileIndex] + 1):
        # 前面数据预处理可能已经干掉了一些case
        try:
            data1 = data.get_group(i).reset_index()
        except KeyError:
            # print("case", i, "被完全去除了")
            pass
            # continue
        # 每个case的数据
        data2 = np.array(data1[["EnterTime", "Condition", "Case"]]).tolist()
        # print(data2)
        # 找出三连B表示被触发，EnterTime即为触发时间
        if len(data2) >= 3:
            if data2[-1][1] == "B" and data2[-2][1] == "B" and data2[-3][1] == "B":
                triggerTime.append(float(data2[-1][0]))
            else:
                distriggerTime.append(float(data2[-1][0]))
        else:
            distriggerTime.append(float(data2[-1][0]))



    print("第一轮")
    print(len(triggerTime))
    if not len(triggerTime) == 0 and not len(distriggerTime) == 0:
        print("触发成功率", len(triggerTime) / (len(triggerTime) + len(distriggerTime)))
    if not len(triggerTime) == 0:
        print("平均触发时间", np.mean(triggerTime))
    if not len(distriggerTime) == 0:
        print("平均未触发进入时间", np.mean(distriggerTime))
    print("-----------------------------")

    for i in range(inTimes[fileIndex] + 1, inTimes2[fileIndex] + 1):
        # 前面数据预处理可能已经干掉了一些case
        try:
            data1 = data.get_group(i).reset_index()
        except KeyError:
            # print("case", i, "被完全去除了")
            pass
            # continue
        # 每个case的数据
        data2 = np.array(data1[["EnterTime", "Condition"]]).tolist()
        # print(data2)
        # 找出三连B表示被触发，EnterTime即为触发时间
        if len(data2) >= 3:
            if data2[-1][1] == "B" and data2[-2][1] == "B" and data2[-3][1] == "B":
                triggerTime.append(float(data2[-1][0]))
            else:
                distriggerTime.append(float(data2[-1][0]))
        else:
            distriggerTime.append(float(data2[-1][0]))

    # print(fileList[fileIndex])
    print("第二轮")
    if not len(triggerTime) == 0 and not len(distriggerTime) == 0:
        print("防误触成功率", len(distriggerTime) / (len(triggerTime) + len(distriggerTime)))
    if not len(triggerTime) == 0:
        print("平均触发时间", np.mean(triggerTime))
    if not len(distriggerTime) == 0:
        print("平均未触发进入时间", np.mean(distriggerTime))
    print("-----------------------------")


