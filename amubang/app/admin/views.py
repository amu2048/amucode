
from app.models import Helplist,User,Points,Addtechnology
from . import admin
from flask import flash, session, request, json,render_template
from app import db
from .lib import createRandomString  #密钥生成器

#小程序后台界面
@admin.route('/',methods=['POST','GET'])
def index():

    return render_template('admin/index.html')

#积分列表
@admin.route('/jifenlist<int:page>',methods=['POST','GET'])
def jifenlist(page=None):
    if page is None:
        page = 1
    # 按时间倒序查询 使用自带分页助手paginate返回页码和按多少页分页
    page_data = Points.query.filter_by().order_by(Points.addriqi.desc()).paginate(page=page,per_page=10)


    return render_template('admin/jifenlist.html', page_data=page_data)

#积分码生成接口 传如积分值 num  返回积分码 points
@admin.route('/jifen',methods=['POST','GET'])
def jifen ():
    return render_template('admin/jifen.html')
#积分码生成接口 传如积分值 num  返回积分码 points
@admin.route('/Exchange',methods=['POST','GET'])
def Exchange ():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('积分兑换码生成Exchange接口：接收的数据data:', data)
    if len(data) <0:
        code = '请输入积分值'
    else:
        integral = data['num']  #积分值
        code = createRandomString(16)  #积分码
        points = Points(
            integral=integral,
            star = 0,
            code = code
        )
        db.session.add(points)
        db.session.commit()

    code = json.dumps(code, ensure_ascii=False)
    print('积分生成接口响应',code)
    return code
#积分码已交付 未给钱 把积分减掉  传入积分兑换码 code
@admin.route('/tuikuan/<int:id>',methods=['POST','GET'])
def tuikuan (id = None):
    print('积分退款接口：退款的id:', id)

    points = Points.query.filter_by(id=id).first()
    if points.userid is None:
        points.star = 3  #积分状态已失效
        points.zb = '管理员删除了这个兑换码'
        db.session.add(points)
        db.session.commit()
        res = '兑换码失效'
    else:
        userinfo = User.query.filter_by(userid=points.userid).first()
        userinfo.usePoint = userinfo.usePoint - points.integral
        points.star = 2  #此积分数据状态已退款
        points.zb = '退款减积分'
        db.session.add(points)
        db.session.commit()
        res = '退款成功'
    print('退积分接口响应：',res)

    return res

#添加养殖技术文章
@admin.route('/addtechnology',methods=['POST','GET'])
def addtechnology():
    pass