


#首页的基本数据返回逻辑
def get_index_ison():
    data = {
        #缺陷占比的统计图数据
        "ydata": [{"name": '黄笑',"value": 11},
                     {"name": '郑龙旭',"value": 22},
                     {"name": '王皓月',"value": 8},
                     {"name": '孟祥含',"value": 5},
                     {"name": '谢明科',"value": 2},
                     {"name": '鱼跃',"value": 8},
                     {"name": '陈思凡',"value": 6},
                     {"name": '周洪宇',"value": 5},
                     {"name": '文龙',"value": 7},
                     {"name": '潘征',"value": 3}
                    ],
        # 缺陷占比的统计图颜色
        "color": ["#8d7fec", "#5085f2", "#e75fc3", "#f87be2", "#f2719a", "#fca4bb", "#f59a8f", "#fdb301", "#57e7ec", "#cf9ef1"],

        # 缺陷占比的统计列表人名
        "xdata": ['黄笑', "郑龙旭", "王皓月", "孟祥含", '谢明科', '鱼跃', '陈思凡', '周洪宇', '文龙', '潘征'],

        "ceshi3":{ "value": 20.2, "text": '-',  "color": '#4ac7f5', "xAxis": ['测试进度'], "values": ['43'],},

        "ceshi4": {"value": 20.2, "text": '-', "color": '#25f3e6', "xAxis": ['bug修复率'], "values": ['40'], },

        "ceshi5":{ "value": 20.2, "text": '-', "color": '#ffff43', "xAxis": ['case执行率'], "values": ['31'], },

        "ceshi7": [{ "value": 11, "name": '小于20岁' }, {  "value": 12, "name": '20~24岁' },
                   { "value": 13, "name": '25~29岁' },  { "value": 14, "name": '30~34岁' },
                   { "value": 15, "name": '35~39岁' }, { "value": 10, "name": '40~49岁' },
                   { "value": 20, "name": '大于50岁' },],

        "ceshi6":[10, 20, 30, 5, 15, 2, 8, 10],

        "ceshi2":{"zhuceliang":[10, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
                  "huoyueliang":[10.0, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
                  "tongbizengjia":[2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
                  "pingjuxinzeng":[4.0, 3.2, 2.3, 5.5, 4.3, 11.2, 15.3, 22.4, 21.0, 13.5, 12.0, 10.2]
                  },
        "chinaDatas":[
                [{"name": '黑龙江', "value": 0}],[{"name": '内蒙古', "value": 0}],[{"name": '吉林', "value": 2}],
                [{"name": '辽宁', "value": 0}],[{"name": '河北', "value": 0}],[{"name": '天津', "value": 0}],
                [{"name": '山西', "value": 0}],[{"name": '陕西', "value": 0}],[{"name": '甘肃', "value": 0}],
                [{"name": '宁夏', "value": 0}],[{"name": '青海', "value": 0}],[{"name": '新疆', "value": 0}],
                [{"name": '西藏', "value": 0}],[{"name": '四川', "value": 0}],[{"name": '重庆', "value": 0}],
                [{"name": '山东', "value": 0}],[{"name": '河南', "value": 0}],[{"name": '江苏', "value": 0}],
                [{"name": '安徽', "value": 0}],[{"name": '湖北', "value": 0}],[{"name": '浙江', "value": 0}],
                [{"name": '福建', "value": 0}],[{"name": '江西', "value": 0}],[{"name": '湖南', "value": 0}],
                [{"name": '贵州', "value": 0}],[{"name": '广西', "value": 0}],[{"name": '海南', "value": 2}],
                [{"name": '上海', "value": 1}]
                 ]
            }
    return data