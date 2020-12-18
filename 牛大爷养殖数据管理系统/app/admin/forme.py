# 导入Flask-Wtf包 主要用于表单处理的
from flask_wtf import FlaskForm
"""从wtf框架中导入 
StringField:标签
PasswordField:密码框
SubmitField: 登入按钮
"""
from wtforms import StringField, PasswordField, SubmitField,SelectField,TextAreaField
from flask_wtf.file import FileAllowed ,FileField,FileRequired# 验证文件后缀名FileField
"""导入验证器
DataRequired:提示
ValidationError:自定义ERR提示
regexp:正则表达式
EqualTo:比较器 比较两次密码是否一致
"""
from wtforms.validators import DataRequired,ValidationError,EqualTo,regexp,Length
#导入数据user表模型
from app.models import Users,Admin

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
            "required":"required"
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
            "required":"required"
        }
    )

    submit = SubmitField(
        "登录"
    )
    #自定义处理器 传入表单上传的数据 获取user的值
    def validate_user(self,field):
        #获取表单数据
        print("进入validate_user函数")
        user = field.data
        #调用用户user模型sql 查询这账号 数据
        na = Users.query.filter_by( account = user).count()
        print(na)
        #如果 获取的数据为0条 证明无此账号
        if na == 0:
            #wtforms.validators中导入ValidationError 自定义err提示
            raise ValidationError("您的账号不存在")

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
        user = Admin.query.filter_by( name = name ).first()
        if not  user.chek_pwd(old_pwd):
            print("001")
            raise ValidationError("旧密码错误！")

#添加管理员
class AdminaddFrom(FlaskForm):
    account =StringField(
        label="管理员账号",
        validators=[
            DataRequired("请输入管理员账号!")
        ],
        description="管理员账号",
        render_kw={
            "id" : "input_pwd",
            "class":"form - control",
            "placeholder":"账号唯一作为登录账号使用",
            "required":"required",
        }
    )
    userName = StringField(
        label="姓名",
        validators=[
            DataRequired("请输入您的姓名!" )
        ],
        description="账号",
        render_kw={
            "class": "form - control",
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
            "class": "form - control",
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
            "class": "form - control",
            "placeholder": "两次密码须一致",
            "required": "required",
        }
    )
    weixin = StringField(
        label='微信',
        validators=[DataRequired('请填写微信号')],
        description="微信",
        render_kw={
            "class": "form - control",
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
            "class": "form - control",
            "placeholder": "请输入您的电话",
            "required": "required",
        }
    )
    userAddress = StringField(
        label="地址",
        validators=[
            DataRequired("请输入您的联系地址!")
        ],
        description="地址",
        render_kw={
            "class": "form - control",
            "placeholder": "请输入您的联系地址",
            "required": "required",
        }
    )
    face = FileField(
        label="头像",
        validators=[
            # 文件必须选择;
            FileRequired(),
            # 指定文件上传的格式;
            FileAllowed(['png', 'jpg', 'jpeg', 'gif'], "只接收png/jpg/jpeg/gif格式的头像")
        ]
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("说点什么吧!")
        ],
        description="简介",
        render_kw={
            "class":"form - control",
            "rows" : "10",
            "id": "input_info",
        }
    )
    submit = SubmitField(
        "注册"
    )
    #验证账号是否被注册
    def validate_account(self,field):
        account = field.data
        account = Admin.query.filter_by(account = account).count()
        if account == 1:
            print("管理员已被注册")
            raise ValidationError("账号已被注册换一个试试！")
    #验证电话号是否唯一
    def validate_userphone(self,field):

        userphone=field.data
        userphone = Admin.query.filter_by(phone = userphone).count()
        print("查询手机号不存在可以添加")
        if userphone == 1:
            print("手机号已存在")
            raise ValidationError("手机号已备占用！")
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
































