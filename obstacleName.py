import pandas as pd
# 障碍物文件说明：
# 点命名方式：“AA B C DD E”
# AA：障碍物序号
# B：障碍物类型，O-点障碍物；L-线障碍物
# C：点序号
# DD：点尺寸，点障碍物为半径，线障碍物为宽度，单位：分米
# E：可通过性，Y-可通过；N-不可通过

# 翻译障碍物名称，将数据存入df_name中
n = []
AA = []
B = []
C = []
DD = []
E = []
i_list = []


def obstacleName(name):
    for i in name:
        s = i.split(' ')
        AA.append(s[0])
        B.append(s[1])
        C.append(int(s[2]))
        DD.append(float(s[3]))
        E.append(s[4])
        i_list.append(s)
    # print(i_list)
    # print(AA, B, C, DD, E)
    df_name = pd.DataFrame({'AA': AA, 'B': B, 'C': C, 'DD': DD, 'E': E}, pd.Index(range(len(i_list))))
    return df_name


