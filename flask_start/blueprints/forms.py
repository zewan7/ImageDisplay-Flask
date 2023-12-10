import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel, EmailCaptchaModel
from exis import db, redis_client



# 表单验证
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=2, max=20, message="用户名格式错误!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误!")])
    password_confirm = wtforms.StringField(validators=[EqualTo('password', message="两次密码不一致！")])

    # 1.邮箱是否被注册
    def validate_email(self, field):
        # 当前的email  ------->field获取当前的数据
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经注册！")

    # 2. 验证码是否正确
    def validate_captcha(self, field):
        # 当前的captcha
        captcha = field.data
        email = self.email.data
        # mysql验证
        # captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        # if not captcha_model:
        #     raise wtforms.ValidationError(message="邮箱或验证码错误！")
        # redis验证
        redis_captcha = int(redis_client.get(email))
        if redis_captcha != int(captcha):
            raise wtforms.ValidationError(message="邮箱或验证码错误！")


        # # TODO ：可以删掉captcha_model
        # else:
        #     db.session.delete(captcha_model)
        #     db.session.commit()


# 忘记密码表单验证
class ForgetThePasswordForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误!")])
    password_confirm = wtforms.StringField(validators=[EqualTo('password', message="两次密码不一致！")])

    # 1.邮箱是否存在
    def validate_email(self, field):
        # 当前的email  ------->field获取当前的数据
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            raise wtforms.ValidationError(message="该邮箱没有注册！")

    # 2. 验证码是否正确
    def validate_captcha(self, field):
        # 当前的captcha
        captcha = field.data
        email = self.email.data
        # captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        # if not captcha_model:
        #     raise wtforms.ValidationError(message="邮箱或验证码错误！")

        redis_captcha = int(redis_client.get(email))
        if redis_captcha != int(captcha):
            raise wtforms.ValidationError(message="邮箱或验证码错误！")

        # TODO ：可以删掉captcha_model
        # else:
        #     db.session.delete(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误!")])


class PublishingForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=2, max=100, message="标题格式错误!")])
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误!")])
