import requests
import json
class RunMethod:
    #post请求模式模型
    def post_main(self,url,data,header=None):
        res = None
        #如果头部消息不为空进入
        if header !=None:
            #request框架，传入url,参数，头，并转将返回结果转换成json格式
            print("发送post请求",url,type(url),data,type(data),header,type(header))
            res =requests.post(url=url,data=data,headers=header)
        else:
            res=requests.post(url=url,data=data).json()
        #print("res类型l",type(res),res)
        res = res.json()
        #print("res类型2", type(res), res)
        return json.dumps(res)   #字典转json
    #get请求模式模型
    def get_main(self,url,data,header=None):
        res = None
        #如果头部消息不为空进入
        if header !=None:
            #request框架，传入url,参数，头，并转将返回结果转换成json格式
            res =requests.get(url=url,data=data.json(),headers=header.json()).json()
        else:
            res=requests.get(url=url,data=data).json()
        return res.json()
    #接口请求运行模型
    def run_main(self,method,url,data=None,header=None):
        if method =="post":
            res = self.post_main(url,data,header)
        else:
            res = self.get_main(url, data, header)
        print("res:",res)
        return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)
