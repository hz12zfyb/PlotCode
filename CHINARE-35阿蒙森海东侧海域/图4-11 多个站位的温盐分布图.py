# -*- coding: utf-8 -*-
import sys
sys.path.append('D:/Refresh/py36')
import support_pie,read_CTDdata
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec


plt.rcParams['font.sans-serif'] = ['Times New Roman']
font_red = {'color':  'red' } 
font_blue =  {'color':  'blue'}
plt.rcParams['figure.figsize'] = (9,3)
file_dir = 'D:/Refresh/data/CHINARE-35/全水深CTD/'
stationnames = read_CTDdata.get_stationname(file_dir)
data_sum = read_CTDdata.get_data(file_dir)
df = pd.read_excel('D:/Refresh/data/CHINARE-35/data_all.xlsx').set_index('Station')
df_station = pd.read_excel('D:/Refresh/py36/色素数据处理/station_information_35次.xlsx')\
.set_index('Station') 
#df_station = df_station.drop(['R1-01','R1-03','R1-04','AM-01'])
df_station = df_station.sort_values('growth_time')
paint_order = np.array(df_station.index)


depth = 210
data_plt = np.zeros(shape=(len(stationnames),depth,3))
gs = gridspec.GridSpec(1,len(stationnames))

for i in range(len(stationnames)):
    data_plt[i,:,0] = data_sum[i][:depth,5]    #温度
    data_plt[i,:,1] = data_sum[i][:depth,16]   #盐度
    data_plt[i,:,2] = data_sum[i][:depth,18]   #深度
#    print(np.max(data_plt[i,:,1]))
    ##按顺序画图
    order = np.where(paint_order == stationnames[i])[0][0]
    ax = plt.subplot(gs[0,order])
    plt.plot(data_plt[i,:,0],data_plt[i,:,2],'red')
    ax.set_xlim(-2,2)
#    ax.set_xticks((-1.5,0,1.5))
    ax.xaxis.set_ticks_position('bottom')
    if stationnames[i] == 'A7-08':
        ax.set_xlabel('Temperature / ℃',fontdict=font_red)
    text = stationnames[i]+'  '+support_pie.getChar(order)+' \nIce free days:\n  '+\
    str(int(df_station.iloc[order]['growth_time']))+' days'
    ax.text(-1.9,3,text)
    ax.set_ylim(-40,200)
    ax.invert_yaxis()   #Y轴反向 
#    ax.spines['right'].set_color('none')
#    ax.spines['top'].set_color('none')
    if order != 0:
        ax.set_yticks(())
    else:      
        ax.set_yticks((0,50,100,150,200))
        ax.set_ylabel('Depth / m')    
    ax1 = ax.twiny()
    ax1.plot(data_plt[i,:,1],data_plt[i,:,2],'blue')
    ax1.set_xticks((33,34,35))
    ax1.set_xlim(33,35)
    if stationnames[i] == 'A7-08':
        ax1.set_xlabel('Salinity / PSU',fontdict = font_blue)

    
fig_name = 'D:/Refresh/data/CHINARE-35/pic/所有站位的垂向温盐分布图-english.png' 
plt.savefig(fig_name,bbox_inches='tight',dpi=1000,pad_inches=0.1)   
plt.show()