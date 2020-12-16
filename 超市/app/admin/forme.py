# 导入flask_wtf包 主要用于表单处理的
from flask_wtf import FlaskForm
# 从wtf框架中导入 标签账号   密码框  登入按钮
from wtforms import StringField, PasswordField, SubmitField
# 导入验证器
from wtforms.validators import DataRequired,ValidationError
from app.models import User

class LoginForm(FlaskForm):
    """登入表单"""
    name = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号!",)
        ],
        description="账号",
        render_kw={
            "id": "userv",
            "placeholder": "请输入账号"
        }

    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码!")
        ],
        description="密码框",
        render_kw={
            "placeholder": "请输入密码"
        }
    )

    submit1 = SubmitField(
        "登录",
        render_kw={
            "id": "lg"
        }
    )
    #自定义处理器 传入表单上传的数据
    def validate_name(self,field):
        #获取表单数据
        name = field.data
        print(name)
        #调用用户user模型sql 查询这账号 数据
        na = User.query.filter_by(name=name).count()
        print(na)
        #如果 获取的数据为0条 证明无此账号
        if na == 0:
            #wtforms.validators中导入ValidationError 自定义err提示
            raise ValidationError("您的账号不存在")



