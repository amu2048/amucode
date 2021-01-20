from app.models import Helplist,User,Points,Weight
from . import home
from flask import flash, session, request, json
from app import db
from  .cont import geodistance

#体重估算
@home.route('/weightestimation',methods=['POST'])
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

#登录注册
@home.route('/login',methods=['POST'])
def login():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('登录login接口：接收的数据data:', data)
    usercount = User.query.filter_by(userid=data['userId']).count()
    if usercount ==1:  #如果这个用户存在 那么不从写积分 更新数据
            user = User.query.filter_by(userid=data['userId']).first()
            user.userid=data['userId']
            user.userUrl=data['userUrl']
            user.gender=data['gender']
            user.province=data['province']
            user.city=data['city']
            user.country=data['country']
            db.session.commit()  # 提交
            print('登录login接口：老用户直接更新用户信息:')

    else: #否则 初始积分10
        user = User(
            userid=data['userId'],
            userUrl=data['userUrl'],
            gender=data['gender'],
            province=data['province'],
            city=data['city'],
            country=data['country'],
            usePoint = 10
        )
        db.session.add(user)
        db.session.commit()
        print('登录login接口：新用户添加成功:')


    return '002'



#添加求助数据
@home.route('/postNeed',methods=['POST'])
def postNeed():
    data = eval(json.dumps(request.form)) #获取接收到亲求的数据
    print('添加求助postNeed接口:',data)
    if data['srvCost'] =='':
        print("悬赏为空")
        srvCost = 0
    else:
        srvCost = int(data['srvCost'])
    #查询出用户积分
    user = User.query.filter_by(userid= data['userId']).first()
    #判断积分是否足够支付
    if user.usePoint < srvCost:
        print("用户积分不足")
        respCode = '101'  #积分不足
    else:
        try:
            #预先扣除发布者的积分
            user.usePoint = user.usePoint - srvCost
            db.session.commit()  # 提交
            #保存发布求助数据
            help = Helplist(
                    userId=data['userId'],
                    srvTitle=data['srvTitle'],
                    srvDesc=data['srvDesc'],
                    posDes=data['posDes'],
                    longitude=data['longitude'],
                    latitude=data['latitude'],
                    srvCost=srvCost,
                    srvType=data['srvType'],
                    urgent=data['urgent'],
                    endTime=data['endTime'],
                    userUrl=data['userUrl'],
                    star=99,
                    mobile=data['mobile']
                )
            db.session.add(help)
            db.session.commit()
            print("保存求助信息数据成功")
            respCode = '0'
        except BaseException:
            respCode = '1'
            print(BaseException)
    res={}
    res['respCode'] = respCode
    print('添加求助postNeed接口返回响应数据res:',res)
    return res

#获取求助列表
@home.route('/searchServiceNeeded',methods=['POST'])
def helplist():
    data = eval(json.dumps(request.form))  # 获取接收到亲求的数据
    print('获取求助列表helplist:',data)
    uslongitude =data['longitude']#用户当前经度
    uslatitude = data['latitude']  #用户当前纬度
    urgent = data['urgent']  #是否加急
    srvType =data['srvType']
    #如果选择紧急任务
    if urgent == 'true':
        print('选择紧急数据')
        list = Helplist.query.filter_by(urgent=urgent,star=99).all()
    else:
        if srvType == '全部' or srvType == 'undefined':
            print('全部')
            list = Helplist.query.filter_by(star=99).order_by(Helplist.srvCost.desc()).all()
        else:
            print('其他',srvType)
            list = Helplist.query.filter_by(srvType=srvType,star=99).order_by(Helplist.srvCost.desc()).all()
    res=[]
    for i in list:
        des={}
        des['taskId'] = i.id
        des['latitude']=i.latitude
        des['longitude'] = i.longitude
        des['posDes'] = i.posDes
        des['userId'] = i.userId
        des['userUrl'] = i.userUrl
        des['srvTitle'] = i.srvTitle
        des['srvDesc'] = i.srvDesc
        des['srvCost'] = i.srvCost
        #des['taskId'] = i.taskId
        des['srvDistance'] = geodistance( uslongitude,uslatitude,des['longitude'],des['latitude'])    #米数KM 传入经度1 纬度1 经度2 纬度2
        res.append(des)
    res = json.dumps(res, ensure_ascii=False)
    print('获取求助列表helplist响应数据res:',res)
    return res


#确认领取任务 立即帮助
@home.route('/acceptRequest',methods=['POST'])
def acceptRequest():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('领取任务acceptRequest接口:', data)
    taskId=data['taskId']  #领取的任务id
    helpid=data['helperId']    #领取任务的人
    helpurl = data['helpUrl']  # 领取任务的人
    print('领取人 %s 领取的任务id %s' %( helpid, taskId))
    try:
        help = Helplist.query.filter_by(id =taskId).first() #获取这个任务id人的联系电话
        mobile  = help.mobile
            #存入是否被领取
        help.star = 2  # 已被领取待确认中
        help.helpid = helpid  # 领取人ID
        help.helpurl = helpurl  # 领取人的头像
        db.session.commit() # 提交
        print('数据状态修改成待确认')
            #存好数据库 需要通知发布任务者 来确认任务
            #逻辑代谢
        status ='0'  #成功
    except BaseException:
        status = '1' #失败
    res = {}
    res['status'] = status
    res['mobile'] = mobile
    print('领取任务acceptRequest接口响应数据:', res)

    return res
#我帮助的数据
@home.route('/searchMyService',methods=['POST'])
def searchMyService():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('我帮助列表searchMyService接口:', data)
    userid = data['userId']
    myhelp = Helplist.query.filter_by(helpid=userid).order_by(Helplist.star).all()
    res = []
    for i in myhelp:
        des = {}
        des['taskId'] = i.id
        des['userId'] = i.userId
        des['srvTtitle'] = i.srvTitle
        des['srvDesc'] = i.srvDesc
        des['srvType'] = i.srvType
        des['mobile'] = i.mobile
        des['srvCost'] = i.srvCost
        des['star'] = i.star
        des['posDes'] = i.posDes
        res.append(des)
    res = json.dumps(res, ensure_ascii=False)
    print('我帮助列表searchMyService接口响应:', res)
    return res
#获取个人信息 我的积分
@home.route('/getUserInfo',methods=['POST'])
def getUserInfo():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('我的个人信息getUserInfo接口:', data)
    userid = data['userId']
    usercount = User.query.filter_by(userid=userid).count()

    if usercount == 1:
        user = User.query.filter_by(userid=data['userId']).first()
        res = {}
        res['userId'] = user.userid  #用户名字
        res['usePoint'] = user.usePoint  #用户剩余积分

    res = json.dumps(res, ensure_ascii=False)
    print('我的个人信息getUserInfo接口响应:', res)
    return res


#获取我的求助信息
@home.route('/searchMyNeed',methods=['POST'])
def searchMyNeed():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('获取我的求助searchMyNeed接口:', data)
    #我名下的求助信息 且状态不是100失效状态的数据
    userseek = Helplist.query.filter(Helplist.userId ==data['userId']).filter(Helplist.star != 100).order_by(Helplist.star).all()
    #userseek = Helplist.query.filter_by(userId=data['userId']).order_by(Helplist.star).all()

    res = []
    if len(userseek)>0:
        for i in userseek:
            des = {}
            des['taskId'] = i.id
            des['srvTtitle'] = i.srvTitle
            des['srvCost'] = i.srvCost
            des['srvDesc'] = i.srvDesc
            des['srvType'] = i.srvType
            des['startTime'] = i.endTime
            des['helplerId'] = i.helpid
            des['helplurl'] = i.helpurl
            des['star'] = i.star
            res.append(des)

    res = json.dumps(res, ensure_ascii=False)
    print('获取我的求助searchMyNeed接口响应:', res)
    return res
#确认他帮我
@home.route('/Confirmhelp',methods=['POST'])
def Confirmhelp():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('确认他帮助我Confirmhelp接口:', data)
    help = Helplist.query.filter_by(id=data['taskId']).first()
    try:

        help.star = 1  # 已确认 待完成
        db.session.commit()  # 提交
        respCode = '0'
    except BaseException:
        respCode = '1'
    res={}
    res['respCode'] = respCode
    print('确认他帮助我Confirmhelp接口响应:', res)
    return res


#不要他帮我
@home.route('/noConfirmhelp',methods=['POST'])
def noConfirmhelp():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('否认他帮助我noConfirmhelp接口:', data)
    help = Helplist.query.filter_by(id=data['taskId']).first()
    try:

        help.star = 99  # 拒绝他帮我 把数据从新让其他人领取
        help.helpid = '' #清空帮助人id
        help.helpurl = ''  # 清空帮助人头像
        db.session.commit()  # 提交
        respCode = '0'
    except BaseException:
        respCode = '1'
    res={}
    res['respCode'] = respCode
    print('否认他帮助我noConfirmhelp接口响应:', res)
    return res


#确认完成帮助 给予积分
@home.route('/confirmServiceComplete',methods=['POST'])
def confirmServiceComplete():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('确认完成帮助给予积分confirmServiceComplete接口:', data)
    help = Helplist.query.filter_by(id=data['taskId']).first()
    try:
        #把悬赏积分 加到 任务领取人的积分中
        user = User.query.filter_by(userid= help.helpid).first()
        user.usePoint = user.usePoint + help.srvCost

        help.star = 200 #任务已完成状态
        db.session.commit()  # 提交
        respCode = '0'
    except BaseException:
        respCode = '1'
    res={}
    res['respCode'] = respCode
    print('确认完成帮助给予积分confirmServiceComplete接口响应:', res)
    return res
#取消求助信息
@home.route('/cancelhelp',methods=['POST'])
def cancelhelp():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('取消求助信息cancelhelp接口:', data)
    help = Helplist.query.filter_by(id=data['taskId']).first()
    try:
        #把悬赏积分 回加到发布者积分处
        user = User.query.filter_by(userid= help.userId).first()
        user.usePoint = user.usePoint + help.srvCost

        help.star = 100 #任务已失效
        db.session.commit()  # 提交
        respCode = '0'
    except BaseException:
        respCode = '1'
    res={}
    res['respCode'] = respCode
    print('取消求助信息cancelhelp接口响应:', res)
    return res

#兑换码兑换积分 传入兑换码points 和 用户 userId
@home.route('/Pointsexchange',methods=['POST'])
def Pointsexchange():
    data = eval(json.dumps(request.form))  # 获取接收到请求的数据
    print('积分兑换Pointsexchange接口:', data)
    print(data['points'], data['userId'])
    points=data['points']
    #根据积分码查询
    Pointsexchange= Points.query.filter_by(code = points.replace(" ", "")).first()
    print(Pointsexchange)
    #如果这个积分码状态是无效的 直接返回响应码 0 有效 1 无效
    if Pointsexchange is None :
        print('无数据')
        respCode = '1'
    elif Pointsexchange.star != 0 :
        print('状态不是0 此积分无效')
        respCode = '2'
    else:
        # 获取用户信息
        userinfo = User.query.filter_by(userid= data['userId']).first()
        userinfo.usePoint = userinfo.usePoint + Pointsexchange.integral
        Pointsexchange.star = 1 # 已经兑换 把兑换码状态改变
        Pointsexchange.userid =  userinfo.userid
        db.session.commit()  # 提交
        respCode = '0'
    res={}
    res["respCode"]=respCode
    return res










