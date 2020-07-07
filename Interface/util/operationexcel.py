#导入读取excel的包
import xlrd
from  xlutils.copy import copy

class OperationExcel:
    def __init__(self,filename=None,sheetid=None):   #定义构造函数，可以自定义读取的函数和用例文件名
        if filename:   #如果用力文件名不为空，则使用传入的文件名并定义为class内变量
            self.filename=filename
            self.sheetid=sheetid
            #print('filename文件未传入')
        else:    #如果未指定打开哪个用例，则使用默认地址的用例模板
            self.filename = '../dataconfig/interface.xlsx'   #../ 在当前py文件的上级目录下的dataconfig文件
            self.sheetid=0
            #print('使用默认文件路径',self.filename)
        self.data = self.getdata()  #调用读入excel函数获取用例对象
    #获取excel的数据
    def getdata(self):
        data=xlrd.open_workbook(self.filename)   #打开指定的excel文件
        tables=data.sheets()[self.sheetid]     #获取sheet表，就是excel的那张表，索引0开始
        return tables   #将打开的excel文件对象返回去
    #获取单元格的行数
    def getlines(self):
        tables=self.data   #self.data打开excel对象的实例化
        return tables.nrows   # 获取这个excel实例的行数   nrows
    #获取单元格内容 传入行，列
    def getcell(self,row,col):
        return  self.data.cell_value(row,col)
    #写入excel
    def writedata(self,row,col,value):
        read_data = xlrd.open_workbook(self.filename)  #打开用例表
        #复制这份数据
        write_data = copy(read_data)
        #读取出这个表的数据内容
        sheet_data = write_data.get_sheet(0)
        #写入数据的行 列 和要写入的值
        sheet_data.write(row,col,value)
        #将原有表数据和添加新的数据结合一起再保存，覆盖原文件。
        write_data.save(self.filename)

    #根据caseid找到对应的内容
    def get_rows_data(self,case_id):
        #根据case_id找到所在行号
        row_num = self.get_row_num(case_id)
        #获取该行的内容
        rows_data = self.get_row_values(row_num)
        return rows_data

    #根据对应的caseid找到对应的行号
    def get_row_num(self,case_id):
        #设置初始值行号为0
        num = 0
        #获取caseid列的所有行的值
        clols_data = self.get_cols_data()
        #遍历 col_data 逐行遍历是否在这个列
        for col_data in clols_data:
            #第一次遍历是地0行，然后判断传入的参数case_id是否在这个第0行的值里面
            #print("caseid值：",case_id,"col_data值：",col_data)
            if case_id in col_data:
                #如果case_id在这个行的值里面证明找到了case_id所在的行号就返回 num
                return num
            #否则就是找到这个case_id 那就num加一换一行遍历
            num =num +1

    #根据行号，获取该行的内容
    def get_row_values(self,row):
        # 实例化 换取整个excel表的数据
        tables = self.data
        #根据xlrd框架的函数，row_values(row)根据行号获取行内容
        row_data = tables.row_values(row)
        return row_data
    #获取某一列的内容
    def get_cols_data(self,col_id=None):
        #如果传入的例id不是空进入
        if col_id != None:
            #获取当前列的值
            coldata = self.data.col_vaues(col_id)
        #如果没指定获取某一列的值，那就默认使用0列的值，也是用例模板的caseid列
        else:
            coldata = self.data.col_values(0)
            #print("获取默认id列的所有值",coldata)
        return coldata


if __name__=='__main__':
    opers=OperationExcel()
    print (opers.getcell(1,1))  #获取1行1列






