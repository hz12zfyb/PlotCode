# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 17:10:06 2019
Rivaro et al. (2014)
@author: Administrator
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('D:/Refresh/py36')
import support_pie
import numpy as np


df = pd.read_excel('D:/Refresh/data/CHINARE-362/data_all.xlsx').set_index('Station')
df_station =pd.read_excel('D:/Refresh/py36/色素数据处理/station_information_362次.xlsx').set_index('Station')
#df_station = df_station.drop([ 'R1-01', 'R1-03', 'R1-04'])
# print(df_station.index)
df_station['%MW'] = 0.00
for i in df_station.index:
    df_cal = df.loc[i]
    min_depth = np.min(df_cal['Depth [m]'])
    S_surface = df_cal[df_cal['Depth [m]'] == min_depth]['Salinity [psu]']
    try:
        S_bottom  = df_cal[df_cal['Depth [m]'] ==200].loc[i]['Salinity [psu]']
    except:
#        max_depth = np.max(df_cal['Depth [m]'])
#        S_bottom  = df_cal[df_cal['Depth [m]'] ==max_depth]['Salinity [psu]']
        print(i)
    df_station['%MW'][i] = (1-(S_surface-6)/(S_bottom-6))*100
#plt.scatter(df_station['Longitude [degrees_east]'],
#            df_station['Latitude [degrees_north]'],
#            s = df_station['mealtwater_per']*100)

image = support_pie.loadtif()    
lon_left,lon_right,lat_bottom,lat_top = -108,-88,-75,-65
#lon_left,lon_right,lat_bottom,lat_top = -62,-42,-64,-59
lon,lat,value = support_pie.inter_data(df_station['Longitude [degrees_east]'],df_station['Latitude [degrees_north]'],
             df_station['%MW'],1000)
#plt.contourf(lon,lat,value,n=100,cmap='rainbow')
#plt.colorbar()
#support_pie.contourf_re(image,lon_left,lon_right,lat_bottom,lat_top)

fig_name = 'D:/Refresh/data/CHINARE-36/pic/研究区域%MW分布.png' 
#plt.savefig(fig_name,bbox_inches='tight',dpi=1000,pad_inches=0.03)
plt.show()
