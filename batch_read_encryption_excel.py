# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 12:00:11 2020

@author: panglei
"""

import win32com.client
import os
import pandas as pd
import time

def get_datafram(filename,password,sheet_num,row_begin):
    """
    ###运行前kill excel进程！！！
    参数一：文件路径
    参数二：文件密码
    参数三：sheet序号
    参数四：读取起始行
    return: 解密后输出的df
    """
    xlApp = win32com.client.Dispatch("Excel.Application")
    xlApp.Visible = False
    xlwb = xlApp.Workbooks.Open(filename, False, True, None, Password=password)
    #xlwb = xlApp.Workbooks.Open(filename, UpdateLinks=0, ReadOnly=False, Format=None, Password=password)
    #获取工作表具体情况
    # 获取行数
    rows=xlwb.Worksheets(sheet_num).UsedRange.Rows.Count
    # 获取列数
    col=xlwb.Worksheets(sheet_num).UsedRange.Columns.Count
    #数据遍历重新写出
    df_list=[]
    for i in range(rows):
        #每一行的值加入一个list
        df_row_list=[]
        for j in range(col):   
          #获取每个单元格的值
            a=xlwb.Worksheets(sheet_num).Cells(i+row_begin,j+1).Value
            df_row_list.append(a)
        df_list.append(df_row_list)
    #转换写出
    df=pd.DataFrame(df_list)
    #xlwb.Close()
    return df 

if __name__ == "__main__":
    start = time.time()
    path = r'C:/工作/@合并文件文件夹/'
    os.chdir(path) #若想改变工作路径可以用chdir函数
    filelist = []
    for root,dirs,files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.xlsx':
                filelist.append(file)   
    dataframe_0 = pd.DataFrame()
            
    for i in range(len(filelist)):
        #df = pd.read_excel(filelist[i], sheet_name=0)
        filename, password = path+filelist[i],'cups'
        dataframe = get_datafram(filename,password,1,2)
        dataframe_0 = pd.concat([dataframe_0,dataframe], axis=0)
        end = time.time()
        print('已运行%f秒'%(end-start))
        print(filelist[i]+'读取完成')

    
    filename, password = path+filelist[0],'cups'
    dataframe_col = get_datafram(filename,password,1,1)
    dataframe_0.columns = dataframe_col.iloc[0].tolist()#+['a','b','c','d','e','f']
    writer = pd.ExcelWriter(path+'合并.xlsx' )
    dataframe_0.to_excel(writer, index=False,encoding='utf-8',sheet_name='Sheet1')
    writer.save()    
##############################################################################    
# # -*- coding: utf-8 -*-
# import win32com.client as win32
# import re
# import pandas as pd
# import time

# def get_card(i, xlwb):
#     card = xlwb.Worksheets(1).Cells(i, 6).Value
#     card = re.split('[ ,，、\n:：；;/（）()]', card)
# #    card_list = list(filter(None, card))
#     card_list = [i for i in card if len(i)>=16 and len(i)<=19]
    
#     return card_list

# def get_deception(i, xlwb):
#     _ = [13, 17, 18, 19] # 6:*交易卡号, 12:诈骗手法, 13:欺诈来电号码, 17:备注, 18:专员跟踪处理, 19:风险岗跟踪处理
#     deception = xlwb.Worksheets(1).Cells(i, 12).Value # deception = ''
#     deception += '：'
#     for j in _:
#         value = xlwb.Worksheets(1).Cells(i,j).Value
#         if len(value) == 0:
#             continue
#         else:
#             deception += value
#             deception += '。'
#     deception = deception.replace('\n', '。')
    
#     return deception

# if __name__ == "__main__":
#     start = time.time()
#     xlApp = win32.Dispatch("Excel.Application")
#     xlApp.Visible = False # 设置是否打开Excel
# #    xlApp.DisplayAlerts=True # 设置是否显示警告和消息框
#     filename, password = r"C:\Users\15999\Desktop\银联创新业务疑似欺诈交易报备表6.22.xlsx", '95516'
#     xlwb = xlApp.Workbooks.Open(filename, UpdateLinks=0, ReadOnly=False, Format=None, Password=password)
#     #xlwb = xlApp.Workbooks.Open(filename, False, True, None, Password=password)
#     rows=xlwb.Worksheets(1).UsedRange.Rows.Count # 获取行数
#     columns_index = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 15, 16]
#     #col=xlwb.Worksheets(1).UsedRange.Columns.Count # 获取列数
#     df_list = []
#     for i in range(3, rows+1):
#         card_list = get_card(i, xlwb)
#         if len(card_list) != 0:
#             row_list = []
#             for j in columns_index:
#                 row_list.append(xlwb.Worksheets(1).Cells(i, j).Value)
#             deception = get_deception(i, xlwb)
#             for j in card_list:
#                 card_deception = []
#                 card_deception.append(j)
#                 card_deception.append(deception)
#                 df_list.append(card_deception+row_list)
#         else:
#             continue
#     columns_list = []
#     columns_index = [6, 12] + columns_index
#     for i in columns_index:
#         columns_list.append(xlwb.Worksheets(1).Cells(2, i).Value)
#     df = pd.DataFrame(df_list)
#     df.columns = columns_list
#     writer = pd.ExcelWriter('创新业务疑似欺诈交易new.xlsx') #, encoding='gbk'
#     df.to_excel(writer, header=True, index=False)
#     writer.save()
#     end = time.time()
#     print('共运行%f秒'%(end-start))
##############################################################################
# xlwb = xlApp.Workbooks.Open(filename, UpdateLinks=0, ReadOnly=False, Format=None, Password=password)
# rows=xlwb.Worksheets(1).UsedRange.Rows.Count # 获取行数
# col=xlwb.Worksheets(1).UsedRange.Columns.Count # 获取列数
# xlws = xlwb.Worksheets(1)
# # Get the content in the rectangular selection region
# # content is a tuple of tuples
# content = xlws.Range(xlws.Cells(0, 0), xlws.Cells(rows, col)).Value 
# # Transfer content to pandas dataframe
# dataframe = pd.DataFrame(list(content))

# #xlwb.SaveAs(os.path.join(os.getcwd(), file.split('.xlsx')[0] + '.xls'), FileFormat=1) 
# xlwb.SaveAs(os.path.join(os.getcwd(),'ce.xlsx'), FileFormat=1) 
# xlwb.Close()

# rows=xlwb.Worksheets(1).UsedRange.Rows.Count # 获取行数
# col=xlwb.Worksheets(1).UsedRange.Columns.Count # 获取列数

# row_list = []
# for i in range(1, rows+1):
#         for j in range(col):
#             row_list.append(xlwb.Worksheets(1).Cells(i, j).Value)


# xlwb = xlApp.Workbooks.Open(filename, Password=password)
# # xlwb = xlApp.Workbooks.Open(filename)
# xlws = xlwb.Sheets(1) # counts from 1, not from 0
# #print xlws.Name
# #print xlws.Cells(1, 1) # that's A1
# from win32com.client import Dispatch
# xlApp = Dispatch("Excel.Application")
# xlApp.Visible = False # True代表Excel在前台打开，False是在后台打开
# xlwb = xlApp.Workbooks.Open(Filename=filename,UpdateLinks=2,ReadOnly=True,Format = None,Password=password)
# sheet_data = xlwb.Sheets(1)
# print(sheet_data)
# # Create an accessible temporary file, and then delete it. We only need a valid path.
# f = NamedTemporaryFile(delete=False, suffix='.csv')  
# f.close()
# os.unlink(f.name)  # Not deleting will result in a "File already exists" warning

# xlCSVWindows = 0x17  # CSV file format, from enum XlFileFormat
# xlwb.SaveAs(Filename=f.name, FileFormat=xlCSVWindows)  # Save the workbook as CSV
# df_1 = pd.read_csv(f.name)  # Read that CSV from Pandas
# #print df