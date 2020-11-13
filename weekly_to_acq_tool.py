# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:18:21 2020

@author: panglei
"""

import pandas as pd
import os
import time

df_raw_dir = r'C:/工作/每周发收单/20201109/bk_fxbdb.tbl_bkfxb_fraudrate_mchnt_y_dtl_01123902.txt'
df_tool_dir = r'C:/工作/参数表&小工具/相关参数表.xlsx'
df_history_dir = r'C:/工作/每周发收单/每周向收单发送欺诈高风险商户台账_截至20201108.xlsx'
df_fraud_rate_history_dir = r'C:/工作/每周发收单/风险商户台账-2020年9月.xlsx'
result_dir = r'C:/工作/每周发收单/test.xlsx'

df_raw_colname = ['type', '商户代码', '商户名称', 'acq_ins_id_cd', 'fraud_at', 'fraud_cnt',
                  'fraud_card', 'trans_sum', 'trans_cnt', 'ratio', 'record_dt']
df_raw = pd.read_table(df_raw_dir, delimiter=',',
                       header=0, squeeze=True, dtype=object, names=df_raw_colname)
df_tool_fgs = pd.read_excel(df_tool_dir,sheet_name = '地区分公司对应',header=0, squeeze=True,dtype=object)
df_tool_acq = pd.read_excel(df_tool_dir,sheet_name = '机构列表',header=0, squeeze=True,dtype=object)
df_history = pd.read_excel(df_history_dir,sheet_name = 'Sheet1',header=0, squeeze=True,dtype=object)

df_raw[['fraud_at','trans_sum','fraud_cnt','ratio']] = df_raw[['fraud_at','trans_sum','fraud_cnt','ratio']].astype(float)
df_raw = df_raw[df_raw['record_dt']=='20201108']
#%%互联网
df_internet = df_raw[df_raw['type']=='互联网']
df_fraud_internet = df_internet[df_internet['fraud_at']>50000]
df_fraud_internet = df_fraud_internet[df_fraud_internet['ratio']>0.001]
def ratio_func(arr):
    if arr>0.001 and arr<=0.005:
        level = 1
    elif arr>0.005 and arr<=0.03:
        level = 2
    elif arr>0.03:
        level = 3
    return level

df_fraud_internet['fraud_level'] = df_fraud_internet['ratio'].apply(ratio_func)

#%% 实体
df_entity = df_raw[df_raw['type']=='实体']
df_fraud_entity = df_entity[(df_entity['fraud_at']>30000)|(df_entity['fraud_cnt']>=3)]
df_fraud_entity = df_fraud_entity[df_fraud_entity['ratio']>0.025]

def entity_func(arr):
    if arr>0.025 and arr<=0.3:
        level = 1
    elif arr>0.3 and arr<=0.9:
        level = 2
    elif arr>0.9:
        level = 3
    return level
df_fraud_entity['fraud_level'] = df_fraud_entity['ratio'].apply(entity_func)
#%% 双免
df_nopow = df_raw[df_raw['type']=='双免']
df_fraud_nopow = df_nopow[(df_nopow['fraud_at']>2000)|(df_nopow['fraud_cnt']>=3)]
df_fraud_nopow = df_fraud_nopow[df_fraud_nopow['ratio']>0.2]

def nopow_func(arr):
    if arr>0.2 and arr<=0.5:
        level = 1
    elif arr>0.5 and arr<=0.9:
        level = 2
    elif arr>0.9:
        level = 3
    return level
df_fraud_nopow['fraud_level'] = df_fraud_nopow['ratio'].apply(nopow_func)

df_fraud = pd.concat([df_fraud_internet,df_fraud_entity,df_fraud_nopow],axis=0)
df_fraud['ratio'] = df_fraud['ratio']*10000
#df.apply(lambda x: (1 if np.isnan(x[0]) and x[1] == 0 else 0), axis=1)
df_fraud['acq_key'] = df_fraud['acq_ins_id_cd'].str[:4]
df_fraud['province_key'] = df_fraud['acq_ins_id_cd'].str[4:6]
df_fraud['province_key_1'] = df_fraud['acq_ins_id_cd'].str[4:]
df_tool_fgs = df_tool_fgs[['REGION_CD','地区码','CUP_BRANCH_NM']]
df_tool_fgs.columns = ['province_key','province_key_1','分公司']

df_tool_acq = df_tool_acq[['机构代码','机构名称']]
df_tool_acq.columns = ['acq_key','机构名称']

df_fraud = pd.merge(df_fraud,df_tool_acq,how='left',on='acq_key')
df_fraud = pd.merge(df_fraud,df_tool_fgs[['province_key','分公司']],how='left',on='province_key')
df_fraud = pd.merge(df_fraud,df_tool_fgs[['province_key_1','分公司']],how='left',on='province_key_1')
###分公司还有宁波的情况要处理
df_fraud = pd.merge(df_fraud,df_history[['商户代码','欺诈率BP','当月测算','发送风险预警时间']],how='left',on='商户代码')
df_fraud['欺诈率较上次变化'] = df_fraud['ratio']-df_fraud['欺诈率BP']

df_fraud = df_fraud.drop_duplicates()
#%% 分公司问题修正
def cal_test(field1, field2):
    if type(field2)==float:
        return field1
    else:
        return field2
df_fraud['分公司'] = df_fraud.apply(lambda m: cal_test(m['分公司_x'], m['分公司_y']), axis=1)

#%% 匹配过去三个月六个月欺诈率
df_fraud_rate_history = pd.read_excel(df_fraud_rate_history_dir,sheet_name ='线上风险商户',header=0, squeeze=True,dtype=object)
df_fraud_rate_past3month = df_fraud_rate_history[df_fraud_rate_history['时间']=='2020M6-2020M8']
df_fraud_rate_past6month = df_fraud_rate_history[df_fraud_rate_history['时间']=='2020M3-2020M5']

df_fraud = pd.merge(df_fraud,df_fraud_rate_past3month[['商户代码','欺诈比率','级别']],how='left',on='商户代码')
df_fraud = pd.merge(df_fraud,df_fraud_rate_past6month[['商户代码','欺诈比率','级别']],how='left',on='商户代码')


df_fraud = df_fraud[['type','商户代码', '商户名称', 'acq_ins_id_cd', 'fraud_at', 'fraud_cnt',
       'fraud_card', 'trans_sum', 'trans_cnt', 'ratio', 'record_dt','fraud_level', 
       '机构名称', '欺诈率BP', '7-9月测算', '发送风险预警时间', '欺诈率较上次变化', '分公司',
       '欺诈比率_x', '级别_x', '欺诈比率_y', '级别_y']]

df_fraud.columns = ['类型','商户代码', '商户名称', '收单机构代码', '欺诈金额', '欺诈笔数',
       '欺诈卡数', '交易金额', '交易笔数', '欺诈率', 'record_dt','风险级别', 
       '机构名称', '上次发送欺诈率', '上次发送欺诈等级', '发送风险预警时间', '欺诈率较上次变化', '分公司',
       '欺诈率3个月', '级别3个月', '欺诈比率6个月', '级别6个月']       

df_fraud['上次发送欺诈等级'].replace(['I', 'II','III','-'], [1,2,3,0], inplace=True)
df_fraud['上次发送欺诈等级'].fillna(0)
df_fraud['欺诈等级是否变化'] = df_fraud['风险级别']-df_fraud['上次发送欺诈等级']
df_fraud['上次发送欺诈等级'].replace([0,1,2,3,-1,-2,-3], ['不变','上升','上升','上升','下降','下降','下降'], inplace=True)
df_fraud['上次发送欺诈等级'].fillna('-')

writer = pd.ExcelWriter(result_dir)
df_fraud.to_excel(writer, index=False, encoding='utf-8')
writer.save()