import requests
from lxml import html
url='https://zhujia.zhuwang.cc/areapriceinfo-220000.shtml'
page=requests.Session().get(url)
tree=html.fromstring(page.text)
result=tree.xpath('//*[@id="footer"]/div[2]/table/tbody/tr[1]/td[2]')
print(result)