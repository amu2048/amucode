#导入app包 APP包中初始化已经定义蓝图启动 所以只要运行APP，run即可
from app import app

if __name__ == '__main__':
    #生产地址
    #app.run(debug=True,host='0.0.0.0',port=5003)
    # 测试地址
    app.run(debug=True,port=8080)












