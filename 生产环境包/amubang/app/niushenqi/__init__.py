#导入蓝图框架
from flask import Blueprint

#定义蓝图 ndywe时调用app下的ndywe的view视图 访问ndywe就指向ndywe的view
niushenqi = Blueprint("niushenqi",__name__)
import app.niushenqi.view