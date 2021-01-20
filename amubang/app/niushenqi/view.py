from app.models import Helplist,User,Points,Weight
from . import niushenqi
from flask import flash, session, request, json
from app import db


@niushenqi.route('/')
def ceshi():
    return '测试妞神器项目与主页'
#体重估算
@niushenqi.route('/weightestimation',methods=['POST'])
def weightestimation():
    print("触发体重估算接口" )
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    xiongwei = float(data["xiongwei"])
    index = data["index"]
    print("触发体重估算接口，接收数据 胸围 %s,体型 %s " % (xiongwei, index))
    weight= Weight.query.filter_by(cm=round(xiongwei)).first()  #查询出胸围对应的数据
    if index == '0':  #正常
        tall = weight.average
    elif index == '1':
        tall = weight.fat
    else:
        tall = weight.thin
    res = {}
    res['tall'] = tall
    return res

#养牛技术列表
@niushenqi.route('/technologylist',methods=['POST'])
def technologylist():
    technologylist = Addtechnology.query.filter_by(star=0).all()  # 查询出养殖技术本周有效数据
    res = []
    for i in technologylist:
        des = {}
        des['viewid'] = i.id
        des['imgsrc'] = i.imgsrc
        des['count'] = i.count
        des['name'] = i.name
        res.append(des)
    res = json.dumps(res, ensure_ascii=False)
    return  res
































