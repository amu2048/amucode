import requests
import json
def sengport(url, data,header):
    print("发送post请求", url, data,header)
    res = requests.post(url=url, data=data, headers=header)
    print("响应数据的类型", type(res),res)
    res = res.json()
    print("响应数据的类型", type(res), res)


if __name__=='__main__':
    url ="http://192.168.1.102:8080/InterfaceOne/encryption"
    print("url", type(url))
    data ={"pwd":"admin"}
    data =json.dumps(data)
    print("data", type(data))
    header = {'Content-Type': 'application/json'}
    print("tou",type(header))
    a = sengport(url,data,header)