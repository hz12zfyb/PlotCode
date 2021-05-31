# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 11:59:03 2019

@author: Administrator
"""

import pdfplumber
import pandas as pd
import os
import numpy as np
file_name = 'D:/Refresh/data/南极色素-20201028-冯毓彬/440结果.pdf'

#def read_tableinpdf(file_name):
with pdfplumber.open(file_name) as pdf:
    page_number = 0
    for i in range(4):  ##   
        page = pdf.pages[page_number]
        page_number += 1          
        a1 = page.extract_tables()
        if i ==0 :
            df2 = pd.DataFrame(data=a1[0][1:],columns=a1[0][0]).set_index('')
        else:
            df2 = df2.append(pd.DataFrame(data=a1[0][1:],columns=a1[0][0]).set_index(''))
        
df2.to_excel('result.xlsx')

#dfs = df.append([df1,df2])
#dfs.to_excel('id名称.xlsx',index=None)
#k = list(dfs['结果\nID'])
#v = list(dfs['样品名称'])
#dict_s = { i:v[k.index(i)] for i in k }
#path = 'D:/Refresh/a/'



path = os.getcwd()
filename_list = os.listdir(path)
a = 0
for i in range(len(filename_list)):
    if filename_list[i][:2] == '结果':            
        used_name = path + '/' + filename_list[i]
#        #样品
        new_mingcheng = list(df2[df2['结果\nID'] == filename_list[i][3:-4]]['样品名称'])
        new_name = path + '/' + new_mingcheng[0] + '-440.pdf'
        
        #混标
#        new_mingcheng = list(df2[df2['结果\nID'] == filename_list[i][3:-4]]['样品名称'])
#        new_date = list(df2[df2['结果\nID'] == filename_list[i][3:-4]]['采集日期'])[0]
#        new_name = path + '/' + new_date.replace(':','-').replace('/','-') +'-' + new_mingcheng[0] + '.pdf'

        os.rename(used_name,new_name)
        print("文件%s重命名成功,新的文件名为%s" %(used_name,new_name))
        
        a += 1
    else:
        continue
     

#df2['样品名称'][df2['结果\nID'] == filename_list[59][2：]]


    
    
    
    
    
    