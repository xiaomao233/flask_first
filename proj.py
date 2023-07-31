from pyproj import Transformer


# epsg:4326是WGS84坐标系，epsg:2415是 UTM区域49N坐标系，详细内容访问http://epsg.io/2415   4527    32650
# B：纬度；L：经度
def BL2UTM(B, L):   # 经纬度转UTM坐标
    transformer = Transformer.from_crs("epsg:4326", "epsg:4527")
    x, y = transformer.transform(B, L)
    # x = x - 954500  # 数据处理，避免数据过大计算困难
    # y = y - 4389000
    return x, y


def UTM2BL(x, y):
    # x = x + 954500  # 还原实际UTM坐标值
    # y = y + 4389000
    transformer = Transformer.from_crs("epsg:4527", "epsg:4326")
    B, L = transformer.transform(x, y)
    return B, L


# print(BL2UTM(39.53090754, 116.2906905))
# print(BL2UTM(39.53098309, 116.2907048))
#
# print(UTM2BL(270.3934307309698, 84.59197312805804))
# print(BL2UTM(39.53088701, 116.29095456))
# print(BL2UTM(39.53132948, 116.29095327))
# print(BL2UTM(39.53264140, 116.29093034))
# print(BL2UTM(39.53264988, 116.29018635))
# print(BL2UTM(39.53277335, 116.28772869))
# print(BL2UTM(39.53087268, 116.28775822))
