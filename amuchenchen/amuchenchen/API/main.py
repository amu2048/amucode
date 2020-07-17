#阿木陈尘网后端接口，数据分析

from flask import Flask,url_for,request,render_template,jsonify,make_response
from amuchenchen.amuchenchen.API import api
#定义app实例化flask
app = Flask(__name__)

#路由
@app.route('/')
def index():
    print("开始调用数据获取")
    data = api.get_index_ison()


    data = jsonify(data)
    rst = make_response(data)
    #print("响应1：", rst)
    #print("ditu:",rst.json["chinaDatas"])
    #gongjulist = api.get_userfile()
    #print(gongjulist["nicheng"])
    #rst.set_cookie('name',max_age=60 * 60)  # cookie参数是键值对成对出现的，可以通过键名获取值，max_age=60 * 60 * 0.25代表cookie有效时间15分钟
    # 添加跨域
    rst.headers['Access-Control-Allow-Origin'] = "*"
    rst.headers['Access-Control-Allow-Methods'] = "get"

    return rst










if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port= 8202)
    #app.run(debug=True, host='0.0.0.0', port=8100) #生产
