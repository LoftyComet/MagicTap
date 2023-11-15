import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm


def color_map(data, cmap):
    """数值映射为颜色"""

    dmin, dmax = np.nanmin(data), np.nanmax(data)
    dmax = dmax * 0.75
    print(dmin, dmax)
    cmo = plt.cm.get_cmap(cmap)
    cs, k = list(), 256 / cmo.N

    for i in range(cmo.N):
        c = cmo(i)
        for j in range(int(i * k), int((i + 1) * k)):
            cs.append(c)
    cs = np.array(cs)
    for dataIndex in range( len(data)):
        if data[dataIndex] > dmax:
            data[dataIndex] = dmax
    data = np.uint8(255 * (data - dmin) / (dmax - dmin))

    return cs[data]


# def color_map(data, cmap):
#     """数值映射为颜色"""
#
#     dmin, dmax = np.nanmin(data), np.nanmax(data)
#     cmo = plt.cm.get_cmap(cmap)
#     cs, k = list(), 256 / cmo.N
#
#     for i in range(cmo.N):
#         c = cmo(i)
#         for j in range(int(i * k), int((i + 1) * k)):
#             cs.append(c)
#     cs = np.array(cs)
#     data = np.uint8(255 * (data - dmin) / (dmax - dmin))
#
#     return cs[data]


x = []
y = []
z = []
v = []
df = pd.read_csv("data3.csv", encoding="utf-8")
data = df.groupby('Case')
startIndex = 0
for key, value in data.groups.items():
    startIndex = key
    break
for j in range(3):
    data2 = []
    x.clear()
    y.clear()
    z.clear()
    v.clear()
    for i in range(startIndex + j*15, startIndex + (j+1)*15):
        try:
            data1 = np.array(data.get_group(i).reset_index()).tolist()
            print(data1)
        except KeyError:
            # print("case", i, "被完全去除了")
            pass
        for temp in data1:
            data2.append(temp)
    for temp in data2:
        if not temp[2] == 0 and not temp[3] == 0 and not temp[4] == 0:
            if len(x) == 0:
                x.append(temp[2])
                y.append(temp[3])
                z.append(temp[4])
                v.append(temp[6])
            elif len(x) >= 1:
                if not temp[2] == x[len(x) - 1]:
                    x.append(temp[2])
                    y.append(temp[3])
                    z.append(temp[4])
                    v.append(temp[6])
    # x = np.array(x)
    # y = np.array(y)
    # z = np.array(z)


    # 创建颜色渐变
    colors = np.linspace(0, 1, len(v))

    # 创建画布和3D坐标轴
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    cmap = 'cool'  # jet, hsv等也是常用的颜色映射方案
    colors = color_map(v, cmap)
    # 绘制连续线条，并设置颜色
    # for i in range(1, len(v) - 1):
    #     ax.plot(x[i - 1:i + 1], y[i - 1:i + 1], z[i - 1:i + 1], c=plt.cm.viridis(v[i]))
    for i in range(1, len(v) - 1):
        ax.plot(x[i - 1:i + 1], y[i - 1:i + 1], z[i - 1:i + 1], c=colors[i])
    # line = ax.plot(x, y, z, cmap=plt.cm.CMRmap)


    # 添加颜色渐变的颜色条
    # cbar = plt.colorbar(line, ax=ax)
    # cbar.set_label('Color Gradient')

    # 设置坐标轴标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 设置图标题
    plt.title('Color Gradient 3D Line')

    # 显示图形
    plt.show()

