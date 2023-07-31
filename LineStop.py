import math
from proj import *


class LineStop():
    def __init__(self, num, point1, point2, width1, width2):
        self.num = num
        self.point1 = BL2UTM(point1[0], point1[1])
        self.point2 = BL2UTM(point2[0], point2[1])
        self.width1 = width1 / 10
        self.width2 = width2 / 10

    def show(self):
        print(self.num, self.point1, self.point2, self.width1, self.width2)

    def midpoint2vertex(self):  # point1,point2为已知两个中点的UTM坐标，width1,width2为对应的宽度
        k1 = (self.point1[1] - self.point2[1]) / (self.point1[0] - self.point2[0])  # 中线斜率
        y1 = self.point1[1] + (self.width1 / 2) * math.sqrt(k1 * k1 + 1)  # y1,y2为靠近点point1的两点的纵坐标
        y2 = self.point1[1] - (self.width1 / 2) * math.sqrt(k1 * k1 + 1)
        x1 = self.point1[0] + k1 * (self.point1[1] - y1)  # x1,x2为靠近点point1的两点的横坐标
        x2 = self.point1[0] + k1 * (self.point1[1] - y2)

        y3 = self.point2[1] + (self.width2 / 2) * math.sqrt(k1 * k1 + 1)  # y3,y4为靠近点point2的两点的纵坐标
        y4 = self.point2[1] - (self.width2 / 2) * math.sqrt(k1 * k1 + 1)
        x3 = self.point2[0] + k1 * (self.point1[1] - y3)  # x3,x4为靠近点point1的两点的横坐标
        x4 = self.point2[0] + k1 * (self.point1[1] - y4)

        x1, y1 = UTM2BL(x1, y1)
        x2, y2 = UTM2BL(x2, y2)
        x3, y3 = UTM2BL(x3, y3)
        x4, y4 = UTM2BL(x4, y4)
        return [[x1, y1], [x2, y2], [x4, y4], [x3, y3], [x1, y1]]


