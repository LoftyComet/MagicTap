import csv
import math
import matplotlib as mpl
import pandas as pd
import pyvista as pv

import numpy as np
import matplotlib.pyplot as plt

def export_to_pts(points, filename):
    with open(filename, 'w') as file:
        for point in points:
            line = f"{point[0]} {point[1]} {point[2]}\n"
            file.write(line)


def get_target_pos(ball_radius, ori_x, ori_y, ori_z):
    ans_x = []
    ans_y = []
    ans_z = [ori_z] * 16
    for i in range(16):
        angle = i * (2 * math.pi / 16)
        x = ori_x + ball_radius * math.cos(angle)
        y = ori_y + ball_radius * math.sin(angle)
        ans_x.append(x)
        ans_y.append(y)
    print(ans_x, ans_y, ans_z)
    return ans_x, ans_y, ans_z


def color_map(data, cmap, threshold):
    """数值映射为颜色"""

    dmin, dmax = np.nanmin(data), np.nanmax(data)
    dmax = dmax * threshold
    dmax = 2.5
    print(dmin, dmax)
    cmo = plt.cm.get_cmap(cmap)
    cs, k = list(), 256 / cmo.N

    for i in range(cmo.N):
        c = cmo(i)
        for j in range(int(i * k), int((i + 1) * k)):
            cs.append(c)
    cs = np.array(cs)
    for dataIndex in range(len(data)):
        # data[dataIndex] -= 0.5
        data[dataIndex] += 0.5
        if data[dataIndex] > dmax:
            data[dataIndex] = dmax
        if data[dataIndex] < dmin:
            data[dataIndex] = dmin
    data = np.uint8(255 * (1 - (data - dmin) / (dmax - dmin)))
    print("-----")
    print(data)
    print("-----")
    return cs[data]


# 将坐标轴宽度转换为 s 参数的单位
def axis_to_s(axis_width, scale_factor):
    return (axis_width * scale_factor) ** 2


# x = np.linspace(0, 2*np.pi, 200)
# y = np.sin(x)
# ps = np.stack((x,y), axis=1)
# segments = np.stack((ps[:-1], ps[1:]), axis=1)
#
# cmap = 'viridis' # jet, hsv等也是常用的颜色映射方案
# colors = color_map(np.cos(x)[:-1], cmap)
# colors = color_map(y[:-1], cmap)
# line_segments = LineCollection(segments, colors=colors, linewidths=3, linestyles='solid', cmap=cmap)
#
# fig, ax = plt.subplots()
# ax.set_xlim(np.min(x)-0.1, np.max(x)+0.1)
# ax.set_ylim(np.min(y)-0.1, np.max(y)+0.1)
# ax.add_collection(line_segments)
# cb = fig.colorbar(line_segments, cmap='jet')
#
# plt.show()


expIndex = [[12, 9, -1, 15, 7, 5, 9, 12, 4], [15, 9, 1, 3, 3, 15, 12, 12, 12], [15, 9, 1, 3, 3, 15, 12, 12, 12],
            [3, 13, 15, 6, 6, 14, 12, 13, 6], [14, 11, 15, 9, 15, 13, 7, 4, 4], [15, 10, 10, 14, 7, 4, 7, 9, 8],
            [3, 9, 2, 15, -1, 5, 14, 13, 13], [5, 8, -1, 5, 9, 10, 1, 6, 15], [1, 13, 2, 9, 10, 13, 8, 1, 8],
            [3, 5, 14, 7, 14, 1, 3, 7, 14], [12, 2, 11, 2, -1, 6, 15, 4, 13], [3, 15, 2, 7, 5, 6, 9, 2, -1],
            [13, 13, 11, 6, 13, 5, 11, -1, 6], [10, 10, 3, 4, 14, 13, 2, 2, 1], [12, 12, -1, 13, 15, 10, 1, 10, 15],
            [5, 12, 2, 13, 14, 2, 6, 12, 14], [9, 8, 14, 3, 12, 6, -1, 3, 9], [6, 9, 1, 1, 2, 6, 8, 5, 2],
            [14, 10, 15, 5, 12, 4, -1, 13, 4]]
# 手动调整每一轮圆心位置
centerX = [0, 0, 0, 0, 0, 0, 0, 0, 0]
centerY = [1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1]
centerZ = [0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537]
# 开始结束序号(左闭右开) qq1
begin = 7
end = 8
# 行号代表实验轮次 列号代表玩家序号 X Y Z代表三维坐标
# 偏差是在原来基础上加上矩阵内对应的数组
moveX2 = [[0.11, 0.12, 0.08, 0.05, 0.01, -0.05, 0.1, 0, 0.1, 0.07, -0.01, -0.3, 0.03, 0.04, 0.01, 0.06, 0.06, 0.07, 0],
          [-0.01, -0.03, -0.04, -0.06, 0, 0.05, -0.03, 0, -0.02, -0.16, -0.04, 0.07, 0.06, -0.13, -0.13, 0.01, -0.08,
           0.05, -0.05],
          [0.05, 0.05, 0.06, 0.06, 0.05, 0.04, 0.05, 0.02, 0.12, -0.07, 0.05, 0.07, 0.04, 0.02, 0.03, 0.01, -0.05,
           -0.04, 0.06],
          [-0.05, -0.02, -0.02, 0.04, 0.03, 0.04, -0.03, -0.01, 0.09, 0.06, 0, 0.06, 0.05, 0.01, 0.02, 0.04, 0.05, 0.06,
           -0.02],
          [0.073, 0.08, 0.05, -0.01, -0.02, 0, -0.04, -0.01, -0.09, 0.02, -0.03, 0.11, -0.04, 0.02, 0.04, 0, -0.02,
           -0.06, 0.08],
          [-0.11, -0.11, -0.09, -0.07, -0.11, -0.14, -0.11, -0.13, -0.09, -0.16, -0.08, -0.06, -0.1, -0.12, -0.1, -0.08,
           -0.12, -0.1, -0.11],
          [0.01, 0.07, 0.07, 0.04, 0.01, 0.16, 0.01, 0, 0.11, 0.06, -0.01, 0.1, 0.01, 0.05, 0.07, 0.05, 0, 0.05, 0.01],
          [0.05, -0.03, -0.02, 0.01, 0.04, 0.01, -0.03, -0.01, 0.04, -0.03, -0.03, 0.02, -0.04, 0, -0.05, -0.05, -0.03,
           0, -0.01],
          [-0.07, -0.1, -0.1, -0.07, -0.02, -0.02, -0.12, -0.1, 0.01, -0.08, -0.11, -0.06, -0.04, -0.06, -0.07, -0.06,
           -0.04, -0.05, -0.02]]
moveY2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.01, 0, 0, 0, 0.01, 0.01, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [-0.02, -0.01, 0, 0, -0.01, 0.02, 0.02, 0, 0, 0, 0.03, 0.03, -0.01, 0, 0.01, 0, 0.01, 0.01, 0],
          [-0.018, 0, 0, 0, 0, 0, 0, 0, 0.01, 0, 0, -0.01, 0, 0, 0, 0, 0, 0, -0.02],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, -0.01, -0.01, 0, 0, 0.02, 0.02, 0.02, 0, -0.02, 0.01, 0, 0.01, 0.01, 0.01, 0.01, 0.03, 0.03, -0.05],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
moveZ2 = [
    [0.07, 0.1, 0.11, 0.06, -0.07, 0.10, 0.03, 0.07, -0.01, 0.12, 0.09, 0.08, -0.12, 0.09, 0.07, 0.05, 0.08, 0.11, 0.09],
    [0.12, 0.01, 0.01, 0.01, 0.05, 0.05, -0.13, 0.01, -0.11, -0.09, -0.04, 0.07, -0.07, 0, 0.02, 0.03, 0.02, 0.03, -0.03],
    [-0.01, 0, -0.03, 0.02, 0.19, 0.16, 0.09, 0.07, 0.04, -0.01, 0.04, 0.05, -0.01, 0.04, 0.01, 0.01, 0.02, 0.03, -0.03],
    [0.01, -0.01, 0.01, 0, 0.02, 0.01, -0.02, 0.02, -0.03, -0.15, 0, 0.08, -0.1, -0.03, 0, -0.11, -0.01, -0.05, 0.02],
    [0.04, -0.01, 0, 0.02, 0.06, 0.04, 0, 0.05, -0.09, 0, 0.05, 0.08, 0, 0.01, 0, 0.06, 0, -0.04, 0.06],
    [0.25, 0.2, 0.22, 0.22, 0.16, 0.12, 0.12, 0.21, 0.21, 0.22, 0.15, 0.2, 0.12, 0.19, 0.2, 0.23, 0.27, 0.26, 0.27],
    [0.03, 0.05, 0.05, 0.01, 0.08, 0.08, -0.03, 0.04, 0, 0.01, 0.06, 0.01, 0.08, 0.06, 0.03, 0.05, -0.05, 0.04, 0.01],
    [0.25, 0.16, 0.16, 0.28, 0.15, 0.23, 0.18, 0.16, 0.1, 0.14, 0.07, 0.16, 0.16, 0.16, 0.17, 0.16, 0.17, 0.18, 0.13],
    [0.21, 0.16, 0.12, 0.14, 0.17, 0.17, 0.18, 0.19, 0.18, 0.21, 0.16, 0.15, 0.09, 0.18, 0.11, 0.17, 0.19, 0.14, 0.16]]

# 旋转矩阵(行号代表实验轮次 列号代表玩家序号)
rotationMatrix = [
    [[[1, -0.06, 0], [0.06, 1, 0], [0, 0, 1]], [[1, -0.02, 0], [0.02, 1, -0.01], [0, 0.01, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
     [[1, -0.02, 0], [0.02, 1, 0], [0, 0, 1]], [[1, -0.06, 0], [0.06, 1, 0], [0, 0, 1]], [[1, 0, 0.07], [0, 1, 0], [-0.07, 0, 1]],
     [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
     [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[0.95, 0.31, 0.06], [-0.31, 0.95, -0.01], [-0.06, 0, 1]],
     [[1, 0, 0], [0, 0.99, -0.13], [0, 0.13, 0.99]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0.04], [0, 1, 0], [-0.04, 0, 1]],
     [[1, -0.03, 0], [0.03, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
     [[1, 0, 0], [0, 1, 0], [0, 0, 1]]],
    [[[1, -0.02, 0.05], [0.02, 1, -0.01], [-0.05, 0.01, 1]], [[1, 0.03, 0], [-0.03, 1, -0.06], [0, 0.06, 1]], [[1, 0.05, 0], [-0.05, 1, -0.05], [0, 0.05, 1]],
     [[1, 0, 0.04], [0, 1, -0.04], [-0.04, 0.04, 1]], [[1, 0, -0.03], [0, 1, -0.01], [0.03, 0.01, 1]], [[1, -0.05, 0], [0.05, 1, -0.03], [0, 0.03, 1]],
     [[1, 0, 0.04], [0, 0.99, -0.12], [-0.04, 0.12, 0.99]], [[1, 0.04, -0.02], [-0.04, 1, -0.01], [0.02, 0.02, 1]], [[1, -0.04, 0.06], [0.05, 0.99, -0.12], [-0.08, 0.12, 0.99]],
     [[1, -0.04, 0.08], [-0.03, 0.99, -0.12], [-0.08, 0.12, 0.99]],
     [[1, 0.05, 0], [-0.05, 1, -0.05], [0, 0.05, 1]], [[1, -0.05, -0.04], [0.05, 1, 0], [0.04, 0, 1]], [[1, -0.05, 0.04], [0.06, 0.99, -0.11], [-0.03, 0.12, 0.99]],
     [[1, 0.02, 0.07], [-0.02, 1, -0.06], [-0.07, 0.06, 1]], [[1, 0.01, 0.06], [-0.01, 1, -0.02], [-0.06, 0.02, 1]], [[1, -0.03, 0], [0.03, 1, 0], [0, 0, 1]],
     [[1, 0, 0.04], [0, 1, -0.06], [-0.04, 0.06, 1]], [[1, -0.06, 0], [0.06, 1, -0.02], [0, 0.02, 1]], [[1, 0.06, 0.02], [-0.05, 1, -0.05], [-0.02, 0.05, 1]]
     ],
    [[[1, 0, 0], [0, 1, -0.1], [0, 0.1, 1]], [[1, 0, 0], [0, 1, -0.06], [0, 0.06, 1]], [[1, 0, 0], [0, 1, -0.07], [0, 0.07, 1]],
     [[1, 0, 0.03], [0, 1, 0], [-0.03, 0, 1]], [[1, 0, 0], [0, 1, 0.05], [0, -0.05, 1]], [[1, 0, 0.06], [0, 1, 0.07], [-0.06, -0.07, 1]],
     [[1, 0, -0.01], [0, 1, 0.02], [0.01, -0.02, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, -0.08], [0, 1, -0.01], [0.08, 0.01, 1]],
     [[0.99, 0, 0.12], [0, 1, -0.01], [-0.12, 0.01, 0.99]], [[1, 0, -.07], [0, 1, 0.01], [0.07, -0.01, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
     [[1, 0, 0], [0, 1, -0.05], [0, 0.05, 1]], [[1, 0, 0], [0, 1, -0.02], [0, 0.02, 1]], [[1, 0, 0.06], [0, 1, -0.03], [-0.06, 0.03, 1]],
     [[1, 0, 0.02], [0, 1, -0.02], [-0.02, 0.02, 1]], [[1, 0, 0.05], [0, 1, -0.02], [-0.05, 0.02, 1]], [[1, 0, 0.06], [0, 1, -0.04], [-0.06, 0.04, 1]],
     [[1, 0, 0], [0, 1, -0.04], [0, 0.04, 1]]],
    [[[1, 0.02, 0.09], [-0.02, 1, 0], [-0.09, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
     [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0.02, 0], [-0.02, 1, 0], [0, 0, 1]],[[1, 0, 0.08], [0, 1, 0], [-0.08, 0, 1]], [[1, 0, 0.08], [0, 1, 0], [-0.08, 0, 1]],
     [[1, 0, 0.04], [0, 1, 0], [-0.04, 0, 1]], [[1, 0, -0.03], [0, 1, 0], [0.03, 0, 1]], [[1, -0.01, 0.07], [0.01, 0.99, -0.12], [-0.07, 0.12, 0.99]],
     [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0.01, 0], [-0.01, 1, 0.06], [0, -0.06, 1]], [[1, 0.01, 0.08], [0, 0.99, -0.13], [-0.08, 0.13, 0.99]],
     [[1, 0, 0.04], [0, 1, -0.06], [-0.04, 0.06, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, -0.09], [0, 0.09, 1]],
     [[1, 0, 0], [0, 1, -0.02], [0, 0.02, 1]], [[1, 0, 0], [0, 1, -0.04], [0, 0.04, 1]],
     [[1, 0, 0.03], [0, 1, -0.01], [-0.03, 0.01, 1]]],
    [[[1, 0, 0.04], [0, 1, -0.07], [-0.04, 0.07, 1]], [[1, -0.03, 0.04], [0.04, 1, -0.07], [-0.03, 0.07, 1]], [[1, -0.02, 0.04], [0.02, 1, -0.06], [-0.04, 0.07, 1]],
     [[1, 0.04, 0.01], [-0.03, 1, -0.07], [-0.01, 0.07, 1]], [[1, 0, 0.03], [0, 1, 0], [-0.03, 0, 1]], [[1, -0.03, 0.06], [0.03, 1, -0.04], [-0.06, 0.04, 1]],
     [[1, 0.05, 0.08], [-0.04, 1, -0.07], [-0.08, 0.07, 0.99]], [[1, 0.04, 0.04], [-0.04, 1, -0.04], [-0.04, 0.04, 1]], [[0.99, 0.1, 0.04], [-0.1, 0.99, -0.1], [-0.05, 0.1, 0.99]],
     [[1, 0.04, 0.07], [-0.04, 1, -0.06], [-0.07, 0.06, 1]], [[1, 0, 0.06], [0, 1, -0.03], [-0.06, 0.03, 1]], [[1, -0.02, 0.02], [0.02, 1, 0.02], [-0.02, -0.02, 1]],
     [[0.99, 0.01, 0.1], [0, 0.99, -0.12], [-0.1, 0.12, 0.99]], [[1, -0.04, 0.04], [0.05, 1, -0.06], [-0.04, 0.06, 1]], [[1, 0, 0.03], [0, 1, -0.03], [-0.03, 0.03, 1]],
     [[1, 0, 0.03], [0, 1, -0.04], [-0.03, 0.04, 1]], [[1, 0, 0.05], [0, 1, -0.05], [-0.05, 0.05, 1]], [[1, 0, 0.05], [0, 1, -0.02], [-0.05, 0.02, 1]],
     [[1, -0.04, 0.04], [0.04, 1, -0.05], [-0.04, 0.05, 1]]],
[[[1, 0, 0.03], [0, 1, -0.03], [-0.03, 0.03, 1]], [[1, 0.01, 0.07], [0, 1, -0.07], [-0.07, 0.07, 0.99]], [[1, 0, 0.05], [0, 1, -0.05], [-0.05, 0.05, 1]],
     [[1, 0, 0], [0, 1, -0.02], [0, 0.02, 1]], [[1, 0, 0], [0, 1, -0.04], [0, 0.04, 1]], [[1, 0.01, 0.07], [0, 0.99, -0.11], [-0.07, 0.11, 0.99]],
     [[1, 0, -0.01], [0, 1, -0.05], [0.01, 0.05, 1]], [[1, 0, 0.06], [0, 1, -0.03], [-0.06, 0.03, 1]], [[1, 0, 0.06], [0, 1, -0.08], [-0.06, 0.08, 1]],
     [[1, 0.02, 0.08], [-0.02, 1, -0.02], [-0.08, 0.02, 1]], [[1, 0, 0], [0, 0.99, -0.1], [0, 0.1, 0.99]], [[1, 0, -0.05], [0, 1, -0.03], [0.05, 0.03, 1]],
     [[1, 0.01, 0.08], [0, 0.99, -0.1], [-0.08, 0.1, 0.99]], [[1, 0, 0.06], [0, 1, -0.05], [-0.07, 0.05, 1]], [[1, 0, 0.02], [0, 1, -0.02], [-0.02, 0.02, 1]],
     [[1, 0., 0], [0, 1, -0.02], [0, 0.02, 1]], [[1, 0, 0.06], [0, 1, 0], [-0.06, 0, 1]], [[1, 0, 0.07], [0, 1, -0.01], [-0.07, 0.01, 1]],
     [[1, 0, 0], [0, 1, 0.01], [0, -0.01, 1]]],
    [[[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0.05], [0, 1, 0], [-0.05, 0, 1]],
     [[1, 0, -0.05], [0, 1, 0], [0.05, 0, 1]], [[1, 0, 0.01], [0, 1, 0], [0.01, 0, 1]],
     [[0.99, -0.11, 0.10], [0.11, 0.99, 0.01], [-0.1, 0.01, 0.99]],
     [[1, -0.02, 0], [0.02, 1, -0.06], [0, 0.06, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
     [[1, -0.05, 0.04], [0.05, 1, 0], [-0.04, 0, 1]],
     [[1, 0, 0.08], [0, 1, 0], [-0.08, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
     [[1, 0, 0.07], [0, 1, 0], [-0.07, 0, 1]], [[1, 0, 0.08], [0, 1, 0], [-0.08, 0, 1]],
     [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
     [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0.05, 0.05], [-0.05, 0.99, -0.09], [-0.05, 0.09, 0.99]],
     [[1, 0, 0], [0, 1, -0.02], [0, 0.02, 1]],
     [[1, 0, 0.03], [0, 1, -0.02], [0, 0.02, 1]]],
[[[1, 0, 0.03], [0, 1, 0.06], [-0.03, -0.06, 1]], [[1, 0.01, 0.1], [0, 1, -0.05], [-0.1, 0.05, 0.99]], [[1, 0, 0.08], [0, 1, -0.05], [-0.08, 0.05, 1]],
     [[1, 0, 0.08], [0, 1, 0.05], [-0.08, -0.05, 1]], [[1, 0, 0], [0, 1, -0.05], [0, 0.05, 1]], [[1, 0, 0.08], [0, 1, 0.01], [-0.08, -0.01, 1]],
     [[1, 0, 0.07], [0, 1, -0.04], [-0.07, 0.04, 1]], [[1, 0, 0.03], [0, 1, -0.03], [-0.03, 0.03, 1]], [[1, 0, 0.01], [0, 1, -0.06], [-0.01, 0.06, 1]],
     [[0.99, 0.01, 0.1], [0, 1, -0.08], [-0.1, 0.08, 0.99]], [[1, 0.01, 0.07], [0, 1, -0.08], [-0.07, 0.08, 0.99]], [[1, 0, 0.02], [0, 1, -0.01], [-0.02, 0.01, 1]],
     [[1, 0.01, 0.06], [0, 1, -0.08], [-0.06, 0.08, 0.99]], [[1, -0.04, 0.05], [0.04, 1, -0.05], [-0.05, 0.05, 1]], [[1, 0, 0.03], [0, 1, -0.03], [-0.03, 0.03, 1]],
     [[1, 0, 0.03], [0, 1, -0.04], [-0.03, 0.04, 1]], [[1, 0, 0.05], [0, 1, -0.05], [-0.05, 0.05, 1]], [[1, 0, 0.05], [0, 1, -0.02], [-0.05, 0.02, 1]],
     [[1, -0.04, 0.04], [0.04, 1, -0.05], [-0.04, 0.05, 1]]],
    [[[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0.01, 0.1], [0, 1, -0.07], [-0.1, 0.07, 0.99]], [[1, 0.01, 0.07], [0, 0.99, -0.11], [-0.07, 0.1, 0.99]],
     [[1, 0, 0.04], [0, 1, -0.08], [-0.04, 0.08, 1]], [[1, 0, -0.02], [0, 1, -0.06], [0.02, 0.06, 1]], [[1, 0, 0], [0, 1, -0.05], [0, 0.05, 1]],
     [[1, 0, 0.08], [0, 1, -0.06], [-0.08, 0.05, 1]], [[1, 0, 0.02], [0, 1, -0.02], [-0.02, 0.02, 1]], [[1, 0, -0.05], [0, 1, -0.02], [0.05, 0.02, 1]],
     [[1, 0, 0.07], [0, 1, -0.02], [-0.07, 0.02, 1]], [[1, 0.02, 0.07], [-0.01, 1, -0.07], [-0.07, 0.07, 1]], [[1, 0, 0.02], [0, 1, -0.04], [-0.02, 0.04, 1]],
     [[1, 0, 0.04], [0, 0.99, -0.1], [-0.04, 0.1, 0.99]], [[1, 0, 0.05], [0, 1, -0.05], [-0.05, 0.05, 1]], [[1, 0, 0.05], [0, 1, -0.05], [-0.05, 0.05, 1]],
     [[1, 0, 0.05], [0, 1, -0.01], [-0.05, 0.01, 1]], [[1, 0, 0.05], [0, 1, -0.01], [-0.05, 0.01, 1]], [[1, 0, 0.07], [0, 1, -0.05], [-0.07, 0.05, 1]],
     [[1, 0, 0], [0, 1, -0.03], [0, 0.03, 1]]]]

x = []
y = []
z = []
v = []
triggerX = []
triggerY = []
triggerZ = []
targetPosX = []
targetPosY = []
targetPosZ = []
distance = []
z_dis = []
expKind = ""
zeroExist = True
ballSize = 0
expRounds = 0
radius = 0
# 三种选择技术
for j in range(3):
    if j == 0:
        expKind = "tap"
    elif j == 1:
        expKind = "longpress"
    elif j == 2:
        expKind = "magic"
    # 3种DD值
    DD = ""
    for q in range(3):


        targetPosX.clear()
        targetPosY.clear()
        targetPosZ.clear()
        if q == 2:
            ballSize = 80 * math.pi
            radius = 0.015
            targetPosX, targetPosY, targetPosZ = get_target_pos(0.35, centerX[expRounds], centerY[expRounds],
                                                                centerZ[expRounds])

            DD = "H"
        elif q == 0:
            radius = 0.03
            ballSize = 100 * math.pi * 4
            targetPosX, targetPosY, targetPosZ = get_target_pos(0.3, centerX[expRounds], centerY[expRounds],
                                                                centerZ[expRounds])
            DD = "M"
        elif q == 1:
            ballSize = 100 * math.pi * 9
            radius = 0.045
            targetPosX, targetPosY, targetPosZ = get_target_pos(0.25, centerX[expRounds], centerY[expRounds],
                                                                centerZ[expRounds])
            print(111, targetPosX)
            DD = "L"

        # 导出坐标球pts位置
        # targetPoint = []
        # for op in range(len(targetPosX)):
        #     targetPoint.append([targetPosX[op], targetPosY[op], targetPosZ[op]])
        #     export_to_pts(targetPoint, "targetPoint" + str(j) + "-" + DD + ".pts")

        data2 = []
        x.clear()
        y.clear()
        z.clear()
        v.clear()
        triggerX.clear()
        triggerY.clear()
        triggerZ.clear()
        oriX = 0
        oriY = 0
        oriZ = 0
        # 找出基准坐标 第一位
        df = pd.read_csv("data\\" + "1" + "\\" + expKind + "\\" + "trajectory.csv", encoding="utf-8")
        data = df.groupby('Case')
        startIndex = 0
        # 找到开始序号
        for key, value in data.groups.items():
            startIndex = key
            break
        # 每一组第一位的数据
        tempLoc = np.array(data.get_group(startIndex + q * 15 + expIndex[0][q + j * 3] - 1).reset_index()).tolist()
        # print(tempLoc[-1])
        oriX = tempLoc[-1][2]
        oriY = tempLoc[-1][3]
        oriZ = tempLoc[-1][4]
        # print(startIndex + q * 15 + expIndex[0][q + j * 3] - 1)
        # 19名被试，从1开始编号
        for k in range(begin, end):
            # 跳过有问题的点
            # if j == 0 and q == 2 and k == 9:
            #     continue
            # elif j == 2 and q == 2 and k == 13:
            #     continue
            # elif j == 2 and q == 2 and k == 11:
            #     continue
            # elif j == 1 and q == 2 and k == 1:
            #     continue
            # elif j == 1 and q == 2 and k == 5:
            #     continue
            # elif j == 1 and q == 2 and k == 13:
            #     continue
            # elif j == 1 and q == 2 and k == 11:
            #     continue
            # elif j == 1 and q == 2 and k == 6:
            #     continue
            # elif j == 1 and q == 0 and k == 2:
            #     continue
            # elif j == 1 and q == 0 and k == 3:
            #     continue
            # elif j == 1 and q == 0 and k == 12:
            #     continue
            # elif j == 1 and q == 0 and k == 7:
            #     continue
            # elif j == 1 and q == 0 and k == 10:
            #     continue
            # elif j == 2 and q == 0 and k == 12:
            #     continue
            # elif j == 2 and q == 0 and k == 10:
            #     continue
            # elif j == 2 and q == 0 and k == 13:
            #     continue
            # elif j == 2 and q == 0 and k == 9:
            #     continue
            # elif j == 0 and q == 0 and k == 5:
            #     continue
            # elif j == 2 and q == 0 and k == 11:
            #     continue
            # elif j == 2 and q == 0 and k == 10:
            #     continue
            # elif j == 2 and q == 1 and k == 4:
            #     continue
            # elif j == 2 and q == 1 and k == 5:
            #     continue
            # elif j == 2 and q == 1 and k == 9:
            #     continue
            # elif j == 2 and q == 1 and k == 13:
            #     continue
            # elif j == 0 and q == 1 and k == 9:
            #     continue
            # elif j == 0 and q == 1 and k == 10:
            #     continue
            # elif j == 1 and q == 1 and k == 9:
            #     continue
            # elif j == 1 and q == 1 and k == 18:
            #     continue
            # elif j == 1 and q == 1 and k == 13:
            #     continue
            # elif j == 1 and q == 1 and k == 12:
            #     continue

            distance.clear()
            z_dis.clear()
            df = pd.read_csv("data\\" + str(k) + "\\" + expKind + "\\" + "trajectory.csv", encoding="utf-8")
            data = df.groupby('Case')
            startIndex = 0
            # 找到开始序号
            for key, value in data.groups.items():
                startIndex = int(key)
                # print("start", startIndex)
                break
                # 对于每个文件，是3种不同DD混在一起，所以要给他分开
            ballIndex = expIndex[k - 1][q + j * 3]
            # print("ballIndex", ballIndex)
            if ballIndex == -1:
                zeroExist = False
                ballIndex = 1
            data1 = np.array(data.get_group(startIndex + q * 15 + ballIndex - 1).reset_index()).tolist()

            # 由于坐标有偏移，以第一组为基准进行校准
            if not zeroExist:
                moveX = data1[0][2] - oriX
                moveY = data1[0][3] - oriY
                moveZ = data1[0][4] - oriZ
                zeroExist = True
            else:
                moveX = data1[-1][2] - oriX
                moveY = data1[-1][3] - oriY
                moveZ = data1[-1][4] - oriZ

            # print("---------")
            # print(startIndex + q * 15 + expIndex[k - 1][q + j * 3] - 1)
            df = pd.read_csv("data\\" + str(k) + "\\" + expKind + "\\" + "trajectory.csv", encoding="utf-8")
            data = df.groupby('Case')
            points = []

            # 15个目标球
            # for i in range(startIndex + q * 15, startIndex + (q + 1) * 15):
            # for i in range(startIndex + q * 16, startIndex + (q + 1) * 16):
            # qq2
            for i in range(1, 49):  # 左闭右开
                # for i in range(1, 4):
                try:
                    # 每一个人每轮数据
                    # !!!
                    data1 = np.array(data.get_group(i).reset_index()).tolist()
                    # print(data1)
                except KeyError:
                    print("case", i, "被完全去除了")
                    # pass
                # 只需要存一次目标球位置就够了
                # if k == 1:
                # if i == startIndex + q * 15:
                #     targetPosX.append(data1[0][2])
                #     targetPosY.append(data1[0][3])
                #     targetPosZ.append(data1[0][4])
                # targetPosX.append(data1[-1][2])
                # targetPosY.append(data1[-1][3])
                # targetPosZ.append(data1[-1][4])

                for temp in data1:
                    # temp[2] -= moveX
                    # temp[3] -= moveY
                    # temp[4] -= moveZ
                    # temp[2] += moveX2[q + j * 3][k - 1]
                    # temp[3] += moveY2[q + j * 3][k - 1]
                    # temp[4] += moveZ2[q + j * 3][k - 1]
                    #
                    # tempRotation = np.array(rotationMatrix[q + j * 3][k - 1])
                    # tempX = temp[2]
                    # tempY = temp[3]
                    # tempZ = temp[4]
                    # oldXYZ = np.array([[tempX], [tempY], [tempZ]])
                    # newXYZ = np.dot(tempRotation, oldXYZ)
                    #
                    # # newXYZ = np.dot([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], newXYZ)
                    #
                    # newXYZ.tolist()
                    # # print(oldXYZ, newXYZ)
                    # # print("-----------------")
                    # # points.append([newXYZ[0], newXYZ[1], newXYZ[2]])
                    # temp[2] = newXYZ[0][0]
                    # temp[3] = newXYZ[1][0]
                    # temp[4] = newXYZ[2][0]
                    z_dis.append(abs(temp[4] - centerZ[q + j * 3]) * 1000)
                    data2.append(temp)
                triggerX.append(data1[0][2])
                triggerY.append(data1[0][3])
                triggerZ.append(data1[0][4])
            # with open("Z" + expKind + DD + str(k) + ".csv", "a", encoding="utf-8", newline="") as f:
            #     # 2. 基于文件对象构建 csv写入对象
            #     csv_writer = csv.writer(f)
            #
            #     for temp in z_dis:
            #         temp2 = str(temp)
            #         csv_writer.writerow([temp2])
            #     # 5. 关闭文件
            #     f.close()
            #     for locIndex in range(len(data1) - 1):
            #         tempDistance = math.sqrt((data1[locIndex + 1][2] - data1[locIndex][2]) ** 2 + (
            #                 data1[locIndex + 1][3] - data1[locIndex][3]) ** 2 + (
            #                                          data1[locIndex + 1][4] - data1[locIndex][4]) ** 2)
            #         # print(tempDistance)
            #         distance.append(tempDistance)
            print(np.std(z_dis))
            # 导出到 .pts 文件

            # export_to_pts(points, "output" + str(k) + "-" + expKind + "-" + DD + ".pts")
            toJump = False
            jumpTimes = 0
            for temp in data2:
                # if not temp[2] == 0 and not temp[3] == 0 and not temp[4] == 0:
                #     if temp[3] > 0.5:
                #         # 手部遮挡会影响接下来的av值，先去除接下来的20条试试
                #         if toJump:
                #             # print("jump")
                #             jumpTimes += 1
                #             if jumpTimes == 21:
                #                 toJump = False
                #         else:
                #             x.append(temp[2])
                #             y.append(temp[3])
                #             z.append(temp[4])
                #             v.append(temp[6])
                #
                #
                # else:
                #     toJump = True
                x.append(temp[2])
                y.append(temp[3])
                z.append(temp[4])
                v.append(temp[6])


        print("z轴离散值", np.std(z))
        cmap = 'bwr'  # jet, hsv等也是常用的颜色映射方案
        colors = color_map(v, cmap, 0.75)
        mpl.rcParams['legend.fontsize'] = 10
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(projection='3d')
        # 画16个目标球，s为点的面积
        print(targetPosX, targetPosY, targetPosZ)
        # 获取坐标轴的宽度（x 轴的范围）
        x_axis_width = plt.gca().get_xlim()[1] - plt.gca().get_xlim()[0]
        # 绘制16个目标球
        ax.scatter(targetPosX, targetPosY, targetPosZ, s=ballSize, color='#0F38F5')
        # 画坐标轴
        # ax.plot([-0.7, 0.5], [1.8, 1.8], [0.6, 0.6], color='black')
        # ax.plot([-0.7, -0.7], [0.6, 1.8], [0.6, 0.6], color='black')
        # ax.plot([-0.7, -0.7], [1.8, 1.8], [0, 0.6], color='black')
        # ax.scatter(x, y, z, c=colors, s=1, alpha=0.005)
        ax.scatter(x, y, z, c=colors, s=1)
        # for d in range(1, len(v) - 1):
        #     ax.plot(x[d - 1:d + 1], y[d - 1:d + 1], z[d - 1:d + 1], c=colors[d])
        # ax.plot(x, y, z, label='parametric curve', linewidth=0.1)
        ax.legend()

        # 隐藏刻度线
        ax = plt.gca()
        # ax.axes.xaxis.set_ticks([])
        # ax.axes.yaxis.set_ticks([])
        # ax.axes.zaxis.set_ticks([])

        # ax.axes.xaxis.set_ticklabels([])
        # ax.axes.yaxis.set_ticklabels([])
        # ax.axes.zaxis.set_ticklabels([])
        plt.grid(False)

        # 调整视角
        ax.view_init(elev=90, azim=0, roll=0)
        # ax.view_init(elev=90, azim=0, roll=0)
        # 调整坐标轴
        # my_x_ticks = np.arange(-0.7, 0.5, 0.1)
        # my_y_ticks = np.arange(0.6, 1.8, 0.1)
        # plt.xticks(my_x_ticks)
        # plt.yticks(my_y_ticks)
        # dx = 1.2
        # dy = 1.2
        # dz = 1.2
        # ax.set_box_aspect([dx, dy, dz])
        # plt.axis("equal")

        ax.set_xlim3d(xmin=-1, xmax=1)
        ax.set_ylim3d(ymin=0, ymax=2)
        ax.set_zlim3d(zmin=0, zmax=2)
        # 关闭坐标轴
        plt.axis('off')

        # 画颜色条
        # fig, axes = plt.subplots(4, 1, figsize=(10, 5))
        # fig.subplots_adjust(hspace=4)
        # cmap1 = copy.copy(cm.bwr)
        # norm1 = mcolors.Normalize(vmin=0, vmax=100)
        # im1 = cm.ScalarMappable(norm=norm1, cmap=cmap1)
        # cbar1 = fig.colorbar(
        #     im1, cax=axes[0], orientation='horizontal',
        #     ticks=np.linspace(0, 100, 11),
        #     label='colorbar with Normalize'
        # )

        #  image 为四通道图像（RGBA）
        # fig.savefig(str(expRounds), transparent=True, dpi=1000, bbox_inches='tight', pad_inches=0.0)

        # plt.show()
        # 清空缓存
        plt.close(fig)

        expRounds += 1

        # with open("ori_data" + str(expRounds) + ".csv", "a", encoding="utf-8", newline="") as f:
        #     # 2. 基于文件对象构建 csv写入对象
        #     csv_writer = csv.writer(f)
        #     temp = []
        #     for i in range(len(x)):
        #         temp.append(i)
        #         temp.append(x[i])
        #         temp.append(y[i])
        #         temp.append(z[i])
        #         csv_writer.writerow(temp)
        #         temp.clear()
        #     csv_writer.writerow("q")
        #     # 5. 关闭文件
        #     f.close()

        '''测试mayavi中的plot3d，points3d函数
        :return: None
        '''
        trigger_points = []
        points = []
        for qq in range(len(x)):
            points.append([x[qq], y[qq], z[qq]])
        for qq in range(len(triggerX)):
            trigger_points.append([triggerX[qq], triggerY[qq], triggerZ[qq]])
        p2 = pv.PolyData(trigger_points)

        mesh = pv.PolyData(points)  # PolyData对象的实例化
        # mesh.plot(point_size=2, style='points')
        # p = pv.Plotter(off_screen=True)
        p = pv.Plotter()
        targetPosX = [0.35, 0.3233578, 0.2474874, 0.1339392, 0 ,    -0.1339392 ,-0.2474874 ,-0.3233578 ,-0.35, -0.3233578, -0.2474874, -0.1339393, 0  ,   0.1339393, 0.2474873, 0.3233579]
        targetPosY = [1.1 , 1.233939 , 1.347487  ,1.423358 , 1.45 , 1.423358,   1.347487 ,  1.233939  , 1.1   ,0.9660608 ,0.8525127 , 0.7766422 , 0.75,  0.7766422,0.8525126 ,0.9660608]
        targetPosZ = [0.537,0.537,0.537,0.537,0.537,0.537,0.537,0.537,0.537,0.537,0.537,0.537,0.537,0.537,0.537,0.537]
        # 目标球
        for q1 in range(len(targetPosX)):
            sphere = pv.Sphere(radius=radius, center=(targetPosX[q1], targetPosY[q1], targetPosZ[q1]))
            p.add_mesh(sphere, color='lightblue', opacity=0.5)
        cmap = 'bwr'
        v_max = max(v)
        v_min = min(v)
        v_new = []
        for temp_v in v:
            v_new.append((v_max - temp_v) / (v_max - v_min))
        # p.add_mesh(mesh, cmap=cmap, point_size=5)
        p.add_mesh(mesh, scalars=v_new, cmap=cmap, point_size=5)
        # 障碍球
        p.add_mesh(p2, color='#000000', point_size=20)

        p.show_grid()
        p.camera_position = 'zx'
        p.show_grid = True

        # p.screenshot(expKind + DD + ".png", transparent_background=True, window_size=[500, 500], scale=10)
        count = 0
        for trigger_point in trigger_points:
            for i in range(16):
                if trigger_points.index(trigger_point) + 1 == 31:
                    print(trigger_point[0])
                    print(111,
                        math.sqrt((trigger_point[0] - targetPosX[i]) ** 2 + (trigger_point[1] - targetPosY[i]) ** 2 + (
                                trigger_point[2] - targetPosZ[i]) ** 2))
                    # break

                if math.sqrt((trigger_point[0] - targetPosX[i])**2 + (trigger_point[1] - targetPosY[i])**2 + (trigger_point[2] - targetPosZ[i])**2) - 0.015 < 0:
                    # print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
                    # print(math.sqrt((trigger_point[0] - targetPosX[i]) ** 2 + (trigger_point[1] - targetPosY[i]) ** 2 + (
                    #             trigger_point[2] - targetPosZ[i]) ** 2))
                    # 满足条件
                    print(trigger_points.index(trigger_point) + 1, i)
                    count += 1
                else:
                    pass
                    # print(trigger_point[0])
        print("count", count)

        df111 = pd.read_csv("data\\" + "obs.csv", encoding="utf-8")
        temp1 = df111["X"].tolist()
        temp2 = df111["Y"].tolist()
        temp3 = df111["Z"].tolist()

        # for q1 in range(len(temp1)):
        #     sphere = pv.Sphere(radius=radius, center=(temp1[q1], temp2[q1], temp3[q1]))
        #     p.add_mesh(sphere, color='lightblue', opacity=0.5)

        p.show(cpos="zx")
        print(1)


# 0.35 0.3233578 0.2474874 0.1339392 0     -0.1339392 -0.2474874 -0.3233578 -0.35 -0.3233578 -0.2474874 -0.1339393 0     0.1339393 0.2474873 0.3233579
# 1.1  1.233939  1.347487  1.423358  1.45  1.423358   1.347487   1.233939   1.1   0.9660608  0.8525127  0.7766422  0.75  0.7766422 0.8525126 0.9660608
# 0.537