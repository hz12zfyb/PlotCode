# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 12:54:48 2019
积分色素浓度画图
@author: Administrator
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os,sys
sys.path.append('D:/Refresh/py36')
import support_pie
from matplotlib.colors import LogNorm
import matplotlib as mpl 
import matplotlib.pylab as p
from matplotlib.mlab import griddata

#设定调

#读取数据
df = pd.read_excel('D:/Refresh/data/CHINARE-32/水柱积分藻种数据.xlsx',
                   sheet_name='Sheet2全').set_index('station')
#df = df.drop(['D2-03'])
image = support_pie.loadtif()
plt.rcParams['figure.figsize'] = (9,12)
plt.subplots_adjust(wspace=0.01,hspace=0.1)
plt.rc('font',family='Times New Roman')
df['Pheophorbide A'][10] = 0.2
#画图分析



def del_nan(value):
    arg_nan = np.where(np.isnan(value))
    arg = list(np.arange(len(value)))
    for i in range(len(arg_nan[0])):
        i = i+1
        x = arg_nan[0][-i]
        del arg[x]
    value = value[arg]
    return value,arg

def inter_data(x,y,z):
    n = 1000
    lon_left,lon_right,lat_bottom,lat_top = -61,-44,-64,-59
    xi, yi = p.meshgrid(p.linspace(lon_left,lon_right,n),
                        p.linspace(lat_bottom,lat_top,n))
    zi = griddata(x,y,z,xi,yi,interp='nn')
    return xi,yi,zi

def plot(pigment,df_plt,image):
#    fig = plt.figure()


    #所有字体matplotlib.font_manager.fontManager.ttflist
    plt.rcParams['font.sans-serif'] = ['Times New Roman']

    #station_index = np.array(df_plt['Station'])
    lon = np.array(df_plt.loc[:,'Longitude [degrees_east]'])
    lat = np.array(df_plt.loc[:,'Latitude [degrees_north]'])
    value = np.array(df_plt.loc[:,pigment])
    lon,lat,value = inter_data(lon,lat,value)
#    norm = LogNorm(vmin=np.min(value),
#           vmax=np.max(value)) 
    norm = mpl.colors.Normalize(vmin=value.min(),
                                vmax=value.max()*0.8)
    B = plt.contourf(lon,lat,value,25,cmap='rainbow',
                   norm=norm,alpha=1)
    #colorbar 
    cb = plt.colorbar(B,format='%d')
#    cb_ticks = cb.get_ticks()
#    cb.set_ticks(cb_ticks[::2]) 
      
    C = plt.contour(lon,lat,value,5,colors='white',linewidths=0.5,
                      norm=norm)
    plt.clabel(C,inline=True,fontsize=8,colors='black',fmt='%d')
    #岛屿
    lon_left,lon_right,lat_bottom,lat_top = -61,-44,-64,-59
    support_pie.contourf_re(image,lon_left,lon_right,lat_bottom,lat_top)

    
def plot_scatter(pigment,df_plt,image):
#    fig = plt.figure()
    lon_left,lon_right,lat_bottom,lat_top = -61,-44,-64,-59
    support_pie.contourf(image,lon_left,lon_right,lat_bottom,lat_top)
    #所有字体matplotlib.font_manager.fontManager.ttflist
    plt.rcParams['font.sans-serif'] = ['Times New Roman']

    #station_index = np.array(df_plt['Station'])
    station_lon = np.array(df_plt.loc[:,'Longitude [degrees_east]'])
    station_lat = np.array(df_plt.loc[:,'Latitude [degrees_north]'])
    colors = np.array(df_plt.loc[:,pigment])

    norm = LogNorm(vmin=np.min(colors),
           vmax=np.max(colors))
    plt.scatter(station_lon,station_lat,
                c = colors,cmap='rainbow',s = 60,norm=norm) 


    cb = plt.colorbar(format='%.1f')
    cb_ticks = cb.get_ticks()
    cb.set_ticks(cb_ticks[::2])

x,y=-60.5,-59.5
fontsize={'size':12,'weight':'normal'} 
             
plt.subplot(4,2,1)
plt.gca().xaxis.set_ticks_position('top')  
plot('tchla/μg m-2',df,image)
plt.text(x,y,s='Chlorophyll a/mg·$\mathregular{m^{-2}}$',
         fontdict=fontsize)
plt.text(-46,-59.5,'a',fontdict=fontsize)
#plt.xticks(())

plt.subplot(4,2,2)
plt.gca().xaxis.set_ticks_position('top') 
plot('Pheophorbide A',df,image)
plt.text(x,y,s='Pheophorbide A/mg·$\mathregular{m^{-2}}$',
         fontdict=fontsize)
plt.text(-46,-59.5,'b',fontdict=fontsize)
plt.yticks(())

plt.subplot(4,2,3)
plot('Pheophytin A',df,image)
plt.text(x,y,s='Pheophytin A/mg·$\mathregular{m^{-2}}$',
         fontdict=fontsize)
plt.text(-46,-59.5,'c',fontdict=fontsize)
#plt.yticks(())
plt.xticks(())

plt.subplot(4,2,4)
plt.gca().xaxis.set_ticks_position('top')  
plot('Chlorophyll C2',df,image)
plt.text(x,y,s='Chlorophyll $\mathregular{c_2}$/mg·$\mathregular{m^{-2}}$',
         fontdict=fontsize)
plt.text(-46,-59.5,'d',fontdict=fontsize)
plt.yticks(())
plt.xticks(())

plt.subplot(4,2,5)
plot('Fucoxanthin',df,image)
plt.text(x,y,s='Fucoxanthin/mg·$\mathregular{m^{-2}}$',
         fontdict=fontsize)
plt.text(-46,-59.5,'e',fontdict=fontsize)
#plt.yticks(())
plt.xticks(())

plt.subplot(4,2,6)
plot('Chlorophyll C3',df,image)
plt.text(x,y,s='Chlorophyll $\mathregular{c_3}$/mg·$\mathregular{m^{-2}}$',
         fontdict=fontsize)
plt.text(-46,-59.5,'f',fontdict=fontsize)
plt.xticks(())
plt.yticks(())

plt.subplot(4,2,7)
plot('Chlorophyll B',df,image)
plt.text(x,y,s='Chlorophyll B/mg·$\mathregular{m^{-2}}$',
         fontdict=fontsize)
plt.text(-46,-59.5,'g',fontdict=fontsize)
#plt.yticks(())
plt.xticks(())


plt.savefig('D:/Refresh/data/CHINARE-32/pic/诊断色素积分分布.png',
            bbox_inches='tight',dpi=1000,pad_inches=0.1)
plt.show()

###积分chla 分布
#plt.rcParams['figure.figsize'] = (11,6)
#plot('tchla',df,image)
#plt.text(x,y,s='Chlorophyll a/μg·$\mathregular{m^{-2}}$',
#         fontdict=fontsize)
#plt.gca().xaxis.set_ticks_position('top')
#plt.text(-46,-59.5,'f',fontdict=fontsize)
#plt.savefig('D:/Refresh/data/CHINARE-32/pic/CHEMTAX藻种分布/chla积分分布.png',
#            bbox_inches='tight',dpi=1000,pad_inches=0.1)