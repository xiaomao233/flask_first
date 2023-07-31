document.write("< script language = javascript src = 'math.min.js'>< / script>");
// function runge(y){
//     y = parseFloat(y);
//     return 1 / (1 + y * y);
// }

function spline3_Parameters(x_vec, opt=0){
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
    if(opt === 0){
        //data = new Array(size_of_Interval * 4).fill(0);
        let data = math.zeros(size_of_Interval * 4);
        data[0] = 6;
        data[4] = -6;
        parameter.push(data);
        //data = np.zeros(size_of_Interval * 4);
        data = math.zeros(size_of_Interval * 4);
        data[-4] = 6;
        data[-8] = -6;
        parameter.push(data);
    }

    //opt = 1，给定左右两端点的一阶导值
    if(opt === 1){
        //data = new Array(size_of_Interval * 4).fill(0);
        let data = math.zeros(size_of_Interval * 4);
        data[0] = 3 * x_new[0] * x_new[0];
        data[1] = 2 * x_new[0];
        data[2] = 1;
        parameter.push(data);
        //data = new Array(size_of_Interval * 4).fill(0);
        data = math.zeros(size_of_Interval * 4);
        data[-4] = 3 * x_new[x_new.length - 1] * x_new[x_new.length - 1];
        data[-3] = 2 * x_new[x_new.length - 1];
        data[-2] = 1;
        parameter.push(data);
    }

    //opt = 2，给定左右两端点的二阶导值
    if(opt === 2){
        //data = new Array(size_of_Interval * 4).fill(0);
        let data = math.zeros(size_of_Interval * 4);
        data[0] = 6 * x_new[0];
        data[1] = 2;
        parameter.push(data);
        //data = new Array(size_of_Interval * 4).fill(0);
        data = math.zeros(size_of_Interval * 4);
        data[-4] = 6 * x_new[x_new.length - 1];
        data[-3] = 2;
        parameter.push(data);
    }
    return parameter
}


function solution_of_equation(functype, parametes, x, y=0, func=runge, opt=0, lval=0, rval=0){
    //建立三对角线性方程组并求解，得到各段三次函数的系数并返回
    //functype 表示需要拟合的是给定函数 / 给定点集
    let size_of_Interval = x.length - 1;
    //let result = new Array(size_of_Interval * 4).fill(0);
    let result = math.zeros(size_of_Interval * 4);
    let i = 1;
    if(functype !== 'give_func' && functype !== 'give_nodes'){
    //     raise ValueError("functype should be 'give_func' or 'give_nodes' ")
        throw {Error:"functype should be 'give_func' or 'give_nodes'"};
    }

    if(functype === 'give_func'){
        while(i < size_of_Interval) {
            result[(i - 1) * 2] = func(x[i]);
            result[(i - 1) * 2 + 1] = func(x[i]);
            i += 1;
        }
        result[(size_of_Interval - 1) * 2] = func(x[0]);
        result[(size_of_Interval - 1) * 2 + 1] = func(x[x.length - 1]);
    }

    if(functype === 'give_nodes'){
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
    }
    //默认情况：opt = 0，not-a-knot边界条件：左边两端点三阶导相等，右边两端点三阶导也相等
    if(opt === 0)
        result[result.length-2] = result[result.length-1] = 0;
    //opt = 1 或 opt = 2，给定左右两端点的一阶导值 / 二阶导值
    if(opt === 1 || opt === 2){
        result[result.length-2] = lval;
        result[result.length-1] = rval;
    }
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


//  画线函数 待研究
// def draw_pic(functype, x, y, func=runge, xnd=0, ynd=0):
//     fig = plt.figure()
//     plt.plot(x, y, label='interpolation')
//     if functype == 'give_func':
//         plt.plot(x, func(x), label='raw')
//     l = len(xnd)
//     for i in range(0, l):
//         plt.plot(xnd[i], ynd[i], 'bo')
//     plt.legend()
//     plt.show()
//     plt.close(fig)