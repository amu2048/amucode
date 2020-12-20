from datetime import datetime
from app import db
# 会员数据表 库模型
class Users(db.Model):
    print('进入会员数据表 Users表模型')
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 序号 primary_key 键
    account = db.Column(db.String(100), unique=True) #账号 唯一 unique唯一不能重复
    name = db.Column(db.String(100))  # 用户姓名 字符串型 100长度  用于找回密码验证真实姓名
    pwd = db.Column(db.String(100))  # 密码
    sex = db.Column(db.Integer())  #性别 1男2女
    birthday = db.Column(db.String(255))  # 用户生日
    phone = db.Column(db.String(11), unique=True)  # 电话
    address = db.Column(db.String(255))  # 用户家庭地址
    weixin = db.Column(db.String(100))  # 邮箱
    info = db.Column(db.String(255))  # 简介 Text文本类型
    face = db.Column(db.String(255))  # 头像
    auth = db.Column(db.String(255))  # 菜单权限
    addriqi = db.Column(db.DateTime, default=datetime.now)  # 添加时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    #userlog = db.relationship('Userlog', backref="users")      #会员日志外键关联 Userlog表 与 user表关联

    def __repr__(self):
        return "<User %r>" % self.account
    #自定义函数 验证传入的pwd 库存的pwd 与 验证传入的pwd是一致的返回true
    def chek_pwd(self,pwd):
        from werkzeug.security import check_password_hash
        print("模型中 pwd",self.pwd)
        return check_password_hash(self.pwd,pwd)

# 会员登录日志表
class Userlog(db.Model):
    print('进入会员登录日志表Userlog表模型')
    __tablename__ = "userlog"
    __table_args__ = {'extend_existing': True}
    #__table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 序号 primary_key 键
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id')),  #
    account = db.Column(db.String(255))
    ip = db.Column(db.String(100))  # 登录IP
    op = db.Column(db.String(300))
    addriqi = db.Column(db.DateTime, default=datetime.now)  # 添加时间
    def __repr__(self):
        return  "<User %r>" % self.id

# 管理员模型
class Admin(db.Model):
    print('进入会员数据表 Users表模型')
    __tablename__ = "admin"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 序号 primary_key 键
    account = db.Column(db.String(100), unique=True) #账号 唯一 unique唯一不能重复
    name = db.Column(db.String(100))  # 用户姓名 字符串型 100长度  用于找回密码验证真实姓名
    pwd = db.Column(db.String(100))  # 密码
    sex = db.Column(db.Integer())  #性别 1男2女
    birthday = db.Column(db.String(255))  # 用户生日
    phone = db.Column(db.String(11), unique=True)  # 电话
    address = db.Column(db.String(255))  # 用户家庭地址
    weixin = db.Column(db.String(100), unique=True)  # 邮箱
    info = db.Column(db.Text)  # 简介 Text文本类型
    face = db.Column(db.String(255))  # 头像
    auth = db.Column(db.String(255))  # 菜单权限
    addriqi = db.Column(db.DateTime, default=datetime.now)  # 添加时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    #userlog = db.relationship('Userlog', backref="users")      #会员日志外键关联 Userlog表 与 user表关联

    def __repr__(self):
        return "<User %r>" % self.account
    #自定义函数 验证传入的pwd 库存的pwd 与 验证传入的pwd是一致的返回true
    def chek_pwd(self,pwd):
        from werkzeug.security import check_password_hash
        print("模型中 pwd",self.pwd)
        return check_password_hash(self.pwd,pwd)

#操作日志表
class Oplog(db.Model):
    print('进入会员登录日志表Userlog表模型')
    __tablename__ = "oplog"
    __table_args__ = {'extend_existing': True}
    #__table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 序号 primary_key 键
    account = db.Column(db.String(255))
    ip = db.Column(db.String(100))  # 登录IP
    op = db.Column(db.String(255))  # 操作位置
    addriqi = db.Column(db.DateTime, default=datetime.now)  # 添加时间
    def __repr__(self):
        return  "<User %r>" % self.id

class Adminlog(db.Model):
    print('进入会员登录日志表Userlog表模型')
    __tablename__ = "adminlog"
    __table_args__ = {'extend_existing': True}
    #__table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 序号 primary_key 键
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id')),  #
    account = db.Column(db.String(255))
    ip = db.Column(db.String(100))  # 登录IP
    op = db.Column(db.String(300))
    addriqi = db.Column(db.DateTime, default=datetime.now)  # 添加时间
    def __repr__(self):
        return  "<User %r>" % self.id

#买卖记录表模型
class Sales(db.Model):
    print('进入买卖记录Sales表模型')
    __tablename__ = "sales"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 序号 primary_key 键
    account = db.Column(db.String(255))  # 所属用户
    cattleid = db.Column(db.Integer)  #肉牛唯一识别ID可以重复根据所属用户不重复
    cattlename = db.Column(db.String(255))#昵称
    buyprice = db.Column(db.Integer)  # 购买时总价
    sellprice = db.Column(db.Integer)  # 出栏时总价
    buyweight = db.Column(db.Integer)  # 购买时体重
    sellweight = db.Column(db.Integer)  # 出售时体重
    buyunitprice = db.Column(db.Integer)  # 购买时单价
    sellunitprice = db.Column(db.Integer)  # 出售时单价
    buyday = db.Column(db.String(255))  # 购买时间
    sellday = db.Column(db.String(255))  # 出售时间
    buynum = db.Column(db.String(255))  # 购买批次
    sellnum = db.Column(db.String(255))  # 出售批次
    buycontatcs = db.Column(db.String(255))  # 购买时联系人
    sellcontacts = db.Column(db.String(255))  # 出售时联系人
    buycity = db.Column(db.String(255))  # 购买时地点
    sellcity = db.Column(db.String(255))  # 出售时地点
    remarks = db.Column(db.String(255))  # 备注
    buyfreight = db.Column(db.Integer)  #购买运费
    sellfreight = db.Column(db.Integer)  # 出栏时运费
    buycattlefild = db.Column(db.String(255))  # 购买时肉牛图片
    sellcattlefild = db.Column(db.String(255))  # 出栏时肉牛图片
    addriqi = db.Column(db.DateTime,  default=datetime.now)  # 添加时间

    def __repr__(self):
        return  "<User %r>" % self.id


#公告数据库模型
class Notice(db.Model):
    print('进入公告Notice表模型')
    __tablename__ = "notice"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # 公告标题
    table = db.Column(db.String(255))  #公告内容
    url = db.Column(db.String(255))  #点击公告跳转的连接
    state = db.Column(db.Integer)   #公告有效状态
    priority = db.Column(db.Integer)   #公告有优先级
    addriqi = db.Column(db.DateTime,  default=datetime.now)  # 添加时间
    def __repr__(self):
        return  "<User %r>" % self.id

if __name__=="__main__":
    db.create_all()

































