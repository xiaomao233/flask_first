class CircleStop:
    def __init__(self, num, point, radius):
        self.num = num
        self.point = point
        self.radius = radius / 10

    def show(self):
        print(self.num, self.point, self.radius)
