# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 18:07:14 2020

@author: panglei
"""


import os
import sys
import seaborn as sns
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import *  
from datetime import datetime
from pandas.tseries.offsets import Day,MonthEnd
import matplotlib.dates as mdate
import time

start = time.time()
df_mchnt_dir = r"C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/商户交易累计/2020-06-03-11-02 商户交易.xlsx"
df_test = pd.read_excel(df_mchnt_dir,sheet_name = 'Sheet1',dtype=object,header=0)

success_list = ['00','']
df_success = df_test[df_test['resp_cd4'].isin(success_list)]

date_list = (df_success.groupby('hp_settle_dt').agg('sum')).index.to_list()

#%%cell
df_sum_0 = pd.DataFrame(columns=['mchnt_cd', 'trans_at', 'sys_tra_no', 'trans_at_average_100','trans_at_bigthan_4800','trans_at_bigthan_2000',
                                 'trans_num_permachnt_loan', 'card_accptr_nm_addr', 'loan_at_ratio','hp_settle_dt','risk_level'])

df_sended = pd.read_excel(r'C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/向拉卡拉报送商户代码台账.xlsx',header=0, squeeze=True,dtype=object)
df_sended_level = df_sended[['商户代码','商户风险分级']]
df_sended_level.columns = ['mchnt_cd','risk_level']
    
for date_i in date_list:
    df_sucess = df_success[df_success['hp_settle_dt']==date_i]
    #当日金额
    mchnt_trans_at = df_sucess.groupby('mchnt_cd')['trans_at'].agg('sum')
    mchnt_trans_at = mchnt_trans_at.sort_values(ascending=False)    
    #交易笔数
    mchnt_trans_num = df_sucess.groupby('mchnt_cd')['sys_tra_no'].agg('count')
    mchnt_trans_num = mchnt_trans_num.sort_values(ascending=False)
    #笔均金额
    grouped = df_sucess.groupby('mchnt_cd')
    def average_100(arr):
        total = 0
        count = 0
        for element in arr:
            if element>100:
                total = total + element
                count = count + 1
        if count==0:
            return 0
        else:
            return total/count            
    trans_at_average_100 = grouped['trans_at'].agg(average_100)
    trans_at_average_100 = pd.DataFrame({'mchnt_cd':trans_at_average_100.index,'trans_at_average_100':trans_at_average_100.values})
    #大于4800元的笔数占比
    grouped = df_sucess.groupby('mchnt_cd')
    def bigthan_4800(arr):
        total = 0
        count = 0
        for element in arr:
            total = total + 1
            if element>=4500:
                count = count + 1
        if count==0:
            return 0
        else:
            return count/total
    trans_at_bigthan_4800 = grouped['trans_at'].agg(bigthan_4800)
    trans_at_bigthan_4800 = pd.DataFrame({'mchnt_cd':trans_at_bigthan_4800.index,'trans_at_bigthan_4800':trans_at_bigthan_4800.values})  
    #贷记卡金额占比
    #大于2000元的笔数占比
    grouped = df_sucess.groupby('mchnt_cd')
    def bigthan_2000(arr):
        total = 0
        count = 0
        for element in arr:
            total = total + 1
            if element>=2000:
                count = count + 1
        if count==0:
            return 0
        else:
            return count/total
    trans_at_bigthan_2000 = grouped['trans_at'].agg(bigthan_2000)
    trans_at_bigthan_2000 = pd.DataFrame({'mchnt_cd':trans_at_bigthan_2000.index,'trans_at_bigthan_2000':trans_at_bigthan_2000.values})  
    
    
    grouped = df_sucess[df_sucess['card_attr'].isin(['02','03'])].groupby('mchnt_cd')
    trans_num_permachnt_loan = grouped['trans_at'].agg('sum')
    trans_num_permachnt_loan = pd.DataFrame({'mchnt_cd':trans_num_permachnt_loan.index,'trans_num_permachnt_loan':trans_num_permachnt_loan.values})
    
    #匹配合并
    machnt = pd.merge(mchnt_trans_at,mchnt_trans_num,how='left',on = 'mchnt_cd')
    machnt = pd.merge(machnt,trans_at_average_100,how='left',on = 'mchnt_cd')
    machnt = pd.merge(machnt,trans_at_bigthan_4800,how='left',on = 'mchnt_cd')
    machnt = pd.merge(machnt,trans_at_bigthan_2000,how='left',on = 'mchnt_cd')    
    machnt = pd.merge(machnt,trans_num_permachnt_loan,how='left',on = 'mchnt_cd')
    machnt = pd.merge(machnt,df_sended_level,how='left',on = 'mchnt_cd')
    #machnt = pd.merge(machnt,pd.concat([df['mchnt_cd'],df['card_accptr_nm_addr']], axis=1),how='left',on = 'mchnt_cd')
    machnt['loan_at_ratio'] = machnt['trans_num_permachnt_loan']/machnt['trans_at']
    machnt = machnt.drop_duplicates()
    
    #疑似风险
    #交易金额
    machnt_risk = machnt[machnt['trans_at']>25000]
    #交易笔数
    machnt_risk = machnt_risk[machnt_risk['sys_tra_no']>9]
    #贷记卡交易占比
    machnt_risk = machnt_risk[machnt_risk['loan_at_ratio']>0.98]
    #大于4800的交易占比
    machnt_risk = machnt_risk[machnt_risk['trans_at_bigthan_4800']>0.6]
    #笔均金额
    machnt_risk = machnt_risk[machnt_risk['trans_at_average_100']>=3000]
    machnt_risk['hp_settle_dt'] = date_i
    df_sum_0 = pd.concat([df_sum_0,machnt_risk], axis=0)
    end = time.time()
    print('已运行%f秒'%(end-start))
    print(date_i+'数据处理完毕')
writer = pd.ExcelWriter(r'C:/工作/典型事件/手机POS交易数据疑似套现/规则测算/mchnt_risk_date1105_3.xlsx')
df_sum_0.to_excel(writer, index=False,encoding='utf-8')
writer.save()

''' 
    #日均金额
    grouped = df_sucess.groupby('mchnt_cd')
    def average_day(df):
        df = df.sort_values(by='hp_settle_dt_origin')
        trans_days = (df['hp_settle_dt_origin'][-1]-df['hp_settle_dt_origin'][0]).days
        if trans_days==0:
            return df['trans_at'].sum()
        else:
            return df['trans_at'].sum()/trans_days
        
    trans_at_average_day = grouped[['trans_at','hp_settle_dt_origin']].apply(average_day)
    trans_at_average_day = pd.DataFrame({'mchnt_cd':trans_at_average_day.index,'trans_at_average_day':trans_at_average_day.values})
'''