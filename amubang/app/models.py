from datetime import datetime
from app import db
# 求助列表 库模型
class Helplist(db.Model):
    print('进入会员数据表 Users表模型')
    __tablename__ = "helplist"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 序号 primary_key 键
    userId = db.Column(db.String(100)) #微信登录的名字
    userUrl = db.Column(db.String(255)) #微信登录的头像
    longitude = db.Column(db.String(100))  # 经度
    latitude = db.Column(db.String(100))  # 纬度
    srvType = db.Column(db.String(255))  # 求助类型，在选择求助类型时 已经触发重写 所以这里再data数据中获取
    srvTitle = db.Column(db.String(255))  # 求助标题
    srvDesc = db.Column(db.String(255))  # 求助内容
    srvCost = db.Column(db.Integer)  # 悬赏积分
    endTime = db.Column(db.String(100))  # 求助有效期
    urgent = db.Column(db.String(255))  # 是否是加急
    mobile = db.Column(db.String(100))  # 求助人的电话号
    posDes = db.Column(db.String(255))  # 求助的地址
    helpid = db.Column(db.String(255))  # 领取人ID
    helpurl= db.Column(db.String(255))  # 领取人头像
    star = db.Column(db.Integer)   #求助数据是否已完成
    addriqi = db.Column(db.DateTime, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<User %r>" % self.id

class User(db.Model):
    print('进入会员数据表 Users表模型')
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 序号 primary_key 键
    openid = db.Column(db.String(255)) #微信用户的唯一ID
    nickName = db.Column(db.String(100)) #微信登录的名字
    avatarUrl = db.Column(db.String(255)) #微信登录的头像
    usePoint =db.Column(db.Integer)  #剩余积分点
    gender =db.Column(db.Integer)  #性别 0女 1男
    province = db.Column(db.String(255)) #省份
    city = db.Column(db.String(255)) #城市
    country = db.Column(db.String(255))#国家
    star = db.Column(db.String(255))  #求助数据是否已完成
    addriqi = db.Column(db.DateTime, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<User %r>" % self.id


#积分兑换详情表
class Points(db.Model):
    print('进入积分兑换 Points表模型')
    __tablename__ = "points"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 序号 primary_key 键
    code = db.Column(db.String(100))   #积分兑换码
    integral = db.Column(db.Integer)   #对应积分
    star = db.Column(db.Integer)   #是否兑换
    userid = db.Column(db.String(100))  # 谁兑换的
    zb = db.Column(db.String(255))  # 备注
    addriqi = db.Column(db.DateTime, default=datetime.now)  # 添加时间


    def __repr__(self):
        return "<User %r>" % self.id
# 牛神奇--体重估算表
class Weight(db.Model):
    print('进入积分兑换 Weight体重对照表')
    __tablename__ = "weight"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 序号 primary_key 键
    cm = db.Column(db.String(100))   #胸围
    thin = db.Column(db.String(100))   #偏瘦型
    average = db.Column(db.String(100))   #正常
    fat = db.Column(db.String(100))  # 偏胖
    def __repr__(self):
        return "<Weight %r>" % self.id
# 牛神奇--养殖技术表
class Addtechnology(db.Model):
    print('牛神奇--养殖技术表')
    __tablename__ = "addtechnology"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 序号 primary_key 键
    imgsrc = db.Column(db.String(255))   #文章列表图片地址
    title = db.Column(db.String(255))   #标题
    desc = db.Column(db.String(255))   #简介
    url = db.Column(db.String(255))  # 转跳的url地址
    star = db.Column(db.Integer)   #文章的状态
    watch = db.Column(db.Integer)   #阅读数
    like = db.Column(db.Integer)   #点赞数
    pinglun = db.Column(db.Integer)   #评论数
    addriqi = db.Column(db.DateTime, default=datetime.now)  # 添加时间
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
    def __repr__(self):
        return "<Addtechnology %r>" % self.id

if __name__=="__main__":
    db.create_all()

































