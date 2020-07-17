from amuchenchen.amuchenchen.API.sqlconnect import SQL as s


def get_ceshi_sql():
    #sql语句获取ceshi1表中的个人缺陷数据
    sql ="select * from ceshi1"
    da = s("select",sql)
    #print(da)
    ydatali= []
    colorli= []
    xdatali =[]
    for i in da:
        name = i["name"]
        value = i["bugnum"]
        color = i["color"]
        #组合新的参数格式添加到集合里赋值给ydata
        ydatali.append({"name": name, "value": value})
        colorli.append(color)
        xdatali.append(name)
        #print(ydata)
    data = {

            # 缺陷占比的统计图数据人的占比
            "ydata": ydatali,
            # 缺陷占比的统计图颜色
            "color": colorli,
            # 缺陷占比的统计列表人名
            "xdata": xdatali

    }
    #print(data)
    return data
if __name__ == '__main__':
    get_ceshi_sql()








