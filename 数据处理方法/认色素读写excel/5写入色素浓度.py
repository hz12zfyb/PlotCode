 # -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 22:17:57 2019
遇到以下问题，打开下text.xlsx即可
    pigment[i,j] = ws.cell(j+5,6+5*i).value

ValueError: could not convert string to float: 
@author: Administrator
"""

#import openpyxl 
import numpy as np
import xlrd
import pandas as pd
#读
def get_stationname(station_num):
    stationnames,depths,voyages = [],[],[]
    for i in range(station_num):
        voyage = ws.cell(0,5+5*i).value.split('th')[0]
        voyages.append(voyage) 
        cell_value = ws.cell(2,6+5*i).value
        depth = cell_value.split('-')[-1].replace('m','')
        n = len(depth) +2
        stationnames.append(cell_value[:-n])
        depths.append(depth)
    return stationnames,depths,voyages

def get_pigmentname(pigment_num):
    pigmentnames = []
    for i in range(pigment_num):
        pigmentname = ws.cell(5+i,0).value        
        pigmentnames.append(pigmentname.split(',')[2])
    return pigmentnames

excel_dir = 'D:/Refresh/data/南极色素-20201028-冯毓彬/text.xlsx'
wb = xlrd.open_workbook(excel_dir)
ws = wb.sheet_by_name('station')
station_num = int((ws.ncols - 3)/5) #179
pigment_num = 27
stationnames,depths,voyages = get_stationname(station_num)
pigmentnames = get_pigmentname(pigment_num)
pigment = np.zeros(shape=(station_num,pigment_num))
for i in range(station_num):
    for j in range(pigment_num):
        if ws.cell(j+5,5+5*i).value != '':
            pigment[i,j] = ws.cell(j+5,6+5*i).value
        else:
            pigment[i,j] = 0
#phide-a 与660nm 相比较 选择浓度较小的值
#for i in range(station_num):
#    value_660 = ws.cell(34,6+5*i).value
#    value_440 = pigment[i,10]
#    if value_440 == 0:
#        pigment[i,10] = value_660
#    elif value_440 != 0 and value_660 != '':
#        pigment[i,10] = min(value_660,value_440)
    
            
df =pd.DataFrame(pigment)  
df.columns = pigmentnames
df.insert(0,'voyage',voyages)
df.insert(1,'station',stationnames)
df.insert(2,'depth',depths)

df.to_excel(excel_dir.replace('text','色素数据'),sheet_name = '色素浓度ngL',index=None)




   








