# 解决寻循环引用
# 插件对象
from flask_sqlalchemy import SQLAlchemy
# 邮箱
from flask_mail import Mail
from flask_redis import FlaskRedis
db = SQLAlchemy()
mail = Mail()
redis_client = FlaskRedis()

