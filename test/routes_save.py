import webbrowser
import folium
import pandas as pd
from sqlalchemy import create_engine

# 初始化数据库连接，使用pymysql模块
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/flask?charset=utf8")
location_route = []  # 作业路径点的坐标
sql2 = '''select latitude, longtitude, operate_mode from routes'''  # 查询作业路径的纬度，经度和 operatemode 的sql语句
df_route = pd.read_sql_query(sql2, engine)
df_route[['latitude']] = df_route[['latitude']].astype(float)
df_route[['longtitude']] = df_route[['longtitude']].astype(float)
df_route[['operate_mode']] = df_route[['operate_mode']].astype(int)

latitude_list = df_route['latitude'].values
longtitude_list = df_route['longtitude'].values
operate_mode_list = df_route['operate_mode'].values


for i in range(len(latitude_list)):
    location_route.append([latitude_list[i], longtitude_list[i], operate_mode_list[i]])
print(location_route)
print(len(location_route))
location_Mid = [39.53185896666667, 116.289751905]
# 中心区域的确定
m = folium.Map(
    location=location_Mid,
    max_zoom=20,
    zoom_start=17,
    tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
    attr='default',
    control_scale=True
)

for i in range(len(location_route)):
    if i + 1 == len(location_route):  # 最后一个点
        break
    else:
        location_i = [[location_route[i][0], location_route[i][1]],
                      [location_route[i + 1][0], location_route[i + 1][1]]]
    if location_route[i][2] == 1:  # 作业路径
        route = folium.PolyLine(  # polyline方法为将坐标用线段形式连接起来
            location_i,  # 将坐标点连接起来
            weight=2,  # 线的大小为2
            color='red',  # 线的颜色为红色
            opacity=0.5  # 线的透明度
        ).add_to(m)  # 将这条线添加到刚才的区域m内
    else:  # 经过但不作业路径
        route = folium.PolyLine(  # polyline方法为将坐标用线段形式连接起来
            location_i,  # 将坐标点连接起来
            weight=2,  # 线的大小为2
            color='blue',  # 线的颜色为蓝色
            opacity=0.5  # 线的透明度
        ).add_to(m)  # 将这条线添加到刚才的区域m内

m.save('f2.html')
webbrowser.open('f2.html')
