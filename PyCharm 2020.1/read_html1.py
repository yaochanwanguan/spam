import pandas as pd

url='http://ranking.promisingedu.com/qs'
df = pd.read_html(url)[0]
# 默认是dataframe组成的list，list[0]即第一个表格，dataframe格式
print(df)

df.to_csv('free ip.csv', encoding='utf_8_sig', header=1, index=0)
print('done!')