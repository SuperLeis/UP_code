#coding=utf-8

import os
from win32com.client import Dispatch,constants
from docx2pdf import convert
def WordToPdf(wordPath, pdfPath):
    '''
    wordPath参数对应的是word的完整路径
    pdfPath参数对应的是pdf的完整路径
    '''
    # 调用word程序
    word =Dispatch('Word.Application')
    # 打开word文件
    doc = word.Documents.Open(wordPath)
    doc.ExportAsFixedFormat(
    #对应pdf完整的路径
    pdfPath,
    # 指定是以 PDF 还是 XPS 格式保存文档
    constants.wdExportFormatPDF,
    # 选用，非必须，指定导出过程是仅包括文本，还是同时包括文本和标记
    Item=constants.wdExportDocumentWithMarkup, 
    # 选用，非必须，指定是否导出书签以及要导出的书签类型。
    CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
    word.Quit(constants.wdDoNotSaveChanges)
#wordPath = r"C:\Users\admin\Desktop\测试\测试1.doc"
#pdfPath = r"C:\Users\admin\Desktop\测试\测试1.pdf"
word_folder = r"C:\工作\每周发收单\20200916\高风险商户预警提示函"

for item in os.listdir(word_folder):
    if item[:2]!='~$':
        wordPath = word_folder +os.sep + item
        pdfPath = word_folder + os.sep +item.replace('.docx','.pdf')
        convert(wordPath,pdfPath)
