from flask import Flask, session, g
import config
from exis import db, mail, redis_client
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp

# 数据库更新
from flask_migrate import Migrate
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer

# 2.登录邮箱
app = Flask(__name__)
# 加载配置config
app.config.from_object(config)
# 添加app
db.init_app(app)
# 邮件
mail.init_app(app)
redis_client.init_app(app)

# 执行sql控制
# flask db init：只需要执行一次
# flask db migrate：将orm模型生成迁移脚本
# flask db upgrade：将迁移脚本映射到数据库中
migrate = Migrate(app, db)

# 注册蓝图
bps = [qa_bp, auth_bp]
for Bp in bps:
    app.register_blueprint(Bp)


# 钩子函数
@app.before_request
def my_before_request():
    # 判断是否登录
    user_id = session.get("user_id")
    if user_id:
        # 获取user_id
        user = UserModel.query.filter_by(username=user_id).first()
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


# 上下文处理器
# 它可以使得所有模板文件都能读取到该变量（user）。
# 当需要向多个 html 页面传输数据时, 使用该函数更方便
@app.context_processor
def my_context_processor():
    # 返回变量可见
    return {"user": g.user}


"""# 每次请求之后被执行的
# 这里注意, 需要传入参数（response 这个形参名字可以改）
# 因为是请求完成后执行, 自然就有响应返回
@app.after_request
def handel_after(response):
    print("每次请求之后被执行的")
    return response
"""

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=9001)
    # # 推送应用程序上下文
    # with app.app_context():
    #     db.create_all()

    http_server = WSGIServer(('0.0.0.0', 9001), app)
    http_server.serve_forever()
