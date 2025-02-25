import os

# 在app.config中设置好链接信息
# 然后使用SQLAlchemy(APP）创建一个APP对象
# 会自动读取config链接信息
# 阿里云服务器上mysql
HOSTNAME = "47."
POST = "3306"
USERNAME = "e"
PASSEORD = "5"
DATABASE = "web202211"
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSEORD}@{HOSTNAME}:{POST}/{DATABASE}?charset=utf8mb4"
# DB_URI = f"mysql+pymysql://{USERNAME}:{PASSEORD}@{HOSTNAME}:{POST}/{DATABASE}"
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "cukua"
MAIL_PASSWORD = "wcw***********"
MAIL_DEFAULT_SENDER = "cukuangren@qq.com"

SECRET_KEY = os.urandom(18)

# redis
redis_host = '127.0.0.1'
redis_port = 6379
redis_password = '5tgb%TGB'
REDIS_URL = f"redis://:{redis_password}@{redis_host}:{redis_port}/0"
