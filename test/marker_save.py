import webbrowser
import folium


# 中心区域的确定
m = folium.Map(
    location=[39.53185896666667, 116.289751905],
    max_zoom=20,
    zoom_start=18,
    tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
    attr='default',
    control_scale=True
)

marker1 = folium.vector_layers.CircleMarker(
    location=[39.53735896666667, 116.284751905],
    tooltip='nice',
    radius=10
).add_to(m)
# Circle_i = folium.vector_layers.Circle(
#         location=[39.53185896666667, 116.289751905],
#         tooltip="你鼠标移动到了这里",
#         radius=1,
#         color="red",
#         fill=True,
#         fill_color="red",
#         fill_opacity=1
#     ).add_to(m)

m.save('circle_marker.html')
webbrowser.open('circle_marker.html')

