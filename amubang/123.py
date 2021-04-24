import requests
# 引用requests库
from bs4 import BeautifulSoup
# 引用BeautifulSoup库
res_movies = requests.get('https://zhujia.zhuwang.cc/areapriceinfo-220100.shtml')
# 获取数据
bs_movies = BeautifulSoup(res_movies.text,'html.parser')
# 解析数据
#print(bs_movies)
list_movies= bs_movies.find_all('td')  #定位提取长春各地区的价格数据
data = []
for i in list_movies:
   data.append(i.text)
nanguan = data[:6]
kuancheng = data[6:12]
chaoyang = data[12:18]
erdao = data[18:24]
lvyuan = data[24:30]
shuangyang = data[30:36]
nongan = data[36:42]
jiutai = data[42:48]
yushu = data[48:54]
dehui = data[54:60]
li = ['地  区','外三元','内三元','土杂猪','玉 米','豆 柏']
print(li)
print(nanguan)
print(kuancheng)
print(chaoyang)
print(erdao)
print(lvyuan)
print(shuangyang)
print(nongan)
print(jiutai)
print(yushu)
print(dehui)

