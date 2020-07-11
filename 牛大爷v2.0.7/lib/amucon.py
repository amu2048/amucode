from flask import request
import json


#判断是否存在cookie
def Ifcookie():
    print("进入判断cookie程序")
    if len(request.cookies) >= 1:
        print("cookie验证成功")
        return '0'
    else:
        print("cookie验证失败")
        return '1'
#将数据库的元祖转换数据头变成键值对格式并返回
def setdic(a):
    di=["id","name","gmpicihao","bianhao","gmdata","gmzongjia","gmtizhong","gmyunfei","gmdanjia","gmdidian","gmlianxiren","beizhu"]
    #di={"id":"","name":"","dmpicihao":"","bianhao":"","gmdata":"","gmzongjia":"","gmtizhong":"","gmyunfei":"","gmdanjia":"","gmdidian":"","gmlianxiren":"","beizhu":""}
    dic={}
    for i in range(0,len(a)):
        dic[di[i]]=a[i]
    #return json.dumps(dic,ensure_ascii=False)

    return dic


















#将字典头转换成汉字
def cndic(a):
    cn={'id':"序号", 'name': '用户名', 'gmpicihao': '购买批次号', 'bianhao': '肉牛编号', 'gmdata': '购买时间', 'gmzongjia': '购买总价', 'gmtizhong': '体重', 'gmyunfei': '运费', 'gmdanjia': '单价', 'gmdidian': '购买地点', 'gmlianxiren': '卖方信息', 'beizhu': '备注'}
    list=[]
    print("执行提取传入数据的字典头")


    for i in a:
       list.append(cn[i])


    return list















