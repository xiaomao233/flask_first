import webbrowser
import folium
from sqlalchemy import create_engine
from obstacleName import *
from LineStop import *


# 初始化数据库连接，使用pymysql模块
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/flask?charset=utf8")

# 对于L型障碍物，已知的坐标（经纬度坐标）是短边中点的坐标和L型障碍物宽度（单位：分米）
# 定义一个函数，midpoint2vertex(point1, point2, width1, width2)
# 通过已知的两个中点的坐标（纬度，经度）和对应的宽度（分米），求出L型障碍物4个顶点的坐标（纬度，经度）
sql3 = '''select name, latitude, longtitude from barriers'''  # 查询障碍物的名字，点的纬度，经度
df_stop = pd.read_sql_query(sql3, engine)
# print(df_stop)
stop_name = df_stop['name'].values  # 将dataframe数据转换为list
# print(stop_name)
# print(type(stop_name))
df_name = obstacleName(stop_name)   # 对障碍物名进行切割提取障碍物数据

# 将df_stop中的'B'和'L'两列中的数据转化为float型
df_stop[['latitude']] = df_stop[['latitude']].astype(float)
df_stop[['longtitude']] = df_stop[['longtitude']].astype(float)

# 将障碍物的位置信息（纬度，经度）整合至表中
df_name['lat'] = df_stop['latitude']
df_name['lon'] = df_stop['longtitude']
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
    location=[39.53185896666667, 116.289751905],
    max_zoom=20,
    zoom_start=17,
    tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
    attr='default',
    control_scale=True
)

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
