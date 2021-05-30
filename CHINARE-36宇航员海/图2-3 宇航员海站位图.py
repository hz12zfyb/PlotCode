# -*- coding: utf-8 -*-
"""
Created on Sat Jun 5 10:42:02 2019

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
df_station = pd.read_excel('D:/Refresh/py36/色素数据处理/station_information_36次.xlsx')\
.set_index('Station') 
#df_station = df_station.drop(['R1-01','R1-03','R1-04','AM-01'])
#image = support_pie.loadtif()
color = ['#d55c00', '#cc7aa7', '#0071b2']
plt.rcParams['figure.figsize'] = (7.7, 3.9)
plt.rcParams['font.sans-serif'] = ['Times New Roman']
fig = plt.figure()
#画锋面
#txt_dir = 'D:/Refresh/py36/色素数据处理/宇航员海20191210.txt'
#df = pd.read_table(txt_dir,header=0,sep='\\t', engine='python')
#plt.plot(df['lon'],df['lat'],'b:')
#txt_dir = 'D:/Refresh/py36/色素数据处理/宇航员海20191223.txt'
#df = pd.read_table(txt_dir,header=0,sep='\\t', engine='python')
#plt.plot(df['lon'],df['lat'],'y:')
txt_dir = 'D:/Refresh/py36/色素数据处理/宇航员海20200106.txt'
df = pd.read_table(txt_dir,header=0,sep='\\t', engine='python')
plt.plot(df['lon'],df['lat'],'b:')

#plt.plot(m['SACCF'][:,0],m['SACCF'][:,1],'b')
#plt.text(50,-61,'SACCF',fontdict ={
#        'color':  'b','size': 8} )
df = pd.DataFrame(data=m['ACCSB'],columns=['lon','lat']).\
set_index('lon')
df['lon_tran'] = support_pie.lon_180_360(df.index)
df = df.sort_values('lon_tran')
plt.plot(df['lon_tran'],df['lat'],'gray')
#plt.text(32,-61,'ACCSB',fontdict ={
#        'color':  'k','size': 8} )

#画水深
lon_left,lon_right,lat_bottom,lat_top = 30,80,-70,-60
plt.xlim((lon_left,lon_right))
plt.ylim((lat_bottom,lat_top))
support_pie.contourf_area(image,lon_left,lon_right,lat_bottom,lat_top,1)
#所有字体matplotlib.font_manager.fontManager.ttflist
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

#画站位
station_index, station_lon, station_lat, station_area =\
df_station.index, df_station.iloc[:,1], df_station.iloc[:,2], df_station.iloc[:,4]
station_num = len(station_index)
fontsize = np.ones_like(station_lon)*8
for i in range(station_num):
    plt.scatter(station_lon[i],station_lat[i],
    s=5,c='black')#color[station_area[i]-1])
    plt.text(station_lon[i]+0.3,station_lat[i]-0.15,station_index[i],
    fontdict = {'size': fontsize[i], 'color': 'black'})
#加地名  
font1 = {'family': 'Times New Roman',
        'color':  'red',
        'weight': 'black',
        'size': 8,
        }  #大型地名
font2 = {'family': 'Times New Roman',
        'color':  'blue',
        'weight': 'heavy',
        'size': 8,
        }  #岛屿地名 
font3 = {'family': 'Times New Roman',
        'color':  'black',
        'weight': 'black',
        'size': 8,
        }  #中型地名 
font4 = {'family': 'Times New Roman',
        'color':  'black',
        'weight': 'normal',
        'size': 8,
        }  #小型地名 
#South Shetland Islands  
#plt.text(-60.8406,-62.0774,'South Shetland I.',font2,rotation= 30)


fig_name = 'D:/Refresh/data/CHINARE-36/pic/研究区域地形图/研究区域.png' 
fig.savefig(fig_name,bbox_inches='tight',dpi=1000,pad_inches=0.01)
plt.show()
