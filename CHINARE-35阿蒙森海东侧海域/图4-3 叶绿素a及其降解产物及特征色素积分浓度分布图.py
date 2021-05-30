# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 12:54:48 2019
积分色素浓度画图 散点和分布图两种
@author: Administrator
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('D:/Refresh/py36')
import support_pie
from matplotlib.colors import LogNorm
import matplotlib as mpl 

def del_nan(value):
    arg_nan = np.where(np.isnan(value))
    arg = list(np.arange(len(value)))
    for i in range(len(arg_nan[0])):
        i = i+1
        x = arg_nan[0][-i]
        del arg[x]
    value = value[arg]
    return value,arg


def plot(pigment,df_plt,image):
    lon = np.array(df_plt.loc[:,'Longitude [degrees_east]'])
    lat = np.array(df_plt.loc[:,'Latitude [degrees_north]'])
    value = np.array(df_plt.loc[:,pigment])
    lon,lat,value = support_pie.inter_data(lon,lat,value,1000)
#    norm = LogNorm(vmin=np.min(value),
#           vmax=np.max(value)) 
    norm = mpl.colors.Normalize(vmin=value.min(),
                                vmax=value.max()*0.8)
    B = plt.contourf(lon,lat,value,25,cmap='rainbow',
                   norm=norm,alpha=1)
    #colorbar 
    plt.colorbar(B,format='%.1f')      
    C = plt.contour(lon,lat,value,5,colors='white',linewidths=0.5,
                      norm=norm)
    plt.clabel(C,inline=True,fontsize=12,colors='black',fmt='%.1f')
    #岛屿
    support_pie.contourf_re(image,lon_left,lon_right,lat_bottom,lat_top)

    
def plot_scatter(pigment,df_plt,image):
#    fig = plt.figure()
    support_pie.contourf(image,lon_left,lon_right,lat_bottom,lat_top)

    #station_index = np.array(df_plt['Station'])
    station_lon = np.array(df_plt.loc[:,'Longitude [degrees_east]'])
    station_lat = np.array(df_plt.loc[:,'Latitude [degrees_north]'])
    colors = np.array(df_plt.loc[:,pigment])/5

    norm = LogNorm(vmin=np.min(colors),
           vmax=np.max(colors))
    plt.scatter(station_lon,station_lat,
                c = colors,cmap='rainbow',s = 60,norm=norm) 

    cb = plt.colorbar(format='%.1f')
    cb_ticks = cb.get_ticks()
    cb.set_ticks(cb_ticks[::2])
#读取数据
df = pd.read_excel('D:/Refresh/data/CHINARE-35/水柱积分藻种数据.xlsx',
                   sheet_name='Sheet1').set_index('Station')


fontsize={'size':14,'weight':'normal'} 

lon_left,lon_right,lat_bottom,lat_top = -108,-88,-73,-65
z = ['Chlorophyll A','Pheophorbide A','Pheophytin A','Fucoxanthin','19-hex',
     'Alloxanthin','Peridinin','Chlorophyll B'] #色素列名
text = ['Chlorophyll a/mg·$\mathregular{m^{-2}}$',
        'Pheophorbide a/mg·$\mathregular{m^{-2}}$',
        'Pheophytin a/mg·$\mathregular{m^{-2}}$',
        'Fucoxanthin/mg·$\mathregular{m^{-2}}$',
        "19'-hexanoyloxyfucoxanthin/mg·$\mathregular{m^{-2}}$",
        'Alloxanthin/mg·$\mathregular{m^{-2}}$',
        'Peridinin/mg·$\mathregular{m^{-2}}$',
        'Chlorophyll b/mg·$\mathregular{m^{-2}}$'] #题名
index,column = [4,2] #行和列的数量  【2*2 也可，z和title列数量（4）对应就好】
fig_dir = 'D:/Refresh/data/CHINARE-35/pic/特征色素积分分布-english.png' #图片保存路径

plt.rcParams['font.sans-serif']=['Times New Roman']  
fig = plt.figure()
plt.rcParams['figure.figsize'] = (10,10)
plt.subplots_adjust(wspace=0.01,hspace=0.1)

image = support_pie.loadtif()
num = 0
for i in range(index):
    for j in range(column):
        plt.subplot(index,column,num+1)
        plt.gca().xaxis.set_ticks_position('top')  
        plot(z[num],df,image)
        plt.text(-90,-66,support_pie.getChar(num),fontdict=fontsize)
        plt.text(-107.7,-66.5,s=text[num],fontdict=fontsize)

#        plt.text(char_x,char_y,support_pie.getChar(num),
#                 fontdict=fontsize)
        if i != 0 :
            plt.xticks(())
        if j != 0:
            plt.yticks(())
        num += 1
             
plt.savefig(fig_dir,bbox_inches='tight',dpi=1000,pad_inches=0.1)
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