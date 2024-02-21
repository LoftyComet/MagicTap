import csv
import math
import matplotlib as mpl
import pandas as pd
import pyvista as pv

import numpy as np
import matplotlib.pyplot as plt
import xlwt
import xlrd


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
    # print(ans_x, ans_y, ans_z)
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


def project_point_on_line_segment(point, line_start, line_end):
    # Step 1: Compute the direction vector `v` of the line segment
    v = line_end - line_start

    # Step 2: Compute the vector `w` between the point and the line start
    w = point - line_start

    # Step 3: Calculate the projection of w onto v
    mu = np.dot(w, v) / np.dot(v, v)

    # Step 4: Clamp the value of mu between 0 and 1
    # mu = np.clip(mu, 0, 1)

    # Step 5: Calculate the projection point
    projection = line_start + mu*v

    return mu, projection


def get_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


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
# 手动调整每一轮圆心位置
centerX = [0, 0, 0, 0, 0, 0, 0, 0, 0]
centerY = [1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1]
centerZ = [0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537]
# 开始结束序号(左闭右开) qq1
begin = 1
end = 21
# 行号代表实验轮次 列号代表玩家序号 X Y Z代表三维坐标
x = []
y = []
z = []
v = []
triggerX = []
triggerY = []
triggerZ = []
trigger_case_X = []
trigger_case_Y = []
targetPosX = []
targetPosY = []
targetPosZ = []
distance = []

ID_kinds = [[0, 1, 2], [1, 2, 0], [2, 0, 1], [0, 1, 2], [1, 2, 0], [2, 0, 1],[0, 1, 2], [1, 2, 0], [2, 0, 1],[0, 1, 2],
            [1, 2, 0], [2, 0, 1],[0, 1, 2], [1, 2, 0], [2, 0, 1],[0, 1, 2], [1, 2, 0], [2, 0, 1],[0, 1, 2], [1, 2, 0]]
# 每轮第一次点击终点编号
first_end_index = [14, 3, 0, 5, 2, 7, 4, 9, 6, 11, 8, 13, 10, 15, 12, 1, 14, 3, 0, 5]
# 每轮第一次点击起点编号
first_start_index = [7, 10, 9, 12, 11, 14, 13, 0, 15, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12]
rotation_directions = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
# 由于每次点击的触发点在下一轮开头，需要转化一下
#
# 0 +7 ; 1 -7
z_dis = []
expKind = ""
zeroExist = True
expRounds = 0
radius = 0

# 四种选择技术
for j in range(4):
    if j == 0:
        expKind = "tap"

    elif j == 1:
        expKind = "longpress"
    elif j == 2:
        expKind = "pinch"
    elif j == 3:
        expKind = "magic"
    print(expKind, "start")


    # 3种DD值
    DD = ""
    for q in range(3):

        targetPosX.clear()
        targetPosY.clear()
        targetPosZ.clear()


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
        wb = xlwt.Workbook()
        ws = wb.add_sheet(expKind)
        # 20名被试，从1开始编号
        for k in range(begin, end):
            ID_kind = ID_kinds[k-1][q]
            ID_index = 0
            if q == 0:
                radius = 0.015
                targetPosX, targetPosY, targetPosZ = get_target_pos(0.35, centerX[0], centerY[0],
                                                                    centerZ[0])
                DD = "H"
                ID_index = ID_kinds[k-1].index(0)
            elif q == 1:
                radius = 0.03
                targetPosX, targetPosY, targetPosZ = get_target_pos(0.3, centerX[0], centerY[0],
                                                                    centerZ[0])
                DD = "M"
                ID_index = ID_kinds[k-1].index(1)
            elif q == 2:
                radius = 0.045
                targetPosX, targetPosY, targetPosZ = get_target_pos(0.25, centerX[0], centerY[0],
                                                                    centerZ[0])
                DD = "L"
                ID_index = ID_kinds[k-1].index(2)
            distance.clear()
            distance_case = 0
            z_dis.clear()
            df = pd.read_csv("data\\" + str(k) + "\\" + expKind + "\\" + "trajectory.csv", encoding="utf-8")
            data = df.groupby('Case')
            startIndex = 0
            # 找到开始序号
            for key, value in data.groups.items():
                startIndex = int(key)
                # print("start", startIndex)
                break
            # print("---------")
            df = pd.read_csv("data\\" + str(k) + "\\" + expKind + "\\" + "trajectory.csv", encoding="utf-8")
            data = df.groupby('Case')
            points = []
            trigger_case_X.clear()
            trigger_case_Y.clear()
            # qq2
            for i in range(startIndex + ID_index * 16, startIndex + ID_index * 16 + 16):  # 左闭右开
                try:
                    # 每一个人48次的点击数据
                    # !!!
                    data1 = np.array(data.get_group(i).reset_index()).tolist()
                    # print(data1)
                except KeyError:
                    print("case", i, "被完全去除了", expKind, DD, k)
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
                # 每次点击的所有数据行
                for temp in data1:
                    z_dis.append(abs(temp[4] - centerZ[0]) * 1000)
                    data2.append(temp)
                triggerX.append(data1[0][2])
                triggerY.append(data1[0][3])
                triggerZ.append(data1[0][4])
                trigger_case_X.append(data1[0][2])
                trigger_case_Y.append(data1[0][3])
                for locIndex in range(len(data1) - 1):
                    tempDistance = math.sqrt((data1[locIndex + 1][2] - data1[locIndex][2]) ** 2 + (
                            data1[locIndex + 1][3] - data1[locIndex][3]) ** 2 + (
                                                     data1[locIndex + 1][4] - data1[locIndex][4]) ** 2)
                    # print(tempDistance)
                    distance_case += tempDistance
                    distance.append(tempDistance)
                # 所用时间等于总行数-6 * 0.02
                # if i == startIndex + ID_index * 16 + 16 - 1:
                #     print((len(z_dis) - 6) * 0.02)
            # 第一个起点较特殊
            line_start = np.array([targetPosX[first_start_index[k-1]], targetPosY[first_start_index[k-1]]])
            line_end = np.array([targetPosX[first_end_index[k-1]], targetPosY[first_end_index[k-1]]])
            point = np.array([trigger_case_X[1], trigger_case_Y[1]])
            mu, projection = project_point_on_line_segment(point, line_start, line_end)
            # dx
            # print(get_distance(line_end, line_start) - get_distance(projection, line_start))
            # print(get_distance(line_end, line_start))
            ws.write(k, 0, get_distance(line_end, line_start) - get_distance(projection, line_start))
            # ws.write(k, 0, get_distance(line_end, line_start))
            rotation_direction = rotation_directions[k - 1]
            temp = first_end_index[k - 1]
            # 剩余14次点击
            for i in range(1, 15):
                line_start = np.array([trigger_case_X[i], trigger_case_Y[i]])

                if rotation_direction == 0:
                    temp = (temp + 7) % 16
                else:
                    temp = (temp - 7) % 16
                line_end = np.array([targetPosX[temp], targetPosY[temp]])
                point = np.array([trigger_case_X[i+1], trigger_case_Y[i+1]])
                mu, projection = project_point_on_line_segment(point, line_start, line_end)
                # dx

                # print(get_distance(line_end, line_start) - get_distance(projection, line_start))
                # ws.write(k, i, get_distance(line_end, line_start))
                ws.write(k, i, get_distance(line_end, line_start) - get_distance(projection, line_start))
                # print(get_distance(line_end, line_start))
            wb.save(expKind + DD + '.xls')
            # print("over")
            # print(np.std(z_dis))
            # print(distance_case)
            for temp in data2:
                x.append(temp[2])
                y.append(temp[3])
                z.append(temp[4])
                v.append(temp[6])
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
        targetPosX = [0.35, 0.3233578, 0.2474874, 0.1339392, 0, -0.1339392, -0.2474874, -0.3233578, -0.35, -0.3233578,
                      -0.2474874, -0.1339393, 0, 0.1339393, 0.2474873, 0.3233579]
        targetPosY = [1.1, 1.233939, 1.347487, 1.423358, 1.45, 1.423358, 1.347487, 1.233939, 1.1, 0.9660608, 0.8525127,
                      0.7766422, 0.75, 0.7766422, 0.8525126, 0.9660608]
        targetPosZ = [0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537, 0.537,
                      0.537, 0.537]
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
        p.camera_position = 'zx'
        p.show_grid = True

        # p.screenshot(expKind + DD + ".png", transparent_background=True, window_size=[500, 500], scale=10)

        # 快速验证
        count = 0
        for trigger_point in trigger_points:
            for i in range(16):
                if trigger_points.index(trigger_point) + 1 == 31:
                    pass
                    # print(trigger_point[0])
                    # print(111,
                    #       math.sqrt(
                    #           (trigger_point[0] - targetPosX[i]) ** 2 + (trigger_point[1] - targetPosY[i]) ** 2 + (
                    #                   trigger_point[2] - targetPosZ[i]) ** 2))
                    # break

                if math.sqrt((trigger_point[0] - targetPosX[i]) ** 2 + (trigger_point[1] - targetPosY[i]) ** 2 + (
                        trigger_point[2] - targetPosZ[i]) ** 2) - 0.015 < 0:
                    # print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
                    # print(math.sqrt((trigger_point[0] - targetPosX[i]) ** 2 + (trigger_point[1] - targetPosY[i]) ** 2 + (
                    #             trigger_point[2] - targetPosZ[i]) ** 2))
                    # 满足条件
                    # print(trigger_points.index(trigger_point) + 1, i)
                    count += 1
                else:
                    pass
                    # print(trigger_point[0])
        print("count", count)

        # df111 = pd.read_csv("data\\" + "obs.csv", encoding="utf-8")
        # temp1 = df111["X"].tolist()
        # temp2 = df111["Y"].tolist()
        # temp3 = df111["Z"].tolist()

        # for q1 in range(len(temp1)):
        #     sphere = pv.Sphere(radius=radius, center=(temp1[q1], temp2[q1], temp3[q1]))
        #     p.add_mesh(sphere, color='lightblue', opacity=0.5)

        # p.show(cpos="zx")
        print(1)
