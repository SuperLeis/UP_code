# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:02:00 2020

@author: panglei
"""
#import win32com.client
import os
import pandas as pd
import time

if __name__ == "__main__":
    start = time.time()
    path = r'C:/工作/@合并文件文件夹/Demo10/Demo1000/'
    os.chdir(path) #若想改变工作路径可以用chdir函数
    filelist = []
    dataframe_0 = pd.DataFrame()
    file_list = os.listdir(path)
    for file in os.listdir(path):
        os.rename(os.path.join(path,file),os.path.join(path,file)+".txt")
    for i in range(1,1001):   
        dataframe = pd.read_table(path+str(i)+'.txt',header=None)
        dataframe.columns  = [i]
        dataframe_0 = pd.concat([dataframe_0,dataframe], axis=1)
        end = time.time()
        print('已运行%f秒'%(end-start))
        print(str(i)+'.txt'+'读取完成')    
            
    writer = pd.ExcelWriter(path+'合并文件Demo1000_2.xlsx' )
    dataframe_0.to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
    writer.save()    
    
'''  
    for i in range(len(filelist)):
        #df = pd.read_excel(filelist[i], sheet_name=0)
        #filename, password = path+filelist[i],'cups'
        dataframe = pd.read_table(filelist[i],)
        #dataframe.drop([len(dataframe)-1],inplace=True)
        dataframe_0 = pd.concat([dataframe_0,dataframe], axis=0)
        end = time.time()
        print('已运行%f秒'%(end-start))
        print(filelist[i]+'读取完成')  
    for root,dirs,files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.xlsx':
                filelist.append(file) 
'''