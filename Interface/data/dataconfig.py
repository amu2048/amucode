#使用类的形式设置全局变量，以下字段配置的是对应excel中的第几列
class global_var:
    #case_id
    Id = '0'
    request_name = '1'
    url = '2'
    run = '3'
    request_way = '4'
    header = '5'
    case_depend ='6'
    data_depend ='7'
    field_depend ='8'
    data ='9'
    expect ='10'
    result = '11'

#获取caseid所在的列索引
def get_id():
    return global_var.Id
#获取url所在的列索引
def get_url():
    return  global_var.url
#获取是否执行所在的列索引
def get_run():
    return  global_var.run
# 获取请求方式所在的列索引
def get_run_way():
    return global_var.request_way
#获取请求头所在的列索引
def get_header():
    return  global_var.header
#获取case依赖id所在的列索引
def get_case_depend():
    return  global_var.case_depend
#获取依赖的数据所在的列索引
def get_data_depend():
    return  global_var.data_depend
#获取以来的数据所属字段所在的列索引
def get_field_depend():
    return  global_var.field_depend
#获取请求数据所在的列索引
def get_data():
    return  global_var.data
#获取预期结果所在的列索引
def get_expect():
    return  global_var.expect
#获取实际结果所在的列索引
def get_result():
    return  global_var.result
#获取头信息
def get_header_value():
    header = {
        "contenttype":"application/json;charset=utf-8"
    }

    return header















