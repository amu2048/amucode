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
from app.home.forme import LoginForm,RegistFrom,BuycattleFrom,SellcattleFrom,PwdFrom,UserupFrom,CattleupFrom
#导入数据库模型 导入user 用于读写user表数据
from app.models import Users,Userlog,Sales,Oplog,Notice
from werkzeug.security import generate_password_hash
import uuid
from app import db
import  datetime
import random
from functools import wraps
import os
#用户头像上传的保存地址
#UPLOAD_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),r'static\limg\faceimg')
#生产liunx
UPLOAD_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),r'static/limg/faceimg')
#买卖记录肉牛保存的地址
#SALES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),r'static\limg\cattleimg')
#生产地址
SALES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),r'static/limg/cattleimg')
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
        if "lcshome" not in session:
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
        print("提交的数据是：",data)
        user = Users.query.filter_by(account=data["account"]).first()
        print('数据库中的姓名1',user.name)
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
        session["lcshome"] = "q1993"  #此项防止存在管理员的缓存导致可以访问其他页面
        #写入会员登录日志
        userlog =Userlog(
            account=user.account,
            ip = request.remote_addr,
            op='用户 %s 登录' % (session['account'])
        )
        db.session.add(userlog)
        db.session.commit()

        return redirect(url_for("home.index",page=1))
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
        if data['face'] != None:
            # 获取上传文件的文件名;
            filena = form.face.data.filename
            # print(str(filename))
            filename = uuid.uuid4().hex + filena
            # 将上传的文件保存到服务器;
            form.face.data.save(os.path.join( UPLOAD_PATH, filename))
            print("touxiang 上传成功")
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
            flash("注册成功,请点登录","ok")
        else:
            filename = str(random.randint(0,5)) + '.png'
            user = Users(
                account=data['userId'],
                name=data['userName'],
                pwd=generate_password_hash(data['userpassword']),
                sex=data['sex'],
                weixin=data['weixin'],
                birthday=data['birthday'],
                phone=data['userphone'],
                address=data['userAddress'],
                face=filename,
                info=data['info'],
                uuid=uuid.uuid4().hex
            )
            db.session.add(user)
            print("保存数据")
            db.session.commit()
            flash("注册成功,请登录", "ok")
        return redirect(url_for('home.login'))
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
    userlog = Userlog(
        account=session['account'],
        ip=request.remote_addr,
        op = '用户 %s 退出' % (session['account'])
    )
    db.session.add(userlog)
    db.session.commit()
    # 退出时 把本地缓存的seesion密码去掉
    session.pop("username", None)
    session.pop("userface", None)
    session.pop("account", None)
    session.pop("lcshome", None)
    return redirect(url_for("home.login"))

'''=====首页====='''
#首页
@home.route("/index/<int:page>/",methods=["GET","POST"])
@home_login_req
def index(page=None ):
    if page is None:
        page = 1
    #获取公告 状态为1启用状态的公告数据
    notice = Notice.query.filter_by(state = 1 ).order_by(Notice.priority).paginate(page=page,per_page=10)

    return render_template("home/index.html",notice=notice)

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
#修改买卖记录
@home.route("/cattle_up/<int:id>/",methods=["GET","POST"])
@home_login_req
def cattle_up(id = None):
    sales = Sales.query.get_or_404(int(id))
    form = CattleupFrom(
        cattlename=sales.cattlename,
        buyprice = sales.buyprice,
        sellprice=sales.sellprice,
        buyweight=sales.buyweight,
        sellweight=sales.sellweight,
        buyunitprice=sales.buyunitprice,
        sellunitprice=sales.sellunitprice,
        buyday = sales.buyday,
        sellday=sales.sellday,
        buynum=sales.buynum,
        sellnum=sales.sellnum,
        buycity=sales.buycity,
        sellcity=sales.sellcity,
        buycontatcs=sales.buycontatcs,
        sellcontatcs=sales.sellcontatcs,
        buyphone=sales.buyphone,
        sellphone=sales.sellphone
    )
    if form.validate_on_submit():
        print("进入修改买卖记录")
        data = form.data
        print("buyprice ", data['buyprice'])
        result = Sales.query.filter_by(id=id).first()
        if data['buyprice'] != "":
            result.buyprice = data['buyprice']
        else:
            result.buyprice = 0
        if data['sellprice'] != "":
            result.sellprice = data['sellprice']
        else:
            result.sellprice = 0
        if data['cattlename'] != "":
            result.cattlename = data['cattlename']
        if data['buyweight'] != "":
            result.buyweight = data['buyweight']
        else:
            result.buyweight = 0
        if data['sellweight'] != "":
            result.sellweight = data['sellweight']
        else:
            result.sellweight = 0
        if data['buyunitprice'] != "":
            result.buyunitprice = data['buyunitprice']
        else:
            result.buyunitprice = 0
        if data['sellunitprice'] != "":
            result.sellunitprice = data['sellunitprice']
        else:
            result.sellunitprice = 0
        if data['buyday'] != "":
            result.buyday = data['buyday']
        else:
            result.buyday = ''
        if data['sellday'] != "":
            result.sellday = data['sellday']
        else:
            result.sellday = ''
        if data['buynum'] != "":
            result.buynum = data['buynum']
        else:
            result.buynum = ''
        if data['sellnum'] != "":
            result.sellnum = data['sellnum']
        else:
            result.sellnum = ''
        if data['buycity'] != "":
            result.buycity = data['buycity']
        else:
            result.buycity = ''
        if data['sellcity'] != "":
            result.sellcity = data['sellcity']
        else:
            result.sellcity = ''
        if data['buycontatcs'] != "":
            result.buycontatcs = data['buycontatcs']
        else:
            result.buycontatcs = ''
        if data['sellcontatcs'] != "":
            result.sellcontatcs = data['sellcontatcs']
        else:
            result.sellcontatcs = ''
        if data['buyphone'] != "":
            result.buyphone = data['buyphone']
        else:
            result.buyphone = ''
        if data['sellphone'] != "":
            result.sellphone = data['sellphone']
        else:
            result.sellphone = ''

        db.session.commit()
        print("提交数据库开始修改买卖记录数据")
        flash("修改成功,请点击返回去查看", "ok")
        oplog = Oplog(
            account=session["account"],
            ip=request.remote_addr,
            op="修改买卖记录 %s " %( id )
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('home.cattle_list',page=1))

    return render_template("home/cattle_up.html", form =form )
#查看买卖记录
@home.route("/cattle_view/<int:id>/",methods=["GET"])
@home_login_req
def cattle_view(id = None):
    sales = Sales.query.get_or_404(int(id))
    if sales.buycity != "":
        buycity=sales.buycity
    else:
        buycity='XXX'
    if sales.sellcity != "":
        sellcity=sales.sellcity
    else:
        sellcity='XXX'
    #肉牛简介分析封装字典格式返回 前端 肉牛简介显示
    beefinfobuy="此牛于 %s 日，在 %s 购买。以 %s 元计单价 %s 元/公斤购买成功。" %(sales.buyday,buycity,sales.buyprice,sales.buyunitprice)
    beefinfosell="此牛于 %s 日，在 %s 出售。以 %s 元计单价 %s 元/公斤出售成功。" %(sales.sellday,sellcity,sales.sellprice,sales.sellunitprice)
    beefinfo = {}
    if sales.sellprice == None:
        beefinfo['buy'] = beefinfobuy
    else:
        beefinfo['buy'] = beefinfobuy
        beefinfo['sell'] = beefinfosell

    return render_template("home/cattle_view.html", sales=sales,beefinfo=beefinfo)

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
    form = BuycattleFrom(cattleid='2001')
    if form.validate_on_submit():
        print("触发添加肉牛")
        data = form.data
        print("接收到的表单数据为：",data)
        if data['buyweight'] != '':
            buyweight = data['buyweight']
            buyunitprice = format(float(data['buyprice']) / (float(buyweight) * 2), '.2f')
        else:
            buyunitprice = data['buyprice']
            buyweight = None
            print("否则buyweight=", buyweight)
        if data['buyfreight'] != '':
            buyfreight = data['buyfreight']
        else:
            buyfreight = None
            print("否则buyweight=", buyweight)
        print("接收添加购买记录的单价",buyunitprice)
        if data['buycattlefild'] != None:
            # 获取上传文件的文件名;
            filena = form.buycattlefild.data.filename
            # print(str(filename))
            filename = uuid.uuid4().hex  + filena
            # 将上传的文件保存到服务器;
            form.buycattlefild.data.save(os.path.join( SALES_PATH, filename))
        else:
            filename =  'no.png'

        sales = Sales(
            account = session['account'],
            cattleid=data['cattleid'],
            cattlename=data['cattlename'],
            buyprice=data['buyprice'],
            buyweight=buyweight,
            buyunitprice=buyunitprice,
            buyday=data['buyday'],
            buynum=data['buynum'],
            buycontatcs=data['buycontatcs'],
            buyphone=data['buyphone'],
            buycity=data['buycity'],
            buyfreight=buyfreight,
            buycattlefild=filename,
            sellcattlefild='no.png',
            remarks=data['remarks']
            )
        db.session.add(sales)
        db.session.commit()
        flash("添加购买记录成功", "ok")
        oplog =Oplog(
            account=session["account"],
            ip= request.remote_addr,
            op="添加购买记录:肉牛id：%s ，肉牛昵称： %s ，购买总价：%s，购买时体重： %s " %(data['cattleid'],data['cattlename'],data['buyprice'],data['buyweight'])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('home.cattle_list',page=1))
    return render_template("home/buycattle_add.html",form=form)
#添加出栏记录
@home.route("/sellcattle_add/<int:id>/",methods=["GET","POST"])
@home_login_req
def sellcattle_add(id=None):
    form = SellcattleFrom()
    beef = Sales.query.get_or_404(int(id))
    if form.validate_on_submit():

        print("触发添加肉牛出栏记录")
        data = form.data
        if data['sellweight'] != '':
            sellweight = data['sellweight']
            sellunitprice = format(float(data['sellprice']) / (float(data['sellweight']) * 2), '.2f')
        else:
            sellunitprice = data['sellprice']
            sellweight = None
        if data['sellfreight'] != '':
            sellfreight = data['sellfreight']
        else:
            sellfreight = None

        print("接收到的表单数据为：", data)
        if data['sellcattlefild'] != None:
            # 获取上传文件的文件名;
            filena = form.sellcattlefild.data.filename
            # uuid唯一值 + 文件名 构成这个图片唯一名字
            filename = uuid.uuid4().hex + filena
            # 将上传的文件保存到服务器;
            form.sellcattlefild.data.save(os.path.join( SALES_PATH, filename))
        else:
            filename = 'no.png'
        result = Sales.query.filter_by(id =int(id)).first()
        result.sellprice = data['sellprice']
        result.sellweight = sellweight
        result.sellunitprice = sellunitprice
        result.sellday = data['sellday']
        result.sellnum = data['sellnum']
        result.sellcontatcs = data['sellcontatcs']
        result.sellphone = data['sellphone']
        result.sellcity = data['sellcity']
        result.sellfreight = sellfreight
        result.sellcattlefild = filename
        db.session.commit()
        flash('添加出栏记录成功', "ok")
        oplog = Oplog(
            account=session["account"],
            ip=request.remote_addr,
            op="添加出栏记录:肉牛数据id：%s ，出售总价：%s，出售时体重： %s " %( id,data['sellprice'],data['sellweight'])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('home.cattle_list',page=1))
    return render_template("home/sellcattle_add.html",form=form,beef=beef)

'''=====会员管理====='''
#查看会员详情
@home.route("/user_view/<int:id>/",methods=["GET"])
@home_login_req
def user_view(id=None):
    #get_or_404获取指定id的数据
    user  = Users.query.get_or_404(int(id))
    return render_template("home/user_view.html",user=user)

#修改个人资料
@home.route("/userUpdate/",methods=["GET","POST"])
@home_login_req
def userUpdate():
    form = UserupFrom()
    if form.validate_on_submit():
        print("触发修改个人信息")
        data = form.data
        result = Users.query.filter_by(account=session['account']).first()
        if data['weixin'] != '':
            print("更新weixin")
            result.weixin = data['weixin']
        if data['birthday'] != '':
            print("更新birthday")
            result.birthday = data['birthday']
        if data['userAddress'] != '':
            print("更新userAddress")
            result.userAddress = data['userAddress']
        if data['face'] != None:
            print("更新face")
            # 获取上传文件的文件名;
            filena = form.face.data.filename
            # print(str(filename))
            filename = uuid.uuid4().hex + filena
            # 将上传的文件保存到服务器;
            form.face.data.save(os.path.join(UPLOAD_PATH, filename))
            print("图片上传成功")
            result.face = filename
            session["userface"] = filename
        if data['info'] != '':
            print("更新info")
            result.info = data['info']
        if data['userphone'] != '':
            print( "获取的手机号：",data['userphone'])
            result.phone = data['userphone']
        db.session.commit()
        print("提交数据库开始修改数据")
        flash("修改成功,请点击返回去查看", "ok")

        oplog = Oplog(
            account=session["account"],
            ip=request.remote_addr,
            op="修改个人信息 "
        )
        db.session.add(oplog)
        db.session.commit()

    return render_template("home/userUpdate.html",form=form)

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








