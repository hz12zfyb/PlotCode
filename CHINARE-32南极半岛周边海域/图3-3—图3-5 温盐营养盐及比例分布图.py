# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 16:27:33 2019
ppc psc micro nano pico
@author: Administrator
"""
import sys
sys.path.append('D:/Refresh/py36')
import support_pie 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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


df = pd.read_excel('D:/Refresh/data/CHINARE-32/data_all.xlsx').set_index('Station')
#df = df.drop('AM-01')
image = support_pie.loadtif()
depths = [0,25,50,100,200]
#AP
#带比值
nutrition_name = ['Temperature','Salinity','Nitrate','Phosphate','Silicate','N/P ratio','SI/P ratio','N/SI ratio']
nutrition = ['Temperature [℃]','Salinity [psu]','NO3 [μmol/L]','PO4 [μmol/L]','Si [μmol/L]','N/P','SI/P','N/SI']
nutrition_min,nutrition_max = [-1.7,33.5,10,1,70,11,30,0.2],\
                              [1.7,34.7,35,2.5,100,16,50,0.4]
nutrition_danwei = ['℃','PSU','μmol·$\mathregular{L^{-1}}$','μmol·$\mathregular{L^{-1}}$',
                    'μmol·$\mathregular{L^{-1}}$',' ',' ',' ']                               
#分三个图画
#nutrition_name = ['Temperature','Salinity']
#nutrition = ['Temperature [℃]','Salinity [psu]']
#nutrition_min,nutrition_max = [-1.7,33.5],\
#                              [1.7,34.7]
#nutrition_danwei = ['℃','PSU'] 
 
#nutrition_name = ['Nitrate','Phosphate','Silicate']
#nutrition = ['NO3 [μmol/L]','PO4 [μmol/L]','Si [μmol/L]']
#nutrition_min,nutrition_max = [10,1,70],\
#                              [35,2.5,100]
#nutrition_danwei = ['μmol·$\mathregular{L^{-1}}$','μmol·$\mathregular{L^{-1}}$',
#                    'μmol·$\mathregular{L^{-1}}$']  
#
#nutrition_name = ['N/P ratio','SI/P ratio','N/SI ratio']
#nutrition = ['N/P','SI/P','N/SI']
#nutrition_min,nutrition_max = [11,30,0.2],\
#                              [16,50,0.4]
#nutrition_danwei = [' ',' ',' ']  



#不带比值
#nutrition = ['Temperature [℃]','Salinity [psu]','NO3 [μmol/L]','PO4 [μmol/L]','Si [μmol/L]']
#nutrition_min,nutrition_max = [-1.7,33.5,10,1,70],[1.7,34.7,35,2.5,100]
#
#nutrition_name =['T','S','Nitrate','Phosphate','Silicate']
#nutrition_danwei = ['℃','PSU','μmol·$\mathregular{L^{-1}}$','μmol·$\mathregular{L^{-1}}$',
#'μmol·$\mathregular{L^{-1}}$']
#特征色素浓度
#nutrition = ['Chlorophyll A','Pheophorbide A','Pheophytin A',
#             'Chlorophyll C2','Fucoxanthin','Chlorophyll C3','Chlorophyll B']
#nutrition_min,nutrition_max = [0,0,0,0,0,0,0,0],\
#                              [0.4,0.25,0.05,2,2,0.6,0.05]
#AS
#nutrition_min,nutrition_max = [-1.7,32.7,21,1.5,25,8,13,0.25],\
#                                [1.7,34.5,34,2.5,80,15,40,0.86]
#nutrition_name = ['T','S','Nitrate','Phosphate','Silicate','N/P','SI/P','N/SI']
#nutrition_danwei = ['℃','PSU','μmol·$\mathregular{L^{-1}}$','μmol·$\mathregular{L^{-1}}$',
#                    'μmol·$\mathregular{L^{-1}}$',' ',' ',' ']
#nutrition_min,nutrition_max = [-1.7,32.7,21,1.5,25],\
#                                [1.7,34.5,34,2.5,80]
#nutrition_name = ['T','S','Nitrate','Phosphate','Silicate']
#nutrition_danwei = ['℃','PSU','μmol·$\mathregular{L^{-1}}$','μmol·$\mathregular{L^{-1}}$',
#                    'μmol·$\mathregular{L^{-1}}$']

plt.rcParams['figure.figsize'] = (30,12)  #【8，12】  【12，12】
index,column = 5,8
fontsize = 14
plt.subplots_adjust(wspace=0.1,hspace=0.1)
rang = 0
for i in range(column): 
    for j in range(index): 
        num = j * column + i + 1
        print(num)
        plt.subplot(index,column,num)

        lon_left,lon_right,lat_bottom,lat_top = -61,-44,-64,-59 #NAP
#        lon_left,lon_right,lat_bottom,lat_top = -125,-85,-76,-65 #AS
#        lon_left,lon_right,lat_bottom,lat_top = -108,-88,-73,-65
        #导入数据
        df_plt = df.loc[df['depth'] == depths[j]]

        value = np.array(df_plt[nutrition[i]])        
        value,arg = del_nan(value)
        lon = np.array(df_plt['Longitude [degrees_east]'])[arg]
        lat = np.array(df_plt['Latitude [degrees_north]'])[arg]
        lon,lat,value = support_pie.inter_data(lon,lat,value,100)
        #画分布图   
        norm = mpl.colors.Normalize(vmin=nutrition_min[i],
                                    vmax=nutrition_max[i])
#        Cbar = plt.contourf(lon[:2,:2],lat[:2,:2],
#                            [[nutrition_min[i],nutrition_max[i]],[nutrition_min[i],nutrition_max[i]]],
#                            cmap='jet',extend='max')
#        if j == index-1:
#            plt.subplot(index+1,column,num+1)
#            B1 = plt.colorbar(Cbar,orientation='horizontal')
#            B1.set_clim(nutrition_min[i],nutrition_max[i])
#            plt.subplot(index+1,column,num)
        plt.contourf(lon,lat,value,100,cmap='rainbow',extend='max',
                       norm=norm)
            
        C = plt.contour(lon,lat,value,5,colors='white',linewidths=0.5,
                          norm=norm)
        plt.clabel(C,inline=True,fontsize=8,colors='black',fmt='%.2f')
        s = nutrition_name[i] +' / '+nutrition_danwei[i]#+ ' \nDepth : ' + str(depths[j]) + 'm'
        xuhao = support_pie.getChar(i) +" - " +str(depths[j]) + 'm'
        #AP
        if j == 0:
            plt.text(-60.8,-59.8,s,fontsize=12)   
        plt.text(-48.5,-59.8,xuhao,fontsize=12) 
        #AS
#        plt.text(-108,-67,s,fontsize=fontsize)   
#        plt.text(-90,-66,support_pie.getChar(rang),fontsize=fontsize)         
        #画底图
        support_pie.contourf_re(image,lon_left,lon_right,lat_bottom,lat_top)
        rang = rang +1
        #画坐标轴
        if i != 0:
            plt.yticks(())
        if j != 0:
            plt.xticks(())
        else:
            plt.gca().xaxis.set_ticks_position('top') 


plt.savefig('D:/Refresh/data/CHINARE-32/pic/TSNPSI及其比例分布.png',
            bbox_inches='tight',dpi=1000,pad_inches=0.1)            
plt.show()