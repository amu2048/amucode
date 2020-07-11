import sqlite3
'''mode模式：select或inset；sql：封装好的sql语句；fet：单行或多行返回执行的结果，默认多行，如果为one仅有一行    '''
def SQL(mode,sql,fet='fetchall'):
    #初始化执行数据库操作
    #创建连接数据库的对象
    print("连接db数据库amuwang.db")
    con=sqlite3.connect("amuwang.db")
    #创建工作流，使用数据库对象
    cur=con.cursor()
    #判断执行模式
    if mode=="select":
        print("执行select数据库模式")
        print("开始执行sql",sql,type(sql))
        #执行sql
        cur.execute(sql)
        print("sql执行结束")
        #执行完毕，判断索取执行结果的数量，应为select会返回多条数据
        if fet=='one':
            print("获取返回单条数据")
            data=cur.fetchone()
        else:
            print("获取返回多条数据")
            data = cur.fetchall()
       
        print("结果类型应为元组",type(data))  #验证下返回结果的元素格式 用type函数
        cur.close()
    #inset模式
    if mode=="inset":
        #先挂起
        cur.execute(sql)
        #提交确认执行，这时inset特有
        cur.commit()
        #关闭
        cur.close()
    print(data)
    return  data
if __name__ == '__main__':
    sql = "select * from user where name ='amu'"
    SQL("select",sql)