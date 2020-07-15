#阿木陈尘网后端接口，数据分析

from flask import Flask,url_for,request,render_template,jsonify,make_response
from amuchenchen.API.api import ApiMain
#定义app实例化flask
app = Flask(__name__)

#路由
@app.route('/')
def index():
    data = ApiMain.get_index_ison()


    # print("调用index")
    # data = {
    #     #缺陷占比的统计图数据
    #     "ydata": [{"name": '黄笑',"value": 11},
    #              {"name": '郑龙旭',"value": 18},
    #              {"name": '王皓月',"value": 8},
    #              {"name": '孟祥含',"value": 5},
    #              {"name": '谢明科',"value": 2},
    #              {"name": '鱼跃',"value": 8},
    #              {"name": '陈思凡',"value": 6},
    #              {"name": '周洪宇',"value": 5},
    #              {"name": '文龙',"value": 7},
    #              {"name": '潘征',"value": 3}
    #             ],
    #     # 缺陷占比的统计图颜色
    #     "color": ["#8d7fec", "#5085f2", "#e75fc3", "#f87be2", "#f2719a", "#fca4bb", "#f59a8f", "#fdb301", "#57e7ec", "#cf9ef1"],
    #     # 缺陷占比的统计列表人名
    #     "xdata": ['黄笑', "郑龙旭", "王皓月", "孟祥含", '谢明科', '鱼跃', '陈思凡', '周洪宇', '文龙', '潘征'],
    #     "chinaDatas":[
    #         [{"name": '黑龙江', "value": 0}],[{"name": '内蒙古', "value": 0}],[{"name": '吉林', "value": 2}],
    #         [{"name": '辽宁', "value": 0}],[{"name": '河北', "value": 0}],[{"name": '天津', "value": 0}],
    #         [{"name": '山西', "value": 0}],[{"name": '陕西', "value": 0}],[{"name": '甘肃', "value": 0}],
    #         [{"name": '宁夏', "value": 0}],[{"name": '青海', "value": 0}],[{"name": '新疆', "value": 0}],
    #         [{"name": '西藏', "value": 0}],[{"name": '四川', "value": 0}],[{"name": '重庆', "value": 0}],
    #         [{"name": '山东', "value": 0}],[{"name": '河南', "value": 0}],[{"name": '江苏', "value": 0}],
    #         [{"name": '安徽', "value": 0}],[{"name": '湖北', "value": 0}],[{"name": '浙江', "value": 0}],
    #         [{"name": '福建', "value": 0}],[{"name": '江西', "value": 0}],[{"name": '湖南', "value": 0}],
    #         [{"name": '贵州', "value": 0}],[{"name": '广西', "value": 0}],[{"name": '海南', "value": 0}],
    #         [{"name": '上海', "value": 1}]
    #          ]
    #     }
    data = jsonify(data)
    rst = make_response(data)
    #rst.set_cookie('name',max_age=60 * 60)  # cookie参数是键值对成对出现的，可以通过键名获取值，max_age=60 * 60 * 0.25代表cookie有效时间15分钟
    # 添加跨域
    rst.headers['Access-Control-Allow-Origin'] = "*"
    rst.headers['Access-Control-Allow-Methods'] = "get"
    return rst










if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port= 8202)
    #app.run(debug=True, host='0.0.0.0', port=8100) #生产
