import pymysql
db =  pymysql.connect("39.106.14.148","root","AMU19930316amu","amubang" )
import pymysql
from app.models import Addmaterial
from decimal import Decimal
def siliao(a,b):
    a = float(a)  # 活牛体重
    b = float(b)  # 预期日增重量
    #计算肉牛千克干物质所需营养值
    yy = yingyang(a,b)
    print(yy)
    material = Addmaterial.query.all()  #查询出原材料数据
    yuanliao= {}
    #把原材料种类读取出来
    for i in material:
        #print(i.name)
        yuanliao[i.name]=i.price
    global q
    q=1
    for yumi in range(30,80):
        #print("玉米",yumi)
        for doubai in range(8,20):
            #print("豆柏", doubai)
            for maifu in range(1, 20):
                #print("麦麸", maifu)
                    zingjia1 = float(19.2074) +float(yuanliao["玉米"]) * yumi + float(yuanliao["豆柏"]) * doubai + float(yuanliao["麦麸"]) * maifu
                    peidbz =(yumi*5*8.6 + doubai*5*43 + maifu*5*14.4)/100
                    peigai =(yumi*5*0.08 + doubai*5*0.32 + maifu*5*0.2)/100
                    peilin =(yumi*5*0.21 + doubai*5*0.55 + maifu*5*0.78)/100
                    peirnd =yumi*1 + doubai*0.92 + maifu*0.73
                    #print("cudanbai",yy["cdb"]/2)
                    # if peidbz > float(yy["cdb"])/2 or peigai > float(yy["gai"])/2 or peilin > float(yy["lin"])/2 or peirnd >float(yy["RND"])/2:
                    if peidbz > float(yy["cdb"]) / 2 :

                        if zingjia1 <146 and yumi + doubai + maifu == 86:
                            print("粗蛋白含量：",float(yy["cdb"]) / 2, "钙含量为", float(yy["gai"]) / 2,"磷含量为", float(yy["lin"]) / 2)
                            print("序号:"+ str(q) + "   饲料比例：玉米比例 "+ str(yumi) +", 豆柏比例"+str(doubai)+", 麦麸比例"+str(maifu) +", 配方总价：" + str(zingjia1) )
                            print("序号:"+ str(q) + "   配方营养值：粗蛋白质含量g"+ str(peidbz) +", 钙含量g"+str(peigai)+", 磷含量g"+str(peilin) +", 肉牛能量单位个：" + str(peirnd) )
                            q = q+1


def abc(a,b):
    a = float(a)  # 活牛体重
    b = float(b)  # 预期日增重量
#根据体重和日增计算需要的每千克干物质营养值
def yingyang(a,b):
    # 获取营养标准表 所需 的粗蛋白 钙 磷 干物质采食量
    if b > 1.2:
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
        gai = (b - 1.2) * 20 + float(gai)  # 钙
        lin = (b - 1.2) * 5 + float(lin)  # 磷
        RND = kjkg(a, b)
        print("日增 %s公斤 需要分钙 %s 克，磷 %s克"  %(b,gai, lin))
    else:
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "select ganwuzhi,gai ,RND,lin ,cudanbai from biaozhun where tizhong= %s and  rizeng = %s" % (int(a), b)
        cursor.execute(sql)
        data = cursor.fetchone()
        # print("获取到的数据是 : ", data)
        # 关闭数据库连接
        db.close()
        gwz = data["ganwuzhi"]
        gwz = float(gwz)
        cdb = data["cudanbai"]
        cdb = float(cdb)
        gai = data["gai"]
        gai = float(gai)
        lin = data["lin"]
        lin =  float(lin )
        RND = data["RND"]
        RND= float(RND)
        print("干物质是 : ", gwz,"公斤")
    # 每千克干物质需要的营养
    print("干物质为",gwz)
    kgcdb = cdb / gwz
    kggai = gai / gwz
    kglin = lin / gwz
    kgRND = RND /gwz
    print("日增 %s公斤 需要粗蛋白 %s 钙 %s 克，磷 %s克"  %(b,cdb,gai, lin))
    des={}
    des["cdb"]= kgcdb
    des["gai"] = kggai
    des["lin"] = kglin
    des["RND"] = kgRND

    return des

#粗蛋白需要量
def cudanbai(kg,k):
    LBW = kg
    ADG = k
    t = 200
   #增重净能
    NEg = (2092 + 25.1 * LBW)*((ADG / (1 - 0.3 * ADG)) /1000)
   #净蛋白质需要量
    NPg = ADG * (268 - 7.027*(NEg/ADG))
    print("npg",NPg)
    #维持小肠可消化蛋白质公式
    IDCPm = 5.545 * pow(LBW,0.78)
    #IDCPm = 5.45 * pow(LBW, 0.75)
    # if LBW >330:
    #     print(1)
    #     #增重小肠可消化粗蛋白质
    IDCPg = NPg/(0.834-0.0009*LBW)
    # elif LBW <330:
    #     IDCPg = NPg /0.4923
    #妊娠小肠可消化粗蛋白质
    CBW = 15.201 +0.0376*LBW
    from math import e
    NPc = 6.25 * CBW * (0.001669 -(0.00000211*t))* pow(e,(0.0278-0.0000176*t)*t)
    IDCPc = NPc /0.65
    print("IDCPc",IDCPc,"CBW",CBW,"NPc",NPc)
    cudanbai = IDCPg +IDCPm+IDCPc
    print("每日需要粗蛋白 %f 克/日" %(cudanbai))
    return cudanbai
#育肥牛干物质采食量 传入体重 和日增
def ganwuzhi(kg,k):
    LBW = kg
    ADG = k
    DMI = 0.062 * pow(LBW,0.75) + (1.5296 +0.0037*LBW)*ADG
    print("%f 公斤肉牛日增 %f 公斤，日需干物质采食量为 %f 公斤" % (LBW, ADG, DMI))
    return float(DMI)
#根据想要达到日增公斤数 计算出所需能量kj/天  千焦每天 需传入肉牛体重kg 日增公斤数 k  返回肉牛能量单位
def kjkg(kg,k):
    LBW = kg
    ADG = k
    NEg =(2092 +25.1*LBW)*ADG/(1-0.3*ADG)
    RND = NEg/1000 / 8.08
    print("%f 公斤肉牛日增 %f 公斤，日需能量为 %f 千焦, 肉牛能量单位为 %f" % (LBW,ADG,NEg,RND))
    return RND


if __name__=="__main__":

    #siliao(500,1.5)
    #cudanbai(500,1.5)
    yingyang(500,1.5)

