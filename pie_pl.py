# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 10:29:13 2020

@author: panglei
"""

#test_again
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm,colors
import seaborn as sns

df=pd.DataFrame(dict(labels =['LVS','SJM','MCE','Galaxy','MGM','Wynn'],
                     sizes = [24.20,75.90,12.50,12.30,8.10,12.10]))
df=df.sort_values(by='sizes',ascending=False)
df=df.reset_index()

index=np.append(0,np.arange(df.shape[0]-1,0,-1))
df=df.iloc[index,:]
df=df.reset_index()

cmap=cm.get_cmap('Reds_r',6)
color=[colors.rgb2hex(cmap(i)[:3]) for i in index ] 

plt.figure(dpi=500)#设置分辨率
sns.set_palette("RdBu")

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"),dpi=500)

#fig1, ax1 = plt.subplots()
wedges, texts = ax.pie(df['sizes'].values,#labels=df['labels'],
                       startangle=90, shadow=False, counterclock=False,
                       wedgeprops =dict(linewidth=0.5)) 
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    #print(i)
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(df['labels'][i], xy=(x, y), xytext=(1.2*x, 1.2*y), #xytext=(1.35*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, 
                 arrowprops=dict(arrowstyle='-'))

plt.show()

#读取table
test = pd.read_table('C:/工作/典型事件/手机POS交易数据疑似套现/拉卡拉商户交易明细/商户交易每日/@数据厨房原始文件/0903.txt',delimiter=',',dtype=object)
#去掉df所有的\t



