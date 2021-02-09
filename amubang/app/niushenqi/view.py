import uuid
import time
import random

import requests

from app.models import User, Weight, Addtechnology,News
from . import niushenqi
from flask import request, json,render_template,jsonify,send_from_directory,make_response
from app import db
import os
from .lib import return_img_stream  #保存图片
#测试本地地址
IMGURL_PATH = 'http://localhost:2048/niushenqi/getimg/'    #获取图片的前缀域名
IMG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), r'static\niushenqi\images\fabu\\')    #图片保存位置

#是生产地址
#IMGURL_PATH = 'https://we.amuqitan.cn/niushenqi/getimg/'   #获取图片的前缀域名
#IMG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), r'static/niushenqi/images/fabu/')  #图片保存位置
@niushenqi.route('/index')
def ceshi():
    return '测试妞神器项目与主页'\

@niushenqi.route('/getimg/<name>/',methods=['POST','GET'])
def Getimg(name=None):
    #传入图片名字 返回图片

    if name is None:
        name = 1
    print("获取的图片名称是",name)
    response = make_response(send_from_directory(IMG_PATH, name, as_attachment=True))
    return response


# 体重估算
@niushenqi.route('/weightestimation', methods=['POST'])
def weightestimation():
    print("触发体重估算接口")
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    xiongwei = float(data["xiongwei"])
    index = data["index"]
    print("触发体重估算接口，接收数据 胸围 %s,体型 %s " % (xiongwei, index))
    weight = Weight.query.filter_by(cm=round(xiongwei)).first()  # 查询出胸围对应的数据
    if index == '0':  # 正常
        tall = weight.average
    elif index == '1':
        tall = weight.fat
    else:
        tall = weight.thin
    res = {}
    res['tall'] = tall
    return res


# 牛神器--获取养殖技术文章
@niushenqi.route('/technology', methods=['POST'])
def technology():
    print("触发获取养殖技术文章接口")
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    if data["page"] is None:
        page = 1
    else:
        page = int(data["page"])
    # 按时间倒序查询 使用自带分页助手paginate返回页码和按多少页分页
    page_data = Addtechnology.query.order_by(Addtechnology.addriqi.desc()).all()
    # page_data = Addtechnology.query.order_by(Addtechnology.addriqi.desc()).paginate(page=page, per_page=10)  # 页码中的数据
    res = []
    for i in page_data:
        print(121212)
        res.append(i.to_json())
    # for i in page_data:
    # des = {}
    # des['viewid'] = page_data.items[i].id
    # des['imgsrc'] = i.imgsrc
    # des['url'] = i.url
    # des['watch'] = i.watch
    # des['like'] = i.like
    # des['pinglun'] = i.pinglun
    # des['title'] = i.title
    # des['desc'] = i.desc
    # res.append(des)
    ress = {}
    ress["items"] = res
    print('获取文章列表响应数据res:', ress)
    return json.dumps(ress, ensure_ascii=False)


# 牛神器--获取openid --登录注册
@niushenqi.route('/getopenid', methods=['POST'])
def getopenid():
    datas = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('登录login接口：接收的数据data:', datas)
    '''根据code获取用户openid'''
    APPID = "wx813032796757d94f"  # 小程序appid
    SECRET = "e6f53372ac41c118e9e4882834af766f"  # 小程序唯一密钥
    CODE = datas["code"]
    print("请求微信获取opedid")
    url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (
    APPID, SECRET, CODE)
    req = requests.get(url)  # 获取用户openid
    print("打印返回的opid", req.text)
    req = json.loads(req.text)
    openid = req["openid"]
    session_key = req["session_key"]
    # 查询数据库该用户是否注册
    usercount = User.query.filter_by(openid=openid).count()
    if usercount == 1:  # 如果这个用户存在 则更新个人信息
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
        # print("nickName:"+ datas["nickName"]+"avatarUrl:"+data["avatarUrl"]+"gender:"+data["gender"])
        user = User(
            openid=openid,
            nickName=datas['nickName'],
            avatarUrl=datas['avatarUrl'],
            gender=datas['gender'],
            country=datas['country'],
            province=datas['province'],
            city=datas["citys"],
            usePoint=10
        )
        db.session.add(user)
        db.session.commit()
        print('获取openid接口：新用户添加成功:')
    res = {}
    res["openid"] = openid
    res["session_key"] = session_key

    print("获取openid响应数据", res)
    return res


# 牛神奇--上传图片
@niushenqi.route('/upimg', methods=['POST', 'GET'])
def Upimg():
    print("进入上传图片接口")

    fn = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '_%d' % random.randint(0, 100) + '.png'
    avata = request.files.get('img')
    print("上传图片的图片ID信息",eval(json.dumps(request.form)))
    # new = compression_img(avata)
    pic_dir = os.path.join(IMG_PATH, fn)
    avata.save(pic_dir)
    # folder = photosSet.url(hash_openid)
    img_dir = fn + "/"  # 返回图片名字  案后其他接口调用这个图片名字获取图片地址
    print("上传图片接口返回的数据:",img_dir)
    return img_dir

#牛神奇--删除指定名字的图片
@niushenqi.route('/delimg', methods=['POST', 'GET'])
def Delimg():

    data = eval(json.dumps(request.form))  # 获取接收到亲求的数据
    print("进入删除指定名字的文件接口", data)
    imgname = data["delimgname"][:-1]
    file_name = IMG_PATH + imgname
    if os.path.exists(file_name):
        os.remove(file_name)
        print('成功删除文件:', file_name)
        res = "0"
    else:
        print('未找到此文件:', file_name)
        res = "1"
    return res

# 牛神奇--发布供求消息
@niushenqi.route('/newsrelease', methods=['POST'])
def Newsrelease():
    data = eval(json.dumps(request.form))  # 获取接收到亲求的数据
    print('发布供求接口Newsrelease接口:', data)
    if data['imgurl_01'] == 'undefined':
        imgurl_01 = data['imgurl_01']  # 文章附加的图片
    else:
        imgurl_01 = IMGURL_PATH + data['imgurl_01']  # 文章附加的图片
    if data['imgurl_02'] == 'undefined':
        imgurl_02 = data['imgurl_02']  # 文章附加的图片
    else:
        imgurl_02 = IMGURL_PATH + data['imgurl_02']  # 文章附加的图片
    if data['imgurl_03'] == 'undefined':
        imgurl_03 = data['imgurl_03']  # 文章附加的图片
    else:
        imgurl_03 = IMGURL_PATH + data['imgurl_03']  # 文章附加的图片
    if data['imgurl_04'] == 'undefined':
        imgurl_04 = data['imgurl_04']  # 文章附加的图片
    else:
        imgurl_04 = IMGURL_PATH + data['imgurl_04']  # 文章附加的图片
    if data['imgurl_05'] == 'undefined':
        imgurl_05 = data['imgurl_05']  # 文章附加的图片
    else:
        imgurl_05 = IMGURL_PATH + data['imgurl_05']  # 文章附加的图片
    if data['imgurl_06'] == 'undefined':
        imgurl_06 = data['imgurl_06']  # 文章附加的图片
    else:
        imgurl_06 = IMGURL_PATH + data['imgurl_06']  # 文章附加的图片
    try:
    # 保存发布求助数据
        xiaoxi = News(
                userimg=data['userimg'],  # 发布者的头像地址
                username=data['username'],  # 发布者的名字
                openid=data['openid'],  # 发布者的名字
                select_val=data['select_val'],  # 发布的消息类型
                title=data['title'],  # 发布者的文章标题
                neirong=data['neirong'],  # 发布者的文章内容
                dizhi=data['dizhi'],  # 发布者的地址
                haoma=data['haoma'],  # 发布者的电话
                imgurl_01=imgurl_01,  # 文章附加的图片
                imgurl_02=imgurl_02,  # 文章附加的图片
                imgurl_03=imgurl_03,  # 文章附加的图片
                imgurl_04=imgurl_04,  # 文章附加的图片
                imgurl_05=imgurl_05,  # 文章附加的图片
                imgurl_06=imgurl_06,  # 文章附加的图片
                pinglun= 0,  # 文章初始评论数
                dianzan=0,  # 文章初始点赞数
                liulianliang=0,  # 文章初始浏览数
                star=0  # 文章有效性

            )
        db.session.add(xiaoxi)
        db.session.commit()
        print("保存供求数据成功")
        respCode = '0'
    except BaseException:
        respCode = '1'
        print(BaseException)
    res = {}
    res['respCode'] = respCode
    print('发布供求消息Newsrelease接口返回响应数据res:', res)
    return res

# 牛神奇--获取供求消息
@niushenqi.route('/getmessage', methods=['POST'])
def Getmessage():
    data = eval(json.dumps(request.form))  # 获取接收到亲求的数据
    print('获取消息Getmessage:', data)
    # uslongitude = data['longitude']  # 用户当前经度
    # uslatitude = data['latitude']  # 用户当前纬度
    if data['openid'] !="":
        message = News.query.filter_by(star=0,openid=data["openid"]).order_by(News.addriqi.desc()).all()  # 按发布日期倒叙排序 有效数据
    else:
        message = News.query.filter_by(star=0).order_by(News.addriqi.desc()).all() #按发布日期倒叙排序 有效数据
    res = []
    for i in message:
        des = {}
        des["userimg"] = i.userimg,
        des["username"] = i.username,
        des["haoma"] = i.haoma,
        des["id"] = i.id,
        des["select_val"] = i.select_val,
        des["titles"] = i.title,
        des["imgurl_01"] = i.imgurl_01,
        des["imgurl_02"] = i.imgurl_02,
        des["imgurl_03"] = i.imgurl_03,
        des["dianzan"] = i.dianzan,
        des["dizhi"] = i.dizhi

        # des['taskId'] = i.taskId
        #des['srvDistance'] = geodistance(uslongitude, uslatitude, des['longitude'],
        #des['latitude'])  # 米数KM 传入经度1 纬度1 经度2 纬度2
        res.append(des)
    res = json.dumps(res, ensure_ascii=False)
    print('获取消息接口响应数据res:', res)
    return res

# 牛神奇--获取供求消息详情
@niushenqi.route('/getmessages', methods=['POST'])
def Getmessages():
    data = eval(json.dumps(request.form))  # 获取接收到亲求的数据
    print('获取消息详情Getmessages:', data)
    # uslongitude = data['longitude']  # 用户当前经度
    # uslatitude = data['latitude']  # 用户当前纬度
    message = News.query.filter_by(id = data["id"]).all() #查找指定id的供求信息详情
    res = []
    for i in message:
        des = {}
        des["userimg"] = i.userimg,
        des["username"] = i.username,
        des["openid"] = i.openid,
        des["haoma"] = i.haoma,
        des["id"] = i.id,
        des["select_val"] = i.select_val,
        des["titles"] = i.title,
        des["neirong"] = i.neirong,
        des["imgurl_01"] = i.imgurl_01,
        des["imgurl_02"] = i.imgurl_02,
        des["imgurl_03"] = i.imgurl_03,
        des["imgurl_04"] = i.imgurl_04,
        des["imgurl_05"] = i.imgurl_05,
        des["imgurl_06"] = i.imgurl_06,
        des["liulanliang"] = i.liulanliang,
        des["dianzan"] = i.dianzan,
        des["dizhi"] = i.dizhi
        #des['srvDistance'] = geodistance(uslongitude, uslatitude, des['longitude'],
        #des['latitude'])  # 米数KM 传入经度1 纬度1 经度2 纬度2
        res.append(des)
        print("浏览量为：",i.liulanliang)
        messages = News.query.filter_by(id=data["id"]).first()  # 查找指定id的供求信息详情
        messages.liulanliang = i.liulanliang + 1
        db.session.add(messages)
        db.session.commit()
    res = json.dumps(res, ensure_ascii=False)
    print('获取消息接口详情响应数据res:', res)
    return res


# 牛神奇--搜索供求消息详情
@niushenqi.route('/luntansearch', methods=['POST'])
def Luntansearch():
    data = eval(json.dumps(request.form))  # 获取接收到亲求的数据
    print('获取消息详情搜索消息Luntansearch:', data)
    # uslongitude = data['longitude']  # 用户当前经度
    # uslatitude = data['latitude']  # 用户当前纬度
    search= "%" + data["search"] + "%"
    message = News.query.filter(News.title.like(search) ).all() #搜索包含关键字的标题
    res = []
    for i in message:
        des = {}
        des["userimg"] = i.userimg,
        des["username"] = i.username,
        des["haoma"] = i.haoma,
        des["id"] = i.id,
        des["select_val"] = i.select_val,
        des["titles"] = i.title,
        des["neirong"] = i.neirong,
        des["imgurl_01"] = i.imgurl_01,
        des["imgurl_02"] = i.imgurl_02,
        des["imgurl_03"] = i.imgurl_03,
        des["imgurl_04"] = i.imgurl_04,
        des["imgurl_05"] = i.imgurl_05,
        des["imgurl_06"] = i.imgurl_06,
        des["liulanliang"] = i.liulanliang,
        des["dianzan"] = i.dianzan,
        des["dizhi"] = i.dizhi
        #des['srvDistance'] = geodistance(uslongitude, uslatitude, des['longitude'],
        #des['latitude'])  # 米数KM 传入经度1 纬度1 经度2 纬度2
        res.append(des)
    if len(res) <1:
        res = json.dumps([{"select_val":""}], ensure_ascii=False)
    else:
        res = json.dumps(res, ensure_ascii=False)
    print('搜索数据响应数据res:', res)
    return res







# 牛神奇--获取供求消息的点赞数
@niushenqi.route('/like', methods=['POST'])
def Like():
    data = eval(json.dumps(request.form))  # 获取接收到亲求的数据
    print('获取点赞数Like:', data)

    message = News.query().filter_by(star=0).order_by(News.addriqi.desc()).all()  # 按发布日期倒叙排序 有效数据

    res = []
    for i in message:
        print(121212)
        res.append(i.to_json().dianzan)
    print('获取点赞数res:', res)
    return res