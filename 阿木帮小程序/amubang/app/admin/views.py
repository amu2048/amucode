
from app.models import Helplist,User,Points
from . import admin
from flask import flash, session, request, json
from app import db
from .lib import createRandomString  #密钥生成器

#积分码生成接口 传如积分值 num  返回积分码 points
@admin.route('/jifen',methods=['POST','GET'])
def Exchange ():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('积分兑换码生成Exchange接口：接收的数据data:', data)
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
    return code
#积分码已交付 未给钱 把积分减掉  传入积分兑换码 code
@admin.route('/tuikuan',methods=['POST','GET'])
def tuikuan ():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('积分退款接口：接收的数据data:', data)
    code = data['code']  # 积分码
    points = Points.query.filter_by(code=code).first()
    if points is None:
        res = '1' #没有这个数据
    else:
        userinfo = User.query.filter_by(userid=points.userid).first()
        userinfo.usePoint = userinfo.usePoint - points.integral
        points.star = 1  #此积分数据状态无效
        points.zb = '退款减积分'
        db.session.add(points)
        db.session.commit()
        res = '0'
    print('退积分接口响应：',res)

    return res

