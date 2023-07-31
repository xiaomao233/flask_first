def lands(lands_tuple):
    lands_list = []
    for i in lands_tuple:
        i = list(i)  # 将元组转换成列表
        i = list(map(float, i))  # 将str类型转换为float型
        lands_list.append(i)
    location_sum = [0, 0]
    for i in range(len(lands_list)):  # 取地块轮廓坐标取平均值作为地图中心区域
        location_sum = [location_sum[0] + lands_list[i][0], location_sum[1] + lands_list[i][1]]
    location_mid = [location_sum[0] / len(lands_list), location_sum[1] / len(lands_list)]  # 取地图中心点的坐标
    lands_list.append(lands_list[0])
    return location_mid, lands_list
