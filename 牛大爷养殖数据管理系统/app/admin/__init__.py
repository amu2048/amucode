#导入蓝图定义框架
from flask import Blueprint

admin =Blueprint("admin",__name__)
import app.admin.views



