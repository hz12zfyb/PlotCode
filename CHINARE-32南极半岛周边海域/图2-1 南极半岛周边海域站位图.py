# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 10:42:02 2019

@author: Administrator
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import loadmat
import os,sys
sys.path.append('D:/Refresh/py36')
import support_pie


def lon_tran(x):
    y = np.zeros_like(x)
    for i in range(len(x)):
        if x[i]>180:
            y[i] = -(360 - x[i])
        else:
            y[i] = x[i]
    return y

m = loadmat('D:/Refresh/data/Fronts.mat')
df_station = pd.read_excel('D:/Refresh/py36/色素数据处理/station_information_32次.xlsx')\
.set_index('Station') #sheet2有43个站位 
image = support_pie.loadtif()
color = ['#d55c00', '#cc7aa7', '#0071b2']
plt.rcParams['figure.figsize'] = (7.7, 3.9)
plt.rcParams['font.sans-serif'] = ['Times New Roman']
fig = plt.figure()
#画锋面
#plt.plot(m['SACCF'][:,0],m['SACCF'][:,1],'k')
#plt.text(-61,-60,'SACCF',fontdict ={
#        'color':  'k','size': 8} )
#plt.plot(lon_tran(m['ACCSB'][:,0]),m['ACCSB'][:,1],'k','-.')
#plt.text(-60,-61.5,'ACCSB',fontdict ={
#        'color':  'k','size': 8} )

#画水深
lon_left,lon_right,lat_bottom,lat_top = -62,-42,-64,-59
plt.xlim((lon_left,lon_right))
plt.ylim((lat_bottom,lat_top))
support_pie.contourf_area(image,lon_left,lon_right,lat_bottom,lat_top,1)
plt.gca().xaxis.set_ticks_position('top') 
#所有字体matplotlib.font_manager.fontManager.ttflist
#plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
#plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

#画站位
station_index, station_lon, station_lat, station_area =\
df_station.index, df_station.iloc[:,1], df_station.iloc[:,2], df_station.iloc[:,4]
station_num = len(station_index)
fontsize = np.ones_like(station_lon)*6
fontsize[[0,-2,-5,9]] = [6,5,6,6]
for i in range(station_num):
    plt.scatter(station_lon[i],station_lat[i],
    s=7,c=color[station_area[i]-1])
    plt.text(station_lon[i]-0.15,station_lat[i]-0.15,station_index[i],
    fontdict = {'size': fontsize[i], 
                'color': 'black'})
h1 = plt.scatter([0],[1],c=['#d55c00'])
h2 = plt.scatter([1],[2],c=['#cc7aa7'])
h3 = plt.scatter([2],[2],c=['#0071b2'])
first_legend = plt.legend(handles=[h1,h2,h3],markerscale=1,
                          labels=['Region Ⅰ','Region Ⅱ',
                                  'Region Ⅲ'],
                          loc = 'upper right',fontsize=8,
                          framealpha=0.1)
#加地名  
font1 = {'family': 'SimHei',
        'color':  'red',
        'weight': 'black',
        'size': 8,
        }  #大型地名
font2 = {'family': 'SimHei',
        'color':  'blue',
        'weight': 'heavy',
        'size': 8,
        }  #岛屿地名 
font3 = {'family': 'SimHei',
        'color':  'black',
        'weight': 'black',
        'size': 8,
        }  #中型地名 
font4 = {'family': 'SimHei',
        'color':  'black',
        'weight': 'normal',
        'size': 8,
        }  #小型地名 
#South Shetland Islands  
plt.text(-60.8406,-62.0774,'南设德兰群岛',font2,rotation= 30)
#Bransfield Strait 
plt.text(-57.8201,-62.4109,'布兰斯菲尔德海峡',font3,rotation = 30)
#Central Basin 中央海盆
plt.text(-59.3201,-62.3109,'中央海盆',font4,rotation = 30)
#East Basin 东海盆
plt.text(-56.3201,-61.6109,'东海盆',font4,rotation = 30)
#Antarctic Peninsula /James Ross Island 
plt.text(-59.4746,-63.5262,'南极半岛',font2,rotation = 30)
#South Orkney Islands 
plt.text(-46.237,-60.6546,'南奥克尼群岛',font2) 
#South Orkney Plateau
plt.text(-46.137,-61.6546,'南奥\n克尼\n海台',font4) 
#Elephant Island 
plt.text(-55.6263,-61.2229,'象岛',font2)
#Weddell Sea  
plt.text(-45.9297,-63.9083,'威德尔海',font1) 
#Scotia Sea
plt.text(-54.653,-59.3101,'斯科舍海',font1)
#Powell Basin 
plt.text(-51.3815,-61.7758,'鲍威尔海盆',font1,rotation=30) 
#South Scotia Ridge 斯科舍海岭
plt.text(-52.3815,-60.2258,'南斯科舍海岭',font4,rotation=15)
#Philip Ridge 菲利普海岭
plt.text(-52.3815,-60.8758,'菲利普海岭',font4,rotation=30)




fig_name = 'D:/Refresh/data/CHINARE-32/32次南极半岛站位图/研究区域-中文.png' 
fig.savefig(fig_name,bbox_inches='tight',dpi=1000,pad_inches=0.03)
plt.show()



