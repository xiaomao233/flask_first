from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import config
import json
from lands import *
from routes import *
from barriers import *
from curvature import *
import pandas as pd
from b_spline2 import *

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    # return render_template('curve2.html')
    return 'hello world!'


@app.route('/download', methods=['GET'])
def csv():
    csv_tuple = db.session.query(md.Route.id, md.Route.latitude, md.Route.longtitude, md.Route.engine_speed, md.Route.operate_mode).all()
    # print(csv_tuple)
    # print(type(csv_tuple[0]))
    # csv_list = routes(csv_tuple)
    csv_list = list(csv_tuple)
    # print(csv_list)
    name = ['id', 'latitude', 'longtitude', 'engine_speed', 'operate_mode']
    csv = pd.DataFrame(columns=name, data=csv_list)
    # print(csv)
    # csv.to_csv('F:/Py_code/Pycharm_code/flask/data_full.csv', encoding='gbk')
    csv.to_csv('C:/Users/xiaoyudiaomao/Desktop/data_full.csv', encoding='gbk')
    # return "ok"
    return render_template('curve2.html')


import models as md


@app.route('/lands')
def lands_map():
    lands_tuple = db.session.query(md.Land.latitude, md.Land.longtitude).all()
    location_mid, lands_list = lands(lands_tuple)
    return render_template('lands.html', lands_list_json=json.dumps(lands_list), location_mid_json=json.dumps(location_mid))


@app.route('/routes')
def routes_map():
    routes_tuple = db.session.query(md.Route.latitude, md.Route.longtitude, md.Route.operate_mode).all()
    routes_list = routes(routes_tuple)
    return render_template('routes.html', routes_list_json=json.dumps(routes_list))


@app.route('/barriers')
def barriers_map():
    barriers_tuple = db.session.query(md.Barrier.name, md.Barrier.latitude, md.Barrier.longtitude).all()
    Circle, Line4points = barriers(barriers_tuple)
    return render_template('barriers.html', Circle_json=json.dumps(Circle), Line4points_json=json.dumps(Line4points))


@app.route('/click', methods=['GET', 'POST'])
def click():
    data = request.get_json()
    print(data)
    return render_template('click_get_location.html')


@app.route('/marker')
def test():
    return render_template('circle_marker.html')


@app.route('/polyline')
def polyline():
    return render_template('polyline.html')


@app.route('/curve2')
def curve2():
    return render_template('curve2.html')


@app.route('/curve', methods=['GET', 'POST'])
def curve():
    points = request.get_json()
    R = 1000
    if points != None:
        for i in points:
            i[0], i[1] = BL2UTM(i[0], i[1])
        print(points)
        for i in range(1001):
            t = i / 1000
            r = curvature(t, points[0], points[1], points[2], points[3])
            if r < R:
                R = r
        turningR = db.session.query(md.Parameter.turning_radius).all()
        print(turningR)
        print(type(turningR))
        tR = 10
        print(R)
        if R >= tR:
            m = 1
            print(m)
        else:
            m = 0
            print(m)
    return json.dumps(m)


@app.route('/bspline', methods=['GET', 'POST'])
def bspline():
    data = request.get_json()
    starting = data[0]
    ending = data[8]
    print((starting, ending))
    # if data != None:
    for i in data:
        i[0], i[1] = BL2UTM(i[0], i[1])
    data = B_spline(data)

    for i in data:
        i[0], i[1] = UTM2BL(i[0], i[1])
    del(data[0])
    print(data)
    # data.insert(0, starting)
    return json.dumps(data)


@app.route('/spline_curve')
def spline_curve():
    return render_template('spline_curve.html')


@app.route('/save')
def save():
    p = [[21, 12, 1, 1], [21, 12, 1, 1]]
    db.session.query(md.Route).delete()
    db.session.commit()
    j = 0
    for i in p:
        data = md.Route(
            id=j,
            latitude=i[0],
            longtitude=i[1],
            engine_speed=i[2],
            operate_mode=i[3]
        )
        db.session.add(data)
        db.session.commit()
        j = j + 1
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
