import pandas as pd
import csv
import numpy as np


for q in range(1, 16):
    prefix = str(q) + "\\"
    suffix = ".csv"
    fileList = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]

    # 先将参数组合的随机还原
    # 编号
    # 1 -3.333 0.113,
    # 2 -6.667 0.113,
    # 3 -10 0.113,
    # 4 -3.333 0.226,
    # 5 -6.667 0.226,
    # 6 -10 0.226,
    # 7 -3.333 0.339,
    # 8 -6.667 0.339,
    # 9 -10 0.339
    jump1 = True
    csv_reader = csv.reader(open(prefix + "ExpAcceTap.csv"))
    avList = []
    avTemp = []
    ballIndex = []
    for row in csv_reader:
        # 跳过第一行
        if jump1:
            jump1 = False
            continue
        else:
            for k in range(int(len(row)/2)):
                avTemp.append(row[k])
                avTemp.append(row[k + 9])
                avList.append(avTemp)
                avTemp = []
            break
    print(avList)
    for temp in avList:
        print(temp)
        if temp[0] == '-3.333' and temp[1] == '0.113':
            ballIndex.append(1)
        elif temp[0] == "-6.667" and temp[1] == "0.113":
            ballIndex.append(2)
        elif temp[0] == "-10" and temp[1] == "0.113":
            ballIndex.append(3)
        elif temp[0] == "-3.333" and temp[1] == "0.226":
            ballIndex.append(4)
        elif temp[0] == "-6.667" and temp[1] == "0.226":
            ballIndex.append(5)
        elif temp[0] == "-10" and temp[1] == "0.226":
            ballIndex.append(6)
        elif temp[0] == "-3.333" and temp[1] == "0.339":
            ballIndex.append(7)
        elif temp[0] == "-6.667" and temp[1] == "0.339":
            ballIndex.append(8)
        elif temp[0] == "-10" and temp[1] == "0.339":
            ballIndex.append(9)
    print(ballIndex)

    inTimes = [0]*9
    inTimes2 = [0]*9
    inTimes3 = [0]*9
    inTimes4 = [0]*9


    scores1 = []
    scores2 = []
    scores3 = []
    scores4 = []
    tempTimes = 0
    csv_reader2 = csv.reader(open(prefix + "ExpAcceTap.csv"))
    for row in csv_reader2:
        if tempTimes == 2:
            for p in range(9):
                scores1.append(row[p + 18])
        if tempTimes == 3:
            for p in range(9):
                scores2.append(row[p + 18])
        if tempTimes == 4:
            for p in range(9):
                scores3.append(row[p + 18])
        if tempTimes == 5:
            for p in range(9):
                scores4.append(row[p + 18])
        tempTimes += 1
    print(scores1)
    print(scores2)
    print(scores3)
    print(scores4)
    for fileIndex in range(len(fileList)):
        print(fileIndex)
        indexTemp = 0
        temp = 0
        inTimesTemp = []
        jump = True
        lastCase = "0"
        # 先统计每一轮点击次数
        csv_reader = csv.reader(open(prefix + fileList[fileIndex] + suffix))
        for row in csv_reader:
            # 跳过第一行
            if jump:
                jump = False
                continue
            # 以换行符开始
            if len(row) == 0:
                temp += 1
                # 连续两次换行符后，切换记录的列表
                if temp == 2:
                    if indexTemp == 0:
                        inTimesTemp = inTimes
                        temp = 0
                        indexTemp += 1
                    elif indexTemp == 1:
                        inTimesTemp = inTimes2
                        temp = 0
                        indexTemp += 1
                    elif indexTemp == 2:
                        inTimesTemp = inTimes3
                        temp = 0
                        indexTemp += 1
                    elif indexTemp == 3:
                        inTimesTemp = inTimes4
                        temp = 0
                        indexTemp += 1
            else:
                if not row[0] == lastCase:
                    inTimesTemp[fileIndex] += 1
                    lastCase = row[0]
    print(inTimes)
    print(inTimes2)
    print(inTimes3)
    print(inTimes4)
    ballNum = 0
    #for fileIndex in ballIndex:
    for temp in range(1, 10):
        for tempIndex in ballIndex:
            if tempIndex == temp:
                fileIndex = ballIndex.index(tempIndex)
        ballNum += 1
        # 数据集
        df = pd.read_csv(prefix + fileList[fileIndex] + suffix, encoding="utf-8")
        data = df.groupby('Case')

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
                    if float(data2[-1][0]) > 0.07:
                        print(float(data2[-1][0]))
                        distriggerTime.append(float(data2[-1][0]))
            else:

                if float(data2[-1][0]) > 0.07:
                    print(float(data2[-1][0]))
                    distriggerTime.append(float(data2[-1][0]))

        # print("第一轮")
        # if not len(triggerTime) == 0 and not len(distriggerTime) == 0:
        #     print("触发成功率", len(triggerTime) / (len(triggerTime) + len(distriggerTime)))
        # if not len(triggerTime) == 0:
        #     print("平均触发时间", np.mean(triggerTime))
        # else:
        #     print("全部未触发")
        # if not len(distriggerTime) == 0:
        #     print("平均未触发进入时间", np.mean(distriggerTime))
        # else:
        #     print("全部触发")
        # print("-----------------------------")

        with open("data1.csv", "a", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[ballNum, fileIndex + 1, len(triggerTime), len(triggerTime) + len(distriggerTime),
                               len(triggerTime) / (len(triggerTime) + len(distriggerTime)),
                               np.mean(triggerTime), np.mean(distriggerTime), scores1[fileIndex]]])

        triggerTime = []
        distriggerTime = []
        for i in range(inTimes[fileIndex] + 1, inTimes[fileIndex] + inTimes2[fileIndex] + 1):
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
        # print("第二轮")
        # print(len(distriggerTime))
        # print(len(triggerTime))
        # if not len(triggerTime) == 0 and not len(distriggerTime) == 0:
        #     print("防误触成功率", len(distriggerTime) / (len(triggerTime) + len(distriggerTime)))
        # if not len(triggerTime) == 0:
        #     print("平均触发时间", np.mean(triggerTime))
        # else:
        #     print("全部未触发")
        # if not len(distriggerTime) == 0:
        #     print("平均未触发进入时间", np.mean(distriggerTime))
        # else:
        #     print("全部触发")
        # print("-----------------------------")
        with open("data2.csv", "a", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[ballNum, fileIndex + 1, len(triggerTime), len(triggerTime) + len(distriggerTime),
                               len(triggerTime) / (len(triggerTime) + len(distriggerTime)),
                               np.mean(triggerTime), np.mean(distriggerTime), scores2[fileIndex]]])

        triggerTime = []
        distriggerTime = []
        for i in range(inTimes[fileIndex] + inTimes2[fileIndex] + 1, inTimes[fileIndex] + inTimes2[fileIndex] + inTimes3[fileIndex] + 1):
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
        # print("第三轮")
        # if not len(triggerTime) == 0 and not len(distriggerTime) == 0:
        #     print("防误触成功率", len(distriggerTime) / (len(triggerTime) + len(distriggerTime)))
        # if not len(triggerTime) == 0:
        #     print("平均触发时间", np.mean(triggerTime))
        # else:
        #     print("全部未触发")
        # if not len(distriggerTime) == 0:
        #     print("平均未触发进入时间", np.mean(distriggerTime))
        # else:
        #     print("全部触发")
        # print("-----------------------------")
        with open("data3.csv", "a", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[ballNum, fileIndex + 1, len(triggerTime), len(triggerTime) + len(distriggerTime),
                               len(triggerTime) / (len(triggerTime) + len(distriggerTime)),
                               np.mean(triggerTime), np.mean(distriggerTime), scores3[fileIndex]]])

        triggerTime = []
        distriggerTime = []
        for i in range(inTimes[fileIndex] + inTimes2[fileIndex] + inTimes3[fileIndex] + 1,
                       inTimes[fileIndex] + inTimes2[fileIndex] + inTimes3[fileIndex] + inTimes4[fileIndex] + 1):
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
        # print("第四轮")
        # if not len(triggerTime) == 0 and not len(distriggerTime) == 0:
        #     print("防误触成功率", len(distriggerTime) / (len(triggerTime) + len(distriggerTime)))
        # if not len(triggerTime) == 0:
        #     print("平均触发时间", np.mean(triggerTime))
        # else:
        #     print("全部未触发")
        # if not len(distriggerTime) == 0:
        #     print("平均未触发进入时间", np.mean(distriggerTime))
        # else:
        #     print("全部触发")
        # print("-----------------------------")
        with open("data4.csv", "a", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[ballNum, fileIndex + 1, len(triggerTime), len(triggerTime) + len(distriggerTime),
                               len(triggerTime) / (len(triggerTime) + len(distriggerTime)),
                               np.mean(triggerTime), np.mean(distriggerTime), scores4[fileIndex]]])

    with open("data1.csv", "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([])
    with open("data2.csv", "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([])
    with open("data3.csv", "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([])