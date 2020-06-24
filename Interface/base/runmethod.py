import requests
class RunMethod:
    #post请求模式模型
    def post_main(self,url,data,header=None):
        res = None
        #如果头部消息不为空进入
        if header !=None:
            #request框架，传入url,参数，头，并转将返回结果转换成json格式
            res =requests.post(url=url,data=data,header=header).json()
        else:
            res=requests.post(url=url,data=data).json()
        return res
    #get请求模式模型
    def get_main(self,url,data,header=None):
        res = None
        #如果头部消息不为空进入
        if header !=None:
            #request框架，传入url,参数，头，并转将返回结果转换成json格式
            res =requests.get(url=url,data=data,header=header).json()
        else:
            res=requests.get(url=url,data=data).json()
        return res
    #接口请求运行模型
    def run_main(self,method,url,data=None,header=None):
        if method =="post":
            res = self.post_main(url,data,header)
        else:
            res = self.get_main(url, data, header)
        return res
