from . import admin
from flask import render_template, redirect, url_for,flash,session
from app.home.forme import LoginForm
from app.models import Users

# 进入登录界面
@admin.route("/",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit(): #提交表单 要验证
        data = form.data  #获取表单提交的信息
        user = Users.query.filter_by(name=data["name"]).first()
        print("data【name】",data["name"],"表单密码",data["pwd"],"库中密码",user)
        if not user.chek_pwd(data["pwd"]):

            flash("密码错误")
            return redirect(url_for("home1.login"))
        session["user"] =data["name"]
        return redirect(url_for("home1.index"))

    return render_template('home1/login.html',form=form)


# 退出
@admin.route("/logout")
def logout():
    return redirect(url_for("home1.login"))

#首页
@admin.route("/index")
def index():
    print("返回index")
    names=session["user"]
    return render_template("home1/index.html",name=names)

#买卖记录
@admin.route("/nodeindex")
def nodeindex():
    return render_template("home1/Node/index.html")


