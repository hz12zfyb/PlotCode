# -*- coding: utf-8 -*-
import sys
sys.path.append('D:/Refresh/py36')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import support_pie 
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


def plot(value_name,vmin,vmax,title):
    df_plt = pd.read_excel('D:/Refresh/data/CHINARE-36/水柱积分藻种数据.xlsx').set_index('Station')
#导入数据
    value = np.array(df_plt[value_name])      
    value,arg = del_nan(value)
    lon = np.array(df_plt['Longitude [degrees_east]'])[arg]
    lat = np.array(df_plt['Latitude [degrees_north]'])[arg]
    lon,lat,value = support_pie.inter_data(lon,lat,value,1000)
    #画分布图   
    norm = mpl.colors.Normalize(vmin=vmin,
                                vmax=vmax) #20-100 
    B = plt.contourf(lon,lat,value,100,cmap='rainbow',extend='max',
                   norm=norm,alpha=1)
    #colorbar 
#    cb = plt.colorbar(B)  
#    cb.set_ticks(np.round(np.linspace(vmin,vmax,10),1)) 
    C = plt.contour(lon,lat,value,5,colors='white',linewidths=0.5,
                      norm=norm)
    plt.clabel(C,inline=True,fontsize=12,colors='black',fmt='%d')
    #画底图
    lon_left,lon_right,lat_bottom,lat_top = 33,75,-68,-61
    plt.gca().xaxis.set_ticks_position('top')
    support_pie.contourf_re(image,lon_left,lon_right,lat_bottom,lat_top)

    plt.text(lon_left+0.5,-62,title,fontsize=14)
    plt.text(lon_right-1,-62,support_pie.getChar(i),fontsize=14)

    if i not in [0,1]:
            plt.xticks(())
    if i not in [0,2,4,6]:
            plt.yticks(())
    if i == 6:
        im = plt.contourf(lon[:2,0],lat[:2,0], 
                          [[vmin,vmax],[vmin,vmax]],cmap='rainbow')
        fig.subplots_adjust(right=0.85)
        cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.7])
        plt.colorbar(im, cax=cbar_ax)

plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 中文字体设置
#plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (10,10)

image = support_pie.loadtif()
value = ['Diat1_p', 'Diat2_p', 
         'Hapt6HiFe_p','Hapt6LoFe_p',
         #'Hapt6HiFe_pp','Hapt6LoFe_pp',
         'Hapt6_p',
         'Dino1_p','Chloro_p', 'Crypto_p']
title = ['Diatoms-A/%','Diatoms-B/%',
         'P. antarctica (high Fe)/%','P. antarctica (low Fe)/%',
         #'P. antarctica (high Fe)/P. antarctica%','P. antarctica (low Fe)/P. antarctica%',
         'P. antarctica/%',
         'Dinoflagellate/%','Chlorophytes/%','Cryptophytes/%']
value_min,value_max = [0]*8,[60]*8
fig, axes = plt.subplots(4,2, squeeze=True)
plt.subplots_adjust(wspace=0.15,hspace=0.08)
for i in range(8):
    plt.subplot(4,2,i+1)
    plot(value[i],value_min[i],value_max[i],title[i])

#ax = plt.subplot(5,2,10)
#ax.spines['right'].set_color('none')
#ax.spines['top'].set_color('none')
#ax.spines['left'].set_color('none')
#ax.spines['bottom'].set_color('none')
#ax.set_xticks(())
#ax.set_yticks(())
plt.savefig('D:/Refresh/data/CHINARE-36/pic/藻种水柱积分相对丰度平面分布-english.png'
            ,bbox_inches='tight',dpi=1000,pad_inches=0.1)            
plt.show()