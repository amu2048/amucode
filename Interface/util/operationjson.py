import json
class OperationJson():
    #构造函数 定义全局data为读取json函数的实例化
    def __init__(self,filename=None):
        if filename:  # 如果用力文件名不为空，则使用传入的文件名并定义为class内变量
            self.filename=filename
        else:  # 如果未指定打开哪个json，则使用默认地址的json
            self.filename ='../dataconfig/jsonconfig.json'  # ../ 在当前py文件的上级目录下的dataconfig文件
        self.data=self.readdata()
    #读取json文件类
    def readdata(self):
        try:
            #with方法省去关闭文件IO的繁琐，打开指定的json文件赋值给fp并用load函数读取它
            with open(self.filename,'r',encoding='utf-8')as fp:    # r 只读模式， w写模式 ， 指定编码encoding防止中文乱码

                data=json.load(fp)
                return data
        except json.decoder.JSONDecodeError:
            return None
    #写如json文件
    def write(self,writedata):
        with open(self.filename,'w',encoding='utf-8')as fp:    # r 只读模式， w写模式 ， 指定编码encoding防止中文乱码
            data=json.dump(writedata,fp,ensure_ascii=False)     #  如果ensure_ascii ' '为false，则返回值可以包含非ascii值
            return data

    def getdata(self,id):
        return self.data[id]


if __name__=='__main__':
    opers=OperationJson()
    print (opers.getdata("gradeId"))     #获取id为1的在json文件中的值



