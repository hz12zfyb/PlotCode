# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 21:18:09 2019
根据data_all.xlsx 计算水柱积分藻种数据 200米
@author: Administrator
"""
import pandas as pd
import numpy as np

def qiucha(a):
    b = np.zeros(len(a)+1)
    for i in range(len(a)-1):
        b[i+1] = a[i+1] - a[i]
    return b

file_name = 'D:/Refresh/data/CHINARE-34/data_all.xlsx'
#file_name = 'D:/Refresh/data/CHINARE-35/CHEMTAX结果/4.23-wright2010.xlsx'

df = pd.read_excel(file_name,sheet_name='Sheet1(积分用)').set_index('Station')   


stationames = list(set(df.index))
pigmentnames = df.columns[:]  
cint = np.zeros(shape=(df.shape[1],len(stationames)))
cint = np.ma.array(cint, mask=cint > -1)

for i in range(len(stationames)):
    df_cal = df.loc[stationames[i]]
    df_cal = df_cal[df_cal['Depth [m]']<=200]

    for j in range(len(cint)): 
        data_pre = np.array(df_cal[pigmentnames[j]],dtype=float)
        index = np.isnan(data_pre) == False
        if np.sum(index) >0:
            data = data_pre[index]
            depth = np.array(df_cal['Depth [m]'])[index] 
            depth_jianju = qiucha(depth)
            inter_value = 0
            for m in range(len(depth_jianju)-1):
                inter_value += (depth_jianju[m]+depth_jianju[m+1]) * data[m]
            
            cint[j,i] = inter_value/2/(depth[-1] - depth[0])
        else:
            continue

df_cint = pd.DataFrame(cint.T,index=stationames,columns=pigmentnames).sort_index()
for i in ['Chloro', 'Crypto', 'Diat1', 'Diat2', 'Dino1',
       'Hapt6HiFe', 'Hapt6LoFe']:
    df_cint[i+'_p'] = df_cint[i] / df_cint['Chlorophyll A']*100

df_station = pd.read_excel('D:/Refresh/py36/色素数据处理/station_information_34次.xlsx',
                           sheet_name='Sheet1').set_index('Station')    
df_output = pd.concat([df_station,df_cint],axis=1,sort=True)#.dropna()  #删除含有空值的行                
df_output['Depth [m]'] = 0
df_output.to_excel('D:/Refresh/data/CHINARE-34/水柱积分藻种数据1.xlsx')  