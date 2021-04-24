import pymysql
from app.models import Addmaterial
from decimal import Decimal
def siliao():
    material = Addmaterial.query.all()  #查询出原材料数据
    yuanliao= {}
    #把原材料种类读取出来
    for i in material:
        print(i.name)
        yuanliao[i.name]=i.price

        #print('材料价格',yuanliao)
    # #计算原材料组合比例
    # global q
    # q=1
    # for yumi in range(30,80):
    #     #print("玉米",yumi)
    #     for doubai in range(15,20):
    #         #print("豆柏", doubai)
    #         for yufen in range(1, 10):
    #             #print("鱼粉", yufen)
    #             for youzhi in range(4, 10):
    #                 for gai in range(1, 10):
    #
    #                         zongjia = Decimal(10.3058) +Decimal(yuanliao["玉米"]) * yumi + Decimal(yuanliao["豆柏"]) * doubai + Decimal(yuanliao["植物油"]) * youzhi + Decimal(yuanliao["鱼粉"]) * yufen + Decimal(yuanliao["钙粉"]) * gai
    #                         zingjia1 = float(10.3) +float(yuanliao["玉米"]) * yumi + float(yuanliao["豆柏"]) * doubai + float(yuanliao["植物油"]) * youzhi + float(yuanliao["鱼粉"]) * yufen + float(yuanliao["钙粉"]) * gai
    #                         #print(zingjia1)
    #
    #                         zj =zongjia
    #                         if zingjia1 <166 and yumi + doubai + youzhi + gai + yufen == 92:
    #
    #                             print("序号:"+ str(q) + "   饲料比例：玉米比例 "+ str(yumi) +", 豆柏比例"+str(doubai)+", 植物油比例"+str(youzhi) + ", 鱼粉比例" + str(yufen) +",钙粉比例"+str(gai)+",配方总价：" + str(zingjia1) )
    #                             q = q+1

    global q
    q=1
    for yumi in range(30,80):
        #print("玉米",yumi)
        for doubai in range(8,20):
            #print("豆柏", doubai)
            for maifu in range(1, 20):
                #print("麦麸", maifu)


                            zongjia = Decimal(23.6074) +Decimal(yuanliao["玉米"]) * yumi + Decimal(yuanliao["豆柏"]) * doubai +  Decimal(yuanliao["麦麸"]) * maifu
                            zingjia1 = float(19.2074) +float(yuanliao["玉米"]) * yumi + float(yuanliao["豆柏"]) * doubai + float(yuanliao["麦麸"]) * maifu
                            #print(zingjia1)

                            zj =zongjia
                            if zingjia1 <147 and yumi + doubai + maifu == 86:

                                print("序号:"+ str(q) + "   饲料比例：玉米比例 "+ str(yumi) +", 豆柏比例"+str(doubai)+", 麦麸比例"+str(maifu) +",配方总价：" + str(zingjia1) )
                                q = q+1


if __name__=="__main__":
    siliao()