import pymysql
db =  pymysql.connect("39.106.14.148","root","AMU19930316amu","amubang" )
#400-500公斤的肉牛育肥精料配方中的各原料比例 传入精料日食料 j 单位公斤
def pei4_5(j):
    jingliao = j *2
    negnliang = jingliao * 0.66
    doubai = jingliao * 0.24
    kuangwuzhi = jingliao * 0.05
    weiliang = jingliao * 0.05

#输入肉牛公斤数kg 计算返回日粮原料所需量
def riliang(kg):
    kg=kg*2
    jingliao = kg*0.012     #日粮精料是体重的百分1.2
    culiao = (jingliao / 6) * 4   #精料粗料比  6：4
    print("此时肉牛日食精饲料 %f 粗饲料 %f " %(jingliao,culiao))
    if 400<kg<=500:
        pei4_5(jingliao/2)

#根据想要达到日增公斤数 计算出所需能量kj/天  千焦每天 需传入肉牛体重kg 日增公斤数 k
def kjkg(kg,k):
    LBW = kg
    ADG = k
    NEg =(2092 +25.1*LBW)*ADG/(1-0.3*ADG)
    RND = NEg/1000 / 8.08
    print("%f 公斤肉牛日增 %f 公斤，日需能量为 %f 千焦, 肉牛能量单位为 %f" % (LBW,ADG,NEg,RND))
    return RND
#根据想要达到日增公斤数 计算出综合净能需要量kj/天  千焦每天 需传入肉牛体重kg 日增公斤数 k
def zonghejingneng(kg,k):
    LBW = kg
    ADG = k
    F = 1.147

    NEmf = (322*pow(LBW,0.75) + (2092 + 25.1 * LBW) * ADG / (1-0.3 * ADG)) * F
    print("%f 公斤肉牛日增 %f 公斤，日需综合净能量为 %f 千焦" % (LBW, ADG, NEmf))
#粗蛋白需要量
def cudanbai(kg,k):
    LBW = kg
    ADG = k
    t = 200
   #增重净能
    NEg = (2092 + 25.1 * LBW)*((ADG / (1 - 0.3 * ADG)) /1000)
   #净蛋白质需要量
    NPg = ADG * (268 - 7.026*(NEg/ADG))
    print("npg",NPg)
    #维持小肠可消化蛋白质公式
    IDCPm = 5.45 * pow(LBW,0.75)
    if LBW <=330:
        print(1)
        #增重小肠可消化粗蛋白质
        IDCPg = NPg/(0.834-0.0009*LBW)
    elif LBW >330:
        IDCPg = NPg /0.4923
    #妊娠小肠可消化粗蛋白质
    CBW = 15.201 +0.0376*LBW
    from math import e
    NPc = 6.25 * CBW * (0.001669 -(0.00000211*t))* pow(e,(0.0278-0.0000176*t)*t)
    IDCPc = NPc /0.65
    print("IDCPc",IDCPc,"CBW",CBW,"NPc",NPc)
    cudanbai = IDCPg +IDCPm+IDCPc
    print("每日需要粗蛋白 %f 克/日" %(cudanbai))

#育肥牛干物质采食量 传入体重 和日增
def ganwuzhi(kg,k):
    LBW = kg
    ADG = k
    DMI = 0.062 * pow(LBW,0.75) + (1.5296 +0.0037*LBW)*ADG
    print("%f 公斤肉牛日增 %f 公斤，日需干物质采食量为 %f 公斤" % (LBW, ADG, DMI))
    return DMI

class ndy():
    a = input("请输入肉牛体重，单位公斤")
    b = input("请输入预期达到的日增，单位公斤")
    a = float(a) #活牛体重
    b = float(b)  #预期日增重量
    #获取营养标准表 所需 的粗蛋白 钙 磷 干物质采食量
    if b >1.2:
        gwz = ganwuzhi(a,b)  #干物质采食量
        cdb = cudanbai(a,b)  #粗蛋白质
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "select ganwuzhi,gai ,RND,lin ,cudanbai from biaozhun where tizhong= %s  and rizeng = 1.2" % (int(a))
        cursor.execute(sql)
        data = cursor.fetchone()
        # 关闭数据库连接
        db.close()
        gai = data["gai"]
        lin = data["lin"]
        gwz = ganwuzhi(a, b)  # 干物质采食量
        cdb = cudanbai(a, b)  # 粗蛋白质
        gai = (b -1.2)*20 + float(gai) #钙
        lin = (b - 1.2) *5 + float(lin)#磷
        RND= kjkg(a,b)
        print("日增1.4 需要分钙磷",gai,lin)
    else:
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "select ganwuzhi,gai ,RND,lin ,cudanbai from biaozhun where tizhong= %s and  rizeng = %s" %(int(a),b)
        cursor.execute(sql)
        data = cursor.fetchone()
        print("获取到的数据是 : ", data)
        # 关闭数据库连接
        db.close()
        gwz = data["ganwuzhi"]
        cdb = data["cudanbai"]
        gai = data["gai"]
        lin = data["lin"]
        RND = data["RND"]
        print("干物质是 : ", gwz)
    #每千克干物质需要的营养
    kgcdb = cdb/gwz
    kggai = gai / gwz
    kglin = lin / gwz
    #粗料占比 总蛋白质含量 每千克含量克
    jieganzhanbi = 60
    jiuzaozhanbi = 40
    jiegan = 1000 * 0.059 * jieganzhanbi  #秸秆占粗饲料的百分六十
    jiuzao = 1000 * 0.093 * jiuzaozhanbi  #酒糟站粗饲料的百分四十
    culiaodbz = jiegan + jiuzao  #粗饲料中的蛋白质含量
    culiaoRND = 0.38 * jiuzaozhanbi + 0.45 * jieganzhanbi
    #精料中蛋白质含量 每千克干物质含蛋白量 克
    yumizhanbi = 83
    maifuzhanbi = 17
    yumi = 1000*0.086 * yumizhanbi
    yumigai = 1000*0.0008 * yumizhanbi
    yumilin = 1000*0.0021 * yumizhanbi
    yumiRND = 1*yumizhanbi
    maifu = 1000 * 0.144 * maifuzhanbi
    maifugai = 1000 * 0.0018 * maifuzhanbi
    maifulin = 1000*0.0078 * maifuzhanbi
    maifuRND = 0.73*maifuzhanbi
    jingRND = maifuRND + yumiRND
    jingdbz = yumi+ maifu  #精料蛋白质含量
    jinggai = yumigai + maifugai
    jinglin = yumilin + maifulin
    #粗料 精料占比计算
    cubi = abs((RND-jingRND)/(culiaoRND-jingRND))
    jingbi = 1-cubi

    #日粮中各原料占比
    yl_yumijeigan = jieganzhanbi * cubi
    yl_jiucao = jiuzaozhanbi * cubi
    yl_yumi = yumizhanbi * jingbi
    yl_maifu = maifuzhanbi * jingbi








if __name__=="__main__":

    ndy()


