from Interface.base.runmethod import RunMethod
from Interface.data.getdata import GetData


class RunTest:
    def __init__(self):
        #封装实例化，运行模式模型的实例化
        self.run_method = RunMethod()
        #实例化 获取excel封装好的 获取数据类实例化
        self.data = GetData()
    #程序执行的
    def go_on_run(self):
        res = None
        #获取case用例表中的行数
        rows_count = self.data.get_case_lines()
        #遍历 i 在这个行中，从1起 ，因为0行是标题行
        for i in range(1,rows_count):
            url = self.data.get_request_url(i)      #获取当前行的url
            method = self.data.get_request_method(i)     #获取当前行的请求模式
            is_run =self.data.get_is_run(i)
            print('开始获取exceldata数据')
            data = self.data.get_data_json(i)
            header =self.data.is_header(i)
            if is_run:
               res = self.run_method.run_main(method,url,data,header)
            return res



if __name__=='__main__' :
    run = RunTest()
    run.go_on_run()



