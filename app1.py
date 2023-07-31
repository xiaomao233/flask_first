# encoding: utf-8
import os
import sys
import csv
import json

from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

# from upload import csv2json, gen_name
from config import *
from forms import UploadFileForm
import models as md


# 创建Flask  ，实例化app


app = Flask(__name__)
app.config.from_object(Config)  # 关联config.py文件进来
db = SQLAlchemy(app)  # 建立数据库的关系映射

bootstrap = Bootstrap(app)  # 应用Bootstrap

#服务器临时文件夹，json保存根目录，分目录名
files_tmp = u'C:\\Users\\lenovo\\Desktop\\学习任务\\URP项目\\files_tmp\\'
json_root = u'C:\\Users\\lenovo\\Desktop\\学习任务\\URP项目\\json\\'
json_name = ['lands_json\\', 'routes_json\\', 'barriers_json\\', 'parameters_json\\']

fieldname = [['id', 'latitude', 'longtitude', 'altitude'],
                 ['id', 'latitude', 'longtitude', 'engine_speed', 'operate_mode'],
                 ['name', 'latitude', 'longtitude', 'altitude'],
                 ['id', 'operating_width', 'turning_radius','total_length', 'total_width']]
filenum = 0

@app.route('/', endpoint='index')
def index():
    title = 'Flask App'
    return render_template('index.html', title=title)

@app.route('/download', endpoint='download')
def download():
    return render_template('download.html')


@app.route('/upload/', endpoint='upload', methods=['GET', 'POST'])
def upload():
    uff = UploadFileForm()
    filenames = []
    if uff.validate_on_submit():
        filenames.append(uff.lands_file.data.filename)
        filenames.append(uff.routes_file.data.filename)
        filenames.append(uff.barriers_file.data.filename)
        filenames.append(uff.parameters_file.data.filename)
        print(filenames)
        print(type(filenames))
        # 获取当前存储的json文件数量
        filenum = len(os.listdir(json_root + json_name[0]))
        print(filenum)
        flash(u'上传成功')

    for file_type in range(len(filenames)):
            csv_path = files_tmp + filenames[file_type]
            print(csv_path)
            if file_type == 0:
                uff.lands_file.data.save(csv_path)
            elif file_type == 1:
                uff.routes_file.data.save(csv_path)
            elif file_type == 2:
                uff.barriers_file.data.save(csv_path)
            elif file_type == 3:
                uff.parameters_file.data.save(csv_path)

            # 调用csv2json，生成标准数据到json文件
            # json_path = json_root + json_name[file_type] + json_partname[file_type] + str(filenum) + '.json'
            # json_path = json_root + json_name[file_type] + gen_name(file_type, filenum)
            # print(json_path)
            # flash(u'正在导入文件数据...')
            # csv2json(json_path, csv_path, file_type)

            # 保存数据到数据库
            with open(csv_path, 'r') as cf:
                # 创建csv读取器
                reader = csv.DictReader(cf, fieldname[file_type])
                # 读掉原来表头
                try:
                    next(reader)
                except StopIteration:
                    sys.exit()

                for row in reader:
                    # 只有农机参数中不涉及经纬度方向问题
                    if file_type != 3:
                        if row['latitude'][-1] == 'N':
                            row['latitude'] = row['latitude'][0:-1]
                        elif row['latitude'][-1] == 'S':
                            row['latitude'] = '-' + row['latitude'][0:-1]

                        if row['longtitude'][-1] == 'E':
                            row['longtitude'] = row['longtitude'][0:-1]
                        elif row['longtitude'][-1] == 'W':
                            row['longtitude'] = '-' + row['longtitude'][0:-1]

                    # 保存到数据库
                    if file_type == 0:
                        data = md.Land(latitude=row['latitude'],
                                       longtitude=row['longtitude'],
                                       altitude=row['altitude'])
                    elif file_type == 1:
                        data = md.Route(latitude=row['latitude'],
                                        longtitude=row['longtitude'],
                                        engine_speed=row['engine_speed'],
                                        operate_mode=row['operate_mode'])
                    elif file_type == 2:
                        data = md.Barrier(name=row['name'],
                                          latitude=row['latitude'],
                                          longtitude=row['longtitude'],
                                          altitude=row['altitude'])
                    elif file_type == 3:
                        data = md.Parameter(operating_width=row['operating_width'],
                                            turning_radius=row['turning_radius'],
                                            total_length=row['total_length'],
                                            total_width=row['total_width'])
                    db.session.add(data)
                    db.session.commit()

    # 节约服务器空间，删除已经生成过json文件的相应csv文件
    for file in os.listdir(files_tmp):
        os.remove(files_tmp + file)

    return render_template('upload.html', form=uff)


@app.route('/my_leaflet')
def my_leaflet():
    return render_template('my_leaflet.html')


@app.route('/test')
def test():
    return render_template('test.html')
# @app.route('/upload_landfile', methods=['GET', 'POST'])
# def upload_landfile():
#     recv_data = request.get_data()
#     print(recv_data)
#     return render_template('index.html')


@app.route('/show_map')
def show_map():
    return render_template('map.html')


@app.route('/user_add')
def user_add():
    u1 = md.User(user_name='zbz', email='zbz@qq.com')
    u2 = md.User(user_name='wzx', email='wzx@qq.com')
    # 添加记录
    db.session.add(u1)
    db.session.add(u2)
    # 必须有提交动作才能执行添加指令，增删改都是最后需要下面的提交命令
    db.session.commit()

    return "OK"


@app.route('/route')
def route():
    route_list = db.session.query(md.Route.latitude, md.Route.longtitude).all()
    # user_list = md.User.query.order_by(md.User.id).all()
    # print(md.User.user_name, md.User.email)
    print(type(route_list))
    print(route_list)

    return render_template("users.html", route_list=route_list)
    # return 'ok'

def routes(routes_tuple):
    routes_list = []
    for i in routes_tuple:
        i = list(i)
        i = list(map(float, i))
        routes_list.append(i)
    return routes_list

@app.route('/routes')
def routes_map():
    routes_tuple = db.session.query(md.Route.latitude, md.Route.longtitude, md.Route.operate_mode).all()
    routes_list = routes(routes_tuple)
    return render_template('routes.html', routes_list_json=json.dumps(routes_list))

@app.route('/curve')
def curve():
    data = [[39.581396912637935, 116.13201141357422],
            [39.626868974000274, 116.24084472656251],
            [39.6107456716115, 116.35620117187501],
            [39.52319146034901, 116.37577056884767],
            [39.48797993746985, 116.23775482177736],
            [39.39824963706614, 116.18316650390626],
            [39.38021664686007, 116.41456604003908]]

    # data2 = [[50.54136296522163, 28.520507812500004],
    #          [52.214338608258224, 28.564453125000004],
    #          [48.45835188280866, 33.57421875000001],
    #          [50.680797145321655, 33.83789062500001],
    #          [47.45839225859763, 31.201171875],
    #          [48.40003249610685, 28.564453125000004]]
    return render_template('curve2.html', data_json=json.dumps(data))



if __name__ == '__main__':
    # 需要写在model.py文件中才生效，且这个只是用于开发过程中的测试之用
    # 删除所有的表
    # db.drop_all()
    # 创建表
    # db.create_all()
    app.run(debug=True)
    bootstrap.run()
