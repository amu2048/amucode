from amuchenchen.amuchenchen.API import readsqldata as d


#首页的基本数据返回逻辑
def get_index_ison():
    data = {
        #缺陷占比的统计图数据人的占比
        "ceshi1": d.get_ceshi_sql(),
        #        {
        #     # 缺陷占比的统计图数据人的占比
        #     "ydata": [{"name": '黄笑',"value": 11},
        #              {"name": '郑龙旭',"value": 22},
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
        #     "xdata": ['黄笑', "郑龙旭", "王皓月", "孟祥含", '谢明科', '鱼跃', '陈思凡', '周洪宇', '文龙', '潘征']
        # },

        #测试进度统计图
        "ceshi3":{ "value": 20.2, "text": '-',  "color": '#4ac7f5', "xAxis": ['测试进度'], "values": ['43'],},
        #bug修复率统计图
        "ceshi4": {"value": 20.2, "text": '-', "color": '#25f3e6', "xAxis": ['bug修复率'], "values": ['40'], },
        #case执行率统计图
        "ceshi5":{ "value": 20.2, "text": '-', "color": '#ffff43', "xAxis": ['case执行率'], "values": ['31'], },
        #用户分析按年龄比值
        "ceshi7": [{ "value": 11, "name": '小于20岁' }, {  "value": 12, "name": '20~24岁' },
                   { "value": 13, "name": '25~29岁' },  { "value": 14, "name": '30~34岁' },
                   { "value": 15, "name": '35~39岁' }, { "value": 10, "name": '40~49岁' },
                   { "value": 20, "name": '大于50岁' },],
        #手机型号的占比数据
        "ceshi6":[10, 20, 30, 5, 15, 2, 8, 10],
        #左下角的线性图 注册量、活跃量、同比增加、平均增加
        "ceshi2":{"zhuceliang":[10, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
                  "huoyueliang":[10.0, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
                  "tongbizengjia":[2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
                  "pingjuxinzeng":[4.0, 3.2, 2.3, 5.5, 4.3, 11.2, 15.3, 22.4, 21.0, 13.5, 12.0, 10.2]
                  },
        #地图的各个地点的数据
        "chinaDatas":[
                [{"name": '黑龙江', "value": 0}],[{"name": '内蒙古', "value": 0}],[{"name": '吉林', "value": 0}],
                [{"name": '辽宁', "value": 0}],[{"name": '河北', "value": 0}],[{"name": '天津', "value": 0}],
                [{"name": '山西', "value": 0}],[{"name": '陕西', "value": 0}],[{"name": '甘肃', "value": 0}],
                [{"name": '宁夏', "value": 0}],[{"name": '青海', "value": 0}],[{"name": '新疆', "value": 0}],
                [{"name": '西藏', "value": 0}],[{"name": '四川', "value": 0}],[{"name": '重庆', "value": 0}],
                [{"name": '山东', "value": 0}],[{"name": '河南', "value": 0}],[{"name": '江苏', "value": 0}],
                [{"name": '安徽', "value": 0}],[{"name": '湖北', "value": 0}],[{"name": '浙江', "value": 0}],
                [{"name": '福建', "value": 0}],[{"name": '江西', "value": 0}],[{"name": '湖南', "value": 0}],
                [{"name": '贵州', "value": 0}],[{"name": '广西', "value": 0}],[{"name": '海南', "value": 0}],
                [{"name": '上海', "value": 1}]
            ]
        }
    return data
#首页的地图上方的注册用户总计数量
def get_user_cont():
    #设置注册量 字符串格式
    data = "6112"
    return data
#获取左上方的阿木奇谭简介
def get_jianjie():
    data = '阿木奇谭测试工具系统，因测试而生，为测试而忙，在这神奇的奇谭空间，只有你想不到，没有做不到。'
    return data

#简介下面的功能点
def get_gnlist():
    data = ["智能分析", "辅助测试", "AI直观", "数据统计", "领导汇报", "前所未有" ]
    return data

#右侧工具栏的兵器库 小工具
def get_gongjulist():
    data = [{"name":"顺风耳", "names":"短信接收", "url":"https://www.materialtools.com/"},
            {"name":"传信简", "names":"Email", "url":"https://10minutemail.net/"},
            {"name": "筋斗云", "names": "网速测试", "url": "https://wangsuceshi.51240.com/"},
            {"name": "JSON变", "names": "在线解析", "url": "https://www.json.cn/"},
            {"name": "封神榜", "names": "花瓶传单", "url": "https://i.fkw.com/"},
            {"name": "南天门", "names": "性能测试", "url": "https://perfdog.qq.com/login"}
            ]
    return data
#奇谭令里的个人资料
def get_userfile():
    data = {"nicheng":"阿穆家","zhiye": "一名苦爹的测试","diqu": "北京","gongling": "13","biaoqian": "我要成为一名出色的测试开发工程师，我要学会前端技术，后端技术，还是要学代码."}
    return data
#bug例表数据获取
def get_buglist():
    data= [
        {
         "biaoti":"1.iOS微信登入失败,需与后端沟通代码",
         "zhuangtai":"激活",
         "dengji":"1"
         },
        {"biaoti": "2.安卓崩溃，登入发送验证码后闪退崩溃", "zhuangtai": "激活", "dengji": "1"},
        {"biaoti": "3.音频播放失败，点击小学听力，开始播放，吓死你hi播放失败", "zhuangtai": "关闭", "dengji": "2"},

        {"biaoti": "4.ios-生产环境-书架中 曲一线文字遮盖（高一）", "zhuangtai": "激活", "dengji": "2"},
        {"biaoti": "5.后台-我的反馈提交的图片运营后台不显示", "zhuangtai": "激活", "dengji": "2"},
        {"biaoti": "6.我的界面我的缓存请改成我的下载与我的下载页一致性文字", "zhuangtai": "已关闭", "dengji": "4"},


        {"biaoti": "7.ios-生产环境断网播放音频下载文件，播放不了", "zhuangtai": "激活", "dengji": "2"},
        {"biaoti": "8.ios-生产环境（建议）我的设置中选择年级 感觉是从底部向上弹出有那么一闪而过", "zhuangtai": "关闭", "dengji": "4"},
        {"biaoti": "9.断开网络，书架tab中 点击登录，应该提示网络异常", "zhuangtai": "激活", "dengji": "3"},
        {"biaoti": "10.生产环境,学科-书里面的资源拓展、音频、视频弄个固定排序","zhuangtai": "已解决", "dengji": "2"},
        {"biaoti": "11.ios-生产环境-书架中 曲一线文字遮盖（高一）", "zhuangtai": "激活", "dengji": "2"},
        {"biaoti": "12.后台-我的反馈提交的图片运营后台不显示", "zhuangtai": "激活", "dengji": "2"},

        {"biaoti": "13.生产环境,学科-书里面的资源拓展、音频、视频弄个固定排序", "zhuangtai": "已解决", "dengji": "2"},
        {"biaoti": "14.ios-生产环境-书架中 曲一线文字遮盖（高一）", "zhuangtai": "激活", "dengji": "2"},
        {"biaoti": "15.后台-我的反馈提交的图片运营后台不显示", "zhuangtai": "激活", "dengji": "2"},


        {"biaoti": "16.我的界面我的缓存请改成我的下载与我的下载页一致性文字", "zhuangtai": "已关闭", "dengji": "4"}
          ]
    return data