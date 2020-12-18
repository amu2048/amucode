#导入蓝图框架
from flask import Blueprint

#定义蓝图 home时调用app下的home的views视图 访问home就指向home的views
home = Blueprint("home",__name__)
import app.home.views











