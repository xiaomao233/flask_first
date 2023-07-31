import webbrowser
import folium
import pandas as pd
from sqlalchemy import create_engine

# 初始化数据库连接，使用pymysql模块
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/flask?charset=utf8")

# B :纬度； L : 经度
sql1 = '''select latitude, longtitude from lands'''  # 查询地块纬度，经度 sql语句
df_land = pd.read_sql_query(sql1, engine)  # 用pandas中的dataframe
df_land[['latitude']] = df_land[['latitude']].astype(float)
df_land[['longtitude']] = df_land[['longtitude']].astype(float)
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

# 中心区域的确定
m = folium.Map(
    location=location_Mid,
    max_zoom=20,
    zoom_start=17,
    tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
    attr='default',
    control_scale=True
)

land = folium.PolyLine(  # polyline方法为将坐标用线段形式连接起来
    location_land,  # 将坐标点连接起来
    weight=3,  # 线的大小为3
    color='orange',  # 线的颜色为橙色
    opacity=0.8  # 线的透明度
).add_to(m)  # 将这条线添加到刚才的区域m内

m.save('f1.html')
webbrowser.open('f1.html')