# -*- coding: utf-8 -*-
"""
Created on Sun May 24 10:06:42 2020

@author: pang_
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
from pandas.tseries.offsets import Day, MonthEnd
import time
import re
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Mm
import jinja2
import itertools
#12333443
# %%设置工作路径
output_text = []
os.chdir(r'C:/工作/典型事件/tools_dev')
# 设置参数路径
para_dir = r'C:/工作/参数表&小工具/参数/'
# 当天时间
curr_time = datetime.now()
time_str = (curr_time.date()).strftime("%Y-%m-%d")
# 设置画图字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['MSYH.TTC']
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串
sns.set_palette("muted")  # 调色盘"RdBu"
# 柱形图加标签


def show_value_for_barplot(barplot, h_v="v", form='{:.2f}%', percent=1):
    # @param format(p.get_width(), '.2f'), word in string format you want to put in the figure
    # @param (p.get_width(), p.get_y()+ p.get_height() / 2.), x and y pos of word
    # @param xytext, offset of word
    if h_v == "v":
        for p in barplot.patches:
            barplot.annotate(form.format(p.get_height()*percent),
                             (p.get_x() + p.get_width() / 2., p.get_height()),
                             ha='center', va='center', xytext=(0, 5),
                             textcoords='offset points')
    elif h_v == "h":
        for p in barplot.patches:
            barplot.annotate(format(p.get_width(), '.2f'),
                             (p.get_width(), p.get_y() + p.get_height() / 2.),
                             ha='center', va='center', xytext=(30, 0),
                             textcoords='offset points')
# 画柱形图


def barplot_pl():
    return 0


# %%导入原始数据并设置列名
# 1导入csv
#df = pd.read_csv(r'data\数据集1-浪莎支付APP泄露.csv',header=0, squeeze=True,dtype=object)
# 2导入excel
#location_id = pd.read_excel(r'地区国家表.xlsx',sheet_name='Sheet1',dtype=object,header=0)
# 3导入del
df = pd.read_csv(r'data\数据集2-印度伪卡HRT泄露.del', header=0,
                 squeeze=True, dtype=object, delimiter='\t')

# 指定某一列的数据类型
# dtype={'iss_ins_id_cd':str}
# 指定列名
#信总数据
#数据厨房
#风险系统
df.columns = ['主帐号', 'acct_no_conv_sm3', '真实卡号', 'Token号', '卡介质代码', 'card_attr', 'iss_ins_id_cd',
              'acpt_ins_id_cd', '收单机构标识码', 'fw_ins_id_cd', '接收机构标识码', '相关交易机构标识码', 'mchnt_cd', 'mchnt_tp',
              '终端号', 'trans_chnl', 'trans_id', '清算时间', '交易时间', '超时时间戳', 'trans_at', '交易货币代码',
              '转换后交易金额', '总手续费（分）', '银联手续费', '发卡手续费', '清算金额（发送方）', '清算金额（接收方）',
              '清算货币代码（发送方）', '清算货币代码（接收方）', 'pos_entry_md_cd', '服务点条件代码', '系统跟踪号', '检索参考号',
              '是否清算', 'CUPS交易状态', '转入帐户', '转出帐户', 'resp_cd4', '发卡方应答码', '授权标识应答码', '原因码',
              '例外原因码', '交易直间连标志', '卡品牌', 'card_prod_id', '卡等级', '分期付款期数', 'HCE产品类型', '特殊计费类型',
              '特殊计费档次', '接触or非接', '是否小额免密', '是否商户白名单', '是否内部云卡', '商户名称']
"""
浪莎数据
df.columns = ['acct_no_conv_sm3', '卡组织', 'Unnamed: 2', '清算时间', '交易时间', 'trans_at', 'mchnt_cd',
              'mchnt_nm', '收单机构标识码', '真实卡号', 'Token号', '卡介质代码', 'card_attr', 'iss_ins_id_cd',
              'acpt_ins_id_cd', 'fw_ins_id_cd', '接收机构标识码', '相关交易机构标识码', 'mchnt_tp', '终端号', 'trans_chnl',
              'trans_id', '超时时间戳', '交易货币代码', '转换后交易金额', '总手续费（分）', '银联手续费', '发卡手续费',
              '清算金额（发送方）', '清算金额（接收方）', '清算货币代码（发送方）', '清算货币代码（接收方）', 'pos_entry_md_cd',
              '服务点条件代码', 'sys_tra_no', '检索参考号', '是否清算', 'CUPS交易状态', '转入帐户', '转出帐户',
              'resp_cd4', '发卡方应答码', '授权标识应答码', '原因码', '例外原因码', '交易直间连标志', '卡品牌', 'card_prod_id',
              '卡等级', '分期付款期数', 'HCE产品类型', '特殊计费类型', '特殊计费档次', '接触or非接', '是否小额免密',
              '是否商户白名单', '是否内部云卡', '主帐号']

df.columns = ['acct_no_conv_sm3','card_attr','iss_ins_id_cd','acpt_ins_id_cd',
                          'fw_ins_id_cd','loc_trans_tm','hp_settle_dt','mchnt_cd','card_accptr_nm_addr',
                          'trans_at','mchnt_tp','term_id','trans_chnl','trans_id','pos_entry_md_cd',
                          'sys_tra_no','resp_cd4','acq_nm','iss_nm','month','domin_id','card_bin',
                          'card_publish_dt','card_prod_id']
数据字段中文英文格式对应：
'acct_no_conv_sm3'加密卡号,088B2F2B793E8DD451F9EB2A8F6EEB54280C4A0D8FBB3BF40D63ED8EC3506227
'card_attr',卡属性,01
'iss_ins_id_cd',发卡机构代码,63030000
'acpt_ins_id_cd',受理机构代码,49449202
'fw_ins_id_cd',发送机构代码,00010045
'收单机构标识码'
'接收机构标识码'
'相关交易机构标识码'
'终端号'
'trans_chnl',交易渠道,08
'trans_id',交易类型,S22
'清算时间',
'交易时间原始',
'超时时间戳',
'trans_at',交易金额（分）,23450
'转换后交易金额',
'总手续费（分）',
'银联手续费',
'发卡手续费',
'清算金额（发送方）','清算金额（接收方）','清算货币代码（发送方）','清算货币代码（接收方）',
'pos_entry_md_cd',服务点输入方式,012,
'服务点条件代码',
'sys_tra_no',系统跟踪号,118181,
'检索参考号','是否清算','CUPS交易状态',
'resp_cd4',应答码,00,
'发卡方应答码','授权标识应答码','原始清算日期','原始系统跟踪号','原始交易代码','原因码','例外原因码',
'交易直间连标志','卡品牌',
'card_prod_id',卡产品,0,
'卡等级','分期付款期数','分期付款商户补贴费率',
'HCE产品类型','特殊计费类型','特殊计费档次','接触or非接',
'是否小额免密','是否商户白名单','是否内部云卡','商户名称'                       
'loc_trans_tm',交易时间,092719
'hp_settle_dt',交易日期,20190105
'mchnt_cd',商户代码,944000059490170
'mchnt_nm',商户名称,XXX店
'mchnt_tp',商户类型,5949
'term_id',终端代码,01080209
'acq_nm',受理机构中文,汇聚支付
'iss_nm',发卡机构中文,工商银行
'month',交易月,201902
'domin_id',卡bin发行地区,0
'card_bin',卡bin,16622858
'card_publish_dt',卡bin发行年份,20130201
'卡性质代码',                      
"""
# %%导入参数表
# 导入机构代码
ins = pd.read_excel(para_dir+'机构列表.xlsx', sheet_name='Sheet1',
                    converters={'机构代码': str}, header=0)
ins.columns = ['iss_ins_id_cd_match', 'iss_nm']
# 导入地区国家表
location_id = pd.read_excel(
    para_dir+'地区国家表.xlsx', sheet_name='Sheet1', converters={'发卡机构代码后四位': str}, header=0)
location_id.columns = ['iss_ins_id_cd_loc_match', 'province']
# 导入商户类型表
mchnt_cat = pd.read_excel(para_dir+'商户类型表.xlsx', sheet_name='Sheet1',
                          converters={'标准': str, '优惠': str, '减免': str, '特殊计费': str}, header=0)
# 导入卡BIN(带长度位)
PARA_CARD_BIN = pd.read_csv(
    para_dir+'PARA_CARD_BIN.txt', dtype=object)  # 加载,指定它的分隔符是\t
PARA_CARD_BIN.head()
# 导入应答码
resp_cd4_para = pd.read_excel(
    para_dir+'相关参数表_小工具专用.xlsx', sheet_name='应答码匹配', dtype=object, header=0)
# 导入典型市场份额
market_share = pd.read_excel(para_dir+'各机构的市场份额.xlsx', sheet_name='Sheet1',
                             converters={'INS_CATA_NM3': str, 'ROOT_INS_CD': str,
                                         'ROOT_INS_NM': str, 'TRANS_CHNL': str}, header=0)

# %%数据清洗
# 去重
df = df.drop_duplicates()
# 统计nan数量
na_num = df.isna().sum()
# 分离时间
df['loc_trans_tm'] = df['交易时间']
df['loc_trans_tm'] = df['loc_trans_tm'].mask(
    df['交易时间'].str.len() == 10, df['交易时间'].str[4:])
df['loc_trans_tm'] = df['loc_trans_tm'].mask(
    df['交易时间'].str.len() == 6, df['交易时间'])
df['hp_settle_dt'] = df['清算时间']
df['month'] = df['hp_settle_dt'].str[:6]
# 交易金额转化为整数
df['trans_at'] = pd.to_numeric(df['trans_at'], errors='coerce').fillna(0)
df['trans_at'].astype(int)

# 将nan和inf替换为0
df['iss_ins_id_cd'].replace(np.nan, 0, inplace=True)
df['iss_ins_id_cd'].replace(np.inf, 0, inplace=True)
# 去掉无效数据
#df = df[~df['iss_ins_id_cd'].isin([0])]
# #去掉受理机构和发卡机构中文名的列
# df.drop('acq_nm',axis=1,inplace=True)
# df.drop('iss_nm',axis=1,inplace=True)
# 去重
df = df.drop_duplicates()
# 重新匹配
df['iss_ins_id_cd_match'] = df['iss_ins_id_cd'].str[2:6]
df['acpt_ins_id_cd_match'] = df['acpt_ins_id_cd'].str[2:6]
# 类似于vlookup
df = pd.merge(df, ins.loc[:, ['iss_ins_id_cd_match',
                              'iss_nm']], how='left', on='iss_ins_id_cd_match')
# 等号两边的df互相不影响
ins1 = ins.copy(deep=True)
ins1.columns = ['acpt_ins_id_cd_match', 'acq_nm']
df = pd.merge(df, ins1.loc[:, ['acpt_ins_id_cd_match',
                               'acq_nm']], how='left', on='acpt_ins_id_cd_match')
# 去掉match构造列
df.drop('iss_ins_id_cd_match', axis=1, inplace=True)
df.drop('acpt_ins_id_cd_match', axis=1, inplace=True)
# 匹配结束
output_text.append('数据清洗完成')
# %%限定时间段:
# 限定日期范围
df['loc_trans_tm'] = pd.to_datetime(df['loc_trans_tm'], format='%H%M%S')
df['hp_settle_dt'] = pd.to_datetime(df['hp_settle_dt'])
# 自定义时间段
# left_time = datetime(2019, 1, 1, 0)
# right_time = datetime(2019, 9, 1, 0)
left_time = df['hp_settle_dt'].min()
right_time = df['hp_settle_dt'].max()
df_time0 = df
df_time0['hp_settle_dt'] = pd.to_datetime(df['hp_settle_dt'])
df_time0['loc_trans_tm'] = pd.to_datetime(df['loc_trans_tm'], format='%H%M%S')
# 选取对应的时间范围内的数据，多个条件时 '|'代表'或'，'&'代表'且'
df_time = df_time0[(df_time0['hp_settle_dt'] >= left_time)
                   & (df_time0['hp_settle_dt'] <= right_time)]

# 限定时间范围，用于统计一日以内的时间段分布
# left_time_s = datetime(1900, 1, 1, 2,3,3)
# right_time_s = datetime(1900, 1, 1, 12,3,3)
left_time_s = df['loc_trans_tm'].min()
right_time_s = df['loc_trans_tm'].max()
df_time_s = df_time0[(df_time0['loc_trans_tm'] >= left_time_s) & (
    df_time0['loc_trans_tm'] <= right_time_s)]

output_text.append('数据限定时间段为从'+str(left_time)+'到'+str(right_time))
#%%总体情况
df_trans = df_time
# 去重卡片数
card_total = df_trans['acct_no_conv_sm3'].nunique()
output_text.append('本批数据总去重卡片数为：'+str(card_total))
# 总的交易笔数
count_trans = len(df_trans)
output_text.append('总的交易笔数为：'+str(count_trans))
# 成功交易
df_success = df_trans[df_trans['resp_cd4'] == '00']
# 成功交易笔数
count_trans_success = len(df_success)
# 交易金额(分)
sum_trans = df_success['trans_at'].sum()
# 笔均金额
bill_avg_trans = sum_trans/count_trans
# 卡均金额
card_avg_trans = sum_trans/card_total

output_text.append('交易金额为：'+str(sum_trans/100))
output_text.append('笔均金额为：'+str(bill_avg_trans/100))
output_text.append('卡均金额为：'+str(card_avg_trans/100))

# %%卡片维度分析
# %%发卡行分布
df_single_card = df.drop_duplicates(['acct_no_conv_sm3'])
plt.figure(dpi=600)  # 设置分辨率
card_iss_nm_distr = df_single_card['iss_nm'].value_counts()
card_iss_nm_distr = card_iss_nm_distr.reset_index()
card_iss_nm_distr.columns = ['iss_nm', 'card_num']
card_iss_nm_distr['ratio'] = card_iss_nm_distr['card_num']/card_total
splot = sns.countplot(x='iss_nm', data=df_single_card,
                      order=df_single_card['iss_nm'].value_counts()[:10].index)
show_value_for_barplot(splot, h_v="v", percent=100/card_total)
plt.xticks(rotation=15)  # 设置刻度旋转角度
plt.xlabel('发卡行', fontsize=11)  # 设置刻度标签
plt.ylabel('卡片数量', fontsize=11)
plt.savefig("picture/发卡行分布.png", bbox_inches='tight')
plt.show()
# output_text.append('卡片中发卡行占比最多的十家为：'+str(card_iss_nm_distr[:10]*100/card_total)+'%')
print(str(card_iss_nm_distr['iss_nm'][0])+'、'+str(card_iss_nm_distr['iss_nm'][1]))
# %%借贷记分布
plt.figure(dpi=600)  # 设置分辨率
card_attr_distr = df_single_card['card_attr'].value_counts()
card_attr_distr = card_attr_distr.rename(
    {'01': '借记卡', '02': '贷记卡', '03': '准贷记卡'}, axis='index')
card_attr = Series(['其他', '借记卡', '贷记卡', '准贷记卡', '借贷合一卡', '预付费卡', '单用途预付费卡'],
                   index=['0', '01', '02', '03', '04', '05', '06'])
splot = card_attr_distr.plot.pie(autopct='%.2f%%', pctdistance=0.85, startangle=0,
                                 #explode = [0, 0.1, 0],
                                 wedgeprops={'width': 0.4, 'edgecolor': 'w'})
output_text.append('卡片最多为：'+str(card_attr_distr.index[0]) +
                   ',数量占总卡片数量的'+str((splot.patches[0].theta2)/360*100)+'%')
plt.ylabel('', fontsize=11)  # 设置刻度标签
plt.xlabel('借贷记分布', fontsize=11)  # 设置刻度标签
plt.savefig("picture/借贷记分布.png", bbox_inches='tight')
plt.show()

# %%卡组织分布
# df_single_card['CARD_BIN'] = df_single_card['card_bin']
# df_single_card = pd.merge(df_single_card,PARA_CARD_BIN.loc[:,['CARD_BIN','CARD_BRAND']],how='left',on = 'CARD_BIN')
# df_single_card['CARD_BRAND'].replace(np.nan, 0, inplace=True)
# df_single_card['CARD_BRAND'].replace(np.inf, 0, inplace=True)
plt.figure(dpi=600)  # 设置分辨率
card_brand_distr = df_single_card['卡品牌'].value_counts()
card_brand_distr = card_brand_distr.rename({'0': '其他', '1': '6字头银标', '2': '6字头非标',
                                            '3': '银联9字头', '4': 'VISA卡', '5': 'MASTER卡',
                                            '6': 'JCB', '7': '美运卡', '8': '其它卡BIN'}, axis='index')
# splot = card_brand_distr.plot(kind='bar')
# show_value_for_barplot(splot,h_v="v",percent=100/card_total)


def func_pct(pct, allvals):
    absolute = int(pct/100.*allvals)
    return "{:.2f}%\n({:d})".format(pct, absolute)


splot = card_brand_distr.plot.pie(  # autopct='%.2f%%',
    autopct=lambda pct: func_pct(pct, card_total),
    pctdistance=0.85, startangle=0,
    #explode = [0, 0.1, 0],
    wedgeprops={'width': 0.4, 'edgecolor': 'w'})
plt.xticks(rotation=0)
plt.xlabel('卡组织', fontsize=11)  # 设置刻度标签
# plt.ylabel('卡片数量',fontsize=11)
plt.savefig("picture/卡组织分布.png", bbox_inches='tight')
plt.show()
card_brand = Series(['其他', '6字头银标', '6字头非标', '银联9字头', 'VISA卡', 'MASTER卡', 'JCB', '美运卡', '其它卡BIN'],
                    index=['0', '1', '2', '3', '4', '5', '6', '7', '8'])
output_text.append('卡片中卡组织最多的为：'+str(card_brand_distr.index[0]) +
                   ',数量占总卡片数量的'+str((splot.patches[0].theta2)/360*100)+'%')

# %%卡介质分布

plt.figure(dpi=600)  # 设置分辨率
card_media = Series(['未知', '磁条', 'PBOC IC卡', 'EMV IC卡', '无卡', 'Fallback', '无法识别'],
                    index=['0', '1', '2', '3', '4', '5', '9'])
card_media_distr = df_single_card['卡介质代码'].value_counts()
card_media_distr = card_media_distr.rename(card_media.to_dict(), axis='index')
splot = card_media_distr.plot(kind='bar')
show_value_for_barplot(splot, h_v="v", percent=100/card_total)
plt.xticks(rotation=0)
plt.xlabel('卡介质', fontsize=11)  # 设置刻度标签
plt.ylabel('卡片数量', fontsize=11)
plt.savefig('卡介质分布.png', bbox_inches='tight')
plt.show()

output_text.append('卡片中卡介质最多的为：'+str(card_media_distr.index[0]) +
                   ',数量占总卡片数量的'+str(splot.patches[0].get_height()*100/card_total)+'%')
# %%#卡片所在地分布
# 方法一-发卡机构代码后四位,存在问题。

df_single_card['card_location'] = df_single_card['iss_ins_id_cd'].str[-4:]
plt.figure(dpi=600)  # 设置分辨率
# 卡bin发行地区
#df_single_card['card_location'] = df_single_card['domin_id']
splot = sns.countplot(x='card_location', data=df_single_card,
                      order=df_single_card['card_location'].value_counts()[:10].index)
show_value_for_barplot(splot, h_v="v", percent=100/card_total)
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('卡片所在地', fontsize=11)  # 设置刻度标签
plt.ylabel('卡片数量', fontsize=11)
plt.savefig("picture/卡片所在地分布.png", bbox_inches='tight')
plt.show()

# %%#########方法二
"""
#采用线下交易渠道出现最多的商户的地区码max=3如果小于3的话，则补零；
#交易渠道代码01,03,11,17,39,47
"""
# 交易类型过滤，交易时间过滤todo

# 交易渠道过滤
offline = ['03', '11', '23', '17']
df_card_loc = df_time[df_time['trans_chnl'].isin(offline)]
# 用卡号对商户分组
df_card = df_card_loc['mchnt_cd'].groupby(df_card_loc['acct_no_conv_sm3'])
# 对于每一个卡号对应的商户进行统计，得到频率最高的
card_mchnt = df_card.apply(pd.value_counts)
# 丢掉<3的数据
card_mchnt = card_mchnt[card_mchnt < 5]
temp = card_mchnt.groupby('acct_no_conv_sm3').idxmax()
# 提取地区码
card_id_location = (temp.to_frame()['mchnt_cd'].str[1].str[3:7])
# 匹配
card_id_location = {'acct_no_conv_sm3': card_id_location.index,
                    'location_mchnt_id': card_id_location.values}
df_card_id_location = pd.DataFrame(card_id_location)
df_single_card = pd.merge(df_single_card, df_card_id_location.loc[:, [
                          'acct_no_conv_sm3', 'location_mchnt_id']], how='left', on='acct_no_conv_sm3')
# 用发卡机构代码地区一列填充缺失的值
df_single_card.loc[df_single_card['location_mchnt_id'].isnull(
), 'location_mchnt_id'] = df_single_card[df_single_card['location_mchnt_id'].isnull()]['iss_ins_id_cd'].str[-4:]

# if df_single_card['location_mchnt_id'].isnull() == True:
#    df_single_card['location_mchnt_id'] = df_single_card['iss_ins_id_cd'].str[-4:]
# 修改列名
location_id.rename(
    columns={'iss_ins_id_cd_loc_match': 'location_mchnt_id'}, inplace=True)
df_single_card = pd.merge(df_single_card, location_id.loc[:, [
                          'location_mchnt_id', 'province']], how='left', on='location_mchnt_id')
#df_single_card['card_location'] = temp.to_frame()['mchnt_cd'].str[1].str[3:7]
plt.figure(dpi=600)  # 设置分辨率
card_loc_distr = df_single_card['province'].value_counts()
splot = card_loc_distr[:10].plot(kind='bar')
show_value_for_barplot(splot, h_v="v", percent=100/card_total)
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('卡地区', fontsize=11)  # 设置刻度标签
plt.ylabel('卡片数量', fontsize=11)
plt.savefig("picture/卡片所在地分布近似.png", bbox_inches='tight')
plt.show()
output_text.append('卡片中卡片所在地最多的为：'+str(card_loc_distr.index[0]) +
                   ',数量占总卡片数量的'+str(splot.patches[0].get_height()*100/card_total)+'%')

# %%交易特征分析
# %%交易类型大类分布:'trans_id'
customer = ['S22', 'S56', 'S46', 'S10', 'S65', 'S48',
            'S20', 'S35', 'S67', 'S49', 'S50', 'W20', 'W21']
customer_num = len(df_trans[df_trans['trans_id'].isin(customer)])
query = ['S00']
query_num = len(df_trans[df_trans['trans_id'].isin(query)])
withdraw = ['S24']
withdraw_num = len(df_trans[df_trans['trans_id'].isin(withdraw)])
loan = ['S31', 'S78', 'W23']
loan_num = len(df_trans[df_trans['trans_id'].isin(loan)])
service = ['S55', 'S17', 'T43', 'T08', 'W10']
service_num = len(df_trans[df_trans['trans_id'].isin(service)])
trans_distr = Series([customer_num, query_num, withdraw_num, loan_num, service_num],
                     index=['消费类', '查询类', '取款类', '贷记类', '账户服务类'])
plt.figure(dpi=600)  # 设置分辨率
splot = trans_distr.plot(kind='bar')
show_value_for_barplot(splot, h_v="v", percent=100/count_trans)
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('交易类型', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.savefig("picture/交易类型大类分布.png", bbox_inches='tight')
plt.show()
if (loan_num/count_trans > 0.2):
    output_text.append('异常交易类型为：贷记类')
else:
    output_text.append('交易类型大类分布无异常！')

# %%渠道分布
# df_trans['trans_chnl']
offline = ['03', '11', '23', '17']
offline_num = len(df_trans[df_trans['trans_chnl'].isin(offline)])
online = ['07', '08', '20']
online_num = len(df_trans[df_trans['trans_chnl'].isin(online)])
atm = ['01']
atm_num = len(df_trans[df_trans['trans_chnl'].isin(atm)])
channel_distr = Series([offline_num, online_num, atm_num, count_trans-offline_num-online_num-atm_num],
                       index=['线下', '线上', 'ATM', '其他'])
plt.figure(dpi=600)  # 设置分辨率
splot = channel_distr.plot(kind='bar')
show_value_for_barplot(splot, h_v="v", percent=100/count_trans)
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('交易渠道', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.savefig("picture/交易渠道分布.png", bbox_inches='tight')
plt.show()

if (offline_num/online_num > 4/3):
    output_text.append('交易渠道异常')
else:
    output_text.append('交易渠道分布无异常！')

# %%#交易月分布!!!'month'字段含有脏数据，竟然有银行的名字。。。
plt.figure(dpi=600)  # 设置分辨率
#splot=sns.countplot(x='month',data = df_trans,order = df_trans['month'].value_counts().index)
#trans_month_distr = df_trans['month'].value_counts()
df_trans['month'] = pd.to_datetime(df_trans['month'], format='%Y%m')
trans_month_distr = df_trans.groupby('month')['acct_no_conv_sm3'].agg('count')
#trans_month_order = trans_month_distr.sort_values(ascending=False)
splot = trans_month_distr.plot()
# show_value_for_barplot(splot,h_v="v",percent=100/count_trans)
i = 0
for a, b in zip(trans_month_distr.index, trans_month_distr.values):
    i = i+1
    if i % 2 == 0:
        plt.text(a, b+30, '%.0f' % (b), ha='center', va='bottom', fontsize=6,
                 bbox=dict(boxstyle="round", ec=(0.9, 1., 0.9), fc=(0.9, 1., 0.9)))
    else:
        plt.text(a, b-40, '%.0f' % (b), ha='center', va='bottom', fontsize=6,
                 bbox=dict(boxstyle="round", ec=(0.9, 1., 0.9), fc=(0.9, 1., 0.9)))
plt.xticks(rotation=90)  # 设置刻度旋转角度
plt.xlabel('交易时间', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.savefig('picture/交易月分布.png', bbox_inches='tight')
plt.show()
# output_text.append('交易月分布最多的前三个月为：'+
#                    str(trans_month_order.index[0])+
#                    '、'+str(trans_month_order.index[1])+
#                    '、'+str(trans_month_order.index[2])+
#                    ',其中最多月的数量占总交易笔数的'+str(splot.patches[0].get_height()*100/count_trans)+'%')

# %%#金额区间段分布(消费)
df_trans_at = df_trans[df_trans['trans_id'].isin(customer)]
sections = Series([-1, 0, 10000, 100000, 250000,
                   500000, 3500000, 99999999999999])
group_names = ['0', '0~100', '100~1000', '1000~2500',
               '2500~5000', '5000~35000', '35000以上']
# df_trans['trans_at'].astype(int)
cuts = pd.cut(df_trans_at['trans_at'], sections, labels=group_names)
df_trans_at_order = cuts.value_counts().sort_values(ascending=False)
plt.figure(dpi=600)  # 设置分辨率
splot = cuts.value_counts().plot(kind='bar')
show_value_for_barplot(splot, h_v="v", form='{:.2f}%', percent=100/count_trans)
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('金额', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.title('交易金额消费区间段分布')
plt.savefig("picture/消费金额区间段分布.png", bbox_inches='tight')
plt.show()
if (df_trans_at_order[0]/count_trans > 0.5):
    output_text.append('金额区间段分布(消费)异常!请关注！')
else:
    output_text.append('金额区间段分布(消费)无异常！')
output_text.append('金额区间段分布(消费)最多的前三个月为：' +
                   str(df_trans_at_order.index[0])+'、' +
                   str(df_trans_at_order.index[1])+'、' +
                   str(df_trans_at_order.index[2])+'、' +
                   ',其中最密集金额区间段交易占总交易笔数的'+str(splot.patches[0].get_height()*100/count_trans)+'%')

# plt.figure(dpi=600)#设置分辨率
# sns.distplot(df_trans_at['trans_at'],kde=True)
# sns.violinplot(x='trans_at',cut=993,data=df_trans_at,orient='h',width=1.0)
# %%#应答码分布resp_cd4
plt.figure(dpi=600)  # 设置分辨率
resp_cd4_distr = df_trans['resp_cd4'].value_counts()
splot = resp_cd4_distr[:10].plot(kind='bar')
#splot=sns.countplot(x='resp_cd4',data = df_trans,order = df_trans['resp_cd4'].value_counts()[:10].index)
show_value_for_barplot(splot, h_v="v", form='{:.2f}%', percent=100/count_trans)
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('应答码', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.title('应答码分布')
plt.savefig("picture/应答码分布.png", bbox_inches='tight')
plt.show()
if (resp_cd4_distr['51']/count_trans > 0.01):  # 可以继续添加别的应答码
    output_text.append('应答码分布异常!请关注！')
else:
    output_text.append('应答码分布无异常！')
output_text.append('应答码分布(除去00)最多的三个应答码为：' +
                   str(resp_cd4_distr.index[1])+'、' +
                   str(resp_cd4_distr.index[2])+'、' +
                   str(resp_cd4_distr.index[3])+'、')

# %%#输入方式分布pos_entry_md_cd
plt.figure(dpi=600)  # 设置分辨率
pos_entry_md_cd_distr = df_trans['pos_entry_md_cd'].value_counts()
splot = pos_entry_md_cd_distr[:10].plot(kind='bar')
#splot=sns.countplot(x='pos_entry_md_cd',data = df_trans,order = df_trans['pos_entry_md_cd'].value_counts()[:8].index)
show_value_for_barplot(splot, h_v="v", form='{:.2f}%', percent=100/count_trans)
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('服务点输入方式', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.title('服务点输入方式')
plt.savefig("picture/服务点输入方式分布.png", bbox_inches='tight')
plt.show()
output_text.append('输入方式分布最多的三个为：' +
                   str(pos_entry_md_cd_distr.index[1])+'、' +
                   str(pos_entry_md_cd_distr.index[2])+'、' +
                   str(pos_entry_md_cd_distr.index[3])+'、')

# %%#交易时间段分布一天内的
time_breaks = [datetime(1900, 1, 1, 0, 0, 0), datetime(1900, 1, 1, 7, 0, 0),
               datetime(1900, 1, 1, 20, 0, 0), datetime(1900, 1, 1, 23, 0, 0),
               datetime(1900, 1, 1, 23, 59, 59)]

df_time_work = len(df[(df['loc_trans_tm'] > time_breaks[1])
                      & (df['loc_trans_tm'] < time_breaks[2])])
df_time_night = len(df[(df['loc_trans_tm'] > time_breaks[2])
                       & (df['loc_trans_tm'] < time_breaks[3])])
df_time_dawn = len(df[(df['loc_trans_tm'] > time_breaks[3]) | (
    (df['loc_trans_tm'] > time_breaks[0]) & (df['loc_trans_tm'] < time_breaks[1]))])

df_time_distr = Series([df_time_work, df_time_night, df_time_dawn],
                       index=['工作时间', '晚间', '凌晨'])
plt.figure(dpi=600)  # 设置分辨率
splot = df_time_distr.plot(kind='bar')
show_value_for_barplot(splot, h_v="v", form='{:.2f}%', percent=100/count_trans)
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('时间段', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.savefig("picture/交易时间段分布.png", bbox_inches='tight')
plt.show()

if ((df_time_distr['晚间']/count_trans > 0.1)or(df_time_distr['凌晨']/count_trans > 0.1)):
    output_text.append('一天内交易时间段分布异常!请关注！')
else:
    output_text.append('一天内交易时间段分布无异常！')


# %%#收单机构分布分析
# 去掉查询类交易
df_acq = df_time[~df_time['trans_id'].isin(['S00'])]
grouped_acq = df_acq['acct_no_conv_sm3'].groupby(df['acq_nm'])
num_per_acq = grouped_acq.nunique()
num_per_acq = num_per_acq.sort_values(ascending=False)
plt.figure(dpi=600)  # 设置分辨率
splot = num_per_acq[:10].plot(kind='bar')
show_value_for_barplot(splot, h_v="v", percent=100/card_total)
plt.xticks(rotation=15)  # 设置刻度旋转角度
plt.xlabel('收单机构', fontsize=11)  # 设置刻度标签
plt.ylabel('卡片数量', fontsize=11)
plt.savefig("picture/收单机构分布分析.png", bbox_inches='tight')
plt.show()
output_text.append('所有卡片中收单机构占比前五的为：'+str(num_per_acq[:5]))
###############################################################################
# 交易属性
# 限定时间段

# %%
# 收单机构分布
# plt.figure(dpi=600)#设置分辨率
#splot=sns.countplot(x='acq_nm',data = df_trans,order = df_trans['acq_nm'].value_counts()[:10].index)
# show_value_for_barplot(splot,h_v="v",percent=100/count_trans)
# plt.xticks(rotation=15)#设置刻度旋转角度
# plt.xlabel('收单机构',fontsize=11)#设置刻度标签
# plt.ylabel('交易笔数',fontsize=11)
#plt.savefig("picture/收单机构分布.png",bbox_inches = 'tight')
# plt.show()

# %%境内境外分布
country_list = ['0000', '0156', '0010', '0001',
                '0002', '0005', '0037', '0038', '0039']
df_outofchina_1 = df[(df['收单机构标识码'].str[6] == '0') & (
    ~((df['收单机构标识码'].str[6:]).isin(country_list)))]
df_outofchina_2 = df[df['fw_ins_id_cd'] == '0800010344']

plt.figure(dpi=600)
country_distr = pd.DataFrame(
    data={'境内外': [count_trans-len(df_outofchina_2), len(df_outofchina_2)]})
country_distr.index = ['境内', '境外']
splot = country_distr['境内外'].plot.pie(  # autopct='%.2f%%',
    autopct=lambda pct: func_pct(pct, count_trans),
    pctdistance=0.85, startangle=0,
    #explode = [0, 0.1, 0],
    wedgeprops={'width': 0.4, 'edgecolor': 'w'})
plt.ylabel('', fontsize=11)  # 设置刻度标签
plt.xlabel('境内境外交易分布', fontsize=11)  # 设置刻度标签
plt.savefig("picture/境内境外交易分布.png", bbox_inches='tight')
plt.show()
# %%境外交易商户分布
plt.figure(dpi=600)  # 设置分辨率
mchnt_accptr_nm_distr = df_outofchina_2['商户名称'].value_counts()
splot = mchnt_accptr_nm_distr[:10].plot(kind='bar')
#splot=sns.countplot(x='card_accptr_nm_addr',data = df_trans,order = df_trans['card_accptr_nm_addr'].value_counts()[:10].index)
show_value_for_barplot(splot, h_v="v", percent=100/count_trans)
plt.xticks(rotation=90)  # 设置刻度旋转角度
plt.xlabel('境外商户号', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.savefig("picture/境外商户分布.png", bbox_inches='tight')
plt.show()

# %%受理地区省级分布(利用地区码匹配省级区域)
df_trans['acpt_ins_id_cd_loc_match'] = df_trans['acpt_ins_id_cd'].str[-4:]
location_id.rename(columns={'location_mchnt_id': 'acpt_ins_id_cd_loc_match',
                            'province': 'province_acq'}, inplace=True)
df_trans = pd.merge(df_trans, location_id.loc[:, [
                    'acpt_ins_id_cd_loc_match', 'province_acq']], how='left', on='acpt_ins_id_cd_loc_match')
plt.figure(dpi=600)  # 设置分辨率
acq_loca_distr = df_trans['province_acq'].value_counts()
splot = acq_loca_distr[:10].plot(kind='bar')
#splot=sns.countplot(x='province',data = df_trans,order = df_trans['province'].value_counts()[:10].index)
show_value_for_barplot(splot, h_v="v", percent=100/count_trans)
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('受理地区', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.savefig("picture/受理地区省级分布.png", bbox_inches='tight')
plt.show()
output_text.append('受理机构地区最多的前三为：'+str(acq_loca_distr.index[0]) +
                   '、'+str(acq_loca_distr.index[1]) +
                   '、'+str(acq_loca_distr.index[2]) +
                   ',其中最多地区的数量占总交易笔数的'+str(splot.patches[0].get_height()*100/count_trans)+'%')

# %%#商户号分布 df_single_card.grupeby['mchnt_cd']
plt.figure(dpi=600)  # 设置分辨率
card_accptr_nm_distr = df_trans['商户名称'].value_counts()
splot = card_accptr_nm_distr[:10].plot(kind='bar')
#splot=sns.countplot(x='card_accptr_nm_addr',data = df_trans,order = df_trans['card_accptr_nm_addr'].value_counts()[:10].index)
show_value_for_barplot(splot, h_v="v", percent=100/count_trans)
plt.xticks(rotation=90)  # 设置刻度旋转角度
plt.xlabel('商户号', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.savefig("picture/商户分布.png", bbox_inches='tight')
plt.show()
output_text.append('商户最多的前三为：'+str(card_accptr_nm_distr.index[0]) +
                   '、'+str(card_accptr_nm_distr.index[1]) +
                   '、'+str(card_accptr_nm_distr.index[2]) +
                   ',其中交易最多商户的数量占总交易笔数的'+str(splot.patches[0].get_height()*100/count_trans)+'%')
# %%商户号卡片分布
num_per_mchnt = (df_trans['acct_no_conv_sm3'].groupby(
    df_trans['商户名称'])).nunique()
num_per_mchnt = num_per_mchnt.sort_values(ascending=False)
plt.figure(dpi=600)  # 设置分辨率
splot = num_per_mchnt[:10].plot(kind='bar')
show_value_for_barplot(splot, h_v="v", percent=100/card_total)
plt.xticks(rotation=45)  # 设置刻度旋转角度
plt.xlabel('商户名称', fontsize=11)  # 设置刻度标签
plt.ylabel('卡片数量', fontsize=11)
plt.savefig("picture/商户卡片数分布.png", bbox_inches='tight')
plt.show()


# %%#商户类型大类分布 mchnt_cd 8-11位为商户类型
df_trans['mchnt_cd_cat'] = df_trans['mchnt_cd'].str[7:11]
discount = mchnt_cat['标准']
discount_num = len(df_trans[df_trans['mchnt_cd_cat'].isin(discount)])
benefit = mchnt_cat['优惠']
benefit_num = len(df_trans[df_trans['mchnt_cd_cat'].isin(benefit)])
reduction = mchnt_cat['减免']
reduction_num = len(df_trans[df_trans['mchnt_cd_cat'].isin(reduction)])
specialbill = mchnt_cat['特殊计费']
specialbill_num = len(df_trans[df_trans['mchnt_cd_cat'].isin(specialbill)])
mchnt_cat_distr = Series([discount_num, benefit_num, reduction_num, specialbill_num],
                         index=['标准', '优惠', '减免', '特殊计费'])
plt.figure(dpi=600)  # 设置分辨率
splot = mchnt_cat_distr.plot(kind='bar')
show_value_for_barplot(splot, h_v="v", percent=100/count_trans)
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('商户类型', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.savefig("picture/商户类型大类分布.png", bbox_inches='tight')
plt.show()
if ((mchnt_cat_distr[1]*100/count_trans > 5) or (mchnt_cat_distr[2]*100/count_trans > 5) or (mchnt_cat_distr[3]*100/count_trans > 5)):
    output_text.append('商户类型大类分布异常!请关注！')
else:
    output_text.append('商户类型大类分布无异常！')
###############################################################################
# %%综合交叉分布
"""
交易类型大类&收单机构
收单机构&交易月
交易类型大类&收单机构&交易月
"""
# 交易类型大类&收单机构
trans_type_list_1 = ['消费类', '查询类', '取款类', '贷记类', '账户服务类']
trans_type_list = [customer, query, withdraw, loan, service]
for trans_type, str_trans_type in zip(trans_type_list, trans_type_list_1):
    df_trans_type = df_trans[df_trans['trans_id'].isin(trans_type)]
    grouped_trans_type = df_trans_type['acct_no_conv_sm3'].groupby(
        df['acq_nm'])
    num_per_acq_trans_type = grouped_trans_type.nunique()
    num_per_acq_trans_type = num_per_acq_trans_type.sort_values(
        ascending=False)
    plt.figure(dpi=600)  # 设置分辨率
    splot = num_per_acq_trans_type[:10].plot(kind='bar')
    #splot=sns.countplot(x='acq_nm',data = df_consumer,order = df_consumer['acq_nm'].value_counts()[:10].index)
    show_value_for_barplot(splot, h_v="v", percent=100/card_total)
    plt.xticks(rotation=15)  # 设置刻度旋转角度
    plt.xlabel('收单机构', fontsize=11)  # 设置刻度标签
    plt.ylabel('交易笔数', fontsize=11)
    plt.savefig('picture/'+str_trans_type+'交易的收单机构分布.png', bbox_inches='tight')
    plt.show()
# %%交易类型大类-分收单机构统计量


def acq_func(df, bill_sum, bill_count):
    data = {'bill_count': [0], 'bill_sum': [0], 'bill_sum_rate': [0],
            'mchnt_num': [0], 'trans_at_per_bill': [0]}
    df_new = pd.DataFrame(data=data)
    df_new['bill_count'].iloc[0] = df['acct_no_conv_sm3'].count()
    df_new['bill_sum'].iloc[0] = df['trans_at'].sum()
    df_new['bill_sum_rate'].iloc[0] = df_new['bill_sum'].iloc[0]/bill_sum
    df_new['mchnt_num'].iloc[0] = df['mchnt_cd'].nunique()
    df_new['trans_at_per_bill'].iloc[0] = df_new['bill_sum'].iloc[0] / \
        df_new['bill_count'].iloc[0]
    return df_new


i = 0
df_trans_type_tbl = locals()
for trans_type, str_trans_type in zip(trans_type_list, trans_type_list_1):
    df_trans_type = df_trans[df_trans['trans_id'].isin(customer)]
    df_trans_type_sum = df_trans_type['trans_at'].sum()
    df_trans_type_count = df_trans_type['acct_no_conv_sm3'].count()
    df_trans_type_tbl[str_trans_type] = (df_trans_type.groupby('acq_nm')).apply(
        acq_func, bill_sum=df_trans_type_sum, bill_count=df_trans_type_count)


###############################################################################
# %%#收单机构&交易月分布、

acq_list = df_trans['acq_nm'].value_counts()[:10].index.tolist()
ite = 1
for acq in acq_list:
    df_acq = df[df['acq_nm'] == acq]
    plt.figure(dpi=600)  # 设置分辨率
    splot = sns.countplot(x='month', data=df_acq)
    show_value_for_barplot(splot, h_v="v", percent=100/len(df_acq))
    plt.title(acq+'交易月分布')
    plt.xticks(rotation=90)  # 设置刻度旋转角度
    plt.xlabel('时间', fontsize=11)  # 设置刻度标签
    # plt.ylim([0,180000])
    plt.ylabel(acq+'交易笔数', fontsize=11)
    plt.savefig('picture/交易月分布'+str(ite)+'.png', bbox_inches='tight')
    plt.show()
    ite = ite + 1
###############################################################################
# %%#收单机构-交易渠道-分布距离分析
# 对收单机构典型市场份额进行计算处理
# 线下
offline_market_share = market_share[market_share['TRANS_CHNL'] == '线下']
offline_mean = offline_market_share.groupby(
    offline_market_share['ROOT_INS_CD'].str[1:5]).mean()

offline_mean['信用卡金额'] = offline_mean['信用卡金额']/offline_mean['信用卡金额'].sum()
# offline_mean['ROOT_INS_CD'].astype(str)
offline_mean['机构代码'] = offline_mean.index
# 计算分布之间的距离：
df_offline_market_share = df_time[df_time['trans_chnl'].isin(offline)]
df_offline_market_share['trans_at'].astype(float)
# df_offline_market_share['acpt_ins_id_cd']
df_offline_mean = df_offline_market_share['trans_at'].groupby(
    df_offline_market_share['acpt_ins_id_cd'].str[:4]).mean()
#df_offline_mean = df_offline_mean.to_frame()
df_offline_mean = pd.DataFrame(
    {'机构代码': df_offline_mean.index, 'trans_at': df_offline_mean.values})
df_offline_mean['trans_at'] = df_offline_mean['trans_at'] / \
    (df_offline_mean['trans_at'].sum())
df_offline_mean = pd.merge(df_offline_mean, offline_mean.loc[:, [
                           '机构代码', '信用卡金额']], how='left', on='机构代码')
df_offline_mean = df_offline_mean.fillna(0)

df_offline_mean['trans_at'] = df_offline_mean['trans_at'] / \
    (df_offline_mean['trans_at'].sum())
df_offline_mean['信用卡金额'] = df_offline_mean['信用卡金额'] / \
    (df_offline_mean['信用卡金额'].sum())

beta = np.sum((df_offline_mean['trans_at']-df_offline_mean['信用卡金额'])**2)
if beta > 0.05:
    output_text.append('收单机构分布异常，请关注！')

###############################################################################
# %%#交易类型大类&收单机构&交易月
# 标签匹配

df_label = df_time.copy(deep=True)
"""
todo
"""
#%%输出########################################################################
output_text_n = []
i = 1
for string in output_text:
    string = str(i) + ':' + string + '\n'
    i = i+1
    output_text_n.append(string)
fh = open('初步分析结果.txt', 'w', encoding='utf-8')
fh.write("".join(output_text_n))
fh.close()


# %%针对结果做进一步的处理
# 区分风险事件类型
# 信息泄露、合谋盗刷、套现代还、涉赌、跨境移机、伪冒开户、资金转移
# %%卡片占比排第一的收单机构的商户卡片分布
df_acq_mchnt_card = df_time[df_time['acq_nm'] == num_per_acq.index[0]]
num_per_mchnt1 = (df_acq['acct_no_conv_sm3'].groupby(df['商户名称'])).nunique()
num_per_mchnt1 = num_per_mchnt1.sort_values(ascending=False)
plt.figure(dpi=600)  # 设置分辨率
splot = num_per_mchnt1[:10].plot(kind='bar')
show_value_for_barplot(splot, h_v="v", percent=100/card_total)
plt.xticks(rotation=45)  # 设置刻度旋转角度
plt.xlabel('商户名称', fontsize=11)  # 设置刻度标签
plt.ylabel('卡片数量', fontsize=11)
plt.savefig("picture/同一收单的商户分布分析.png", bbox_inches='tight')
plt.show()

# %%绘制自助预授权交易笔数随时间变化曲线
S65_time = df[df['trans_id'] == 'S65']
#S65_time['hp_settle_dt'] = pd.to_datetime(S65_time['hp_settle_dt'])
S65_time.index = S65_time['hp_settle_dt']
del S65_time['hp_settle_dt']
S65_time = S65_time.sort_index()
plt.figure(dpi=600)  # 设置分辨率
splot = S65_time.groupby('hp_settle_dt').size().plot()
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('时间', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
# show_value_for_barplot(splot,h_v="v",form='.0f')
plt.savefig("picture/自助预授权交易笔数随时间变化曲线.png", bbox_inches='tight')

# %%统计异常交易卡片数量
# 计算有代付交易的卡片占总卡片的比率
S31_card_num = df[df['trans_id'] == 'S31']
S31_card_uniqe = S31_card_num['acct_no_conv_sm3'].unique()
S31_card_total = len(S31_card_uniqe)
S31_rate = S31_card_total/card_total
# 按月份分组去重再合并
grouped = S31_card_num['acct_no_conv_sm3'].groupby(S31_card_num['month'])
num_per_month = grouped.nunique()
num_per_month.to_frame()
plt.figure(dpi=600)  # 设置分辨率
splot = num_per_month.plot(kind='bar')
show_value_for_barplot(splot, h_v="v", percent=100/card_total, form='.2f')
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('月份', fontsize=11)  # 设置刻度标签
plt.ylabel('卡片数量', fontsize=11)
plt.savefig("picture/代付交易的卡片占总卡片的比率.png", bbox_inches='tight')
plt.show()

#%%取款类交易的地区分布-受理机构代码后四位

df_withdraw = df_trans[df_trans['trans_id'].isin(withdraw)]
df_withdraw['location_mchnt_id'] = df_withdraw['acpt_ins_id_cd'].str[-4:]
location_id.columns = ['location_mchnt_id','province']
df_withdraw = pd.merge(df_withdraw,location_id,how='left',on=['location_mchnt_id'])
plt.figure(dpi=600)  # 设置分辨率
withdraw_location_distr = df_withdraw['acct_no_conv_sm3'].groupby(df_withdraw['province']).agg('count').sort_values(ascending=False)
splot = withdraw_location_distr[:10].plot(kind='bar')
show_value_for_barplot(splot, h_v="v", percent=100/card_total)
plt.xticks(rotation=0)  # 设置刻度旋转角度
plt.xlabel('交易发生地区', fontsize=11)  # 设置刻度标签
plt.ylabel('交易笔数', fontsize=11)
plt.savefig("picture/取款类交易的地区分布.png", bbox_inches='tight')
plt.show()

# %%估算信息泄露时间段
"""
前后拓展时间，阈值停止
###############################################################################
"""
# 对于窗口的大小和ratio要权衡？？？
left_time_probe = datetime(2016, 6, 1, 0)
right_time_probe = datetime(2016, 7, 10, 0)
ratio_list = [0.5]
alpha = 0.005
flag = True
i = 0
while flag:
    right_time_probe = right_time_probe + i*Day()
    left_time_probe = left_time_probe - i*Day()
    df_time_right_lim = df_time[(df_time['hp_settle_dt'] > left_time_probe) & (
        df_time['hp_settle_dt'] < right_time_probe)]
    ratio = len(df_time_right_lim['acct_no_conv_sm3'].unique())/card_total
    ratio_list.append(ratio)
    if (ratio_list[-1]-ratio_list[-2]) < alpha:
        flag = False
    i = i+1
    print('左侧时间：'+str(left_time_probe),'右侧时间：'+str(right_time_probe))
output_text.append('可能的信息泄露时间段为从'+str(left_time_probe) +
                   '到'+str(right_time_probe))
print(ratio_list)
#%% rolling_test
# def rolling_func(df):
#     return df.nunique() 
df_time['hp_settle_dt_dt'] = pd.to_datetime(df_time['hp_settle_dt'])
df_time_dt = df_time[['hp_settle_dt_dt','acct_no_conv_sm3']]
df_time_dt.index = df_time_dt['hp_settle_dt_dt']
df_time_dt = df_time_dt.sort_index()
#del df_time_dt['hp_settle_dt_dt']
#plt.figure(dpi=600)
#temp_1 = df_time_dt.rolling(window = 90).apply(rolling_func)
#temp_2 = temp_1.drop_duplicates()
maximum = 0.9
for time_begin in df_time['hp_settle_dt_dt'].drop_duplicates().sort_values():
    for T_rolling in range(7,40):
        df_main = df_time_dt[(df_time_dt['hp_settle_dt_dt']>=time_begin-T_rolling*7*Day())&(df_time_dt['hp_settle_dt_dt']<=time_begin)]
        single_card_time = df_main['acct_no_conv_sm3'].nunique()
        if single_card_time/card_total>maximum:
            time_focus = time_begin
            break 
print(time_focus,T_rolling,single_card_time/card_total)
#%%三个月内的卡片覆盖率
card_in_3month_ratio = single_card_time/card_total
#%%消费代付交替交易的卡数占比
def consumer_loan_func(df):
    df.sort_values(by='hp_settle_dt',axis=0,ascending=True, inplace=True)
    count_cons_loan = 0
    df = df[(df['trans_id'].isin(customer))&(df['trans_id'].isin(loan))]
    for i in range(len(df)-1):
        if (((df['trans_id'].iloc[i] in (customer)) and (df['trans_id'].iloc[i+1] in (loan))) or ((df['trans_id'].iloc[i] in (loan)) and (df['trans_id'].iloc[i+1] in (customer)))):
            count_cons_loan = count_cons_loan + 1
    if len(df)!=0:
        return count_cons_loan/len(df)
    else:
        return 0

df_consumer_loan = df_time[['trans_id','hp_settle_dt']].groupby(df_time['acct_no_conv_sm3']).apply(consumer_loan_func)
num_consumer_loan = df_consumer_loan[df_consumer_loan.values>0.75]
#%%头部收单机构的卡片占比
df_top3_acq = df_time[df_time['acq_nm'].isin([num_per_acq.index[0],num_per_acq.index[1],num_per_acq.index[2]])]
top3_acq_card_num = df_top3_acq['acct_no_conv_sm3'].unique()/card_total
#%%卡片余额查询比例

#%%ATM余额查询交易
#%%应答码75、14/41占比异常
#%%卡BIN集中性
#%%资金入账交易占比
#%%余额查询交易占比
#%%发生在凌晨的取现消费类交易占比、笔均金额
#%%交易超过三个月的卡片占比
#%%卡片交易地区与持卡人地区是否一致比例

# %%docx模板输出
document_dir = r'C:/工作/典型事件/tools_dev/数据分析报告.docx'
context = {}
# for row, col in itertools.product(machnt_risk.index, machnt_risk.columns):
#     context[f'{row}_{col}'] = df.loc[row, col]
card_iss_nm_distr['ratio'] = pd.Series(["{0:.2f}%".format(
    val * 100) for val in card_iss_nm_distr['ratio']], index=card_iss_nm_distr.index)
card_iss_nm_distr = round(card_iss_nm_distr, 2)
#context = machnt_risk.set_index('mchnt_cd').T.to_dict('list')
context_card_iss_nm_distr = card_iss_nm_distr.to_dict(orient='records')
table = {
    'tbl_card_iss_nm_distr': context_card_iss_nm_distr
}
df_trans_type_tbl_cons = (
    (df_trans_type_tbl['消费类']).reset_index()).drop('level_1', axis=1)
df_trans_type_tbl_cons['bill_sum_rate'] = pd.Series(["{0:.2f}%".format(
    val * 100) for val in df_trans_type_tbl_cons['bill_sum_rate']], index=df_trans_type_tbl_cons.index)

df_trans_type_tbl_cons = round(df_trans_type_tbl_cons, 2)
df_trans_type_tbl_cons = df_trans_type_tbl_cons.sort_values(
    by='bill_sum', ascending=False)
table2 = {
    'tbl_trans_type_tbl': (df_trans_type_tbl_cons[:10]).to_dict(orient='records')
}
'''
table = {
    'user_labels': ['fruit', 'vegetable', 'stone', 'thing'],
    'tbl_contents': [
        {'label': 'yellow', 'cols': ['banana', 'capsicum', 'pyrite', 'taxi']},
        {'label': 'red', 'cols': ['apple', 'tomato', 'cinnabar', 'doubledecker']},
        {'label': 'green', 'cols': ['guava', 'cucumber', 'aventurine', 'card']},
    ],
}
'''
pic_dir = r'C:/工作/典型事件/tools_dev/picture/'
tpl = DocxTemplate(r'C:/工作/典型事件/tools_dev/数据分析报告_tpl.docx')
rt_date = RichText()
rt_date.add(time_str+'\n', font='方正小标宋简体', size=44)
rt_pargh1 = RichText()
rt_pargh1.add('本批数据限定时间段为从'+str(left_time)+'到'+str(right_time) +
              '数据一共有'+str(count_trans)+'笔交易，一共涉及卡片' +
              str(card_total)+'张，其中成功交易笔数'+str(count_trans_success) +
              '笔，成功交易金额'+format(sum_trans/10000000000, '.2f')+'亿元，笔均金额为' +
              format(bill_avg_trans/100, '.2f')+'元，卡均金额为' +
              format(card_avg_trans/100, '.2f')+'元。',
              font='仿宋_GB2312', size=32)

rt_pargh2 = RichText()

if (ratio_list[-1]>0.95 and right_time_probe-left_time_probe<90):
    rt_pargh2.add('本批数据可能的风险事件类型为信息泄露', font='仿宋_GB2312', size=32)
elif():
    rt_pargh2.add('本批数据可能的风险事件类型为合谋盗刷', font='仿宋_GB2312', size=32)
elif():
    rt_pargh2.add('本批数据可能的风险事件类型为套现代还', font='仿宋_GB2312', size=32)
elif((withdraw_location_distr.index)[0]=='澳门'):
    rt_pargh2.add('本批数据可能的风险事件类型为跨境移机', font='仿宋_GB2312', size=32)
elif():
    rt_pargh2.add('本批数据可能的风险事件类型为资金转移', font='仿宋_GB2312', size=32)
elif(loan_num/count_trans > 0.2):
    rt_pargh2.add('本批数据可能的风险事件类型为涉赌', font='仿宋_GB2312', size=32)
else:
    rt_pargh2.add('本批数据可能的风险事件类型暂时无法确定，烦请进一步深入分析', font='仿宋_GB2312', size=32)


context = {
    'rt_pargh1': rt_pargh1,
    'date': rt_date,
    'rt_pargh2': rt_pargh2
}

width_pic = 130
image = {
    '发卡行分布': InlineImage(tpl, pic_dir+'发卡行分布.png', width=Mm(width_pic)),
    '借贷记分布': InlineImage(tpl, pic_dir+'借贷记分布.png', width=Mm(width_pic/1.5)),
    '卡组织分布': InlineImage(tpl, pic_dir+'卡组织分布.png', width=Mm(width_pic/1.5)),
    '卡介质分布': InlineImage(tpl, pic_dir+'卡介质分布.png', width=Mm(width_pic)),
    '卡片所在地分布近似': InlineImage(tpl, pic_dir+'卡片所在地分布近似.png', width=Mm(width_pic)),
    '交易月分布': InlineImage(tpl, pic_dir+'交易月分布.png', width=Mm(width_pic)),
    '交易时间段分布': InlineImage(tpl, pic_dir+'交易时间段分布.png', width=Mm(width_pic)),
    '交易类型大类分布': InlineImage(tpl, pic_dir+'交易类型大类分布.png', width=Mm(width_pic)),
    '交易渠道分布': InlineImage(tpl, pic_dir+'交易渠道分布.png', width=Mm(width_pic)),
    '消费金额区间段分布': InlineImage(tpl, pic_dir+'消费金额区间段分布.png', width=Mm(width_pic)),
    '服务点输入方式分布': InlineImage(tpl, pic_dir+'服务点输入方式分布.png', width=Mm(width_pic)),
    '应答码分布': InlineImage(tpl, pic_dir+'应答码分布.png', width=Mm(width_pic)),
    '商户分布': InlineImage(tpl, pic_dir+'商户分布.png', width=Mm(width_pic)),
    '商户卡片数分布': InlineImage(tpl, pic_dir+'商户卡片数分布.png', width=Mm(width_pic)),
    '商户类型大类分布': InlineImage(tpl, pic_dir+'商户类型大类分布.png', width=Mm(width_pic)),
    '收单机构分布分析': InlineImage(tpl, pic_dir+'收单机构分布分析.png', width=Mm(width_pic)),
    '消费类交易的收单机构分布': InlineImage(tpl, pic_dir+'消费类交易的收单机构分布.png', width=Mm(width_pic)),
    '查询类交易的收单机构分布': InlineImage(tpl, pic_dir+'查询类交易的收单机构分布.png', width=Mm(width_pic)),
    '取款类交易的收单机构分布': InlineImage(tpl, pic_dir+'取款类交易的收单机构分布.png', width=Mm(width_pic)),
    '贷记类交易的收单机构分布': InlineImage(tpl, pic_dir+'贷记类交易的收单机构分布.png', width=Mm(width_pic)),
    '账户服务类交易的收单机构分布': InlineImage(tpl, pic_dir+'账户服务类交易的收单机构分布.png', width=Mm(width_pic)),
    '交易月分布1': InlineImage(tpl, pic_dir+'交易月分布1.png', width=Mm(width_pic)),
    '交易月分布2': InlineImage(tpl, pic_dir+'交易月分布2.png', width=Mm(width_pic)),
    '交易月分布3': InlineImage(tpl, pic_dir+'交易月分布3.png', width=Mm(width_pic)),
    '交易月分布4': InlineImage(tpl, pic_dir+'交易月分布4.png', width=Mm(width_pic)),
    '交易月分布5': InlineImage(tpl, pic_dir+'交易月分布5.png', width=Mm(width_pic)),
    '交易月分布6': InlineImage(tpl, pic_dir+'交易月分布6.png', width=Mm(width_pic)),
    '交易月分布7': InlineImage(tpl, pic_dir+'交易月分布7.png', width=Mm(width_pic)),
    '交易月分布8': InlineImage(tpl, pic_dir+'交易月分布8.png', width=Mm(width_pic)),
    '交易月分布9': InlineImage(tpl, pic_dir+'交易月分布9.png', width=Mm(width_pic)),
    '交易月分布10': InlineImage(tpl, pic_dir+'交易月分布10.png', width=Mm(width_pic))
}
table.update(table2)
table.update(context)
table.update(image)
jinja_env = jinja2.Environment(autoescape=True)
tpl.render(table, jinja_env)
tpl.save(document_dir)
# %%todo
