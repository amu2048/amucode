from flask import Flask,url_for,request,render_template
from amuchenchen.amuchenchen.API import api

#定义app实例化flask
app = Flask(__name__)

#路由
@app.route('/')
def login():
    pass
'''主页'''
@app.route('/index')
def index():
    #首页的地图上方的注册用户总计数量
    usernum = api.get_user_cont()
    #左上方的阿木奇谭简介
    jianjie = api.get_jianjie()
    #简介下面的功能点
    gnlist = api.get_gnlist()

    # 右侧工具栏的小工具
    gongjulist = api.get_gongjulist()

    # 奇谭令里的个人资料
    userfile = api.get_userfile()

    #获取bug列表数据
    buglist= api.get_buglist()
    return render_template('index.html',usernum=usernum,jianjie=jianjie,gnlist=gnlist,gongju=gongjulist,userfile=userfile,buglist=buglist)










if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port= 8201)
    #app.run(debug=True, host='0.0.0.0', port=8100) #生产










