import os

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

writefrom = "15"
gap = 180
df = pd.read_csv(writefrom + ".csv", encoding="utf-8")

df2 = np.array(df).tolist()
for temp in df2:
    if int(temp[0]) == 1:
        temp[0] = gap + 1
    elif int(temp[0]) == 2:
        temp[0] = gap + 2
    elif int(temp[0]) == 3:
        temp[0] = gap + 3
    elif int(temp[0]) == 4:
        temp[0] = gap + 4
    elif int(temp[0]) == 5:
        temp[0] = gap + 5
    elif int(temp[0]) == 6:
        temp[0] = gap + 6
    elif int(temp[0]) == 7:
        temp[0] = gap + 7
    elif int(temp[0]) == 8:
        temp[0] = gap + 8
    elif int(temp[0]) == 9:
        temp[0] = gap + 9
    elif int(temp[0]) == 10:
        temp[0] = gap + 10
    elif int(temp[0]) == 11:
        temp[0] = gap + 11
    elif int(temp[0]) == 12:
        temp[0] = gap + 12
    elif int(temp[0]) == 13:
        temp[0] = gap + 13
    elif int(temp[0]) == 14:
        temp[0] = gap + 14
    elif int(temp[0]) == 15:
        temp[0] = gap + 15
    elif int(temp[0]) == 16:
        temp[0] = gap + 16
    elif int(temp[0]) == 17:
        temp[0] = gap + 17
    elif int(temp[0]) == 18:
        temp[0] = gap + 18
    elif int(temp[0]) == 19:
        temp[0] = gap + 19
    elif int(temp[0]) == 20:
        temp[0] = gap + 20
    elif int(temp[0]) == 21:
        temp[0] = gap + 21
    elif int(temp[0]) == 22:
        temp[0] = gap + 22
    elif int(temp[0]) == 23:
        temp[0] = gap + 23

with open("1.csv", "a", encoding="utf-8", newline="") as f:
    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    # 3. 构建列表头
    # name = ['top', 'left']
    # csv_writer.writerow(name)
    # 4. 写入csv文件内容
    z = df2

    for zrow in z:
        csv_writer.writerow(zrow)

    # 5. 关闭文件
    f.close()
