import requests

from Interface.base.runmethod import RunMethod
from Interface.data.getdata import GetData
from Interface.util.com_util import CommonUtil
from Interface.data.dependent_data import DependdentData
from Interface.util.send_email import SendEmail
import json
class RunTest:
    def __init__(self):
        #封装实例化，运行模式模型的实例化
        self.run_method = RunMethod()
        #实例化 获取excel封装好的 获取数据类实例化
        self.data = GetData()
        #实例化 断言
        self.com_util = CommonUtil()
        self.send_main = SendEmail()
    #程序执行的
    def go_on_run(self):
        res = None
        #获取case用例表中的行数1
        rows_count = self.data.get_case_lines()
        pass_cont = []
        fail_cont = []
        #遍历 i 在这个行中，从1起 ，因为0行是标题行
        for i in range(1,rows_count):
            is_run = self.data.get_is_run(i)  # 是否执行
            if is_run:
                url = self.data.get_request_url(i)  # 获取当前行的url
                method = self.data.get_request_method(i)  # 获取当前行的请求模式
                request_data = self.data.get_data_json(i)
                expect = self.data.get_expcet_data(i)
                header = self.data.is_header(i)
                depend_case = self.data.is_depend(i)

                if depend_case != None:
                    self.depend_data = DependdentData(depend_case)
                    #获取的以来数据的响应数据
                    depend_repinse_data = self.depend_data.get_data_for_key(i)
                    #获取依赖的key
                    depend_key = self.data.get_depend_field(i)
                    print("获取依赖的key：",depend_key)
                    request_data =json.loads(request_data)
                    request_data[depend_key] = depend_repinse_data
                    request_data = json.dumps(request_data)
                #发起请求
                #print("发情的请求 数据格式",type(request_data),"头格式",type(header))
                res = self.run_method.run_main(method, url, request_data, header)

                #print(i,"的发送的请求为",request_data,"响应：",res)
                #断言 is_contain函数自己写的判断预期结果是否在响应信息中
                if self.com_util.is_contain(expect,res):
                    #如果断言成功 调用写入函数写入pass 表示通过
                    self.data.write_result(i,"pass")
                    #统计有多少成功的用例
                    pass_cont.append(i)
                else:
                    #用例不通过则写入响应数据
                    self.data.write_result(i, str(res))
                    fail_cont.append(i)
        #调用邮件服务发送邮件，传入通过与失败用例的集合
        self.send_main.send_mail_main(pass_cont,fail_cont)




if __name__=='__main__' :
    run = RunTest()
    run.go_on_run()



