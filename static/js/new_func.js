document.write("< script language = javascript src = 'math.min.js'>< / script>");
function runge(y){
    y = parseFloat(y);
    return 1 / (1 + y * y);
}

function spline3_Parameters(x_vec){
    //建立三对角矩阵的 4n 个方程的左边部分
    //parameter为二维数组，用来存放参数，size_of_Interval为区间的个数
    let x_new = [].concat(x_vec);
    //let x_new = math.clone(x_vec);
    let parameter = [];
    let size_of_Interval = x_new.length - 1;
    let i = 1;
    // 相邻两区间公共节点处函数值相等的方程，共2n-2个
    while (i < x_new.length - 1){
        let data = math.zeros(size_of_Interval * 4);
        //let data = new Array(size_of_Interval * 4).fill(0);
        data[(i - 1) * 4] = x_new[i] * x_new[i] * x_new[i];
        data[(i - 1) * 4 + 1] = x_new[i] * x_new[i];
        data[(i - 1) * 4 + 2] = x_new[i];
        data[(i - 1) * 4 + 3] = 1;
        parameter.push(data);

        //data = new Array(size_of_Interval * 4).fill(0);
        data = math.zeros(size_of_Interval * 4);
        data[i * 4] = x_new[i] * x_new[i] * x_new[i];
        data[i * 4 + 1] = x_new[i] * x_new[i];
        data[i * 4 + 2] = x_new[i];
        data[i * 4 + 3] = 1;
        parameter.push(data);
        i += 1;
    }
    // 左右端点处的函数值。为两个方程, 加上前面的2n-2个方程，一共2n个方程
    //let data = new Array(size_of_Interval * 4).fill(0);
    let data = math.zeros(size_of_Interval * 4);
    data[0] = x_new[0] * x_new[0] * x_new[0];
    data[1] = x_new[0] * x_new[0];
    data[2] = x_new[0];
    data[3] = 1;
    parameter.push(data);
    //data = new Array(size_of_Interval * 4).fill(0);
    data = math.zeros(size_of_Interval * 4);
    data[(size_of_Interval - 1) * 4] = x_new[x_new.length - 1] * x_new[x_new.length - 1] * x_new[x_new.length - 1];
    data[(size_of_Interval - 1) * 4 + 1] = x_new[x_new.length - 1] * x_new[x_new.length - 1];
    data[(size_of_Interval - 1) * 4 + 2] = x_new[x_new.length - 1];
    data[(size_of_Interval - 1) * 4 + 3] = 1;
    parameter.push(data);
    //端点函数一阶导数值相等为n-1个方程。加上前面的方程为3n-1个方程。
    i = 1;
    while(i < size_of_Interval)
    {
        //data = new Array(size_of_Interval * 4).fill(0);
        let data = math.zeros(size_of_Interval * 4);
        data[(i - 1) * 4] = 3 * x_new[i] * x_new[i];
        data[(i - 1) * 4 + 1] = 2 * x_new[i];
        data[(i - 1) * 4 + 2] = 1;
        data[i * 4] = -3 * x_new[i] * x_new[i];
        data[i * 4 + 1] = -2 * x_new[i];
        data[i * 4 + 2] = -1;
        parameter.push(data);
        i += 1
    }
    i = 1;
    while(i < x_new.length - 1){
        //data = new Array(size_of_Interval * 4).fill(0);
        let data = math.zeros(size_of_Interval * 4);
        data[(i - 1) * 4] = 6 * x_new[i];
        data[(i - 1) * 4 + 1] = 2;
        data[i * 4] = -6 * x_new[i];
        data[i * 4 + 1] = -2;
        parameter.push(data);
        i += 1
    }
    //两个附加条件
    //默认情况：opt = 0，not-a-knot边界条件：左边两端点三阶导相等，右边两端点三阶导也相等
    //data = new Array(size_of_Interval * 4).fill(0);
    data = math.zeros(size_of_Interval * 4);
    data[0] = 6;
    data[4] = -6;
    parameter.push(data);
    //data = np.zeros(size_of_Interval * 4);
    data = math.zeros(size_of_Interval * 4);
    data[-4] = 6;
    data[-8] = -6;
    parameter.push(data);

    return parameter
}


function solution_of_equation(parametes, x, y=0){
    //建立三对角线性方程组并求解，得到各段三次函数的系数并返回
    //functype 表示需要拟合的是给定函数 / 给定点集
    let size_of_Interval = x.length - 1;
    //let result = new Array(size_of_Interval * 4).fill(0);
    let result = math.zeros(size_of_Interval * 4);
    let i = 1;

    if(x.length !== y.length){
        throw {Error:"Expect a node set!"}
        //     raise ValueError("Expect a node set!");
    }
    while(i < size_of_Interval){
        result[(i - 1) * 2] = y[i];
        result[(i - 1) * 2 + 1] = y[i];
        i += 1;
    }
    result[(size_of_Interval - 1) * 2] = y[0];
    result[(size_of_Interval - 1) * 2 + 1] = y[y.length-1];

    //默认情况：opt = 0，not-a-knot边界条件：左边两端点三阶导相等，右边两端点三阶导也相等
    result[result.length-2] = result[result.length-1] = 0;

    let a = [].concat(parametes);
    let b = [].concat(result);
//    return np.linalg.solve(a, b)
    return math.lsolve(a,b);
}

function calculate(paremeters, x){
    //计算x在拟合得到的函数中的点值
    let res = [];
    for(let dx in x)
        res.push(paremeters[0] * dx * dx * dx + paremeters[1] * dx * dx + paremeters[2] * dx + paremeters[3]);
    return res
}

function give_nodes(x, y, lval=0, rval=0){
    let res = solution_of_equation(spline3_Parameters(x), x, y);
    //for i in range(len(x) - 1):
    //    print(f"x in [{x[i]:.3f}, {x[i + 1]:.3f}]: S(x) = {res[4 * i]:.3f}x^3 + {res[1 + 4 * i]:.3f}x^2 + {res[2 + 4 * i]:.3f}x + {res[3 + 4 * i]:.3f}");
    var x_axis4 = [];
    var y_axis4 = [];
    for(let i in range(x.length - 1)){
        let temp = math.range(x[i], x[i + 1], 0.01);
        x_axis4 = x_axis4.push.apply(temp);
        y_axis4 = y_axis4.push.apply(calculate([res[4 * i], res[1 + 4 * i], res[2 + 4 * i], res[3 + 4 * i]], temp))
    }

    //functions.draw_pic("give_nodes", x_axis4, y_axis4, func=None, xnd=x, ynd=y)
}