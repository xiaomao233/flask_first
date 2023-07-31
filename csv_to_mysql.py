# coding=utf-8
import pymysql
import pandas as pd


file_path = "C:\\Users\\lenovo\\Desktop\\学习任务\\URP项目\\农机作业路径地图可视化与修正工具Web开发\\农机作业路径地图可视化与修正工具Web开发\\附件1：部分作业路径示例.csv"

table_name = "kand"
try:
    con = pymysql.connect(user="root",
                          passwd="123456",
                          db="test",
                          host="localhost",
                          local_infile=1)
    con.set_charset('utf8')
    cur = con.cursor()
    cur.execute("set names utf8")
    cur.execute("SET character_set_connection=utf8;")

    with open(file_path, 'r', encoding='utf8') as f:
        reader = f.readline()
        print(reader)
        # 做成列表
        devide = reader.split(',')
        # 去除最后的换行符
        devide[-1] = devide[-1].rstrip('\n')
        print(devide)

    column = ''
    for dd in devide:
        # 如果标题过长，只能存成text格式
        if dd == "标题":
            column = column + dd + ' TEXT,'
        else:
            column = column + dd + ' varchar(255),'

    # 去除最后一个多余的，
    col = column.rstrip(',')
    # print(column[:-1])

    create_table_sql = 'create table if not exists {} ({}) DEFAULT CHARSET=utf8'.format(table_name, col)
    print(create_table_sql)
    data = 'LOAD DATA LOCAL INFILE \'' + file_path + '\'REPLACE INTO TABLE ' + table_name + \
           ' CHARACTER SET UTF8 FIELDS TERMINATED BY \',' \
           '\' ENCLOSED BY \'\"\' LINES TERMINATED BY \'\n\' IGNORE 1 LINES;'
    cur.execute(create_table_sql)
    cur.execute(data.encode('utf8'))
    print(cur.rowcount)
    con.commit()
except:
    print("发生错误")
    con.rollback()

finally:
    cur.close()
    con.close()
