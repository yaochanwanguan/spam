import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
dt = pd.read_csv('a.csv', names=['发件人', '发件时间', '收件人', '邮件'])
# print(dt)
# 给列重命名
# dt = dt.rename(columns={'From': '发件人', 'Data': '发件时间', 'To': '收件人', 'Mail': '邮件'})
# print(dt)
dt.to_csv('F:/test/b.csv')

#显示所有列
# pd.set_option('display.max_columns', None)
#显示所有行
# pd.set_option('display.max_rows', None)
# #设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth',100)
# 计算缺失值
lack = dt.apply(lambda x:sum(x.isnull())/len(x))
# print(lack)

# 将数据集按时间列进行升序排列
dt.sort_values(by='发件时间', ascending=True, inplace=True)
# print(dt)

# 将序号重新排列
# dt.reset_index(drop=True, inplace=False)
# print(dt)

# 查看数据列信息
# print(dt.info())

# 查看数据基本统计
# print(dt.describe())

# 值替换
dt = dt.replace(np.nan,0)
# print(dt)
# 重复值
dIndex = dt.duplicated('邮件')
# 剔除邮件列的重复值
newDF = dt.drop_duplicates('邮件')
# print(newDF)
print(newDF.reset_index(drop=True, inplace=False))
