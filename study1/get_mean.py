import pandas as pd
import csv
import numpy as np
# 2为加速度分割，3为速度分割
suffix = ".csv"

toUse = 'Acceleration'
# 数据集
data1 = pd.read_csv("in" + toUse + suffix, encoding="utf-8")
data2 = pd.read_csv("middle" + toUse + suffix, encoding="utf-8")
data3 = pd.read_csv("out" + toUse + suffix, encoding="utf-8")

data11 = np.array(data1['Acceleration']).tolist()
data12 = np.array(data2['Acceleration']).tolist()
data13 = np.array(data3['Acceleration']).tolist()
data21 = np.array(data1['Velocity']).tolist()
data22 = np.array(data2['Velocity']).tolist()
data23 = np.array(data3['Velocity']).tolist()

print("使用", toUse, "分割的进入平均a为", np.mean(data11))
print("使用", toUse, "分割的中间平均a为", np.mean(data12))
print("使用", toUse, "分割的出去平均a为", np.mean(data13))
print("使用", toUse, "分割的进入平均v为", np.mean(data21))
print("使用", toUse, "分割的中间平均v为", np.mean(data22))
print("使用", toUse, "分割的出去平均v为", np.mean(data23))
toUse = 'Velocity'
data1 = pd.read_csv("in" + toUse + suffix, encoding="utf-8")
data2 = pd.read_csv("middle" + toUse + suffix, encoding="utf-8")
data3 = pd.read_csv("out" + toUse + suffix, encoding="utf-8")
data11 = np.array(data1['Acceleration']).tolist()
data12 = np.array(data2['Acceleration']).tolist()
data13 = np.array(data3['Acceleration']).tolist()
data21 = np.array(data1['Velocity']).tolist()
data22 = np.array(data2['Velocity']).tolist()
data23 = np.array(data3['Velocity']).tolist()
print("使用", toUse, "分割的进入平均a为", np.mean(data11))
print("使用", toUse, "分割的中间平均a为", np.mean(data12))
print("使用", toUse, "分割的出去平均a为", np.mean(data13))
print("使用", toUse, "分割的进入平均v为", np.mean(data21))
print("使用", toUse, "分割的中间平均v为", np.mean(data22))
print("使用", toUse, "分割的出去平均v为", np.mean(data23))
