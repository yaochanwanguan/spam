import requests
from bs4 import BeautifulSoup
from pandas import Series, DataFrame
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import lxml
import matplotlib.pyplot as plt

urllst = []
ui = 'https://travel.qunar.com/p-cs299878-shanghai-jingdian-1-'
for i in range(1, 4):
    urllst.append(ui + str(i))

# print(urllst)
# ul = urllst[1]
# r = requests.get(ul)
# print(r.text)
# soup = BeautifulSoup(r.text, 'lxml')
# print(soup)
# print(soup.title)

# ul = soup.find('ul',class_="list_item clrfix")
# print(ul)
# ul.text

# li = ul.find_all('li')
# print(li[0].text)
# li1 = li[0]
# print(li1)

datai = []
n=0
for ui in urllst:
    r = requests.get(ui)
    soup = BeautifulSoup(r.text, 'lxml')
        # 访问数据
    ul = soup.find('ul', class_="site-nav-bd-r")
    li = ul.find_all('li')
        # 解析标签
    for i in li:
        n += 1
        dic = {}
        dic['lat'] = i['data-lat']
        dic['lng'] = i['data-lng']
        dic['景点名称'] = i.find('span', class_="cn_tit").text
        dic['攻略提到数量'] = i.find('div', class_="strategy_sum").text
        dic['点评数量'] = i.find('div', class_="comment_sum").text
        dic['景点排名'] = i.find('span', class_="ranking_sum").text
        dic['星级'] = i.find('span', class_="total_star").find('span')['style'].split(':')[1]
        datai.append(dic)
        # 分别获取字段内容
        print(datai[:2])
        link = i.get('href')
        # 过滤空的
        if (link is not None):
    datai.append(link)
    print('成功采集%i条数据' % n)
     # # 分别获取字段内容
f = open(r'taobao.csv', 'w', encoding='utf-8')
for a in datai:
f.write(a + "\n")
f.close()
        # dic = {}
        # # dic['lat'] = i['data-lat']
        # # dic['lng'] = i['data-lng']
        # dic['淘宝网'] = i.find('div', class_="site-nav-menu-hd").text
        # #dic['我的淘宝'] = i.find('a href', class_="site-nav-menu site-nav-mytaobao site-nav-multi-menu J_MultiMenu").text
        # # dic['点评数量'] = i.find('div', class_="comment_sum").text
        # # dic['景点排名'] = i.find('span', class_="ranking_sum").text
        # # dic['星级'] = i.find('span', class_="total_star").find('span')['style'].split(':')[1]
        # datai.append(dic)

# print(datai[:5])
# print(datai[0])
# data = DataFrame(datai[0], index=[0])
# print(data)
# for da in datai:
#     data = pd.concat([data, DataFrame(da, index=[0])], axis=0, ignore_index=False)
#
# print(data)
# data.to_csv('taobao.csv', encoding='utf_8_sig')
df = pd.read_csv('free.csv', encoding='utf-8')
print(df)
# con = create_engine("mysql+pymysql://root:123456@localhost:3306/pythontest?charset=utf8",echo=True)
# df.to_sql('free', con, if_exists='replace', index=False)