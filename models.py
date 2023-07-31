from app import db

# 声明模型类--land


class Land(db.Model):
    # 定义表名
    __tablename__ = 'lands'
    # db.Column表示一个字段
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(20), nullable=False)
    longtitude = db.Column(db.String(20), nullable=False)
    altitude = db.Column(db.String(20), nullable=False)

    # 显示属性
    def __repr__(self):
        return '<land: %s %s %s %s>' % (self.id,  self.latitude, self.longtitude, self.altitude)


# 声明模型类--barrier
class Barrier(db.Model):
    __tablename__ = 'barriers'
    name = db.Column(db.String(20), primary_key=True)
    latitude = db.Column(db.String(20), nullable=False)
    longtitude = db.Column(db.String(20), nullable=False)
    altitude = db.Column(db.String(20), nullable=False)

    # 显示属性
    def __repr__(self):
        return '<barrier %s %s %s %s>' % (self.id, self.latitude, self.longtitude, self.altitude)


# 声明模型类--parameter
class Parameter(db.Model):
    __tablename__ = 'parameters'
    id = db.Column(db.Integer, primary_key=True)
    operating_width = db.Column(db.String(20), nullable=False)
    turning_radius = db.Column(db.String(20), nullable=False)
    total_length = db.Column(db.String(20), nullable=False)
    total_width = db.Column(db.String(20), nullable=False)

    # 显示属性
    def __repr__(self):
        return '<parameter %s %s %s %s %s>' % (self.id, self.operating_width, self.turning_radius, self.total_length)


# 声明模型类--route
class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(20), nullable=False)
    longtitude = db.Column(db.String(20), nullable=False)
    engine_speed = db.Column(db.String(20), nullable=False)
    operate_mode = db.Column(db.String(20), nullable=False)

    # 显示属性
    def __repr__(self):
        return '<route %s %s %s %s %s>' % (self.id, self.latitude, self.longtitude, self.engine_speed, self.operate_mode)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# db.drop_all()
# db.create_all()
