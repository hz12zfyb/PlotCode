# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 16:03:34 2019

@author: Administrator
"""
import pandas as pd
import os
import glob
from pyhdf.SD import SD,SDC
import numpy as np
import heapq
import sys
sys.path.append('D:/Refresh/py36')
import support_pie
    
def loadhdf(file_name):
    hdf_obj = SD(file_name)
    value = hdf_obj.select('ASI Ice Concentration')[:]
    return value

    
    
hdf_name = glob.glob('D:/Refresh/data/SEAICE/LongitudeLatitudeGrid-s3125-Antarctic3125.hdf')
hdf_obj  = SD(hdf_name[0],SDC.READ)

lon = hdf_obj.select('Longitudes')[:].reshape(-1)
lon = support_pie.lon_180_360(lon)
lat = hdf_obj.select('Latitudes')[:].reshape(-1)

df = pd.read_excel('D:/Refresh/py36/色素数据处理/station_information_362次.xlsx',\
                   sheet_name='Sheet1').set_index('Station')
file_names = support_pie.file_name('D:/Refresh/data/SEAICE/anti_AMSR_2019-2020_s3125','.hdf')

date_all = []
for i in range(len(file_names)):
    date_all.append(file_names[i].split('-')[-2])
    

indexs = df.index
data_station = np.zeros(shape=(len(indexs),len(file_names))) - 1
for i in range(len(indexs)):
    print(i)
    for j in range(len(file_names)):
        #ii 取自海冰密集度
        ii = list(np.load('36次阿蒙森海经纬度序号.npy'))
#        ii = list(np.load('35次阿蒙森海经纬度序号.npy'))
#        ii = list(np.load('宇航员海经纬度序号.npy'))
        value = loadhdf(file_names[j]).reshape(-1)[ii]
        station_lon = df.loc[indexs[i]]['Longitude [degrees_east]']
        station_lat = df.loc[indexs[i]]['Latitude [degrees_north]']
        station_result = np.power(lon[ii]-station_lon,2)+np.power(lat[ii]-station_lat,2)
        min_index = map(list(station_result).index, heapq.nsmallest(100, station_result))
        data_station[i,j] = np.mean(value[list(min_index)])   


data_station = pd.DataFrame(data_station,index=indexs,columns=date_all)
data_station.to_excel('362次seaice_time.xlsx')

























