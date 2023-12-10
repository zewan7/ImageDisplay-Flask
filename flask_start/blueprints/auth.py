import random
from flask import Blueprint, jsonify, redirect, url_for, render_template, request, session
from exis import mail, db, redis_client
from flask_mail import Message
import string
from models import EmailCaptchaModel, UserModel
from threading import Thread
from .forms import RegisterForm, LoginForm, ForgetThePasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

#  url_prefix='/auth' url开始
bp = Blueprint('auth', __name__, url_prefix='/auth')


# 登录
@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱还未注册！")
                return redirect(url_for("auth.login"))
            # 密码相同
            if check_password_hash(user.password, password):
                session["user_id"] = user.username
                return redirect("/")

            else:
                print("密码错误！")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


# 退出登录
@bp.route('/logout')
def logout():
    # 清空用户,回首页
    session.clear()
    return render_template('index.html')


# 注册提交
@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        # 输入验证表单是否满足注册需求
        form = RegisterForm(request.form)
        if form.validate():
            # 获取到html的信息
            email = form.email.data
            username = form.username.data
            password = form.password.data
            # 添加到数据库
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # 注册完成直接提交登录
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


# 修改密码
@bp.route('/forgetthepassword', methods=['POST', 'GET'])
def forgetthepassword():
    if request.method == "GET":
        return render_template('forgetthepassword.html')
    else:
        # 输入验证表单是否满足注册需求
        form = ForgetThePasswordForm(request.form)
        if form.validate():
            # 获取到html的信息
            email = form.email.data
            password = form.password.data
            # 修改密码
            user = UserModel.query.filter_by(email=email).first()
            user.password = generate_password_hash(password)
            db.session.commit()
            # 修改完成跳转到登录
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


# 验证码
@bp.route("/captcha/email")
def get_email_captcha():
    # 获取email
    email = request.args.get('email')
    # 随机验证码
    source = string.digits * 4
    captcha = "".join(random.sample(source, 4))
    print(captcha)

    def start_email(app, email, captcha):
        # 处理上下文
        with app.app_context():
            #  发送验证码邮件 ----->>>>>>> 卡前端界面
            message = Message(subject="注册验证码", recipients=[email], body=f"您的验证码是：{captcha}\n有效时间5分钟。")
            mail.send(message)

    thread = Thread(target=start_email, args=(current_app._get_current_object(), email, captcha))
    thread.start()
    # 添加到redis
    redis_client.set(email, captcha, ex=300)
    # 添加验证码到数据库
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # 添加到数据库
    return jsonify({"code": 200, "message": '', "data": None})


# 网页
@bp.route('/zhi')
def zhi():
    return render_template('zhi.html')
