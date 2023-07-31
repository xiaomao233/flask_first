import functions as F
import numpy as np


def give_func(func=F.runge, beg=-5, end=5, segments=10):
    if func == F.runge:
        print("warning: No function input! So we use the default function Runge Function\n")

    interval = 1.0 * (end - beg) / segments
    x_init4 = np.arange(beg, end + 0.0001, interval)
    res = F.solution_of_equation('give_func', F.spline3_Parameters(x_init4), x_init4, y=0, func=func)
    x_axis4 = []
    y_axis4 = []
    xnd = []
    ynd = []
    for i in range(segments):
        temp = np.arange(beg + i * interval, beg + (i + 1) * interval, 0.01)
        xid = beg + i * interval
        xnd = np.append(xnd, xid)
        ynd = np.append(ynd, F.calculate([res[4 * i], res[1 + 4 * i], res[2 + 4 * i], res[3 + 4 * i]], np.array([xid])))
        x_axis4 = np.append(x_axis4, temp)
        y_axis4 = np.append(y_axis4, F.calculate([res[4 * i], res[1 + 4 * i], res[2 + 4 * i], res[3 + 4 * i]], temp))

    i = segments - 1
    xid = beg + (i + 1) * interval
    xnd = np.append(xnd, xid)
    ynd = np.append(ynd, F.calculate([res[4 * i], res[1 + 4 * i], res[2 + 4 * i], res[3 + 4 * i]], np.array([xid])))

    for i in range(len(xnd) - 1):
        print(f"x in [{xnd[i]:.3f}, {xnd[i + 1]:.3f}]: S(x) = {res[4 * i]:.3f}x^3 + {res[1 + 4 * i]:.3f}x^2 + {res[2 + 4 * i]:.3f}x + {res[3 + 4 * i]:.3f}")

    F.draw_pic("give_func", x_axis4, y_axis4, func, xnd, ynd)


def give_nodes(x, y, opt=0, lval=0, rval=0):
    if opt == 0 and (lval != 0 or rval != 0):
        raise ValueError('There should be no parameters of lval and rval by default')
    if opt != 0 and opt != 1 and opt != 0 and opt != 2:
        raise ValueError('opt should be 0 or 1 or 2!')

    if opt == 0:
        res = F.solution_of_equation('give_nodes', F.spline3_Parameters(x), x, y)
    if opt == 1:
        res = F.solution_of_equation('give_nodes', F.spline3_Parameters(x, 1), x, y, opt=1, lval=lval, rval=rval)
    if opt == 2:
        res = F.solution_of_equation('give_nodes', F.spline3_Parameters(x, 2), x, y, opt=2, lval=lval, rval=rval)

    for i in range(len(x) - 1):
        print(f"x in [{x[i]:.3f}, {x[i + 1]:.3f}]: S(x) = {res[4 * i]:.3f}x^3 + {res[1 + 4 * i]:.3f}x^2 + {res[2 + 4 * i]:.3f}x + {res[3 + 4 * i]:.3f}")

    x_axis4 = []
    y_axis4 = []
    for i in range(len(x) - 1):
        temp = np.arange(x[i], x[i + 1], 0.01)
        x_axis4 = np.append(x_axis4, temp)
        y_axis4 = np.append(y_axis4, F.calculate([res[4 * i], res[1 + 4 * i], res[2 + 4 * i], res[3 + 4 * i]], temp))
    F.draw_pic("give_nodes", x_axis4, y_axis4, func=None, xnd=x, ynd=y)

