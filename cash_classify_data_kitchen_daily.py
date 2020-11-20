# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 17:14:16 2020

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
import time

#%% 每次运行checklist
curr_time_0 = datetime.now()-Day()
time_str_2 = (curr_time_0.date()).strftime("%Y-%m-%d")
time_mark = (datetime.now()).strftime("%Y-%m-%d-%H-%M-%S")
#mchnt_begin = 20201001
#mchnt_end = 20201102

os.chdir(r'C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细')
df_old_card_dir = r'卡片交易累计/2020-06-03-11-11 卡片交易台账.csv'
df_new_card_dir = r'卡片交易每周/2020-06-03-11-18 卡片交易/2020-11-18 卡片交易.txt'
card_total_dir = r'卡片交易累计/2020-06-03-11-18 卡片交易台账.csv'
mcc_dir = r'商户交易累计/2020-06-03-11-17 商户交易.xlsx'
card_class_dir = r"C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/卡片交易每周/2020-06-03-11-11t 卡片交易/卡片分类"+time_mark+".xlsx" 
machnt_classfy_dir = r"C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/卡片交易每周/2020-06-03-11-11t 卡片交易/商户维度风险评估"+time_mark+".xlsx"
machnt_classfy_0_dir = r"C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/卡片交易每周/2020-06-03-11-11t 卡片交易/商户维度风险评估每天"+time_mark+".xlsx"
df_to_lakala_this_week_dir = r"C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/卡片交易每周/2020-06-03-11-11t 卡片交易/向拉卡拉报送商户"+time_mark+".xlsx" 

#%% 导入原始数据并设置列名
df_old_card = pd.read_csv(df_old_card_dir,
                 header=0, squeeze=True,dtype=object)
df_new_card = pd.read_table(df_new_card_dir,delimiter=',',
                 header=0, squeeze=True,dtype=object)
df_new_card.columns = ['pri_acct_no_conv_sm3', 'card_attr', 'iss_ins_id_cd', 'acpt_ins_id_cd',
                'fwd_ins_id_cd', 'loc_trans_tm', 'hp_settle_dt', 'mchnt_cd',
                'card_accptr_nm_addr', 'trans_at', 'mchnt_tp', 'term_id', 'trans_chnl',
                'trans_id', 'pos_entry_md_cd', 'sys_tra_no', 'resp_cd4','sys_record_dt']

del df_new_card['sys_record_dt']
df = pd.concat([df_old_card,df_new_card], axis=0)
df.columns = ['pri_acct_no_conv_sm3', 'card_attr', 'iss_ins_id_cd', 'acpt_ins_id_cd',
                'fwd_ins_id_cd', 'loc_trans_tm', 'hp_settle_dt', 'mchnt_cd',
                'card_accptr_nm_addr', 'trans_at', 'mchnt_tp', 'term_id', 'trans_chnl',
                'trans_id', 'pos_entry_md_cd', 'sys_tra_no', 'resp_cd4']
df = df.drop_duplicates()
'''
writer = pd.ExcelWriter(card_total_dir)
df.to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
writer.save()
'''
df.to_csv(card_total_dir, index=False,encoding='utf-8')
#%%##############################################################################

df['trans_at'] = (pd.to_numeric(df['trans_at'], errors='coerce').fillna(0))/100
list_redit_card=['02','03']
df_credit = df[df['card_attr'].isin(list_redit_card)]
df_credit_success = df_credit[df_credit['resp_cd4']=='00']
df_credit_success1 = df_credit[df_credit['resp_cd4']=='00']
df_credit_success['month'] =df_credit_success['hp_settle_dt'].str[:6] 
card_num = df_credit_success['pri_acct_no_conv_sm3'].nunique()
###############################################################################
#过滤掉超低套现风险卡号
#df_credit_success为贷记卡的成功交易
customer = ['S22','S56','S46','S10','S65','S48','S20','S35','S67','S49','S50','W20','W21','']
df_credit_success_filter = df_credit_success
df_credit_success_filter = df_credit_success_filter[df_credit_success_filter['trans_id'].isin(customer)]
def card_filter_month(arr):
    month_num = len(arr.drop_duplicates())
    if (month_num>2):
        return True
    else:
        return False
    
def card_filter(arr):
    num_2000 = 0
    for element in arr:
        if element>=500:
            num_2000 = num_2000 +1
    if (len(arr)>5) and (num_2000>2):
        return True
    else:
        return False
    
def card_acq(arr):
    non_finance = 0
    union_business = 0
    total = 0
    for element in arr:
        if element[:2] == '48':
            non_finance = non_finance + 1
        if element[:4] == '4802':
            union_business = union_business + 1
        total = total +1
    if (((non_finance-union_business)/total)>0.8):
        return True
    else:
        return False                
    
df_type_temp = df_credit_success_filter.groupby('pri_acct_no_conv_sm3')['month'].agg(card_filter_month)
type_month = pd.DataFrame({'pri_acct_no_conv_sm3':df_type_temp.index,'分类':df_type_temp.values})
type_month = type_month[type_month['分类']==True]
df_temp = df_credit_success_filter[df_credit_success_filter['pri_acct_no_conv_sm3'].isin(type_month['pri_acct_no_conv_sm3'])]

df_type_temp1 = df_temp.groupby('pri_acct_no_conv_sm3')['trans_at'].agg(card_filter)
type_at_2000 = pd.DataFrame({'pri_acct_no_conv_sm3':df_type_temp1.index,'分类':df_type_temp1.values})
type_at_2000 = type_at_2000[type_at_2000['分类']==True]
df_temp1 = df_credit_success_filter[df_credit_success_filter['pri_acct_no_conv_sm3'].isin(type_at_2000['pri_acct_no_conv_sm3'])]

df_type_temp2 = df_temp1.groupby('pri_acct_no_conv_sm3')['acpt_ins_id_cd'].agg(card_acq)
type_00 = df_type_temp2[df_type_temp2.values==False]
type_0 = pd.DataFrame({'pri_acct_no_conv_sm3':df_type_temp2.index,'分类':df_type_temp2.values})
type_0 = type_0[type_0['分类']==True] 
df_temp2 = df_credit_success_filter[df_credit_success_filter['pri_acct_no_conv_sm3'].isin(type_0['pri_acct_no_conv_sm3'])]
# df_type_0 = df_credit_success_filter.drop(df_temp2.index)
# def type_0_func()
# df_type_0.groupby('pri_acct_no_conv_sm3').agg(type_0_func)
df_credit_success = df_temp2
###############################################################################
#第一类
df_single_card = df_credit_success.groupby('pri_acct_no_conv_sm3')

def classfy_card(arr):
    flag_min_1000 = 0
    flag_max_1000 = 0
    for element in arr:
        if element<1000:
            flag_min_1000 = flag_min_1000 + 1
        else:
            flag_max_1000 = flag_max_1000 + 1
    if (arr.max()<1000) or (flag_max_1000<=2):
        return '1'
    else:
        return '0'
     
type_1 = df_single_card['trans_at'].agg(classfy_card)

type_1 = type_1[type_1 == '1']
type_1 = pd.DataFrame({'pri_acct_no_conv_sm3':type_1.index,'类别':type_1.values})
df_sheepwool = df_credit_success[df_credit_success['pri_acct_no_conv_sm3'].isin(type_1['pri_acct_no_conv_sm3'])]

def classfy_card_1(arr):
    
    novel_list = ['042','942','041']
    flag_novel = 0
    for element in arr:
        if element in novel_list:
            flag_novel = flag_novel + 1
    if (flag_novel>5):
        return '1_1'
    else:
        return '1'
    
df_single_card_1 = df_sheepwool.groupby('pri_acct_no_conv_sm3')
type_1_1 = df_single_card_1['pos_entry_md_cd'].agg(classfy_card_1)

###############################################################################    
#第三类
df_big_than_5000 = df_credit_success[df_credit_success['trans_at']>5000]

def classfy_card_3(arr):
    month_num = len(arr.drop_duplicates())
    if (month_num>3) and (month_num<=9):
        return '3'
    elif (month_num>9):
        return '4'  
    
df_single_card_3 = df_big_than_5000.groupby('pri_acct_no_conv_sm3')
type_30 = df_single_card_3['month'].agg(classfy_card_3)
type_3 = type_30[type_30 == '3']

#第四类中的危险人群
###############################################################################    
type_4 = type_30[type_30 == '4']

type_4 = pd.DataFrame({'pri_acct_no_conv_sm3':type_4.index,'类别':type_4.values})
df_danger = df_credit_success[df_credit_success['pri_acct_no_conv_sm3'].isin(type_4['pri_acct_no_conv_sm3'])]

def classfy_card_4(arr):
    month_num = len(arr.drop_duplicates())
    return month_num
  
df_single_card_4 = df_danger.groupby('pri_acct_no_conv_sm3')
type_4_1_month_num = df_single_card_4['month'].agg(classfy_card_4)  
type_4_1_month_num = pd.DataFrame({'pri_acct_no_conv_sm3':type_4_1_month_num.index,'月数':type_4_1_month_num.values})   
df_danger =  pd.merge(df_danger,type_4_1_month_num,how='left',on = 'pri_acct_no_conv_sm3')
df_danger['月均'] = df_danger['trans_at']/df_danger['月数']

def classfy_card_4_1(arr):
    month_avrage = arr.sum()
    if month_avrage>15000:
        return '4_1'
    else:
        return '4'
    
df_single_card_4_1 = df_danger.groupby('pri_acct_no_conv_sm3')
type_4_1_month_num = df_single_card_4_1['月均'].agg(classfy_card_4_1)      
    
###############################################################################
#第二类
########仅1000<x<5000
df_single_card = df_credit_success.groupby('pri_acct_no_conv_sm3')

def classfy_card_2(arr):
    flag_num = 0
    for element in arr:
        if (element>1000) and (element<5000) :
            flag_num = flag_num + 1
    if flag_num == len(arr):
        return '2'
    else:
        return '0'
     
type_2 = df_single_card['trans_at'].agg(classfy_card_2)  
type_2 = type_2[type_2 == 2]
################不超过三个月,5000元大于等于3笔

def classfy_card_2_1(arr):
    month_num = len(arr.drop_duplicates())
    trans_num = len(arr)
    if (month_num<=3) and (trans_num>=3) :
        return '2_1'
    else:
        return '0'  
df_single_card_2_1 = df_big_than_5000.groupby('pri_acct_no_conv_sm3')  
type_2_1 = df_single_card_2_1['month'].agg(classfy_card_2_1)    
    
type_2_1 = type_2_1[type_2_1 == '2_1']   
    
##############################################################################
result = pd.concat([type_1_1,type_2,type_2_1,type_3,type_4_1_month_num,type_00], axis=0)
result = pd.DataFrame({'pri_acct_no_conv_sm3':result.index,'类别':result.values})

card_list = pd.DataFrame(df_credit_success1['pri_acct_no_conv_sm3'].unique())
card_list.columns = ['pri_acct_no_conv_sm3']
card_list = pd.merge(card_list,result,how='left',on = 'pri_acct_no_conv_sm3')
card_list = card_list.fillna('2_2')
card_list['类别'][card_list['类别']==False] = '0'

df_mcc_raw_oringe = pd.read_excel(mcc_dir,sheet_name = 'Sheet1',dtype=object,header=0)
#%% 读取商户历史交易
df_mcc_raw = df_mcc_raw_oringe.copy(deep=True)
df_mcc_raw['hp_settle_dt'] = pd.to_numeric(df_mcc_raw['hp_settle_dt'], errors='coerce').fillna(0)
#%% 测试按月统计套现率
df_mhl_0 = pd.DataFrame(columns=['pri_acct_no_conv_sm3', 'card_attr', 'iss_ins_id_cd', 'acpt_ins_id_cd',
       'fwd_ins_id_cd', 'loc_trans_tm', 'hp_settle_dt', 'mchnt_cd',
       'card_accptr_nm_addr', 'trans_at', 'mchnt_tp', 'term_id', 'trans_chnl',
       'trans_id', 'pos_entry_md_cd', 'sys_tra_no', 'resp_cd4',
       'ext_hce_prod_nm', 'ext_hce_prod_in', 'ext_conn_in', 'record_dt','侦测时间'])
machnt_classfy_0 = pd.DataFrame(columns=['商户代码', '总金额', '贷记卡金额', '贷记卡金额占比', '交易笔数', '商户名称', '笔均金额', '卡号数量',
       '贷记卡号数量', '贷记卡卡均交易金额', '单张贷记卡交易金额占商户当日总交易金额中最大的占比', '大于4800笔数占比',
       '高风险金额', '高风险笔数', '中风险金额', '中风险笔数', '低风险金额', '低风险笔数', '近一周日均交易金额',
       '高风险笔数占比', '高风险金额占比', '中风险笔数占比', '中风险金额占比', '低风险笔数占比', '低风险金额占比',
       '中高风险金额占比', '风险金额占比', '商户套现风险分级'])
df_date = df_mcc_raw.groupby('hp_settle_dt')['sys_tra_no'].agg('count')
df_date = pd.DataFrame({'hp_settle_dt':df_date.index,'trans_at':df_date.values})
date_index = df_date.sort_values(by='hp_settle_dt')
for ele in date_index['hp_settle_dt'][-11:]:
    list_date = [20200601,20200701,20200801,20200901,20201008,20201108,20201201,20210101,20210201]
    print(str(ele)+'处理完毕')
#设置商户交易截止时间T，要晚于卡片历史交易。
    #df_mcc = df_mcc_raw[df_mcc_raw['hp_settle_dt']<=list_date[ele+1]]
    #df_mcc = df_mcc[df_mcc['hp_settle_dt']>=list_date[ele]]
    df_mcc = df_mcc_raw[df_mcc_raw['hp_settle_dt']==ele]
    df_mcc['trans_at'] = pd.to_numeric(df_mcc['trans_at'], errors='coerce').fillna(0)
    resp_cd4_list = ['00','']
    df_success = df_mcc[df_mcc['resp_cd4'].isin(resp_cd4_list)]
    #单卡多商户
    #单卡涉及商户数
    def single_card_mchnt_func(arr):
        return len(arr.unique())
    single_card_mchnt = df_success.groupby('pri_acct_no_conv_sm3')['mchnt_cd'].agg(single_card_mchnt_func)
    single_card_mchnt = pd.DataFrame({'pri_acct_no_conv_sm3':single_card_mchnt.index,'single_card_mchnt':single_card_mchnt.values})
    #单卡涉及交易笔数
    single_card_trans_num = df_success.groupby('pri_acct_no_conv_sm3')['sys_tra_no'].agg('count')
    #单卡涉及交易金额
    single_card_trans_at = df_success.groupby('pri_acct_no_conv_sm3')['trans_at'].agg('sum')
    single_card_trans_at = pd.DataFrame({'pri_acct_no_conv_sm3':single_card_trans_at.index,'single_card_trans_at':single_card_trans_at.values})

    card_risk_up_1 = single_card_mchnt[single_card_mchnt['single_card_mchnt']>3]
    card_risk_up_2 = single_card_trans_at[single_card_trans_at['single_card_trans_at']>100000]

    #'5'为单卡涉及商户数多的,单卡涉及金额超过10万
    card_list['类别'][((card_list['类别']=='2_2')|(card_list['类别']=='3'))&(card_list['pri_acct_no_conv_sm3'].isin(card_risk_up_1['pri_acct_no_conv_sm3']))] = '5'
    card_list['类别'][((card_list['类别']=='2_2')|(card_list['类别']=='3'))&(card_list['pri_acct_no_conv_sm3'].isin(card_risk_up_2['pri_acct_no_conv_sm3']))] = '5'
    writer = pd.ExcelWriter(card_class_dir)
    card_list.to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
    writer.save()
    ################################################################################################################################
    #卡号分类完毕
    low_list = ['1','2_1','2_2']
    mid_list = ['3']
    high_list = ['1_1','4_1','5']
    low_card = card_list[card_list['类别'].isin(low_list)]
    low_card['风险程度']='低'
    mid_card = card_list[card_list['类别'].isin(mid_list)]
    mid_card['风险程度']='中'
    high_card = card_list[card_list['类别'].isin(high_list)]
    high_card['风险程度']='高'
    card_class = pd.concat([low_card,mid_card,high_card], axis=0)

    #从商户维度计算统计量

    grouped = df_success.groupby('mchnt_cd')
    trans_num_permachnt = grouped['sys_tra_no'].agg('count')
    trans_num_permachnt = pd.DataFrame({'mchnt_cd':trans_num_permachnt.index,'交易笔数':trans_num_permachnt.values})
    trans_num_permachnt.columns = ['mchnt_cd','交易笔数']
    trans_at_permachnt = grouped['trans_at'].agg('sum')

    ###贷记卡金额
    grouped = df_success[df_success['card_attr'].isin(list_redit_card)].groupby('mchnt_cd')
    trans_num_permachnt_loan = grouped['trans_at'].agg('sum')
    machnt = pd.merge(trans_at_permachnt,trans_num_permachnt_loan,how='left',on = 'mchnt_cd')
    machnt.columns = ['总金额','贷记卡金额']
    machnt['贷记卡金额占比'] = machnt['贷记卡金额']/machnt['总金额']
    machnt = pd.merge(machnt,trans_num_permachnt,how='left',on = 'mchnt_cd')

    ##匹配商户名称
    mchnt_cd_nm = df_success[['mchnt_cd','card_accptr_nm_addr']].drop_duplicates()
    #mchnt_cd_nm = pd.DataFrame({'mchnt_cd':mchnt_cd_nm.index,'商户名称':mchnt_cd_nm.values})
    machnt = pd.merge(machnt,mchnt_cd_nm,how='left',on = 'mchnt_cd')

    ###100元以上的交易的笔均金额
    grouped = df_success.groupby('mchnt_cd')
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
    trans_at_average_100 = pd.DataFrame({'mchnt_cd':trans_at_average_100.index,'笔均金额':trans_at_average_100.values})
    machnt = pd.merge(machnt,trans_at_average_100,how='left',on = 'mchnt_cd')

    ###商户近一周的日均交易金额
    curr_time = datetime.now()-3*Day()
    time_str_1 = (curr_time.date()-Day()).strftime("%Y%m%d")

    grouped = df_success.groupby('mchnt_cd')
    def average_day_last_week(df):
        #df = df.sort_values(by='hp_settle_dt')
        df['hp_settle_dt_time'] = pd.to_datetime(df['hp_settle_dt'],format='%Y%m%d')
        df = df.sort_values(by='hp_settle_dt_time')
        trans_days = (df['hp_settle_dt_time'].iloc[-1]-df['hp_settle_dt_time'].iloc[0]).days    
        if trans_days==0:
            return df['trans_at'].sum()
        elif (trans_days>7):
            df = df[(df['hp_settle_dt']>int((curr_time.date()-7*Day()).strftime("%Y%m%d")))&(df['hp_settle_dt']<int(curr_time.date().strftime("%Y%m%d")))]
            return df['trans_at'].sum()/7
        else:
            df = df[(df['hp_settle_dt']>int((curr_time.date()-7*Day()).strftime("%Y%m%d")))&(df['hp_settle_dt']<int(curr_time.date().strftime("%Y%m%d")))]
            return df['trans_at'].sum()/trans_days
        
    trans_at_average_day_last_week = grouped[['trans_at','hp_settle_dt']].apply(average_day_last_week)
    trans_at_average_day_last_week = pd.DataFrame({'mchnt_cd':trans_at_average_day_last_week.index,'trans_at_average_day_last_week':trans_at_average_day_last_week.values})

    ###商户涉及卡数
    grouped = df_success.groupby('mchnt_cd')
    def uniq(arr):
        return arr.nunique()
    card_num_permachnt = grouped['pri_acct_no_conv_sm3'].agg(uniq)
    card_num_permachnt = pd.DataFrame({'mchnt_cd':card_num_permachnt.index,'卡号数量':card_num_permachnt.values})
    machnt = pd.merge(machnt,card_num_permachnt,how='left',on = 'mchnt_cd')
    ###商户贷记卡数
    grouped = df_success[df_success['card_attr'].isin(list_redit_card)].groupby('mchnt_cd')
    credit_card_num_permachnt = grouped['pri_acct_no_conv_sm3'].agg(uniq)
    credit_card_num_permachnt = pd.DataFrame({'mchnt_cd':credit_card_num_permachnt.index,'贷记卡号数量':credit_card_num_permachnt.values})
    machnt = pd.merge(machnt,credit_card_num_permachnt,how='left',on = 'mchnt_cd')

    ###贷记卡卡均交易金额
    machnt['贷记卡卡均交易金额']=machnt['贷记卡金额']/machnt['贷记卡号数量']
    #%% 单张贷记卡交易金额占商户当日总交易金额中最大的占比
    grouped = df_success.groupby('mchnt_cd')
    def single_mchnt_max_loan(df):
        single_card_trans_at = df.groupby('pri_acct_no_conv_sm3')['trans_at'].agg('sum')
        return (single_card_trans_at.sort_values(ascending=False)[0])/(df['trans_at'].sum())
    single_credit_card_transat_permachnt = grouped.apply(single_mchnt_max_loan)
    single_credit_card_transat_permachnt = pd.DataFrame({'mchnt_cd':single_credit_card_transat_permachnt.index,'单张贷记卡交易金额占商户当日总交易金额中最大的占比':single_credit_card_transat_permachnt.values})
    machnt = pd.merge(machnt,single_credit_card_transat_permachnt,how='left',on = 'mchnt_cd')
    #%% 交易金额大于4800元的笔数占比
    grouped = df_success.groupby('mchnt_cd')
    def bigthan_4800(arr):
        total = 0
        count = 0
        for element in arr:
            total = total + 1
            if element>=4800:
                count = count + 1
        if count==0:
            return 0
        else:
            return count/total
    trans_at_bigthan_4800 = grouped['trans_at'].agg(bigthan_4800)
    trans_at_bigthan_4800 = pd.DataFrame({'mchnt_cd':trans_at_bigthan_4800.index,'大于4800笔数占比':trans_at_bigthan_4800.values})  
    machnt = pd.merge(machnt,trans_at_bigthan_4800,how='left',on = 'mchnt_cd')
    #%% 交易金额大于4800元的金额占比
    grouped = df_success.groupby('mchnt_cd')
    def bigthan_4800_at(arr):
        total = 0
        count = 0
        for element in arr:
            total = total + element
            if element>=4800:
                count = count + element
        if count==0:
            return 0
        else:
            return count/total
    trans_at_bigthan_4800_at = grouped['trans_at'].agg(bigthan_4800_at)
    trans_at_bigthan_4800_at = pd.DataFrame({'mchnt_cd':trans_at_bigthan_4800_at.index,'大于4800金额占比':trans_at_bigthan_4800_at.values})  
    machnt = pd.merge(machnt,trans_at_bigthan_4800_at,how='left',on = 'mchnt_cd')
    
    ###高风险
    df_high_risk = df_success[df_success['pri_acct_no_conv_sm3'].isin(high_card['pri_acct_no_conv_sm3'])]
    trans_at_high_risk = df_high_risk.groupby('mchnt_cd')['trans_at'].agg('sum')
    trans_num_high_risk = df_high_risk.groupby('mchnt_cd')['sys_tra_no'].agg('count')
    card_num_high_risk = df_high_risk.groupby('mchnt_cd')['pri_acct_no_conv_sm3'].agg(uniq)
    high_risk = pd.merge(trans_at_high_risk,trans_num_high_risk,how='left',on = 'mchnt_cd')
    high_risk = pd.merge(high_risk,card_num_high_risk,how='left',on = 'mchnt_cd')
    high_risk.columns = ['高风险金额','高风险笔数','高风险卡数']

    ###中风险
    df_mid_risk = df_success[df_success['pri_acct_no_conv_sm3'].isin(mid_card['pri_acct_no_conv_sm3'])]
    trans_at_mid_risk = df_mid_risk.groupby('mchnt_cd')['trans_at'].agg('sum')
    trans_num_mid_risk = df_mid_risk.groupby('mchnt_cd')['sys_tra_no'].agg('count')
    mid_risk = pd.merge(trans_at_mid_risk,trans_num_mid_risk,how='left',on = 'mchnt_cd')
    mid_risk.columns = ['中风险金额','中风险笔数']

    ###低风险
    df_low_risk = df_success[df_success['pri_acct_no_conv_sm3'].isin(low_card['pri_acct_no_conv_sm3'])]
    trans_at_low_risk = df_low_risk.groupby('mchnt_cd')['trans_at'].agg('sum')
    trans_num_low_risk = df_low_risk.groupby('mchnt_cd')['sys_tra_no'].agg('count')
    low_risk = pd.merge(trans_at_low_risk,trans_num_low_risk,how='left',on = 'mchnt_cd')
    low_risk.columns = ['低风险金额','低风险笔数']

    machnt = pd.merge(machnt,high_risk,how='left',on = 'mchnt_cd')
    machnt = pd.merge(machnt,mid_risk,how='left',on = 'mchnt_cd')
    machnt = pd.merge(machnt,low_risk,how='left',on = 'mchnt_cd')
    machnt = pd.merge(machnt,trans_at_average_day_last_week,how='left',on = 'mchnt_cd')

    machnt['高风险笔数占比'] = machnt['高风险笔数']/machnt['交易笔数']
    machnt['高风险金额占比'] = machnt['高风险金额']/machnt['总金额']
    machnt['中风险笔数占比'] = machnt['中风险笔数']/machnt['交易笔数']
    machnt['中风险金额占比'] = machnt['中风险金额']/machnt['总金额']
    machnt['低风险笔数占比'] = machnt['低风险笔数']/machnt['交易笔数']
    machnt['低风险金额占比'] = machnt['低风险金额']/machnt['总金额']
    machnt['中高风险金额占比'] = machnt['中风险金额占比'] + machnt['高风险金额占比']
    machnt['风险金额占比'] = machnt['中风险金额占比'] + machnt['高风险金额占比']+machnt['低风险金额占比']
    
    machnt = machnt.drop_duplicates(['mchnt_cd'])
################################################################################################################################
#商户分级筛选
#高风险商户
    machnt = machnt.fillna(0)

    high_risk_machnt = machnt[machnt['交易笔数']>5]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['总金额']>=15000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['笔均金额']>=3000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['贷记卡金额占比']>=0.85]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['贷记卡卡均交易金额']>=8000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['大于4800笔数占比']>=0]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['大于4800金额占比']>=0]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['中高风险金额占比']>=0.3]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['高风险笔数']>=-1]
    high_risk_machnt_1 = high_risk_machnt[high_risk_machnt['高风险卡数']>=-1]
    high_risk_machnt_1['商户套现风险分级'] = '高风险1'

    high_risk_machnt = machnt[machnt['交易笔数']>5]
    high_risk_machnt = high_risk_machnt[~high_risk_machnt['mchnt_cd'].isin(high_risk_machnt_1['mchnt_cd'])]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['总金额']>=15000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['笔均金额']>=3000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['贷记卡金额占比']>=0.85]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['贷记卡卡均交易金额']>=0]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['大于4800笔数占比']>=0]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['大于4800金额占比']>=0]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['中高风险金额占比']>=0]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['高风险笔数']>=2]
    high_risk_machnt_2 = high_risk_machnt[high_risk_machnt['高风险卡数']>=-1]
    high_risk_machnt_2['商户套现风险分级'] = '高风险2'

    high_risk_machnt = machnt[machnt['交易笔数']>5]
    high_risk_machnt = high_risk_machnt[~high_risk_machnt['mchnt_cd'].isin(high_risk_machnt_1['mchnt_cd'])]
    high_risk_machnt = high_risk_machnt[~high_risk_machnt['mchnt_cd'].isin(high_risk_machnt_2['mchnt_cd'])]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['总金额']>=15000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['笔均金额']>=3500]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['贷记卡金额占比']>=0.85]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['贷记卡卡均交易金额']>=8000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['大于4800笔数占比']>=0.6]
    high_risk_machnt_3 = high_risk_machnt[high_risk_machnt['大于4800金额占比']>=0.8]
    high_risk_machnt_3['商户套现风险分级'] = '高风险3'

    high_risk_machnt = pd.concat([high_risk_machnt_1,high_risk_machnt_2,high_risk_machnt_3], axis=0)
    #high_risk_machnt['商户套现风险分级'] = '高风险'

    #中风险商户
    mid_risk_machnt = machnt[machnt['交易笔数']>4]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(high_risk_machnt['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['贷记卡金额占比']>0.85]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['笔均金额']>2500]
    mid_risk_machnt_1 = mid_risk_machnt[mid_risk_machnt['中高风险金额占比']>0.35]
    mid_risk_machnt_1['商户套现风险分级'] = '中风险1'

    mid_risk_machnt = machnt[machnt['交易笔数']>4]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(high_risk_machnt['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(mid_risk_machnt_1['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['笔均金额']>2500]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['贷记卡金额占比']>0.85]
    mid_risk_machnt_2 = mid_risk_machnt[mid_risk_machnt['高风险笔数']>=1]
    mid_risk_machnt_2['商户套现风险分级'] = '中风险2'

    mid_risk_machnt = machnt[machnt['交易笔数']>3]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(high_risk_machnt['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(mid_risk_machnt_1['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(mid_risk_machnt_2['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['笔均金额']>2500]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['贷记卡金额占比']>0.85]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['总金额']>7000]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['大于4800笔数占比']>=0.4]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['大于4800金额占比']>=0]
    mid_risk_machnt_3 = mid_risk_machnt[mid_risk_machnt['贷记卡卡均交易金额']>5000]
    mid_risk_machnt_3['商户套现风险分级'] = '中风险3'
    mid_risk_machnt = pd.concat([mid_risk_machnt_1,mid_risk_machnt_2,mid_risk_machnt_3], axis=0)
    #mid_risk_machnt['商户套现风险分级'] = '中风险'

    #低风险商户
    low_risk_machnt = machnt[~machnt['mchnt_cd'].isin(high_risk_machnt['mchnt_cd'])]
    low_risk_machnt = low_risk_machnt[~low_risk_machnt['mchnt_cd'].isin(mid_risk_machnt['mchnt_cd'])]

    non_risk_machnt = low_risk_machnt[low_risk_machnt['交易笔数']==1]
    non_risk_machnt = non_risk_machnt[non_risk_machnt['高风险金额']==0]
    non_risk_machnt_1 = non_risk_machnt[non_risk_machnt['中风险金额']==0]

    low_risk_machnt_raw = low_risk_machnt[~low_risk_machnt['mchnt_cd'].isin(non_risk_machnt_1['mchnt_cd'])]
    low_risk_machnt = low_risk_machnt_raw[low_risk_machnt_raw['总金额']>6500]
    low_risk_machnt = low_risk_machnt[low_risk_machnt['交易笔数']>3]
    mid_risk_machnt_3 = mid_risk_machnt[mid_risk_machnt['贷记卡卡均交易金额']>3000]
    low_risk_machnt = low_risk_machnt[low_risk_machnt['贷记卡金额占比']>0.85]

    non_risk_machnt_2 = low_risk_machnt_raw[~low_risk_machnt_raw['mchnt_cd'].isin(low_risk_machnt['mchnt_cd'])]

    low_risk_machnt['商户套现风险分级'] = '低风险'
    non_risk_machnt = pd.concat([non_risk_machnt_1,non_risk_machnt_2], axis=0)
    non_risk_machnt['商户套现风险分级'] = '暂无风险'
    machnt_classfy = pd.concat([high_risk_machnt,mid_risk_machnt,low_risk_machnt,non_risk_machnt], axis=0)
    #更改列名
    machnt_classfy.rename(columns={'mchnt_cd':'商户代码','card_accptr_nm_addr':'商户名称','trans_at_average_day_last_week':'近一周日均交易金额'},inplace=True)

    #%%调整输出格式
    percent_col = ['贷记卡金额占比','高风险笔数占比','高风险金额占比','中风险笔数占比','中风险金额占比',
    '低风险笔数占比','低风险金额占比','中高风险金额占比','风险金额占比']
    for percent_ele in percent_col:
        machnt_classfy[percent_ele] = pd.Series(["{0:.2f}%".format(val * 100) for val in machnt_classfy[percent_ele]], index = machnt_classfy.index)

    machnt_classfy = round(machnt_classfy,2)
    machnt_classfy['侦测时间'] = ele
    writer = pd.ExcelWriter(machnt_classfy_dir)
    machnt_classfy.to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
    writer.save()
################################################################################################################
    df_this_month = machnt_classfy[(machnt_classfy['商户套现风险分级']!='暂无风险')]
    #df_this_month = machnt_classfy[(machnt_classfy['商户套现风险分级']=='高风险1')|(machnt_classfy['商户套现风险分级']=='高风险2')|(machnt_classfy['商户套现风险分级']=='高风险3')]
    #df_this_month = machnt_classfy[(machnt_classfy['商户套现风险分级']=='低风险')]
    df_this_month_mhl = df_mcc[df_mcc['mchnt_cd'].isin(df_this_month['商户代码'].to_list())]
    df_this_month_mhl['侦测时间'] = ele
    df_mhl_0 = pd.concat([df_mhl_0,df_this_month_mhl],axis=0)
    df_mhl_0.drop_duplicates(inplace=True)
    machnt_classfy_0 = pd.concat([machnt_classfy_0,machnt_classfy],axis=0)
    writer = pd.ExcelWriter(machnt_classfy_0_dir)
    machnt_classfy_0.to_excel(writer, index=False,encoding='utf-8')
    writer.save()
################################################################################################################
    ##向拉卡拉报送商户
    df_sended = pd.read_excel(r'向拉卡拉报送商户代码台账.xlsx',
                    header=0, squeeze=True,dtype=object)
    '''
    df_sended_midhigh = df_sended[(df_sended['商户风险分级']=='高风险')|(df_sended['商户风险分级']=='中风险')|(df_sended['商户风险分级']=='风险')]
    df_sended_low = df_sended[(df_sended['商户风险分级']=='低风险')]
    df_to_lakala_this_week = machnt_classfy[~machnt_classfy['商户代码'].isin(df_sended_midhigh['商户代码'])]

    df_to_lakala_this_week = df_to_lakala_this_week[df_to_lakala_this_week['商户套现风险分级']!='暂无风险']

    df_to_lakala_this_week_1 = df_to_lakala_this_week[(df_to_lakala_this_week['商户套现风险分级']=='高风险')|(df_to_lakala_this_week['商户套现风险分级']=='中风险')]
    df_low_lakala = df_to_lakala_this_week[df_to_lakala_this_week['商户套现风险分级']=='低风险']
    df_to_lakala_this_week_2 = df_low_lakala[~(df_low_lakala['商户代码'].isin(df_sended_low['商户代码'].tolist()))]

    df_to_lakala_this_week = pd.concat([df_to_lakala_this_week_1,df_to_lakala_this_week_2], axis=0)
    '''
    df_to_lakala_this_week = machnt_classfy[~machnt_classfy['商户代码'].isin(df_sended['商户代码'])]
    df_to_lakala_this_week = df_to_lakala_this_week[df_to_lakala_this_week['商户套现风险分级']!='暂无风险']
    writer = pd.ExcelWriter(df_to_lakala_this_week_dir)
    df_to_lakala_this_week.to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
    writer.save()
#%%

df_mid_high = pd.concat([df_high_risk,df_mid_risk], axis=0)
df_mid_high_low = pd.concat([df_high_risk,df_mid_risk,df_low_risk], axis=0)
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['MSYH.TTC']
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串
def plot_risk(df_sucess_time,name):
    df_sucess_time['hp_settle_dt'] = pd.to_datetime(df_sucess_time['hp_settle_dt'],format='%Y%m%d')
    df_sucess_time.index = df_sucess_time['hp_settle_dt']
    df_sucess_time.rename(columns={'hp_settle_dt':'hp_settle_dt_origin'}, inplace = True)
    #del df_sucess_time['hp_settle_dt']
    df_sucess_time = df_sucess_time.sort_index()
    plt.figure(dpi=500)#设置分辨率
    splot = df_sucess_time.groupby('hp_settle_dt')['trans_at'].agg('sum').plot()
    plt.xticks(rotation=0)#设置刻度旋转角度
    plt.xlabel('时间',fontsize=11)#设置刻度标签
    plt.ylabel(name+'交易金额',fontsize=11)
    plt.savefig(name+'交易金额随时间变化曲线.png',bbox_inches = 'tight')

plot_risk(df_mid_high,'中高风险')
plot_risk(df_mid_high_low,'低中高风险')

# writer = pd.ExcelWriter(r"C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/数据室/中高风险交易.xlsx" )
# df_mid_high.to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
# writer.save()

writer = pd.ExcelWriter(r"C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/数据室/低中高风险交易0820.xlsx" )
df_mid_high_low.to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
writer.save()
    
# mid_high = df_success[(df_success['mchnt_cd'].isin(high_risk_machnt['mchnt_cd']))|(df_success['mchnt_cd'].isin(mid_risk_machnt['mchnt_cd']))]
# mid_high = mid_high[mid_high['card_attr'].isin(list_redit_card)]
# qr_mid_high = (mid_high[mid_high['ext_hce_prod_nm']=='Z'])['trans_at'].sum()

# low_mid_high = df_success[(df_success['mchnt_cd'].isin(high_risk_machnt['mchnt_cd']))|(df_success['mchnt_cd'].isin(mid_risk_machnt['mchnt_cd']))|(df_success['mchnt_cd'].isin(low_risk_machnt['mchnt_cd']))]
# low_mid_high = low_mid_high[low_mid_high['card_attr'].isin(list_redit_card)]
# qr_low_mid_high = (low_mid_high[~(low_mid_high['ext_hce_prod_nm']=='Z')])['trans_at'].sum()
    
###############################################################################
#%%报送拉卡拉之后的中高风险商户交易情况
mcclist_to_lakala = pd.read_excel(r'向拉卡拉报送商户代码台账.xlsx',sheet_name = 'Sheet1',dtype=object,header=0)
mcclist_to_lakala.columns = ['mchnt_cd','risk_rank','to_lakala_dt','mchnt_nm','measure','note']
#转化日期格式

df_mcc_lakala = df_success[df_success['mchnt_cd'].isin(mcclist_to_lakala['mchnt_cd'])]
df_mcc_lakala = pd.merge(df_mcc_lakala,mcclist_to_lakala,how='left',on='mchnt_cd')
df_mcc_lakala['hp_settle_dt'] = pd.to_datetime(df_mcc_lakala['hp_settle_dt'],format='%Y%m%d')
df_mcc_lakala['union'] = df_mcc_lakala['mchnt_cd']+str(df_mcc_lakala['hp_settle_dt'])

def after_to_lakala(df):
    return df[df['hp_settle_dt']>(df['to_lakala_dt'] + 3*Day())]
df_after_lakala = df_mcc_lakala.groupby('mchnt_cd').apply(after_to_lakala)
writer = pd.ExcelWriter(r"C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/测算/报送拉卡拉之后的中高风险商户交易情况1104.xlsx" )
df_after_lakala.to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
writer.save()

writer = pd.ExcelWriter(r"C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/测算/报送拉卡拉之前的中高风险商户交易情况1104.xlsx" )
(df_mcc_lakala[~df_mcc_lakala['union'].isin(df_after_lakala['union'].tolist())]).to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
writer.save()

#%%
    
df_sended_1 = pd.read_excel(r'C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/卡片交易每周/2020-06-03-11-04 卡片交易/商户维度风险评估1104.xlsx',
                 header=0, squeeze=True,dtype=object)
df_sended_1 = df_sended_1[df_sended_1['商户套现风险分级'].isin(['高风险','中风险'])]

df_mcc_raw['hp_settle_dt'] = pd.to_datetime(df_mcc_raw['hp_settle_dt'],format='%Y%m%d')   
df_mcc_raw = df_mcc_raw[df_mcc_raw['card_attr'].isin(['02','03'])]
df_mid_high_low_raw = df_mcc_raw[df_mcc_raw['mchnt_cd'].isin(df_sended_1['商户代码'])]
df_sended.rename(columns={'商户代码':'mchnt_cd'}, inplace = True)
df_mid_high_low_raw =  pd.merge(df_mid_high_low_raw,df_sended,how='left',on = 'mchnt_cd')


def plot_risk_rate(df_sucess_time,df_sum,name):
    # df_sucess_time['hp_settle_dt'] = pd.to_datetime(df_sucess_time['hp_settle_dt'],format='%Y%m%d')
    # df_sucess_time.index = df_sucess_time['hp_settle_dt']
    # df_sucess_time.rename(columns={'hp_settle_dt':'hp_settle_dt_origin'}, inplace = True)
    
    # df_sum['hp_settle_dt'] = pd.to_datetime(df_sum['hp_settle_dt'],format='%Y%m%d')
    # df_sum.index = df_sum['hp_settle_dt']
    # df_sum.rename(columns={'hp_settle_dt':'hp_settle_dt_origin'}, inplace = True)    
    #del df_sucess_time['hp_settle_dt']
    df_sucess_time = df_sucess_time.sort_index()
    df_sum = df_sum.sort_index()
    plt.figure(dpi=500)#设置分辨率
    df_temp3 = df_sucess_time.groupby('hp_settle_dt')['trans_at'].agg('sum')/df_sum.groupby('hp_settle_dt')['trans_at'].agg('sum')
    #df_temp3=df_sucess_time.groupby('hp_settle_dt')['trans_at'].agg('sum')
    splot = (df_temp3).plot()
    # i=0
    # for a,b in zip(df_temp3.index,df_temp3.values):
    #     i=i+1
    #     if i%6==0:
    #         plt.text(a, b+0.03, '%.2f%%' % (b*100), ha='center', va= 'bottom',fontsize=6,
    #                  #bbox=dict(boxstyle="round",ec=(0.9,1., 0.9),fc=(0.9,1., 0.9))
    #                  )
    #     elif i%3==0:
    #         plt.text(a, b-0.04, '%.2f%%' % (b*100), ha='center', va= 'bottom',fontsize=6,
    #                  #bbox=dict(boxstyle="round",ec=(0.9,1., 0.9),fc=(0.9,1., 0.9))
    #                  )
    plt.xticks(rotation=15)#设置刻度旋转角度
    #plt.ylim([-100000,1750000])
    plt.xlabel('时间',fontsize=11)#设置刻度标签
    plt.ylabel(name+'',fontsize=11)
    plt.savefig(name+'随时间变化合并.png',bbox_inches = 'tight')
#%%套现时间回溯
cash_T = 31
df_mid_high_low_raw['套现开始日期'] = df_mid_high_low_raw['报送日期']-cash_T*Day()
df_mid_high_low = df_mid_high_low_raw[(df_mid_high_low_raw['hp_settle_dt']>df_mid_high_low_raw['套现开始日期'])]
plot_risk_rate(df_mid_high_low,df_mcc_raw,'中高低风险金额')

df_mid_high_low['trans_at'].sum()/df_mcc_raw['trans_at'].sum()
df_mid_high_low_715 = df_mid_high_low[df_mid_high_low['hp_settle_dt']>datetime(2020, 7, 15, 0)]
df_mcc_715 = df_mcc_raw[df_mcc_raw['hp_settle_dt']>datetime(2020, 7, 15, 0)]
df_mid_high_low_715['trans_at'].sum()/df_mcc_715['trans_at'].sum()

#%% 累计套现率拟合曲线
#df_mid_high_low_pile = df_mid_high_low.groupby('hp_settle_dt')['trans_at'].agg('sum')
df_mhl_0 = df_mhl_0[df_mhl_0['card_attr'].isin(['02','03'])]
df_mhl_0['hp_settle_dt'] = pd.to_datetime(df_mhl_0['hp_settle_dt'],format='%Y%m%d')
df_mid_high_low_pile = df_mhl_0.groupby('hp_settle_dt')['trans_at'].agg('sum')
df_mid_high_low_pile = pd.DataFrame({'hp_settle_dt':df_mid_high_low_pile.index,'trans_at':df_mid_high_low_pile.values})
df_mid_high_low_pile.index = df_mid_high_low_pile['hp_settle_dt']
df_mid_high_low_pile['cumsum'] = df_mid_high_low_pile['trans_at'].cumsum()

df_mcc_raw = df_mcc_raw[df_mcc_raw['card_attr'].isin(['02','03'])]
df_mcc_raw['hp_settle_dt'] = pd.to_datetime(df_mcc_raw['hp_settle_dt'],format='%Y%m%d')
df_mcc_pile = df_mcc_raw.groupby('hp_settle_dt')['trans_at'].agg('sum')
df_mcc_pile = pd.DataFrame({'hp_settle_dt':df_mcc_pile.index,'trans_at':df_mcc_pile.values})
df_mcc_pile.index = df_mcc_pile['hp_settle_dt']
df_mcc_pile['cumsum'] = df_mcc_pile['trans_at'].cumsum()
fit_test_pile = (df_mid_high_low_pile['cumsum']/df_mcc_pile['cumsum'])
plt.figure(dpi=500)#设置分辨率
splot = fit_test_pile.plot()
plt.xticks(rotation=0)#设置刻度旋转角度
plt.xlabel('时间',fontsize=11)#设置刻度标签
plt.ylim(0,1)
plt.ylabel('回溯'+str(cash_T)+'天'+'套现率',fontsize=11)
plt.savefig('回溯'+str(cash_T)+'天'+'套现率随时间变化曲线.png',bbox_inches = 'tight')

#%%
fit_test = (df_mid_high_low.groupby('hp_settle_dt')['trans_at'].agg('sum')/df_mcc_raw.groupby('hp_settle_dt')['trans_at'].agg('sum')).rolling(10).mean(min_period=10)
fit_test.plot()

# %%
df_mid_high_low_pile['month'] = df_mid_high_low_pile['hp_settle_dt'].astype(str).str[:7]
df_mcc_pile['month'] = df_mcc_pile['hp_settle_dt'].astype(str).str[:7]
a = df_mid_high_low_pile.groupby('month')['trans_at'].agg('sum')
b = df_mcc_pile.groupby('month')['trans_at'].agg('sum')

plt.figure(dpi=500)#设置分辨率
splot = (a/b).plot()
plt.xticks(rotation=0)#设置刻度旋转角度
plt.xlabel('时间',fontsize=11)#设置刻度标签
plt.ylim(0,1)
plt.ylabel('回溯'+str(cash_T)+'天'+'套现率',fontsize=11)
plt.savefig('按月套现率随时间变化曲线.png',bbox_inches = 'tight')
# %%贷记卡交易占比变化
df_mcc_full = df_mcc_raw_oringe.copy(deep=True)
df_mcc_full_loan = df_mcc_full[df_mcc_full['card_attr'].isin(['02','03'])]
loan_ratio = (df_mcc_full_loan.groupby('hp_settle_dt')['trans_at'].agg('sum'))/(df_mcc_full.groupby('hp_settle_dt')['trans_at'].agg('sum'))
loan_ratio.plot()
# %%
df_mcc_full_loan = df_mcc_full[df_mcc_full['card_attr'].isin(['02','03'])]
df_mcc_full_loan['hp_settle_dt'] = pd.to_datetime(df_mcc_full_loan['hp_settle_dt'],format='%Y%m%d')
df_mcc_full_loan_pile = df_mcc_full_loan.groupby('hp_settle_dt')['trans_at'].agg('sum')
df_mcc_full_loan_pile = pd.DataFrame({'hp_settle_dt':df_mcc_full_loan_pile.index,'trans_at':df_mcc_full_loan_pile.values})
df_mcc_full_loan_pile.index = df_mcc_full_loan_pile['hp_settle_dt']
df_mcc_full_loan_pile['cumsum'] = df_mcc_full_loan_pile['trans_at'].cumsum()

df_mcc_full['hp_settle_dt'] = pd.to_datetime(df_mcc_full['hp_settle_dt'],format='%Y%m%d')
df_mcc_full_pile = df_mcc_full.groupby('hp_settle_dt')['trans_at'].agg('sum')
df_mcc_full_pile = pd.DataFrame({'hp_settle_dt':df_mcc_full_pile.index,'trans_at':df_mcc_full_pile.values})
df_mcc_full_pile.index = df_mcc_full_pile['hp_settle_dt']
df_mcc_full_pile['cumsum'] = df_mcc_full_pile['trans_at'].cumsum()
fit_test_pile = (df_mcc_full_loan_pile['cumsum']/df_mcc_full_pile['cumsum'])
plt.figure(dpi=500)#设置分辨率
splot = fit_test_pile.plot()
plt.xticks(rotation=0)#设置刻度旋转角度
plt.xlabel('时间',fontsize=11)#设置刻度标签
plt.ylim(0.8,1)
plt.ylabel('贷记卡占比',fontsize=11)
plt.savefig('贷记卡占比随时间变化曲线.png',bbox_inches = 'tight')
# %%
