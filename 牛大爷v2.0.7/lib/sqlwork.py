import pymysql
from lib import readconfig
def SQL(mode,sql,fet='fetchall'):
    #读取配置文件获取数据库配置信息
    host = readconfig.getConfig("database", "host")
    user = readconfig.getConfig("database", "user")
    password = readconfig.getConfig("database", "password")
    name = readconfig.getConfig("database", "name")

    #如果选择查询方式，则执行查询语句
    if mode=="select":
        # 打开数据库
        print("执行连接数据库查询",host, user, password, name,)
        db = pymysql.connect(host, user, password, name,charset='utf8')
        # 使用 cursor() 方法创建一个游标对象 cursor
        print("创建数据库游标",db)
        cursor = db.cursor()
        sq=sql
        # 使用 execute()  方法执行 SQL 查询
        print("执行sql")
        cursor.execute(sq)
        if fet=='one':
            data=cursor.fetchone()
        else:
            data = cursor.fetchall()
        # 使用 fetchone() 方法获取单条数据.cursor.fetchall()多条数据
        print("返回数据为",type(data))
        db.close()
    #如果模式是插入 采用插入语句
    if mode=="inset":
        db = pymysql.connect(host, user, password, name,charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql)
        #提交数据  这个是插入数据的必须条件
        db.commit()
        #关闭数据连接
        db.close()
    return  data

if __name__ == '__main__':
    sql = 'select * from user where name="amu"'
    a= SQL("select",sql,'one')
