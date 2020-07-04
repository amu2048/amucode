from Interface.base.runmethod import RunMethod
from Interface.data.getdata import GetData
from Interface.util.com_util import CommonUtil
from Interface.data.dependent_data import DependdentData

class RunTest:
    def __init__(self):
        #封装实例化，运行模式模型的实例化
        self.run_method = RunMethod()
        #实例化 获取excel封装好的 获取数据类实例化
        self.data = GetData()
        #实例化 断言
        self.com_util = CommonUtil()
    #程序执行的
    def go_on_run(self):
        res = None
        #获取case用例表中的行数1
        rows_count = self.data.get_case_lines()
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
                    request_data[depend_key] = depend_repinse_data
                #发起请求
                res = self.run_method.run_main(method, url, request_data, header)
                print(i,"的发送的请求为",request_data,"响应：",res)
                #断言 is_contain函数自己写的判断预期结果是否在响应信息中
                if self.com_util.is_contain(expect,res):

                    self.data.write_result(i,"断言成功")
                    #print("测试通过")
                else:
                    self.data.write_result(i, "断言失败")
                    #print("测试失败")





if __name__=='__main__' :
    run = RunTest()
    run.go_on_run()



