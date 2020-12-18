from flask import Flask,render_template
# 安装Flask-SQLAlchemy包   用于处理数据库的
from flask_sqlalchemy import SQLAlchemy
import pymysql
#启动flask并开启调试模式
app =Flask(__name__)

# 用flask的配置参数 设置连接数据库地址
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1:3306/2021"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

UPLOAD_FOLDER = r'D:\file'
#seesion令牌
app.config["SECRET_KEY"] = "1993"
#开启调试模式
app.debug =True

# 实例化db代表数据库
db = SQLAlchemy(app)

#导入蓝图 并重命名
from app.home import home as home_blueprint
from app.admin import  admin as admin_blueprint

#蓝图启动器 默认访问home_blueprint  当访问路由后加admin时 执行访问admin_blueprint
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint,url_prefix="/admin")


#全局请求 当找不到访问者输入的url界面报错404 就返回个美化的404网页
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404


