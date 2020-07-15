from flask import Flask,url_for,request,render_template
import pymysql
import datetime
#定义app实例化flask
app = Flask(__name__)

#路由
@app.route('/')
def login():
    pass
'''主页'''
@app.route('/index')
def index():
    return render_template('index.html')










if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port= 8201)
    #app.run(debug=True, host='0.0.0.0', port=8100) #生产










