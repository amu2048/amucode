from Interface.base.runmethod import RunMethod
from Interface.data.getdata import GetData
from Interface.util.com_util import CommonUtil


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
            #print(i)
            url = self.data.get_request_url(i)      #获取当前行的url
            method = self.data.get_request_method(i)     #获取当前行的请求模式
            is_run =self.data.get_is_run(i)    #是否执行
            #print('开始获取exceldata数据')
            data = self.data.get_data_json(i)
            expect = self.data.get_expcet_data(i)
            header =self.data.is_header(i)
            if is_run:
                #print("遍历请求请求模式",method,"请求的路径",url,"请求的数据",data,"请求头",header)
                res = self.run_method.run_main(method,url,data,header)
                print("响应报文",res)
                if self.com_util.is_contain(expect,res):

                    self.data.write_result(i,"断言成功")
                    #print("测试通过")
                else:
                    self.data.write_result(i, "断言失败")
                    #print("测试失败")





if __name__=='__main__' :
    run = RunTest()
    run.go_on_run()



