
from Interface.util.operationexcel import OperationExcel
from Interface.util.operationjson import OperationJson
from Interface.data import dataconfig
class GetData:
    def __init__(self):
        self.opera_excel = OperationExcel()   #构造函数 将操作excel类实例化,如果想指定用例文件，就在这里传入文件路径
    #获取excel行数，也是用例case数
    def get_case_lines(self):
        return self.opera_excel.getlines()
    #获取是否运行
    def get_is_run(self,row):
        flag = None  #定义个空变量
        col = int(dataconfig.get_run())   #data配置文件中设置是否执行的列的索引
        run_model = self.opera_excel.getcell(row,col)  #去excel中读取row行的是否执行列的值
        if run_model == 'yes':
            flag = True
        else:
            flag = False
        return flag
    #是否携带header
    def is_header(self,row):
        col =int(dataconfig.get_header() )   #列索引根据配置文件中的配置
        header = self.opera_excel.getcell(row,col)   #调用excel操作，根据行参数获取单元格的内容
        if header == 'yes':
            return dataconfig.get_header_value()
        else:
            return None
    #获取请求方式
    def get_request_method(self,row):
        col = int(dataconfig.get_run_way())
        request_method = self.opera_excel.getcell(row,col)
        return request_method
    #获取url
    def get_request_url(self,row):
        col = int(dataconfig.get_url())
        url = self.opera_excel.getcell(row,col)
        return url
    #获取请求数据
    def get_request_data(self,row):
        col = int(dataconfig.get_data())
        data = self.opera_excel.getcell(row,col)
        if data =='':
            return None
        return data
    #获取预期结果
    def get_expcet_data(self,row):
        col = int(dataconfig.get_expect())
        expect = self.opera_excel.getcell(row,col)
        if expect == '':
            return None
        return expect
    #通过获取关键字拿到data数据
    def get_data_json(self,row):
        opera_json = OperationJson()
        print(self.get_request_data(row))
        request_data = opera_json.getdata(self.get_request_data(row))
        print('进入operajson类',request_data)
        return request_data








if __name__=='__main__':
    a=GetData()
    print(a.get_case_lines())



