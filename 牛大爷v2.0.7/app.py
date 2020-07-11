from flask import Flask,render_template,url_for,request,jsonify,make_response
from lib import sqlwork
from lib import amucon
import json
import os

'''render_template：返回HTML模板文件的框架 返回的都是templates文件夹内的
url_for：使用url_for函数可以指引路径和反转路由
request：请求框架
jsonify：进行json转换的
make_response：响应数据包含天机cookie'''
app = Flask(__name__)

#打开网址返回登入界面
@app.route('/',methods=['POST', 'GET'])
def shouye():
    #当用户打开网址则跳到这里返回登入页面
    return render_template('login.html')
#用户登入接口 只接受post请求
@app.route('/login',methods=['POST'])
def login():
    data = request.form   #post请求用from获取
    print("接收数据",data,"请求模式是：",request.method)
    #如果请求数据长度小于1，证明浏览器为发送有效请求值
    if len(data) <= 1:
        print ('请求为空')
        # 接收的请求时空则返回请求为空的码5001
        da = {"code": "5001"}
    #否则证明有数据
    else:
        #编写sql 利用凭借字符串的方式  查询数据库是否有这个用户名
        sql = 'select * from user where name="' + data['name'] + '"'
        print ('请求登入sql查询语句是', sql)
        #添加异常判断 以防调用数据库出错
        try:
            das = sqlwork.SQL("select",sql,'one')
            print("查询数据库是否存在的结果为", das)
        except:
            # 数据库异常返回5002
            da = {"code": "5002"}
            return jsonify(da)
        #查询的结果为空贼代表用户未注册
        if das == None:
            print('判断为空')
            # 用户未注册返回0002
            da = {"code": "0000"}
        #查询结果下标1是密码 如果密码等于请求的密码 证明账户密码正确 则进入
        elif das[1] == data['pwd']:
            # 登入成功2000
            #da = {"code": "2000"}
            da = {"code": "2000"}
            da = jsonify(da)
            rst = make_response(da)
            rst.set_cookie('name',das[0],max_age=60*60)  #cookie参数是键值对成对出现的，可以通过键名获取值，max_age=60 * 60 * 0.25代表cookie有效时间15分钟

            return rst

        #否则 那就是码错误
        else:
            print('密码错误')
            # 密码错误 0001
            da = {"code": "0001"}
    #转换成json
    #da=json.loads(da)
    da = jsonify(da)
    #添加跨域
    #rst.headers['Access-Control-Allow-Origin'] = "*"
    #rst.headers['Access-Control-Allow-Methods'] = "POST"

    print('响应数据是:',da )
    return da
#主页，传入用户名字
@app.route('/index',methods=['GET'])
def index():
    print("开始请求主页")
    if len(request.cookies)>=1:

        #da = request.args
        print("请求模式是：",request.method,"请求的cookie为:'",request.cookies,"'")
        #获取请求登入的cookie中的name变量
        names=request.cookies.get("name")
        #path = os.path.split(os.path.realpath(__file__))[0]
        return render_template('index.html',names=names)
    else:
        return render_template('login.html')


#够购买记录
@app.route('/Nodeindex')
def Nodeindex():
    ifcookie=amucon.Ifcookie()
    if ifcookie=='1':
        return render_template('login.html')
    biaoti=["序号",'用户名','购买批次号','肉牛编号','购买时间','购买总价','体重','运费','单价','购买地点','卖方信息','备注']
    shuju=goumaijilu()
    return render_template('Node/index.html',biaoti=biaoti,shuju=shuju)
@app.route('/Nodeadd') #添加数据
def Nodeadd():
    return render_template('Node/add.html')
@app.route('/Nodeedit') #编辑数据
def Nodeedit():
    return render_template('Node/edit.html')


#角色管理界面
@app.route('/Roleindex',methods=['GET'])
def Roleindex():
    return render_template('Role/index.html')
#用户管理界面
@app.route('/Userindex',methods=['GET'])
def Userindex():
    return render_template('User/index.html')
#菜单管理界面
@app.route('/Menuindex',methods=['GET'])
def Menuindex():
    return render_template('Menu/index.html')

'''此处重点接口'''
@app.route('/goumaijilu',methods=['POST'])
def goumaijilu():
    print("查询购买记录程序")
    ifcookie=amucon.Ifcookie()
    print("cookie判断结果",ifcookie)
    if ifcookie =='0':
        print("cookie验证通过开始构建查询购买记录sql")
        sql="select * from gmtable where name='"+ request.cookies.get('name')+"'"
        print('执行的sql',sql)
        data=sqlwork.SQL("select",sql)
    else:
        data="cookie已经失效"
    return   data

#保存新增记录
@app.route('/addgm',methods=['POST'])
def addgm():
    print("addgm添加购买记录程序")
    ifcookie=amucon.Ifcookie()
    print("cookie判断结果",ifcookie)
    if ifcookie ==1:
        return "cookie已经过期"
    #此界面传来的元祖
    print("读取接收的数据a")
    a=request.form
    print("接收的数据是",a)
    name=request.cookies.get("name")
    print("读取用户为", name)
    gmpicihao=a.get('gmpicihao')
    print("读取批次号", gmpicihao)
    bianhao=a.get('bianhao')
    gmdata=a['gmdata']
    gmzongjia=a['gmzongjia']
    gmtizhong=a['gmtizhong']
    gmyunfei=a['gmyunfei']
    gmdanjia=a['gmdanjia']
    gmdidian=a['gmdidian']
    gmlianxiren=a['gmlianxiren']
    beizhu=a['beizhu']
    print('备注是',beizhu)
    id=sqlwork.SQL('select','select MAX(id) from gmtable')
    print(id)
    id=id[0][0]+1
    print(id)
    print("保存新增购买信息接收成功，开始构建新增购买数据sql")
    #如果接收的请求为空 默认
    if len(a)<1:
        return '请求长度过短'
    else:
        sql="INSERT INTO gmtable(id,name,gmpicihao,bianhao,gmdata,gmzongjia,gmtizhong,gmyunfei,gmdanjia,gmdidian,gmlianxiren,beizhu) VALUES ("+str(id)+","+name+","+gmpicihao+","+bianhao+","+gmdata+","+gmzongjia+","+gmtizhong+","+gmyunfei+","+gmdanjia+","+gmdidian+","+gmlianxiren+","+beizhu+")"
        print("构建的插入sql",sql)
        sqlwork.SQL("inset",sql)
        print("插入sql执行完毕")

        ids=sqlwork.SQL('select','select MAX(id) from gmtable')
        if ids==id:
            print("添加数据库成功")
            return render_template('Node/index.html')
        else:
            return render_template('Node/add.html',tishi='保存失败')

















if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port= 1023)
