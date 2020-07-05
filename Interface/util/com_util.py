class CommonUtil:
    #断言 判断一个字符串是否在爱另一个字符串中，返回true或flag
    def is_contain(self,str_one,str_two):
        '''
        判断一个字符串是否在另一个字符串中
        str_one；查找的字符串
        str_two:被查找的字符串
        '''
        flag = None
        #把传入的数据转成str
        if isinstance(str_one,str):
            self.str_one = str_one.encode('utf-8').decode("unicode_escape")
        if isinstance(str_two,str):
            self.str_two = str_two.encode('utf-8').decode("unicode_escape")
        print("断言1",self.str_one, "断言2",self.str_two)
        if self.str_one in self.str_two:
            flag = True
        else:
            flag = False
        return flag

    #获取测试用例通过率计算,并返回自定义文本，以供发邮件正文使用
    def Pass_case(self,pass_list,fail_list):
        #将统计用例通过数转换成浮点类型方便计算
        pass_num = float(len(pass_list))
        fail_num = float(len(fail_list))
        #y用例执行总数
        count_num = pass_num + fail_num
        #通过率计算%.2f 意思保留两位小数，%%格式化添加以一个%号，最后形成 30.34%的效果
        pass_result = "%.2f%%" %(pass_num/count_num * 100)
        fail_result = "%.2f%%" %(fail_num/count_num * 100)
        #返回字典格式用例总数、成功数、失败数、 通过率，失败率，
        return {"count_num":count_num,"pass_num":pass_num,"fail_num":fail_num,"pass_result":pass_result,"fail_result":fail_result}