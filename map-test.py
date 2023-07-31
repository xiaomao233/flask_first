import webbrowser
import folium
from sqlalchemy import create_engine
from obstacleName import *
from LineStop import *
from CircleStop import *

# 初始化数据库连接，使用pymysql模块
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/flask?charset=utf8")

# B :纬度； L : 经度
sql1 = '''select B, L from land'''  # 查询地块纬度，经度 sql语句
df_land = pd.read_sql_query(sql1, engine)  # 用pandas中的dataframe
df_land[['B']] = df_land[['B']].astype(float)
df_land[['L']] = df_land[['L']].astype(float)
land_list = df_land.values  # 将dataframe转换成list

location_land = []  # 地块轮廓点的坐标
location_sumMid = [0, 0]
for i in land_list:
    location_land.append([i[0], i[1]])  # 将list中str型数据转换成float型
location_land.append(location_land[0])  # 往地块list中末尾再加入第一个点，画出封闭的多边形

for i in range(len(location_land)):  # 取地块轮廓坐标取平均值作为地图中心区域
    location_sumMid = [location_sumMid[0] + location_land[i][0], location_sumMid[1] + location_land[i][1]]
location_Mid = [location_sumMid[0] / len(location_land), location_sumMid[1] / len(location_land)]  # 取地图中心点的坐标
# print(location_Mid)

location_route = []  # 作业路径点的坐标
sql2 = '''select B, L, operatemode from route'''  # 查询作业路径的纬度，经度和 operatemode 的sql语句
df_route = pd.read_sql_query(sql2, engine)
df_route[['B']] = df_route[['B']].astype(float)
df_route[['L']] = df_route[['L']].astype(float)
df_route[['operatemode']] = df_route[['operatemode']].astype(int)
route_list = df_route.values
for i in route_list:
    location_route.append([i[0], i[1], i[2]])

# 对于L型障碍物，已知的坐标（经纬度坐标）是短边中点的坐标和L型障碍物宽度（单位：分米）
# 定义一个函数，midpoint2vertex(point1, point2, width1, width2)
# 通过已知的两个中点的坐标（纬度，经度）和对应的宽度（分米），求出L型障碍物4个顶点的坐标（纬度，经度）
sql3 = '''select name, B, L from stop'''  # 查询障碍物的名字，点的纬度，经度
df_stop = pd.read_sql_query(sql3, engine)
# print(df_stop)
stop_name = df_stop['name'].values  # 将dataframe数据转换为list
# print(stop_name)
# print(type(stop_name))
df_name = obstacleName(stop_name)   # 对障碍物名进行切割提取障碍物数据

# 将df_stop中的'B'和'L'两列中的数据转化为float型
df_stop[['B']] = df_stop[['B']].astype(float)
df_stop[['L']] = df_stop[['L']].astype(float)

# 将障碍物的位置信息（纬度，经度）整合至表中
df_name['lat'] = df_stop['B']
df_name['lon'] = df_stop['L']
# print(df_name)
stop_list = df_name.values  # 将整合的表格转换为list
# print(stop_list)
Line = []   # 存放L型障碍物类
Circle = []     # 存放O型障碍物
for i in range(len(stop_list)):     # i是行号
    # print(i)
    if stop_list[i][1] == 'L':  # 第i行的'B'是'L'，表示是L型障碍物
        for j in range(i+1, len(stop_list)):    # 从i+1行开始查找
            # print(j)
            if stop_list[i][0] == stop_list[j][0]:  # 根据同一个障碍物的'AA'相同找到L型障碍物的第二个点
                Line.append(LineStop(stop_list[i][0],   # num即'AA'
                                     [stop_list[i][5], stop_list[i][6]],    # 第一个点的纬度，经度坐标
                                     [stop_list[j][5], stop_list[j][6]],    # 第二个点的纬度，经度坐标
                                     stop_list[i][3],   # 靠近第一个点的宽度
                                     stop_list[j][3]   # 靠近第二个点的宽度
                                     )
                            )
    if stop_list[i][1] == 'O':
        Circle.append(CircleStop(stop_list[i][0],
                      [stop_list[i][5], stop_list[i][6]],
                      stop_list[i][3]
                      ))

# for i in Line:
#     i.show()    # 输出Line的内容
Line4points = []
for i in Line:
    # print(i)
    # 调用LineStop类中midpoint2vertex方法，将得到的障碍物地理坐标序列存入Line4points中
    Line4points.append(i.midpoint2vertex())
# print(Line4points)

# 中心区域的确定
m = folium.Map(
    location=location_Mid,
    max_zoom=20,
    zoom_start=17,
    tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
    attr='default',
    control_scale=True
)

# 点击地图时，会显示一个弹出窗口，显示指针的纬度和经度
m.add_child(folium.LatLngPopup())

# 标记
# marker1 = folium.Marker(
#         location=[39.53132948, 116.29095327],
#         tooltip="Click here"
#     ).add_to(m)
#
# marker2 = folium.Marker(
#         location=[39.53264140, 116.29093034],
#         tooltip="Click here",
#         icon=folium.Icon(color='green')
#     ).add_to(m)

land = folium.PolyLine(  # polyline方法为将坐标用线段形式连接起来
    location_land,  # 将坐标点连接起来
    weight=3,  # 线的大小为3
    color='orange',  # 线的颜色为橙色
    opacity=0.8  # 线的透明度
).add_to(m)  # 将这条线添加到刚才的区域m内

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

# 画障碍物
for i in Circle:
    Circle_i = folium.vector_layers.Circle(
        location=i.point,
        tooltip="O-点障碍物",
        radius=i.radius,
        color="green",
        fill=True,
        fill_color="green",
        fill_opacity=1
    ).add_to(m)

for i in Line4points:
    LL = folium.PolyLine(
        i,
        tooltip="L-线障碍物",
        weight=3,  # 线的大小为3
        color='orange',  # 线的颜色为红色
        opacity=1,  # 线的透明度
        fill=True,
        fill_color="yellow",
        fill_opacity=0.5
    ).add_to(m)
m.save('f2.html')
webbrowser.open('f2.html')
