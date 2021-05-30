# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:28:55 2019
藻种平面分布
@author: fyb
"""

import matplotlib.pyplot as plt
import numpy as np 
import sys
sys.path.append('D:/Refresh/py36')
import support_pie
import pandas as pd 

def add_pie(lon,lat,chla,station_name,algae_con,fig):
    algae_per = algae_con /np.sum(algae_con)
    lon = lon * 0.7520 + 0.1240
    lat = lat * 0.7763 + 0.1119
    left, bottom, width, height =lon-chla/2, lat-chla/2, chla, chla
    ax2  = fig.add_axes([left, bottom, width, height])
    stationnames =['D1-10', 'D2-03', 'D2-06',  'D3-03',
       'D3-06', 'D3-08',   'D4-05', 'D5-03', 'D5-11',  
       'D6-06', 'DA-01', 'DA-03', 'DA-06','DA-08', 
       'DB-01', 'DB-03','DB-08', 'DB-10', 'DC-02',  #以上为南极半岛站位
       'R1-04', 'R1-03', 'R1-01', 'AM-01', 'A6-08', #以下为阿蒙森海站位
       'A6-09', 'A7-10', 'A7-08','A8-08', 'A8-09', 
       'A9-10', 'A9-08', 'A8-07']
    if station_name in stationnames:
        ax2.set_title(station_name,fontsize=12)
    colors = ['#d55c00', '#cc7aa7', '#0071b2', '#55b5e9','#f0e442', '#009e74','#000000']
    wedges = ax2.pie(x= algae_per ,colors = colors,
        shadow = False ,startangle = 90 ,pctdistance = 1 )[0] 
#    ax2.axis('equal')
    return wedges
'''
labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数 autopct= '%3.0f%%' 
shadow，饼是否有阴影
startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
pctdistance，百分比的text离圆心的距离
patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
colors =  colors
'''   
def getChar(number):
    factor, moder = divmod(number, 26) # 26 字母个数
    modChar = chr(moder + 97)          # 65 -> 'A' 97 ->'a'
    if factor != 0:
        modChar = getChar(factor-1) + modChar # factor - 1 : 商为有效值时起始数为 1 而余数是 0
    return modChar

def main(value_name,depth,image,i):
    df_station = pd.read_excel('D:/Refresh//py36/色素数据处理/station_information_32次.xlsx').set_index('Station')
    
    if value_name == 'DCM':
        sheet_name = 'Sheet5'
    else:
        sheet_name = 'Sheet1'
    df_chemtax = pd.read_excel('D:/Refresh/data/CHINARE-32/CHEMTAX结果/6.29.xlsx',
                               sheet_name=sheet_name).set_index('Sample')

#    df_chemtax = df_chemtax.drop(['R1-01','R1-03','R1-04']) #删去罗斯海的站位
    df_chemtax['tchla'] = np.sum(df_chemtax.iloc[:,1:], axis=1)
    df_chemtax_depth = df_chemtax[df_chemtax[value_name] == depth] 

    algae_cons = df_chemtax.loc[df_chemtax[value_name] == depth]  #获取所有站位的depth米藻的浓度
    station_num = algae_cons.shape[0]
    chla_ave = 0.2
#    chla_ave = df_chemtax_depth['tchla'].sum()/station_num
    
    fontsize = 16
    plt.rcParams['figure.figsize'] = (11,6)
    fig = plt.figure()
    #lon_left,lon_right = df_station.iloc[:,1].min()-1,df_station.iloc[:,1].max()+1
    #lat_bottom,lat_top = df_station.iloc[:,2].min()-1,df_station.iloc[:,2].max()+1
    lon_left,lon_right,lat_bottom,lat_top = -61,-44,-64,-59 #NAP
#    lon_left,lon_right,lat_bottom,lat_top = -125,-85,-76,-65 #AS    

    support_pie.contourf_re(image,lon_left,lon_right,lat_bottom,lat_top)
    plt.gca().xaxis.set_ticks_position('top') 
    if value_name =='DCM':
        title_name = getChar(i)  + '  Depth : DCM'
    else:
        title_name = getChar(i)  + '  Depth : ' + str(depth) + ' m' 

#    南极半岛
    plt.text(-48,-59.3,title_name,fontsize=fontsize)
#    plt.text(-44.7,-59.3,getChar(i),fontsize= fontsize)
    plt.text(-55.5,-63.8,'Chlorophyll a/mg·$\mathregular{m^{-3}}$',fontsize=fontsize)
#    阿蒙森海
#    plt.text(-93,-66,title_name,fontsize=fontsize)
#    plt.text(120,-68,getChar(i),fontsize=16)
#    plt.text(-100,-73,'Chlorophyll a/mg·$\mathregular{m^{-3}}$',fontsize=fontsize)

    #加饼图

    algaes = algae_cons.columns[1:]
    for i in range(station_num):
        station_name = algae_cons.index[i]
        station_lon, station_lat = df_station.loc[station_name][1],df_station.loc[station_name][2]
        algae_con = np.array(algae_cons.loc[station_name][1:-1])
        weight = 0.05 * np.sqrt(df_chemtax_depth['tchla'][station_name] / chla_ave)
        weight_max , weight_min = 0.055 , 0.015
        if weight > weight_max:
            weight = weight_max
        elif weight < weight_min:
            weight = weight_min
        else:
            weight = weight
#        weight = 0.05

        if algae_con.sum() != 0:   #应对各个藻皆为0的情况
            x = (station_lon-lon_left)/(lon_right-lon_left)
            y = (station_lat-lat_bottom)/(lat_top-lat_bottom)
            wedges = add_pie(x,y,weight,station_name,algae_con,fig)
        else:
            continue
    
    #图例
#    if depth == 0 or depth == 100 :  #==0
    fig.legend(wedges,algaes,fontsize=14,title="",
#                   bbox_to_anchor=(0.38,0.29), #阿蒙森海
                   bbox_to_anchor=(0.554,0.798), #南极半岛
               ncol=2,framealpha=0.3)
#    bbox_to_anchor(0.2,0.8）图例的位置 loc ='right'
    weight =[0.05/2,0.05,0.05*2]
#    chla_ave = chla_ave/1000 #ng/L 转化为μg/L 32次不需要
    ax  = fig.add_axes([0.6, 0.15, weight[1], weight[0]])
    ax.pie([1,0],colors=['#000000','#fdffff'],shadow = False)
    ax.set_title('%.2f'%(chla_ave/2),fontsize=fontsize)
    ax  = fig.add_axes([0.7, 0.15, weight[1], weight[1]])
    ax.pie([1,0],colors=['#000000','#fdffff'],shadow = False)
    ax.set_title('%.2f'%(chla_ave),fontsize=fontsize)
    ax  = fig.add_axes([0.8, 0.15, weight[1], weight[2]])
    ax.pie([1,0],colors=['#000000','#fdffff'],shadow = False)
    ax.set_title('%.2f'%(chla_ave*2),fontsize=fontsize)
    

    fig_name = 'D:/Refresh/data/CHINARE-32/pic/CHEMTAX藻种分布/' +'result_'+str(depth) +'m.png' 
    fig.savefig(fig_name,bbox_inches='tight',dpi=1000,pad_inches=0.1)
#    fig.savefig('D:/Refresh/data/CHINARE-32/pic/CHEMTAX藻种分布/text_4.23_odv.png',dpi=700)
    plt.show()
image = support_pie.loadtif()
depth_series = [0,25,50,100,200]
for i in range(len(depth_series)):
    main('depth',depth_series[i],image,i)
#画DCM 叶绿素最大层
#main('DCM',1,image,1)
    
    
