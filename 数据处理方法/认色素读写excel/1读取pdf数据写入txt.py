# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 09:28:02 2019
#读取pdf中的excel表格
@author: Administrator
"""
import pdfplumber
import numpy as np
import pandas as pd
import os,sys
sys.path.append('D:/Refresh/py36')
import support_pie


def read_tableinpdf(file_name):
    with pdfplumber.open(file_name) as pdf:
        page_number = 1
        for i in range(5):  ##   
            page = pdf.pages[page_number]                    
            a1 = page.extract_tables()
            if len(a1) <=2:
                for j in range(len(a1)):
                    if i==0 and j==0:    
                        df = pd.DataFrame(data=a1[j][1:],columns=a1[0][0])
                        df = df.replace('',np.nan).dropna(axis=1)
                    else:
                        df2 =pd.DataFrame(data=a1[j][1:],columns=a1[0][0])
                        df2 =df2.replace('',np.nan).dropna(axis=1)
                        df = df.append(df2)
            else:
                break
                
            page_number += 1  
    df = df.set_index(df.columns[0])
    return df[df.columns[[0,1]]]

pico = 0
error_filenames = []
file_dir = 'D:/Refresh/data/南极色素-20201028-冯毓彬/440/'
filenames = support_pie.file_name(file_dir,'.pdf')
for filename in filenames:
    try:
        data = read_tableinpdf(filename)
        txt_name = filename.replace('.pdf','.txt').replace(file_dir,
                                   'D:/Refresh/data/南极色素-20201028-冯毓彬/pdfplumber_txt_440/')       
        data.to_csv(txt_name,sep=',',header=None)
    except:        
        pico += 1
        print(filename)
        error_filenames.append(filename)
        break
print('读取失败率为%.2f'%(pico/190*100))
   


