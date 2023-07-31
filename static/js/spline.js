document.write("< script language = javascript src = 'functions.js'>< / script>");

function give_func(func=functions.runge,beg=-5, end=5, segments=10){
    if(func === functions.runge)
        throw {Warning:"No function input! So we use the default function Runge Function\n"};
    let interval = (end - beg) / segments;
    let x_init4 = math.range(beg, end + 0.0001, interval);
    let y;
    let res = functions.solution_of_equation('give_func', functions.spline3_Parameters(x_init4), x_init4, y = 0, func = func);
    let x_axis4 = [];
    let y_axis4 = [];
    let xnd = [];
    let ynd = [];
    for(let i in segments){
        let temp = math.range(beg + i * interval, beg + (i + 1) * interval, 0.01);
        let xid = beg + i * interval;
        //xnd = xnd.concat(xid);
        xnd = xnd.push.apply(xid);
        ynd = ynd.push.apply(functions.calculate([res[4 * i], res[1 + 4 * i], res[2 + 4 * i], res[3 + 4 * i]], np.array([xid])));
        x_axis4 = x_axis4.push.apply(temp);
        y_axis4 = y_axis4.push.apply(functions.calculate([res[4 * i], res[1 + 4 * i], res[2 + 4 * i], res[3 + 4 * i]], temp));
    }
    i = segments - 1;
    let xid = beg + (i + 1) * interval;
    xnd = xnd.push.apply(xid);
    ynd = ynd.push.apply(functions.calculate([res[4 * i], res[1 + 4 * i], res[2 + 4 * i], res[3 + 4 * i]], np.array([xid])));

    //for(let i in range(xnd.length - 1))
    //    print(f"x in [{xnd[i]:.3f}, {xnd[i + 1]:.3f}]: S(x) = {res[4 * i]:.3f}x^3 + {res[1 + 4 * i]:.3f}x^2 + {res[2 + 4 * i]:.3f}x + {res[3 + 4 * i]:.3f}")

    //functions.draw_pic("give_func", x_axis4, y_axis4, func, xnd, ynd)
}


function give_nodes(x, y, opt=0, lval=0, rval=0){
    if(opt === 0 && (lval !== 0 || rval !== 0))
        throw {Error:"There should be no parameters of lval and rval by default"};
    if(opt !== 0 && opt !== 1 && opt !== 2)
        throw {Error:"opt should be 0 or 1 or 2!"};
    if(opt === 0)
        let res = functions.solution_of_equation('give_nodes', functions.spline3_Parameters(x), x, y);
    if(opt === 1)
        let res = functions.solution_of_equation('give_nodes', functions.spline3_Parameters(x, 1), x, y, opt=1, lval=lval, rval=rval);
    if(opt === 2)
        let res = functions.solution_of_equation('give_nodes', functions.spline3_Parameters(x, 2), x, y, opt=2, lval=lval, rval=rval);

    //for i in range(len(x) - 1):
    //    print(f"x in [{x[i]:.3f}, {x[i + 1]:.3f}]: S(x) = {res[4 * i]:.3f}x^3 + {res[1 + 4 * i]:.3f}x^2 + {res[2 + 4 * i]:.3f}x + {res[3 + 4 * i]:.3f}");
    var x_axis4 = [];
    var y_axis4 = [];
    for(let i in range(x.length - 1)){
        let temp = math.range(x[i], x[i + 1], 0.01);
        x_axis4 = x_axis4.push.apply(temp);
        y_axis4 = y_axis4.push.apply(functions.calculate([res[4 * i], res[1 + 4 * i], res[2 + 4 * i], res[3 + 4 * i]], temp))
    }

    //functions.draw_pic("give_nodes", x_axis4, y_axis4, func=None, xnd=x, ynd=y)
}

