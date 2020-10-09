# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 10:18:21 2020

@author: panglei
"""

import pandas as pd
import os
import time


def excel_merge_func(file_type='.xlsx', path=r'C:/工作/@合并文件文件夹/'):
    start = time.time()
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == file_type:
                filelist.append(file)
    df_all = pd.DataFrame()
    for i in range(len(filelist)):
        if file_type == '.xlsx':
            df = pd.read_excel(
                filelist[i], sheet_name='Sheet1', dtype=object, header=0)
        else:
            df = pd.read_csv(filelist[i], dtype=object, squeeze=True, header=0,
                             # encoding='unicode_escape',
                             encoding='gbk'
                             # delimiter='\t'
                             )
            #df = pd.read_csv(filelist[i],dtype=object,squeeze=True,header=0,delimiter='\t')
        df_all = pd.concat([df_all, df], axis=0)
        end = time.time()
        print('已运行%f秒' % (end-start))
        print('文件'+filelist[i]+'读取完毕')
    return df_all


if __name__ == "__main__":
    path_file = r'C:/工作/@合并文件文件夹/'
    os.chdir(path_file)  # 若想改变工作路径可以用chdir函数
    df_all = excel_merge_func(file_type='.csv', path=path_file)
    print(df_all.columns)
    writer = pd.ExcelWriter(path_file+'合并文件.xlsx')
    df_all.to_excel(writer, index=False, encoding='utf-8')
    writer.save()
