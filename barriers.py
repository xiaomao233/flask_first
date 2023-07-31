from LineStop import *


def obstacleName(name):
    s = name.split(' ')
    s[2] = int(s[2])
    s[3] = float(s[3])
    return s


def barriers(barriers_tuple):
    barriers_list = []
    name_list = []
    for i in barriers_tuple:
        i = list(i)
        name_list = obstacleName(i[0])
        [i[1], i[2]] = list(map(float, [i[1], i[2]]))
        name_list.extend([i[1], i[2]])
        barriers_list.append(name_list)
    # print(barriers_list)
    Line = []  # 存放L型障碍物类
    Circle = []  # 存放O型障碍物
    for i in range(len(barriers_list)):  # i是行号
        if barriers_list[i][1] == 'L':  # 第i行的'B'是'L'，表示是L型障碍物
            for j in range(i + 1, len(barriers_list)):  # 从i+1行开始查找
                if barriers_list[i][0] == barriers_list[j][0]:  # 根据同一个障碍物的'AA'相同找到L型障碍物的第二个点
                    Line.append(LineStop(barriers_list[i][0],  # num即'AA'
                                         [barriers_list[i][5], barriers_list[i][6]],  # 第一个点的纬度，经度坐标
                                         [barriers_list[j][5], barriers_list[j][6]],  # 第二个点的纬度，经度坐标
                                         barriers_list[i][3],  # 靠近第一个点的宽度
                                         barriers_list[j][3]  # 靠近第二个点的宽度
                                         )
                                )
        if barriers_list[i][1] == 'O':
            Circle.append(
                [barriers_list[i][0], [barriers_list[i][5], barriers_list[i][6]], barriers_list[i][3] / 10]
            )
    Line4points = []
    for i in Line:
        # 调用LineStop类中midpoint2vertex方法，将得到的障碍物地理坐标序列存入Line4points中
        Line4points.append(i.midpoint2vertex())
    # print(Line4points)
    return Circle, Line4points
