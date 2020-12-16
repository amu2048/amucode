#把home里的额初始化导进来
from . import home
"""
render_template：用于HTML模板，
redirect：跳转至模板，与前面的不同，
flash：闪现提示,
session:就是session啊
"""
from flask import render_template, redirect, url_for, flash, session,request,Response
#从表单脚本中导入 LoginForm 用于表单数据的验证
from app.home.forme import LoginForm,RegistFrom,BuycattleFrom,SellcattleFrom,PwdFrom
#导入数据库模型 导入user 用于读写user表数据
from app.models import Users,Userlog,Sales
from werkzeug.security import generate_password_hash
import uuid
from app import db
from functools import wraps

'''=====公共部分 登录注册退出 ====='''
#上下文应用处理器



#定义一个装饰器 访问路由时先验证这个装饰器内的逻辑
def admin_login_req(f):

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
        user = Users.query.filter_by(account  =data["user"]).first()
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

        session["birthday"] = user.birthday
        session["username"] = user.name
        session["lcs"] = "1993"  #此项未了防止有人破解seesion 特意增加个盐
        #写入会员登录日志
        userlog =Userlog(
            #user_id = data["user"],
            account=user.account,
            ip = request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()

        return redirect(url_for("home.index"))
    print("返回登录login界面")
    return render_template('home/login.html',form=form)
#注册
@home.route("/register",methods=["GET","POST"])
def register():
    form = RegistFrom()
    if form.validate_on_submit():
        data = form.data
        print('注册提交的数据',data)
        print('uuid:',uuid.uuid4().hex)
        user =Users(
            account = data['userId'],
            name = data['userName'],
            pwd = generate_password_hash(data['userpassword']),
            sex = data['sex'],
            birthday = data['birthday'],
            phone = data['userphone'],
            address = data['userAddress'],
            uuid = uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功,请点击返回按钮去登录","ok")
    return render_template('home/register.html',form=form)
@home.route("/pwd_up",methods=["GET","POST"])
@admin_login_req
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
@admin_login_req
def logout():
    print("进入退出函数")
    #退出时 把本地缓存的seesion密码去掉
    session.pop("username",None)
    session.pop("lcs", None)
    session.pop("birthday", None)
    return redirect(url_for("home.login"))

'''=====首页====='''
#首页
@home.route("/index")
@admin_login_req
def index():
    print("返回index")
    global sessionuserid
    sessionuserid=session["username"]
    return render_template("home/index.html",names = sessionuserid)
    #return render_template("home/index.html",name=names)
'''=====买卖管理====='''
#买卖记录列表
@home.route("/cattle_list/<int:page>/",methods=["GET"])
@admin_login_req
def cattle_list(page=None ):
    if page is None:
        page=1

    #按时间倒序查询 使用自带分页助手paginate返回页码和按多少页分页
    page_data = Sales.query.order_by(Sales.addriqi.desc()).paginate(page=page,per_page=10)

    return render_template("home/cattle_list.html",page_data=page_data)
#删除记录
@home.route("/cattle_del/<int:id>/",methods=["GET"])
@admin_login_req
def cattle_del( id=None):
    sales = Sales.query.get_or_404(int(id))
    db.session.delete(sales)
    db.session.commit()
    flash("删除买卖成功！", "ok")
    return redirect(url_for('home.cattle_list', page=1))



#添加购买记录
@home.route("/buycattle_add",methods=["GET","POST"])
@admin_login_req
def buycattle_add():
    form = BuycattleFrom()
    if form.validate_on_submit():
        print("触发添加肉牛")
        data = form.data
        print("接收到的表单数据为：",data)
        buyunitprice = format(float(data['buyprice']) / (float(data['buyweight'])*2), '.2f')
        print("接收添加购买记录的单价",buyunitprice)
        sales = Sales(
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
            buycattlefild=data['buycattlefild'],
            remarks=data['remarks']
            )
        db.session.add(sales)
        db.session.commit()
        flash("添加成功,请点击返回按钮去查看", "ok")
    return render_template("home/buycattle_add.html",form=form)
#添加出栏记录
@home.route("/sellcattle_add",methods=["GET","POST"])
@admin_login_req
def sellcattle_add():
    form = SellcattleFrom()
    if form.validate_on_submit():
        print("触发添加肉牛出栏记录")
        data = form.data
        print("接收到的表单数据为：", data)
        sellunitprice = format(float(data['sellprice']) / (float(data['sellweight']) * 2), '.2f')
        print("添加出栏记录data['cattleid'] ",data['cattleid'] )
        result = Sales.query.filter_by( cattleid = data['cattleid'] ).first()
        result.sellprice = data['sellprice']
        result.sellweight = data['sellweight']
        result.sellunitprice = sellunitprice
        result.sellday = data['sellday']
        result.sellnum = data['sellnum']
        result.sellcontatcs = data['sellcontatcs']
        result.sellcity = data['sellcity']
        result.sellfreight = data['sellfreight']
        result.sellcattlefild = data['sellcattlefild']
        print("添加出栏记录", result)
        db.session.commit()
        flash("添加成功,请点击返回按钮去查看", "ok")
    return render_template("home/sellcattle_add.html",form=form,sessionuserid = sessionuserid)

'''=====会员管理====='''
#会员列表 传入查看的页码
@home.route("/user_list/<int:page>/",methods=["GET"])
@admin_login_req
def user_list(page=None):
    if page is None:
        page= 1
    page_data = Users.query.order_by(Users.addriqi.desc()).paginate(page=page,per_page=10)
    users_list = Users.query.filter_by().all()
    return render_template("home/user_list.html",page_data=page_data)
#查看会员详情
@home.route("/user_view/<int:id>/",methods=["GET"])
@admin_login_req
def user_view(id=None):
    #get_or_404获取指定id的数据
    user  = Users.query.get_or_404(int(id))
    return render_template("home/user_view.html",user=user)
#删除会员
@home.route("/user_del/<int:id>/",methods=["GET"])
@admin_login_req
def user_del(id = None):
    user = Users.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash("删除会员成功！","ok")
    return redirect(url_for('home.user_list',page=1))


'''=====日志管理====='''
#操作日志列表
@home.route("/oplog_list")
@admin_login_req
def oplog_list():
    return render_template("home/oplog_list.html")
#管理员登录日志列表
@home.route("/adminloginlog_list")
@admin_login_req
def adminloginlog_list():
    return render_template("home/adminloginlog_list.html")
#会员登录日志列表
@home.route("/userloginlog_list/<int:page>/",methods=["GET"])
@admin_login_req
def userloginlog_list(page=None):
    if page is None:
        page=1
    page_data = Userlog.query.order_by(Userlog.addriqi.desc()).paginate(page=page,per_page=15)
    return render_template("home/userloginlog_list.html",page_data=page_data)

'''=====权限管理====='''
#添加权限
@home.route("/auth_add")
@admin_login_req
def auth_add():
    return render_template("home/auth_add.html")
#权限列表
@home.route("/auth_list")
@admin_login_req
def auth_list():
    return render_template("home/auth_list.html")

'''=====角色管理====='''
#添加角色
@home.route("/role_add")
@admin_login_req
def role_add():
    return render_template("home/role_add.html")
#角色列表
@home.route("/role_list")
@admin_login_req
def role_list():
    return render_template("home/role_list.html")

'''=====管理员管理====='''
#添加管理员
@home.route("/admin_add")
@admin_login_req
def admin_add():
    return render_template("home/admin_add.html")
#管理员列表
@home.route("/admin_list")
@admin_login_req
def admin_list():
    return render_template("home/admin_list.html")






