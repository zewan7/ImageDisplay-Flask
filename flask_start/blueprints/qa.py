from flask import Blueprint, render_template, url_for, request, redirect, g
from models import PublishingWork
from .forms import PublishingForm
from exis import db
from decorators import login_required
from datetime import datetime
import os

# 首页
#  url_prefix='/' url开始前缀
bp = Blueprint('qa', __name__, url_prefix='/')


# 首页就有问答
@bp.route('/')
def index():
    return render_template('index.html')


# 发布
@bp.route("/qa/publishing", methods=['POST', 'GET'])
@login_required
def publishing():
    if request.method == "GET":
        return render_template("PublishingWork.html")
    else:
        form = PublishingForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            picture = request.files['photo']
            author_name = g.user.username
            author_id = g.user.id
            now_time = str(datetime.now())
            picture_save = f'/data/Python/Flask_test/flask_start/images/{now_time}+{picture.filename}'
            picture.save(picture_save)
            publish = PublishingWork(title=title, content=content, image_path=picture_save, author_id=author_id,
                                     author_name=author_name)
            db.session.add(publish)
            db.session.commit()
            # todo: 跳转到这篇的详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.publishing"))
