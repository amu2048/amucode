import requests
import json
class RunMethod:
    #post请求模式模型
    def post_main(self,url,data,header=None):
        res = None
        #如果头部消息不为空进入
        if header !=None:
            #request框架，传入url,参数，头，并转将返回结果转换成json格式
            #print("发送请求",url,data,header)
            res =requests.post(url=url,data=data,headers=header).json()
        else:
            res=requests.post(url=url,data=data).json()
        #print("状态码",res.status_code)
        return res
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
        return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)
