import requests

from app.models import User,Weight,Addtechnology
from . import niushenqi
from flask import request, json
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

#牛神器--获取养殖技术文章
@niushenqi.route('/technology',methods=['POST'])
def technology():
    print("触发获取养殖技术文章接口")
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    if data["page"] is None:
        page = 1
    else:
        page = int(data["page"])
    # 按时间倒序查询 使用自带分页助手paginate返回页码和按多少页分页
    page_data = Addtechnology.query.order_by(Addtechnology.addriqi.desc()).all()
    #page_data = Addtechnology.query.order_by(Addtechnology.addriqi.desc()).paginate(page=page, per_page=10)  # 页码中的数据
    res = []
    for i in page_data:
        print(121212)
        res.append(i.to_json())
    #for i in page_data:
        # des = {}
        # des['viewid'] = page_data.items[i].id
        # des['imgsrc'] = i.imgsrc
        # des['url'] = i.url
        # des['watch'] = i.watch
        # des['like'] = i.like
        # des['pinglun'] = i.pinglun
        # des['title'] = i.title
        # des['desc'] = i.desc
        #res.append(des)
    ress={}
    ress["items"] = res
    print('获取文章列表响应数据res:', ress)
    return json.dumps(ress,ensure_ascii=False)

#牛神器--获取openid --登录注册
@niushenqi.route('/getopenid',methods=['POST'])
def getopenid():
    datas = eval(json.dumps(request.form))   # 获取接收到请求的数据
    print('登录login接口：接收的数据data:', datas)
    '''根据code获取用户openid'''
    APPID="wx813032796757d94f"                  #小程序appid
    SECRET="e6f53372ac41c118e9e4882834af766f"    #小程序唯一密钥
    CODE=datas["code"]
    print("请求微信获取opedid")
    url="https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" %(APPID,SECRET,CODE)
    req = requests.get(url) #获取用户openid
    print("打印返回的opid",req.text)
    req = json.loads(req.text)
    openid = req["openid"]
    session_key = req["session_key"]
    #查询数据库该用户是否注册
    usercount = User.query.filter_by(openid=openid).count()
    if usercount == 1:  #如果这个用户存在 则更新个人信息
        print("存在这个用户，开始更新数据")
        use = User.query.filter_by(openid=openid).first()
        use.nickName = datas['nickName'],
        use.avatarUrl = datas['avatarUrl'],
        use.gender = datas['gender'],
        use.country = datas['country'],
        use.province = datas['province'],
        use.city = datas["citys"],
        db.session.commit()  # 提交
        print('登录login接口：老用户直接更新用户信息:')
    else:
        #print("nickName:"+ datas["nickName"]+"avatarUrl:"+data["avatarUrl"]+"gender:"+data["gender"])
        user=User(
            openid = openid,
            nickName=datas['nickName'],
            avatarUrl=datas['avatarUrl'],
            gender=datas['gender'],
            country=datas['country'],
            province=datas['province'],
            city = datas["citys"],
            usePoint=10
        )
        db.session.add(user)
        db.session.commit()
        print('获取openid接口：新用户添加成功:')
    res = {}
    res["openid"]=openid
    res["session_key"] = session_key

    print("获取openid响应数据",res)
    return res






























