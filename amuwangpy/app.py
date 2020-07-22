from flask import Flask,url_for,request,render_template
import pymysql
from lib import sqlwork

import datetime
app = Flask(__name__)
#数据库查询功能，传入sql语句即可
def sqldo(sql):
	# 打开数据库连接
	print("开始执行数据库操作")
	db =  pymysql.connect("39.106.14.148","root","AMU19930316amu","amuwang")     #使用 cursor() 方法创建一个游标对象 cursor
	#print("链接数据库")
	cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
	sq=sql
	print("连接数据库成功")
	# 使用 execute()  方法执行 SQL 查询
	#print("链接城功，开始执行sql语句")
	cursor.execute(sq)
	# 使用 fetchone() 方法获取单条数据.
	data = cursor.fetchone()
	#print("查询结束，查询结果为：",data)
	#关闭数据库链接
	db.close()
	return data
def sqlin(sql):
	# 打开数据库连接
	#print("开始执行数据库操作")
	db =  pymysql.connect("39.106.14.148","root","AMU19930316amu","amuwang")     #使用 cursor() 方法创建一个游标对象 cursor
	print("开始添加注册信息数据库")
	cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
	sq=sql
	# 使用 execute()  方法执行 SQL 查询
	print("链接数据库城功，开始执行sql添加账户语句")
	cursor.execute(sq)
	print('提交sql')
	db.commit()
	# 使用 fetchone() 方法获取单条数据.
	data = cursor.fetchone()
	print("提交成功开始查询是否添加，查询结果为：",data)
	#关闭数据库链接
	db.close()
	return data


'''入口'''
@app.route('/')
def login():
    return render_template('login.html')
'''主页'''
@app.route('/index')
def index():
    data=request.args
    print('账号', data['name'])
    print('密码',data['pwd'])
    sql ="select * from user where name ="+ "'"+data['name']  +"'"  #根据name 查数据库是否存在这个账户 如果存在则返回所有列表
    #sql="select * from user where name = 'amu'"
    print('查询语句是',sql)
    #try:
    print("ks")
    das = sqldo(sql)   #执行sql查找数据
    print("查询结果为", das)

    # except:
    #     # 数据库异常返回5000
    #     print("数据库查询异常,错误码：11110",)
    #     return render_template('500.html',ma='11110')

    if das == None:
        #没有查到该用户 返回注册界面请注册
        return  render_template('login.html',tishi="该用户未注册，请先注册再登入。")
    #elif das[1] == data['pwd']: #校验数据库结果索引为1 的字段的值 也就是密码

    elif data['pwd'] == das['pwd']:
        print("密码正确开始获取公告")
        # 用户名密码都正确返回首页，并返回其用户名das[2]
        sqla = 'select * from gonggao where ID ="1" '    #并查询公告数据库中的公告展示在首页

        #gonggao = sqldo(sqla)
        gonggao = sqldo(sqla)
        print("查询出的公告为:",gonggao)
        print("公告获取完成并加入,开始获取阿木尘工具IP")
        amuchensql = "select ip from ipconfig where name = 'amuchen'"
        sqlamuchen = sqldo(amuchensql)
        amuchenip = sqlamuchen['ip']
        print("阿木尘ip",amuchenip)

        return render_template('index.html', names=das['names'], name=das["name"], pwd=das["pwd"], gonggao=gonggao['content'],amuchen=amuchenip)
        #return render_template('index.html', names=das[2],name=das[0],pwd=das[1])
    else:
        print('密码错误')
        # 密码错误 0001
        return  render_template('login.html', tishi='密码错误')

'''返回测试TDP专页'''
@app.route('/TDP')
def TDP():
    fanhui=request.args
    print('接收到的tdp用户是',fanhui['name'])
    return render_template('qtcs.html',fhuiname=fanhui["name"],fhuipwd=fanhui["pwd"])

'''判断是否注册'''
@app.route('/isnoname')
def isnoname():
    print('查询用户是否被注册')
    da=request.form
    print('查询用户是',da['name'])

    sql = "select * from user where name =" + "'" + da['name'] + "'"
    try:
        das = sqldo(sql)   #执行sql查找数据
    except:
        # 数据库异常返回5000
        return render_template('500.html',ma='11111')
    if das == None:
        #没有查到该用户 返回注册界面请注册
        return  render_template(isnoma="2000")
    else:
        return render_template(isnoma="5000")

@app.route('/zhuce')
def zhuce():
    print('注册接口')
    da=request.args
    print('注册的用户是',da['name'])
    try:
        print('查询该用户是否被注册')
        sql = "select * from user where name =" + "'" + da['name'] + "'"
        das = sqldo(sql)   #执行sql查找数据
    except:
        # 查询数据库是否有注册账号时数据库异常返回
        return render_template('500.html',ma='11111')
        #该用户未注册，注册成功，添加表数据
    if das == None:
        try:
            print('未注册添加表数据')
            sql = "insert into user(name, pwd,names,indata) values('"+da['name'] + "','" + da['pwd'] +"','"+"','"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"')"
            print('执行添加sql',sql)
            sqlin(sql)  # 执行添加数据
            print("查询是否添加成功")
            sql = "select * from user where name =" + "'" + da['name'] + "'"
            print("查询语句",sql)
            da = sqldo(sql)
            print('查询执行完毕，判断是否为空',da)
            if da == None:
                #查不到添加数据 添加失败返回注册失败业
                return "返回注册失败页，失败信息数据库添加数据失败"
            else:
                return render_template('login.html', tishi="注册成功，请登入。")
                #return render_template("index.html",names=da[0])
        except:
            # 注册添加数据时数据库发生异常返回码11112
            return render_template('500.html', ma='11112')
    else:
        #否则该用户已被注册，返回已被注册页面
        return render_template('login.html', tishi='该用户已被注册过，请登入或重新注册。')
'''验证注册码是否存在'''


@app.route('/ifcode')
def ifcode():
    print('执行注册码是否存在接口')
    data = request.args
    print('输入的验证码为', data['code'])
    sql = "select * from code where code =" + "'" + data['code'] + "'"  #查询该验证码是否存在
    a=sqldo(sql)
    if a[1]==1:
        print('验证码查询成功存在',a)
        return '1'   #如果存在这个验证码 返回的时 数字 1
    else:
        return



if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port= 2048)
    #app.run(debug=True, host='0.0.0.0', port=8100) #生产