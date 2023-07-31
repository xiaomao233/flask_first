import spline as sp

# 接口函数一：give_func(func = function, beg = -5, end = 5, segments = 10)
# 函数意义：对给定的函数，在 [beg, end] 范围内进行拟合，共 segments 段（即 segments+1 个点）
# 参数意义：func表示需要拟合的函数，默认为龙格函数；
#         beg、end表示插值的范围，segments表示插值的数量。默认值写在上面。

sp.give_func()
sp.give_func(beg=-5, end=5, segments=6)


def f(x):
    return (x * x * x + 6 * x * x + 7 * x + 1) / (x * x + 1)


sp.give_func(f, -4, 4, 8)

# 接口函数二：give_nodes(x, y, opt = 0, lval = 0, rval = 0)
# 函数意义：对于给定的点集进行插值
# 参数意义：x,y 表示点集的坐标；
# opt表示边界条件的处理：
# opt = 0 表示默认边界条件，not-a-knot边界条件：左边两端点三阶导相等，右边两端点三阶导也相等
# opt = 1 或 opt = 2，表示给定左右两端点的一阶导值 / 二阶导值

x = [27.7, 28, 29, 30]
y = [4.1, 4.3, 4.1, 3.0]
sp.give_nodes(x, y)
sp.give_nodes(x, y, opt=1, lval=3.0, rval=-4.0)
sp.give_nodes(x, y, opt=2, lval=27.0, rval=-34.0)
