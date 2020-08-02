import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# 请求URL
request_url='http://car.bitauto.com/xuanchegongju/?l=8&mid=8'


# 得到页面的内容
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
html = requests.get(request_url, headers=headers, timeout=10)
content = html.text
# 通过content创建BeautifulSoup对象
soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
print(soup)

# 在网页内容上获取相应的汽车名称、最低价格、最高价格和产品图片链接
# 获得表格内容
temptable = soup.find('div', class_='search-result-list')
print(temptable)
# 获取表格所有内容
name_list = temptable.find_all(class_='cx-name text-hover')
price_list = temptable.find_all(class_='cx-price')
photolink_list = temptable.find_all(class_='img')
# 将内容添加至df
df = pd.DataFrame(columns=['名称', '最低价格（万）', '最高价格（万）', '产品图片链接'])
 
for i in range(len(name_list)):
        item = {}
        item['名称'] = name_list[i].text
        price = price_list[i].text
        # 价格暂无时，赋值NaN
        if price == "暂无":
            item['最低价格（万）'] = np.NaN
            item['最高价格（万）'] = np.NaN
        else:
            item['最低价格（万）'] = float(price.split('-')[0])
            item['最高价格（万）'] = float(price.split('-')[1][:-1])
        item['产品图片链接'] = 'http:' + photolink_list[i]['src']
        df = df.append(item, ignore_index=True)
print(df)
df.to_csv('auto_search.csv', index=False, encoding='utf_8_sig')

