# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:04:49 2020

@author: panglei
"""

import pandas as pd
import os

os.chdir(r'C:/工作/@拆分文件文件夹/')
df = pd.read_csv('GoodsRejectDetail.CSV',dtype=object,header=0)
print(df.columns)
'''
print(df.columns)
column_name_1 = '收单机构名称'
#df[column_name_1] = df[column_name_1].apply(lambda x:x.strip())
class_list_1 = list(df[column_name_1].drop_duplicates())

column_name_2 = '分公司'
#df[column_name_2] = df[column_name_2].apply(lambda x:x.strip())
class_list_2 = list(df[column_name_2].drop_duplicates())

for ele1 in class_list_1:
    for ele2 in class_list_2:
        if len(df[(df[column_name_1]==ele1)&(df[column_name_2]==ele2)])>=1:
            writer = pd.ExcelWriter(r'C:/工作/@拆分文件文件夹/'+str(ele1)+str(ele2)+'.xlsx')
            (df[(df[column_name_1]==ele1)&(df[column_name_2]==ele2)]).to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
            writer.save()
'''

#%% 一维拆分
column_name_1 = '受理日期'
#df[column_name_1] = df[column_name_1].apply(lambda x:x.strip())
class_list_1 = list(df[column_name_1].drop_duplicates())
for ele1 in class_list_1:
        writer = pd.ExcelWriter(r'C:/工作/@拆分文件文件夹/'+str(ele1)+'.xlsx')
        (df[(df[column_name_1]==ele1)]).to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
        writer.save()