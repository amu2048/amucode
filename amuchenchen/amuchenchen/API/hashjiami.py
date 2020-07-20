from werkzeug.security import generate_password_hash
a=input("请输入要加密的明文")
pwd =generate_password_hash(a)
print("密码为："+pwd)