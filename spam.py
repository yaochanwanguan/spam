import re
import time
import numpy as np
import pandas as pd
import matplotlib as mpl
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
dt = pd.read_csv('b.csv', names=['发件人', '发件时间', '收件人', '邮件'])
# print(dt)
# 给列重命名
# dt = dt.rename(columns={'From': '发件人', 'Data': '发件时间', 'To': '收件人', 'Mail': '邮件'})
# print(dt)

#显示所有列
# pd.set_option('display.max_columns', None)
#显示所有行
# pd.set_option('display.max_rows', None)
# #设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth',100)
# 计算缺失值
# lack = dt.apply(lambda x:sum(x.isnull())/len(x))
# print(lack)

# 将数据集按时间列进行升序排列
dt.sort_values(by='发件时间', ascending=True, inplace=True)
# print(dt)

# 将序号重新排列
dt.reset_index(drop=True, inplace=True)
# print(dt)

# 查看数据列信息
# print(dt.info())

# 查看数据基本统计
# print(dt.describe())

# 值替换
# dt = dt.replace(np.nan,0)
# print(dt)
# 重复值
dIndex = dt.duplicated('邮件')
# 剔除邮件列的重复值
newDF = dt.drop_duplicates('邮件')
# print(newDF)
# print(newDF.reset_index(drop=True, inplace=False))

# test=newDF.reset_index(drop=True, inplace=False)
# test.to_csv('b.csv')
# dt.to_csv('F:/test/b.csv', newDF.reset_index(drop=True, inplace=False))

# # 无量纲化
# print(dt[['发件时间']])
# scaler = MinMaxScaler().fit(dt[['发件时间']])
# x_trainScaler = scaler.transform(dt[["发件时间"]])
# print(x_trainScaler)

#数据降维

# 特征工程1 =>提取发件人和收件人的邮件服务器地址
def extract_email_server_address(str1):
    it = re.findall(r"@([A-Za-z0-9]*\.[A-Za-z0-9\.]+)", str(str1))
    result = ""
    if len(it) > 0:
        result = it[0]
    if not result:
        result = "unknown"
    return result
dt["to_address"] = pd.Series(map(lambda str: extract_email_server_address(str), dt["收件人"]))
dt["from_address"] = pd.Series(map(lambda str: extract_email_server_address(str), dt["发件人"]))
# print(dt.head(5))
#2(2)、特征工程1 =>查看邮件服务器的数量
print("=================to address================")
print(dt.to_address.value_counts().head(5))
print("总邮件接收服务器类别数量为:" + str(dt.to_address.unique().shape))

print("=================from address================")
print(dt.from_address.value_counts().head(5))
print("总邮件接收服务器类别数量为:" + str(dt.from_address.unique().shape))

from_address_df = dt.from_address.value_counts().to_frame()
len_less_10_from_adderss_count = from_address_df[from_address_df.from_address <= 10].shape
print("发送邮件数量小于10封的服务器数量为:" + str(len_less_10_from_adderss_count))

