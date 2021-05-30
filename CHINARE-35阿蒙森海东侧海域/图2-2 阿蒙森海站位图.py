# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 10:42:02 2019

@author: Administrator
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import loadmat
import sys
sys.path.append('D:/Refresh/py36')
import support_pie


m = loadmat('D:/Refresh/data/Fronts.mat')
df_station = pd.read_excel('D:/Refresh/py36/色素数据处理/station_information.xlsx',
                           sheet_name='AS').set_index('Station') 
#df_station = df_station.drop(['D1-7','D1-6','D1-4'])
image = support_pie.loadtif()
color = ['#d55c00', '#cc7aa7', '#0071b2']
plt.rcParams['figure.figsize'] = (7.7,3.9)
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 中文字体设置
#plt.rcParams['axes.unicode_minus'] = False
fontcn = {'family': 'SimHei','weight' : 'normal','size': 12}
fig = plt.figure()
#画锋面
#plt.plot(m['SACCF'][:,0],m['SACCF'][:,1],'k')
#plt.text(-135,-61,'SACCF',fontdict ={
#        'color':  'k','size': 12})
#df = pd.DataFrame(data=m['ACCSB'],columns=['lon','lat']).\
#set_index('lon')
#df['lon_tran'] = support_pie.lon_180_360(df.index)
#df = df.sort_values('lon_tran')
#plt.plot(df['lon_tran'],df['lat'],'b')
#plt.text(-135,-66,'ACCSB',fontdict ={
#        'color':  'b','size': 12} )

#画水深
lon_left,lon_right,lat_bottom,lat_top = -123,-85,-75,-65
plt.xlim((lon_left,lon_right))
plt.ylim((lat_bottom,lat_top))
support_pie.contourf_area(image,lon_left,lon_right,lat_bottom,lat_top,1)


#画站位
station_index, station_lon, station_lat, station_area =\
df_station.index, df_station.loc[:,'Longitude [degrees_east]'], \
df_station.loc[:,'Latitude [degrees_north]'], df_station.loc[:,'Curise']
station_num = len(station_index)
fontsize = np.ones_like(station_lon)*10
curise2color = {'CHINARE-34':'green','CHINARE-35':'red','CHINARE-36':'blue'}
for i in range(station_num):
    plt.scatter(station_lon[i],station_lat[i],
    s=7,c=curise2color[station_area[i]])
    plt.text(station_lon[i]+0.3,station_lat[i]-0.15,station_index[i],
    fontdict = {'size': fontsize[i], 'color':curise2color[station_area[i]] })
#加地名  
font1 = {'color':  'red',
        'weight': 'black',
        'size': 8,
        }  #大型地名
font2 = {'color':  'black',
        'weight': 'heavy',
        'size': 12,
        }  #岛屿地名 
font3 = {'color':  'black',
        'weight': 'black',
        'size': 8,
        }  #中型地名 
font4 = {'color':  'black',
        'weight': 'normal',
        'size': 8,
        }  #小型地名 
#South Shetland Islands  
plt.text(-91.5,-68.4,'彼得一世岛',fontcn)
plt.text(-99,-73,'瑟斯顿岛',fontcn)
plt.text(-105,-74.5,'派恩岛冰架',fontcn)



fig_name = 'D:/Refresh/data/CHINARE-35/pic/阿蒙森海汇总.png' 
fig.savefig(fig_name,bbox_inches='tight',dpi=1000,pad_inches=0.01)
plt.show()