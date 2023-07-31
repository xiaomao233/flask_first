from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pandas as pd

'''配置数据库'''
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
# 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上创建的数据库名,连接方式参考 \

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flask?charset=utf8'
# 设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy()
sql1 = '''select * from land'''
df = pd.read_sql_query(sql1, db)
print(df)