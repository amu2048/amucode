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






if __name__=='__main__':
    opers=OperationExcel()
    print (opers.getcell(1,1))  #获取1行1列






