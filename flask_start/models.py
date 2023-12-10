# 模型
from datetime import datetime
from exis import db


# 数据库IO操作
class UserModel(db.Model):
    # 用户账号密码
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)


class EmailCaptchaModel(db.Model):
    # 邮箱和验证码
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False)
    captcha = db.Column(db.String(20), nullable=False)


class PublishingWork(db.Model):
    # 首页作品展示
    __tablename__ = 'publishing'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(500), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_name = db.Column(db.String(50), nullable=False)
    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="publishing")
