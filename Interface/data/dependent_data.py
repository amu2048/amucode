#数据依赖相关问题的脚本
from interface.util.operationexcel import OperationExcel
from interface.base.runmethod import RunMethod
from interface.data.getdata import GetData
from jsonpath_rw import jsonpath,parse
import json
class DependdentData():
    def __init__(self,case_id):
        #全局定义个变量值
        self.case_id = case_id
        #实例化excel操作类
        self.opera_excel = OperationExcel()
        self.data = GetData()

    #通过case_id获取该case的整行数据
    def get_case_line_daa(self):
        rows_data = self.opera_excel.get_rows_data(self.case_id)
        return rows_data

    #执行依赖测试，获取结果
    def run_dependent(self):
        run_method = RunMethod()
        row_num = self.opera_excel.get_row_num(self.case_id)
        request_data = self.data.get_data_json(row_num)
        header = self.data.is_header(row_num)
        method = self.data.get_request_method(row_num)  # 获取当前行的请求模式
        url = self.data.get_request_url(row_num)  # 获取当前行的url
        res = run_method.run_main(method,url,request_data,header)
        print("这里的格式",type(res))
        return json.loads(res)
    #根据以来数据的key获取执行依赖测试的case的响应数据，然后返回
    def get_data_for_key(self,row):
        #根据行号获取用例模板中依赖数据的值
        depend_data = self.data.get_depend_key(row)
        #获取这个依赖caseid所执行的结果响应信息
        response_data = self.run_dependent()
        print("依赖数据的响应response_data：" ,type(response_data))
        #类似正则表达式一样，按照depend_data规则在response_data搜索对相应结果.jsonpath_rw框架的函数
        json_exe = parse(depend_data)
        response_data = json.loads(response_data)
        print("response_data类型为",type(response_data))
        #按照find的规则在依赖的case相应信息中获取以来数据想要的东西
        madle = json_exe.find(response_data)
        #print("madle的值",madle)
        #规格是一次循环取出字段按照规则返回
        print("fanhui",[math.value for math in madle] [0])
        return  [math.value for math in madle] [0]



