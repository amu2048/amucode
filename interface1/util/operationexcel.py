import xlrd

class OperationExcel:
    def __init__(self, filename=None, sheetid=None):

        if filename:
            self.filename = filename
            self.sheetid = sheetid
        else:
            self.filename = '../dataconfig/interface.xlsx'   #../ 在当前py文件的上级目录下的dataconfig文件
            self.sheetid = 0
        self.data = self.get_data()


    def get_data(self):
        data = xlrd.open_workbook(self.filename)
        tables = data.sheets()[self.sheetid]
        return tables

    # 获取单元格的行数
    def get_lines(self):

        tables = self.data  # self.data打开excel对象的实例化
        return tables.nrows  # 获取这个excel实例的行数   nrows
    #获取单元格
    def get_cell(self,row,col):
        return self.data.cell_value(row,col)


















