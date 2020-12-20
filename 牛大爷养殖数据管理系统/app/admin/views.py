#把home里的额初始化导进来
from . import admin
"""
render_template：用于HTML模板，
redirect：跳转至模板，与前面的不同，
flash：闪现提示,
session:就是session啊
"""
from flask import render_template, redirect, url_for, flash, session,request,Response
#从表单脚本中导入 LoginForm 用于表单数据的验证
from app.admin.forme import LoginForm,PwdFrom,AdminaddFrom,NoticeaddForm,NoticeupForm
#导入数据库模型 导入user 用于读写user表数据
from app.models import Admin,Adminlog,Sales,Oplog,Users,Userlog,Notice
from werkzeug.security import generate_password_hash
import uuid
from app import db
import  datetime
from functools import wraps
import os
import random
#管理员头像地址
ADMIN_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),r'static\limg\userimg')
#生产Linux地址
ADMIN_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),r'static/limg/faceimg')
'''=====公共部分 登录注册退出 ====='''
#上下文应用处理器 封装全局变量
@admin.context_processor
def tpl_extra():
    #定义一个当前时间的类返回时间
    data = dict(
        online_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    return data

# 定义一个装饰器 访问路由时先验证这个装饰器内的逻辑
def admin_login_req(f):
    @wraps(f)
    #自定义函数
    def decorated_function(*args,**kwargs):
        #判断 sessi中是否存在lcs令牌
        print("开始判断是否在seesion：",session)
        if "lcsadmin" not in session:
            #如果不存在则返回登录界面
            print("不在seesion中")
            return redirect(url_for("admin.login",next=request.url))
        #如果存在 返回继续执行访问
        print("在seesion中 开始返回执行函数")
        return f(*args,**kwargs)
    return decorated_function
#进入登录界面
@admin.route("/",methods=["GET","POST"])
def login():
    form = LoginForm()
    print("进入登陆函数")
    if form.validate_on_submit(): #提交表单 要验证 前端在提交按钮下添加代码{{form.csrf_token}} app.config设置令牌
        print("进入form.validate_on_submit()")
        data = form.data  #获取表单提交的信息
        admins = Admin.query.filter_by(account  =data["account"]).first()
        print('数据库中的姓名',admin.name)
        #调用user中的函数chek_pwd 判断输入的密码和数据库加密后的是否一致 不一致就进入if
        if not admins.chek_pwd(data["mima"]):
            flash("密码错误,请重新输入！","err")
            '''
            flash前端闪现通知密码错误 前段增加语句块来显示
            <div>
            {% for msg in get_flashed_messages() %}
                <p style="color: red;">{{msg}}</p>
            {% endfor %}
             </div>
            '''
            return redirect(url_for('admin.login'))
        #如果密码一致 存入session把用户名存到session中 并返回主页模板
        session["userface"] = admins.face  #前端获取头像名称
        session["account"] = admins.account
        session["username"] = admins.name
        session["lcsadmin"] = "1993"  #此项未了防止有人破解seesion 特意增加个盐
        print("登录成功IP",request.remote_addr)
        #写入会员登录日志
        adminlog =Adminlog(
            account=admins.account,
            ip = request.remote_addr,
            op = '用户 %s 登录' % ( admins.account )
        )
        db.session.add(adminlog)
        db.session.commit()

        return redirect(url_for("admin.index"))
    print("返回登录login界面")
    return render_template('admin/login.html',form=form)
#修改密码
@admin.route("/pwd_up",methods=["GET","POST"])
@admin_login_req
def pwd_up():
    form = PwdFrom()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name = session["username"]).first()
        admin.pwd = generate_password_hash(data["new_pwd"])
        print("修改的新密码为",data["new_pwd"])
        db.session.add(admin)
        db.session.commit()
        flash("密码修改成功,请重新登陆！","ok")
        print("密码修改成功")
        return redirect(url_for("admin.logout"))
    return render_template("admin/pwd_up.html",form=form)
# 退出
@admin.route("/logout",methods=["GET","POST"])
@admin_login_req
def logout():
    print("进入退出函数")
    adminlog = Adminlog(
        account=session['account'],
        ip=request.remote_addr,
        op = '用户 %s 退出' % (session['account'])
    )
    db.session.add(adminlog)
    db.session.commit()
    # 退出时 把本地缓存的seesion密码去掉
    session.pop("userface", None)
    session.pop("account", None)
    session.pop("username", None)
    session.pop("lcsadmin", None)
    return redirect(url_for("admin.login"))

'''=====首页====='''
#首页
@admin.route("/index")
@admin_login_req
def index():
    return render_template('admin/index.html')

'''=====买卖管理====='''
#用户的买卖记录列表
@admin.route("/cattle_list/<int:page>/",methods=["GET"])
@admin_login_req
def cattle_list(page=None ):
    if page is None:
        page=1
    #按时间倒序查询 使用自带分页助手paginate返回页码和按多少页分页
    page_data = Sales.query.order_by(Sales.addriqi.desc()).paginate(page=page,per_page=20)
    return render_template("admin/cattle_list.html",page_data=page_data)
#查看买卖记录
@admin.route("/cattle_view/<int:id>/",methods=["GET"])
@admin_login_req
def cattle_view(id=None):
    #get_or_404获取指定id的数据
    sales  = Sales.query.get_or_404(int(id))
    return render_template("admin/cattle_view.html",sales=sales)
'''=====会员管理====='''
#会员列表
@admin.route("/user_list/<int:page>/",methods=["GET"])
@admin_login_req
def user_list(page=None):
    if page is None:
        page= 1
    page_data = Users.query.order_by(Users.addriqi.desc()).paginate(page=page,per_page=10)
    return render_template("admin/user_list.html",page_data=page_data)
#查看会员详情
@admin.route("/user_view/<int:id>/",methods=["GET"])
@admin_login_req
def user_view(id=None):
    #get_or_404获取指定id的数据
    user  = Users.query.get_or_404(int(id))
    return render_template("admin/user_view.html",user=user)
#删除会员
@admin.route("/user_del/<int:id>/",methods=["GET"])
@admin_login_req
def user_del(id = None):
    user = Users.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash("删除会员成功！","ok")
    print("删除",user.name)
    oplog = Oplog(
        account=session["account"],
        ip=request.remote_addr,
        op="删除会员:会员id：%s ,会员账号：%s " % (id,user.name)
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.user_list',page=1))


'''=====日志管理====='''
#操作日志列表
@admin.route("/oplog_list/<int:page>/",methods=["GET"])
@admin_login_req
def oplog_list(page = None):
    if page is None:
        page=1
    page_data = Oplog.query.order_by(Oplog.addriqi.desc()).paginate(page=page,per_page=20)
    return render_template("admin/oplog_list.html",page_data=page_data)
#管理员登录日志列表
@admin.route("/adminloginlog_list/<int:page>/",methods=["GET"])
@admin_login_req
def adminloginlog_list(page = None):
    if page is None:
        page=1
    page_data = Adminlog.query.order_by(Adminlog.addriqi.desc()).paginate(page=page,per_page=10)
    return render_template("admin/adminloginlog_list.html",page_data=page_data)
#会员登录日志列表
@admin.route("/userloginlog_list/<int:page>/",methods=["GET"])
@admin_login_req
def userloginlog_list(page=None):
    if page is None:
        page=1
    page_data = Userlog.query.order_by(Userlog.addriqi.desc()).paginate(page=page,per_page=20)
    return render_template("admin/userloginlog_list.html",page_data=page_data)

'''=====权限管理=====未实现'''
#公告列表
@admin.route("/notice_list/<int:page>/",methods=["GET"])
@admin_login_req
def notice_list(page=None):
    if page is None:
        page = 1
    #获取公告 状态为1启用状态的公告数据
    notice = Notice.query.filter_by().order_by(Notice.priority).paginate(page=page,per_page=10)
    return render_template("admin/notice_list.html",notice=notice)
#添加公告
@admin.route("/notice_add",methods=["GET","POST"])
@admin_login_req
def notice_add():
    form = NoticeaddForm()
    if form.validate_on_submit():
        print("添加公告")
        data = form.data
        notice = Notice(
            title=data['title'],
            table = data['table'],
            url = data['url'],
            priority = data['priority'],
            state = data['state']
        )
        db.session.add(notice)
        print("保存数据")
        db.session.commit()
        flash("公告添加成功，请返回查看", "ok")





    return render_template("admin/notice_add.html",form=form)

#编辑公告
@admin.route("/notice_up/<int:id>/",methods=["GET","POST"])
@admin_login_req
def notice_up(id):
    form = NoticeupForm()
    if form.validate_on_submit():
        print("触发修改公告")
        data =form.data
        result = Notice.query.filter_by(id = id).first()
        if data['title'] !=  None:
            result.title = data['title']
        if data['url'] != '':
            result.title = data['url']
        result.priority = data['priority']
        result.state = data['state']
        result.table = data['table']

        db.session.commit()
        print("提交数据库开始修改数据")
        flash("修改成功,请点击返回去查看", "ok")

        adminlog = Adminlog(
            account=session["account"],
            ip=request.remote_addr,
            op="修改公告: 公告内容：%s " %(data['table'])
        )
        db.session.add(adminlog)
        db.session.commit()
    return render_template("admin/notice_up.html",form=form)
#删除公告
@admin.route("/notice_del/<int:id>/",methods=["GET","POST"])
@admin_login_req
def notice_del(id):
    notice = Notice.query.get_or_404(int(id))
    db.session.delete(notice)
    db.session.commit()
    flash("公告删除成功！", "ok")
    adminlog = Adminlog(
        account=session["account"],
        ip=request.remote_addr,
        op="删除公告 "
    )
    db.session.add(adminlog)
    db.session.commit()
    return redirect(url_for('admin.notice_list', page=1))




'''=====角色管理====='''
#添加角色
@admin.route("/role_add")
@admin_login_req
def role_add():
    return render_template("home/role_add.html")
#角色列表
@admin.route("/role_list")
@admin_login_req
def role_list():
    return render_template("home/role_list.html")

'''=====管理员管理====='''
#添加管理员
@admin.route("/admin_add",methods=["GET","POST"])
@admin_login_req
def admin_add():
    form = AdminaddFrom()
    if form.validate_on_submit():
        print("添加管理员")
        data = form.data
        if data['face'] != None:
            # 获取上传文件的文件名;
            filena = form.face.data.filename
            # print(str(filename))
            filename = uuid.uuid4().hex + filena
            # 将上传的文件保存到服务器;
            form.face.data.save(os.path.join(ADMIN_PATH, filename))
        else:
            filename = str(random.randint(0, 5)) + '.png'
        admin = Admin(
            account=data['account'],
            name=data['userName'],
            pwd=generate_password_hash(data['userpassword']),
            weixin=data['weixin'],
            phone=data['userphone'],
            address=data['userAddress'],
            face=filename,
            info=data['info'],
            uuid=uuid.uuid4().hex
        )
        db.session.add(admin)
        print("保存数据")
        db.session.commit()
        flash("注册成功,请点击返回按钮去登录", "ok")
        adminlog = Adminlog(
            account=session["account"],
            ip=request.remote_addr,
            op="添加管理员: %s " %(data['account'])
        )
        db.session.add(adminlog)
        db.session.commit()

    return render_template("admin/admin_add.html",form =form)

#管理员列表
@admin.route("/admin_list/<int:page>/",methods=["GET"])
@admin_login_req
def admin_list(page=None):
    if page is None:
        page= 1
    page_data = Admin.query.order_by(Admin.addriqi.desc()).paginate(page=page,per_page=10)
    return render_template("admin/admin_list.html",page_data=page_data)
#查看管理员详情
@admin.route("/admin_view/<int:id>/",methods=["GET"])
@admin_login_req
def admin_view(id=None):
    #get_or_404获取指定id的数据
    admin  = Admin.query.get_or_404(int(id))
    return render_template("admin/admin_view.html",user=admin)
#删除管理员
@admin.route("/admin_del/<int:id>/",methods=["GET"])
@admin_login_req
def admin_del(id = None):
    admin = Admin.query.get_or_404(int(id))
    db.session.delete(admin)
    db.session.commit()
    flash("删除会员成功！","ok")
    print("删除",admin.name)
    adminlog = Adminlog(
        account=session["account"],
        ip=request.remote_addr,
        op="删除会员:会员id：%s ,会员账号：%s " % (id,admin.name)
    )
    db.session.add(adminlog)
    db.session.commit()
    return redirect(url_for('admin.admin_list',page=1))



