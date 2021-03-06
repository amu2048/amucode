# 导入Flask-Wtf包 主要用于表单处理的
from flask_wtf import FlaskForm
"""从wtf框架中导入 
StringField:标签
PasswordField:密码框
SubmitField: 登入按钮
"""
from wtforms import StringField, PasswordField, SubmitField,SelectField,TextAreaField,DateField
from flask_wtf.file import FileAllowed ,FileField,FileRequired# 验证文件后缀名FileField
"""导入验证器
DataRequired:提示
ValidationError:自定义ERR提示
regexp:正则表达式
EqualTo:比较器 比较两次密码是否一致
"""
from wtforms.validators import DataRequired,ValidationError,EqualTo,regexp,Length
#导入数据user表模型
from app.models import Users,Sales,Userlog,Adminlog,Admin
from flask import session
#登入表单验证
class LoginForm(FlaskForm):
    """登入表单 #命名一个user 输入框表单"""
    print("进入longin表单")
    account = StringField(
        label="用户名",
        validators=[
            DataRequired("请输入用户名!",)
        ],
        description="账号",
        render_kw={
            "placeholder":"请输入用户名",
            "required":"required",
        }
    )
    mima = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码!")
        ],
        description="密码框",
        render_kw={
            "placeholder":"请输入密码",
            "required":"required",
        }
    )

    submit = SubmitField(
        "登录"
    )
    #自定义处理器 传入表单上传的数据 获取user的值
    def validate_account(self,field):
        #获取表单数据
        print("进入validate_user函数")
        account = field.data
        #调用用户user模型sql 查询这账号 数据
        na = Users.query.filter_by( account = account).count()
        print(na)
        #如果 获取的数据为0条 证明无此账号
        if na == 0:
            #wtforms.validators中导入ValidationError 自定义err提示
            raise ValidationError("您的账号不存在")
#注册表单
class RegistFrom(FlaskForm):
    userId =StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号!")
        ],
        description="账号",
        render_kw={
            "placeholder":"账号唯一作为登录账号使用",
            "required":"required",
        }
    )
    userName = StringField(
        label="姓名",
        validators=[
            DataRequired("请输入您的真实姓名!" )
        ],
        description="账号",
        render_kw={
            "placeholder": "请输入真实姓名",
            "required": "required",
        }
    )
    userpassword = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码!"),
            Length(min=6,message="密码长度不符合要求")
        ],
        description="密码",
        render_kw={
            "placeholder":"密码长度必须大于6位小于20位",
            "required":"required",
        }
    )
    userRemi = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入密码!"),
            Length(min=6, message="密码长度不符合要求"),
            EqualTo('userpassword', message="两次输入的密码不一致")
        ],
        description="确认密码",
        render_kw={
            "placeholder": "两次密码须一致",
            "required": "required",
        }
    )
    sex =SelectField(
        label='性别',
        render_kw={
            'class': 'form-control'
        },
        choices=[(1, '男'), (2, '女')],
        default=1,
        coerce=int
    )
    weixin = StringField(
        label='微信',
        description="微信",
        render_kw={
        }
    )
    birthday  = StringField(
        label="生日",
        description="生日",
        render_kw={
            "class": "form-group",
            "id":"input_release_time",
            "placeholder": "请选择时间"
        }
    )

    userphone = StringField(
        label="电话",
        validators=[
            DataRequired("请输入您的电话!"),
            regexp("1[345678]\\d{9}",message="手机格式不正确！"),
        ],
        description="电话",
        render_kw={
            "placeholder": "请输入您的电话",
            "required": "required",
        }
    )
    userAddress = StringField(
        label="地址",
        description="地址",
        render_kw={
            "placeholder": "请输入您的联系地址",

        }
    )
    face = FileField(
        label="头像",
        validators=[
            # 文件必须选择;

            # 指定文件上传的格式;
            FileAllowed(['png', 'jpg', 'jpeg', 'gif'], "只接收png/jpg/jpeg/gif格式的头像")
        ]
    )
    info = TextAreaField(
        label="简介",
        description="简介",
        render_kw={
            "class": "form-group",
            "rows" : "10",
            "id": "input_info",
        }
    )
    submit = SubmitField(
        "注册"
    )
    #验证账号是否被注册
    def validate_userId(self,field):
        userId = field.data
        account = Users.query.filter_by(account = userId).count()
        if account == 1:
            raise ValidationError("账号已被注册换一个试试！")
    #验证电话号是否唯一
    def validate_userphone(self,field):
        userphone=field.data
        userphone = Users.query.filter_by(phone = userphone).count()
        if userphone == 1:
            raise ValidationError("手机号已备占用！")

#添加购买记录表单
class BuycattleFrom(FlaskForm):
    print("进入PurchaseFrom表单信息")
    cattleid = StringField(
        label="肉牛编号",
        validators=[
            DataRequired("请输入肉牛Id!")
        ],
        description="肉牛编号",
        render_kw={
            "placeholder": "请输入肉牛Id"
        }
    )
    cattlename = StringField(
        label="肉牛昵称",
        description="肉牛昵称",
        render_kw={
            "placeholder":"肉牛昵称"
        }
    )
    buyday = StringField(
        label="购买时间",
        validators=[
            DataRequired("请输入购买时间!")
        ],
        description="购买时间",
        render_kw={
            "id":"input_release_time",
            "placeholder": "购买时间"
        }
    )
    buyprice = StringField(
        label="购买总价",
        validators=[
            DataRequired("请输入购买总价!")
        ],
        description="购买总价",
        render_kw={
            "placeholder": "请输入购买总价"
        }
    )
    buyweight = StringField(
        label="购买体重",
        description="购买时体重",
        render_kw={
            "placeholder": "请输入购买时的体重"
        }
    )
    buyfreight = StringField(
        label="购买运费",
        description="购买时体重",
        render_kw={
            "placeholder": "请输入购买时的运费"
        }
    )
    buycity = StringField(
        label="购买地点",
        description="购买时地点",
        render_kw={
            "placeholder": "请输入购买时的地点"
        }
    )
    buynum = StringField(
        label="购买批次号",
        description="购买批次号",
        render_kw={
            "placeholder": "请输入购买批次号"
        }
    )
    buycontatcs = StringField(
        label="购买联系人",
        description="购买时联系人",
        render_kw={
            "placeholder": "请输入购买时购买联系人"
        }
    )
    buyphone = StringField(
        label="电话",
        description="电话",
        render_kw={
            "placeholder": "联系人电话",
        }
    )
    remarks = StringField(
        label="备注",
        render_kw={
            "placeholder": "请输入备注"
        }
    )
    buycattlefild  = FileField(
        label="肉牛图片",
        validators=[
            # 文件必须选择;
            #FileRequired(),
            # 指定文件上传的格式;
            FileAllowed(['png', 'jpg', 'jpeg', 'gif'], "只接收png/jpg/jpeg/gif格式的头像")
        ]
    )
    submit = SubmitField(
        "保存",
        render_kw={
             "class":"btn btn-primary"
        }
    )
    def validate_cattleid(self,field):
        #获取表单数据
        print("进入validate_cattleid函数")
        cattleid = field.data
        #调用用户user模型sql 查询这账号 数据
        na = Sales.query.filter_by(account = session['account'], cattleid = cattleid ).count()
        print(na)
        #如果 获取的数据为0条 证明无此账号
        if na != 0:
            raise ValidationError("无法添加！已存在该肉牛ID的购买信息，尝试修改记录吧！")

#添加出售记录
class SellcattleFrom(FlaskForm):
    print("进入PurchaseFrom表单信息")
    sellday = StringField(
        label="出栏时间",
        validators=[
            DataRequired("请输入出栏时间!")
        ],
        description="出栏时间",
        render_kw={
            "class": "form-group",
            "id":"input_release_time",
            "placeholder": "请输入出栏时间"
        }
    )
    sellprice = StringField(
        label="卖出总价",
        validators=[
            DataRequired("请输入卖出总价!")
        ],
        description="卖出总价",
        render_kw={
            "class": "form-group",
            "placeholder": "请输入卖出总价"
        }
    )
    sellweight = StringField(
        label="出栏体重",
        description="出栏时体重",
        render_kw={
            "class": "form-group",
            "placeholder": "请输入购出栏时的体重"
        }
    )
    sellfreight = StringField(
        label="出栏运费",
        description="出栏时的运费",
        render_kw={
            "class": "form-group",
            "placeholder": "请输入购出栏时的运费"
        }
    )
    sellcity = StringField(
        label="卖出地点",
        description="出售时地点",
        render_kw={
            "class": "form-group",
            "placeholder": "请输入出售时的地点"
        }
    )
    sellnum = StringField(
        label="出栏批次号",
        description="出栏批次号",
        render_kw={
            "class": "form-group",
            "placeholder": "请输入出栏批次号"
        }
    )
    sellcontatcs = StringField(
        label="卖出联系人",
        description="卖出联系人",
        render_kw={
            "class": "form-group",
            "placeholder": "请输入卖出时联系人"
        }
    )
    sellphone = StringField(
        label="电话",
        description="电话",
        render_kw={
            "placeholder": "联系人电话",
        }
    )
    sellcattlefild = FileField(
            label="肉牛图片",
            validators=[
                # 指定文件上传的格式;
                FileAllowed(['png', 'jpg', 'jpeg', 'gif'], "只接收png/jpg/jpeg/gif格式的头像")
            ]
        )
    submit = SubmitField(
        "保存",
        render_kw={
             "class":"btn btn-primary"
        }
    )
    def validate_cattleid(self,field):
        #获取表单数据
        print("进入出栏validate_cattleid函数")
        cattleid = field.data
        #调用用户user模型sql 查询这账号 数据
        na = Sales.query.filter_by(account = session['account'], cattleid = cattleid ).count()
        print(na)
        #如果 获取的数据为0条 证明无此账号
        if na == 0:
            raise ValidationError("没有该牛购买信息，请先添加购买信息再回来试试！")

#修改买卖记录
class CattleupFrom(FlaskForm):
    cattlename = StringField(
        label="肉牛昵称",
        description="肉牛昵称",
        render_kw={
            "style": "width:100%",
        }
    )
    buyprice = StringField(
        label="购买总价",
        description="购买总价",
        render_kw={
             "style": "width:45%",
        }
    )
    sellprice = StringField(
        label="卖出总价",
        description="卖出总价",
        render_kw={
            "style": "width:45%",
        }
    )
    buyweight = StringField(
        label="购买体重",
        description="购买时体重",
        render_kw={
             "style": "width:40%",
        }
    )
    sellweight = StringField(
        label="出栏体重",
        description="出栏时体重",
        render_kw={
             "style": "width:40%",
        }
    )
    buyunitprice = StringField(
        label="购买单价",
        description="购买单价",
        render_kw={
             "style": "width:40%",
        }
    )
    sellunitprice = StringField(
        label="出栏单价",
        description="出栏单价",
        render_kw={
             "style": "width:40%",
        }
    )
    buyday = StringField(
        label="购买时间",
        description="购买时间",
        render_kw={
            "id": "input_release_time",
            "style": "width:45%",
        }
    )
    sellday = StringField(
        label="出栏时间",
        description="出栏时间",
        render_kw={
            "id": "input_release_time1",
            "style": "width:45%",
        }
    )
    buynum = StringField(
        label="购买批次号",
        description="购买批次号",
        render_kw={
            "style": "width:45%",
        }
    )
    sellnum = StringField(
        label="出栏批次号",
        description="出栏批次号",
        render_kw={
            "style": "width:45%",
        }
    )
    buycity = StringField(
        label="购买地点",
        description="购买时地点",
        render_kw={
            "style": "width:45%",
        }
    )
    sellcity = StringField(
        label="出售地点",
        description="出售时地点",
        render_kw={
            "style": "width:45%",
        }
    )
    buycontatcs = StringField(
        label="购买联系人",
        description="购买时联系人",
        render_kw={
            "style": "width:45%",
        }
    )
    sellcontatcs = StringField(
        label="卖出联系人",
        description="卖出联系人",
        render_kw={
            "style": "width:45%",
        }
    )
    buyphone = StringField(
        label="电话",
        description="电话",
        render_kw={
            "style": "width:45%",
        }
    )
    sellphone = StringField(
        label="电话",
        description="电话",
        render_kw={
            "style": "width:45%",
        }
    )
    submit = SubmitField(
        "保存",
        render_kw={
            "class": "btn btn-primary"
        }
    )





#修改密码表单
class PwdFrom(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码!"),
            Length(min=6, message="密码长度必须大于6位小于20位")
        ],
        description="旧密码",
        render_kw={
            "placeholder": "请输入旧密码",
            "class": "form-control",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码!"),
            Length(min=6, message="密码长度必须大于6位小于20位")
        ],
        description="密码",
        render_kw={
            "placeholder": "请输入新密码",
            "class": "form-control",
        }
    )
    submit = SubmitField(
          "修改"
        )

    def validate_old_pwd(self, field):
        from flask import session
        print("0001")
        old_pwd = field.data
        name = session["username"]
        print('session["username"]',session["username"])
        user = Users.query.filter_by( name = name ).first()
        if not  user.chek_pwd(old_pwd):
            print("001")
            raise ValidationError("旧密码错误！")
#添加权限
class ActhForm(FlaskForm):
    name = StringField(
        label="卖出联系人",
        validators=[
            DataRequired("请输入卖出时联系人!")
        ],
        description="卖出联系人",
        render_kw={
            "class": "form-group",
            "placeholder": "请输入卖出时联系人"
        }
    )

#修改个人资料
class UserupFrom(FlaskForm):
    weixin = StringField(
        label='微信',
        description="微信",
        render_kw={"placeholder": "请输入微信号"
        }
    )
    birthday  = StringField(
        label="生日",
        description="生日",
        render_kw={
            "class": "form-group",
             "id":"input_release_time",
            "placeholder": "请选择时间"
        }
    )

    userphone = StringField(
        label="电话",

        description="电话",
        render_kw={
            "placeholder": "请输入您的电话",
        }
    )
    userAddress = StringField(
        label="地址",
        description="地址",
        render_kw={
            "placeholder": "请输入您的联系地址",

        }
    )
    face = FileField(
        label="头像",
        validators=[
            # 文件必须选择;

            # 指定文件上传的格式;
            FileAllowed(['png', 'jpg', 'jpeg', 'gif'], "只接收png/jpg/jpeg/gif格式的头像")
        ]
    )
    info = TextAreaField(
        label="简介",
        description="简介",
        render_kw={
            "style" : "width: 500px",
            "id":"input_info",
            "rows" : "10",
        }
    )
    submit = SubmitField(
        "保存修改"
    )
    #验证电话号是否唯一
    def validate_userphone(self,field):
        userphone=field.data
        userphone = Users.query.filter_by(phone = userphone).count()
        if userphone == 1:
            raise ValidationError("手机号已备占用！")






























