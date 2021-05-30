# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 10:57:53 2020

@author: Administrator
"""
import sys
sys.path.append('D:/Refresh/py36')
import read_CTDdata 
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

def set_alpha(x):
    if x <0.25:
        y = 0.3
    elif x>=0.25 and x <0.47:
        y = 0.35
    elif x>=0.47 and x <0.7:
        y = 0.45
    else:
        y = 0.7
    return y
plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 中文字体设置
#plt.rcParams['axes.unicode_minus'] = False
#fontcn = {'family': 'SimHei','weight' : 'normal','size': 14}


plt.rcParams['figure.figsize'] = (12,8)
plt.subplot(2,2,1)
file_dir = 'D:/Refresh/data/CHINARE-35/全水深CTD/'
stationnames = read_CTDdata.get_stationname(file_dir)
data_sum = read_CTDdata.get_data(file_dir)
df = pd.read_excel('D:/Refresh/data/CHINARE-35/data_all.xlsx').set_index('Station')
depth = 197

data_plt = np.zeros(shape=(len(stationnames),depth,4))
for i in range(len(stationnames)):
        data_plt[i,:,0] = data_sum[i][:depth,5]    #温度
        data_plt[i,:,1] = data_sum[i][:depth,16]    #盐度
        data_plt[i,:,2] = data_sum[i][:depth,18]/210    #深度
        data_plt[i,:,3] = data_sum[i][:depth,12]    #密度

df_labels = df[df['Depth [m]'] == 0]['AREA']

labels = dict(zip([1,2,3],
                ['#d55c00','#cc7aa7','#0071b2']))
#画图
#plt.rcParams['figure.figsize'] = (6,4)
#for i in range(len(stationnames)):
for i in [0,2,5,6,7,8,1,3,4]:
    print(i)
#    if i == 10 or i == 11:  
#        continue
#    else:
        # 分段式的alpha值
    for j in range(depth):
        plt.scatter(data_plt[i,j,1],data_plt[i,j,0],
                    s=1,alpha = 1,#set_alpha(data_plt[i,j,2]),
                    c=labels[df_labels[i]],marker='o')

#legend
h1 = plt.scatter([0],[1],c=['#d55c00'])
h2 = plt.scatter([1],[2],c=['#cc7aa7'])
h3 = plt.scatter([2],[2],c=['#0071b2'])
first_legend = plt.legend(handles=[h1,h2,h3],markerscale=1,
                          labels=['Ice free days > 70','10 < Ice free days < 70',
                                  'Ice free days < 10'],
                          loc = 'upper left'
                          #title = 'Region',                          
                          )
plt.gca().add_artist(first_legend)
#h1 = plt.scatter([0],[1],c=['#0071b2'],alpha=0.15)
#h2 = plt.scatter([1],[2],c=['#0071b2'],alpha=0.25)
#h3 = plt.scatter([2],[4],c=['#0071b2'],alpha=0.65)
#h4 = plt.scatter([3],[3],c=['#0071b2'],alpha=1)
#plt.legend(handles=[h1,h2,h3,h4],markerscale=1,
#                          labels=['0-50','50-100','100-150','150-200'],
#                          title = 'Depth/m',
#                          loc = 'lower right')
#xy轴
x1,x2,y1,y2 = -2,2,32.5,34.7
plt.ylim(x1,x2)
plt.xlim(y1,y2)
plt.xlabel('Salinity/PSU')
plt.ylabel('Potential temperature/℃')
plt.gca().xaxis.set_ticks_position('top')

#画等密度线
S_plt,T_plt = data_plt[:,:,1].reshape(-1),data_plt[:,:,0].reshape(-1)
K_plt = data_plt[:,:,3].reshape(-1)
C = plt.tricontour(S_plt,T_plt,K_plt,5,colors='black',linewidths=0.5)
plt.clabel(C,inline=True,fontsize=8)

#增加水团名称 AP
#plt.text(34.35,-1.9,'WWw')
#plt.text(34.17,0.6,'TBW')
#plt.text(34.6,-0.2,'WDw')
plt.text(34.45,1.6,'a',fontsize=14)

image = support_pie.loadtif()
def plot(value_name,vmin,vmax,title):
    df_plt = pd.read_excel('D:/Refresh/data/CHINARE-35/水柱积分藻种数据.xlsx').set_index('Station')
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
    cb = plt.colorbar(B) 
    cb.set_ticks(np.round(np.linspace(vmin,vmax,10),0)) #设置小数位数
    C = plt.contour(lon,lat,value,5,colors='white',linewidths=0.5,
                      norm=norm)
    plt.clabel(C,inline=True,fontsize=14,colors='black',fmt='%d')
    #画底图
    lon_left,lon_right,lat_bottom,lat_top = -108,-88,-73,-65
    plt.gca().xaxis.set_ticks_position('top')
    support_pie.contourf_re(image,lon_left,lon_right,lat_bottom,lat_top)
    plt.text(-107.5,-65.7,title,fontsize=14)
    plt.text(-90,-65.7,support_pie.getChar(i+1),fontsize=14)

value = ['MLD/m','%MW','Stability']
title = ['MLD/m','MW%','$\mathregular{E_{stability}}$']
value_min,value_max = [10,2.5,3],[50,7,12]
for i in range(3):
    plt.subplot(2,2,i+2)
    plot(value[i],value_min[i],value_max[i],title[i])
plt.savefig('D:/Refresh/data/CHINARE-35/pic/文章用图25+1-英文.png'
            ,bbox_inches='tight',dpi=1000,pad_inches=0.1)            
plt.show()