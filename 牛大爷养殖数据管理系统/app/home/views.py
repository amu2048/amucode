#把home里的额初始化导进来
from . import home
"""
render_template：用于HTML模板，
redirect：跳转至模板，与前面的不同，
flash：闪现提示,
session:就是session啊
"""
from flask import render_template, redirect, url_for, flash, session,request
#从表单脚本中导入 LoginForm 用于表单数据的验证
from app.home.forme import LoginForm,RegistFrom,BuycattleFrom,SellcattleFrom,PwdFrom
#导入数据库模型 导入user 用于读写user表数据
from app.models import Users,Userlog,Sales,Oplog
from werkzeug.security import generate_password_hash
import uuid
from app import db
import  datetime

from functools import wraps
import os
UPLOAD_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),r'static\limg\userimg')
'''=====公共部分 登录注册退出 ====='''
#上下文应用处理器 封装全局变量
@home.context_processor
def tpl_extra():
    #定义一个当前时间的类返回时间
    data = dict(
        online_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    return data


#定义一个装饰器 访问路由时先验证这个装饰器内的逻辑
def home_login_req(f):
    @wraps(f)
    #自定义函数
    def decorated_function(*args,**kwargs):
        #判断 sessi中是否存在lcs令牌

        print("开始判断是否在seesion：",session)
        if "username" not in session:
            #如果不存在则返回登录界面
            print("不在seesion中")
            return redirect(url_for("home.login",next=request.url))
        #如果存在 返回继续执行访问
        print("在seesion中 开始返回执行函数")
        return f(*args,**kwargs)
    return decorated_function
#进入登录界面
@home.route("/",methods=["GET","POST"])
def login():
    form = LoginForm()
    print("进入登陆函数")
    if form.validate_on_submit(): #提交表单 要验证 前端在提交按钮下添加代码{{form.csrf_token}} app.config设置令牌
        print("进入form.validate_on_submit()")
        data = form.data  #获取表单提交的信息
        user = Users.query.filter_by(account=data["account"]).first()
        print('数据库中的姓名',user.name)
        #调用user中的函数chek_pwd 判断输入的密码和数据库加密后的是否一致 不一致就进入if
        if not user.chek_pwd(data["mima"]):
            flash("密码错误,请重新输入！","err")
            '''
            flash前端闪现通知密码错误 前段增加语句块来显示
            <div>
            {% for msg in get_flashed_messages() %}
                <p style="color: red;">{{msg}}</p>
            {% endfor %}
             </div>
            '''
            return redirect(url_for("home.login"))
        #如果密码一致 存入session把用户名存到session中 并返回主页模板
        session["userface"] = user.face  #前端获取头像名称
        session["account"] = user.account
        session["username"] = user.name
        session["lcs"] = "1993"  #此项未了防止有人破解seesion 特意增加个盐
        #写入会员登录日志
        userlog =Userlog(
            account=user.account,
            ip = request.remote_addr,
            op='用户 %s 登录' % (session['account'])
        )
        db.session.add(userlog)
        db.session.commit()

        return redirect(url_for("home.index"))
    print("返回登录login界面")
    return render_template('home/login.html',form=form)
#注册
@home.route("/register",methods=["GET","POST"])
def register():
    #from werkzeug.datastructures import CombinedMultiDict
    #form = RegistFrom(CombinedMultiDict([request.form, request.files]))
    form = RegistFrom()
    if form.validate_on_submit():
        print('进入注册提交的数据')
        data = form.data
        # 获取上传文件的文件名;
        filena = form.face.data.filename
        #print(str(filename))
        filename = data['userId'] + filena
        # 将上传的文件保存到服务器;
        form.face.data.save(os.path.join( UPLOAD_PATH, filename))
        print("上传成功")
        flash("上传成功", 'ok')
        user =Users(
            account = data['userId'],
            name = data['userName'],
            pwd = generate_password_hash(data['userpassword']),
            sex = data['sex'],
            weixin= data['weixin'],
            birthday = data['birthday'],
            phone = data['userphone'],
            address = data['userAddress'],
            face = filename,
            info = data['info'],
            uuid = uuid.uuid4().hex
        )
        db.session.add(user)
        print("保存数据")
        db.session.commit()
        flash("注册成功,请点击返回按钮去登录","ok")
    return render_template('home/register.html',form=form)
@home.route("/pwd_up",methods=["GET","POST"])
@home_login_req
#修改密码
def pwd_up():
    form = PwdFrom()
    if form.validate_on_submit():
        data = form.data
        user = Users.query.filter_by(name = session["username"]).first()
        user.pwd = generate_password_hash(data["new_pwd"])
        print("修改的新密码为",data["new_pwd"])
        db.session.add(user)
        db.session.commit()
        flash("密码修改成功,请重新登陆！","ok")
        print("密码修改成功")
        return redirect(url_for("home.logout"))
    return render_template("home/pwd_up.html",form=form)


# 退出
@home.route("/logout",methods=["GET","POST"])
@home_login_req
def logout():
    print("进入退出函数")
    #退出时 把本地缓存的seesion密码去掉
    session.pop("username",None)
    session.pop("lcs", None)
    session.pop("birthday", None)
    userlog = Userlog(
        account=session['account'],
        ip=request.remote_addr,
        op = '用户 %s 退出' % (session['account'])
    )
    db.session.add(userlog)
    db.session.commit()
    return redirect(url_for("home.login"))

'''=====首页====='''
#首页
@home.route("/index")
@home_login_req
def index():
    print("返回index")
    print(" session['userface']", session["userface"])
    return render_template("home/index.html")
    #return render_template("home/index.html",name=names)
'''=====买卖管理====='''
#买卖记录列表
@home.route("/cattle_list/<int:page>/",methods=["GET"])
@home_login_req
def cattle_list(page=None ):
    if page is None:
        page=1

    #按时间倒序查询 使用自带分页助手paginate返回页码和按多少页分页
    page_data = Sales.query.filter_by(account = session["account"] ).order_by(Sales.addriqi.desc()).paginate(page=page,per_page=10)

    return render_template("home/cattle_list.html",page_data=page_data)
#删除记录
@home.route("/cattle_del/<int:id>/",methods=["GET"])
@home_login_req
def cattle_del( id=None):
    sales = Sales.query.get_or_404(int(id))
    db.session.delete(sales)
    db.session.commit()
    flash("删除买卖成功！", "ok")
    oplog = Oplog(
        account=session["account"],
        ip=request.remote_addr,
        op="删除买卖记录:肉牛id：%s " % (id)
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('home.cattle_list', page=1))
#添加购买记录
@home.route("/buycattle_add",methods=["GET","POST"])
@home_login_req
def buycattle_add():
    form = BuycattleFrom()
    if form.validate_on_submit():
        print("触发添加肉牛")
        data = form.data
        print("接收到的表单数据为：",data)
        buyunitprice = format(float(data['buyprice']) / (float(data['buyweight'])*2), '.2f')
        print("接收添加购买记录的单价",buyunitprice)
        sales = Sales(
            account = session['account'],
            cattleid=data['cattleid'],
            cattlename=data['cattlename'],
            buyprice=data['buyprice'],
            buyweight=data['buyweight'],
            buyunitprice=buyunitprice,
            buyday=data['buyday'],
            buynum=data['buynum'],
            buycontatcs=data['buycontatcs'],
            buycity=data['buycity'],
            buyfreight=data['buyfreight'],
            remarks=data['remarks']
            )
        db.session.add(sales)
        db.session.commit()
        flash("添加成功,请点击返回按钮去查看", "ok")
        oplog =Oplog(
            account=session["account"],
            ip= request.remote_addr,
            op="添加购买记录:肉牛id：%s ，肉牛昵称： %s ，购买总价：%s，购买时体重： %s " %(data['cattleid'],data['cattlename'],data['buyprice'],data['buyweight'])
        )
        db.session.add(oplog)
        db.session.commit()
    return render_template("home/buycattle_add.html",form=form)
#添加出栏记录
@home.route("/sellcattle_add",methods=["GET","POST"])
@home_login_req
def sellcattle_add():
    form = SellcattleFrom()
    if form.validate_on_submit():
        print("触发添加肉牛出栏记录")
        data = form.data
        print("接收到的表单数据为：", data)
        sellunitprice = format(float(data['sellprice']) / (float(data['sellweight']) * 2), '.2f')
        print("添加出栏记录data['cattleid'] ",data['cattleid'] )
        result = Sales.query.filter_by( account = session['account'],cattleid = data['cattleid'] ).first()
        result.sellprice = data['sellprice']
        result.sellweight = data['sellweight']
        result.sellunitprice = sellunitprice
        result.sellday = data['sellday']
        result.sellnum = data['sellnum']
        result.sellcontatcs = data['sellcontatcs']
        result.sellcity = data['sellcity']
        result.sellfreight = data['sellfreight']
        #result.sellcattlefild = data['sellcattlefild']
        print("添加出栏记录", result)
        db.session.commit()
        flash("添加成功,请点击返回按钮去查看", "ok")
        oplog = Oplog(
            account=session["account"],
            ip=request.remote_addr,
            op="添加出栏记录:肉牛id：%s ，肉牛昵称： %s ，出售总价：%s，出售时体重： %s " %(data['cattleid'],data['cattlename'],data['sellprice'],data['sellweight'])
        )
        db.session.add(oplog)
        db.session.commit()
    return render_template("home/sellcattle_add.html",form=form)

'''=====会员管理====='''
#查看会员详情
@home.route("/user_view/<int:id>/",methods=["GET"])
@home_login_req
def user_view(id=None):
    #get_or_404获取指定id的数据
    user  = Users.query.get_or_404(int(id))



'''=====日志管理====='''
#操作日志列表
@home.route("/oplog_list/<int:page>/",methods=["GET"])
@home_login_req
def oplog_list(page = None):
    if page is None:
        page=1
    page_data = Oplog.query.filter_by(account = session["account"] ).order_by(Oplog.addriqi.desc()).paginate(page=page,per_page=20)
    return render_template("home/oplog_list.html",page_data=page_data)
#会员登录日志列表
@home.route("/userloginlog_list/<int:page>/",methods=["GET"])
@home_login_req
def userloginlog_list(page=None):
    if page is None:
        page=1
    page_data = Userlog.query.filter_by(account = session["account"] ).order_by(Userlog.addriqi.desc()).paginate(page=page,per_page=20)
    return render_template("home/userloginlog_list.html",page_data=page_data)








