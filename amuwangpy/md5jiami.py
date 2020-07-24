import hashlib

def md5(pwd):
    a= hashlib.md5(pwd.encode('utf-8'))
    print('加密的密码',a.hexdigest())
    return a.hexdigest()

a = md5('amu317')
print(a)