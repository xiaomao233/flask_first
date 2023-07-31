import math


def midpoint2vertex(point1, point2, width1, width2):    # point1,point2为已知两个中点的UTM坐标，width1,width2为对应的宽度
    k1 = (point1[1] - point2[1])/(point1[0] - point2[0])    # 中线斜率
    y1 = point1[1] + (width1 / 2) * math.sqrt(k1 * k1 + 1)   # y1,y2为靠近点point1的两点的纵坐标
    y2 = point1[1] - (width1 / 2) * math.sqrt(k1 * k1 + 1)
    x1 = point1[0] + k1 * (point1[1] - y1)  # x1,x2为靠近点point1的两点的横坐标
    x2 = point1[0] + k1 * (point1[1] - y2)

    y3 = point2[1] + (width2 / 2) * math.sqrt(k1 * k1 + 1)   # y3,y4为靠近点point2的两点的纵坐标
    y4 = point2[1] - (width2 / 2) * math.sqrt(k1 * k1 + 1)
    x3 = point2[0] + k1 * (point1[1] - y3)  # x3,x4为靠近点point1的两点的横坐标
    x4 = point2[0] + k1 * (point1[1] - y4)
    return [[x1, y1], [x2, y2], [x4, y4], [x3, y3], [x1, y1]]


print(midpoint2vertex([310.2890990851447, 81.12588237598538], [311.02443614508957, 89.58981640730053], 0.6, 0.6))
