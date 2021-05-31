# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 10:38:13 2019
计算MLD 深度
需要更改55-70 和109行
36次
# name 0 = depSM: Depth [salt water, m]
# name 1 = t090C: Temperature [ITS-90, deg C]
# name 2 = sal00: Salinity, Practical [PSU]
# name 3 = density00: Density [density, kg/m^3]
# name 4 = potemp090C: Potential Temperature [ITS-90, deg C]
# name 5 = sbox0Mm/Kg: Oxygen, SBE 43 [umol/kg]
# name 6 = oxsolMm/Kg: Oxygen Saturation, Garcia & Gordon [umol/kg]
# name 7 = svCM: Sound Velocity [Chen-Millero, m/s]
# name 8 = flag:
@author: fyb
35次
# name 1 = latitude: Latitude [deg]
# name 4 = prDM: Pressure, Digiquartz [db]
# name 5 = t090C: Temperature [ITS-90, deg C]
# name 8 = c1mS/cm: Conductivity, 2 [mS/cm]
# name 16 = sal00: Salinity, Practical [PSU]
# name 18 = depSM: Depth [salt water, m], lat = -70.4867
"""
import sys
sys.path.append('D:/Refresh/py36')
import read_CTDdata 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gsw
import heapq


def Moving_Average(data,n):
    data_output = np.zeros(shape=len(data)-n)
    for i in range(len(data_output)):
        data_output[i] = np.average(data[i:i+n])
    return data_output 

#密度变化最大的深度        
def Get_MLD0(i): 
#    station_depth = data_sum[i][-1,12]     
    MLD_arg_d = np.argmax(np.gradient(data_sum[i][7:200,10])) +7
    MLD_depth_d = data_sum[i][MLD_arg_d,12]
    QI = 1 - np.std(data_sum[i][:MLD_arg_d,10])/np.std(data_sum[i][:int(1.5*MLD_arg_d),10])
    data_c = Moving_Average(data_sum[i][:200,9],7)
    MLD_arg_c = np.argmin(np.gradient(data_c))    
    MLD_depth_c = data_sum[i][MLD_arg_c,12]
#    QC = 1 - np.std(data_sum[4][MLD_arg_c:station_depth,9])/np.std(data_sum[4][int(station_depth-1.5*(station_depth-MLD_arg_c)):station_depth,9])
    return MLD_depth_d,QI,MLD_depth_c
#N2最大值的深度
def Get_MLD1(i): 
    min,max = 10,100
    ave = 3 #移动平均 必须
    # 32次 17,6,8,2,12
    # 33次 32,28,16,2,26
    # 34次 32,28,8,2,36 
    # 35次 16,5,4,1,18
    # 36次 2,1,,0,0缺少纬度和压力数据 用深度代替压力
    # 362次 32,28,8,2,36 
    # 36次 MVP 5,3,,0,1 
    Data = data_sum[i] 
    #Data = Data[::-1] #33 362次需要反向数据
    SA = Moving_Average(Data[min:max,2],ave)
    CT = Moving_Average(Data[min:max,1],ave)
    p  = Moving_Average(Data[min:max,0],ave)
#    lat =Moving_Average(Data[min:max,1],ave)

    depth = Moving_Average(Data[min:max,0],ave)
#    XCTD
#    SA = Moving_Average(xctd_salt[10:100,2],3)
#    CT = Moving_Average(xctd_pt[10:100,2],3)
#    depth = Moving_Average(xctd_dep[10:100,2],3)
    N2,p_mid = gsw.stability.Nsquared(SA,CT,p)#,lat)
    
    mld = depth[np.argmax(N2)]
    E = N2/9.832*1000000
    mean_E = np.mean(E)
    #df = pd.DataFrame(data=E,index=depth[:-1])
    return mld,mean_E#,df

def Get_MLD1_mvp(i): 
    min,max = 10,100
    ave = 3 #移动平均 必须
    # 36次 MVP 5,3,0,1 
    Data = data_sum[i] 
    SA = Moving_Average(Data[min:max,5],ave)
    CT = Moving_Average(Data[min:max,3],ave)
    p  = Moving_Average(Data[min:max,0],ave)
    #lat = Moving_Average(Data[min:max,0],ave)
    depth = Moving_Average(Data[min:max,1],ave)
    N2,p_mid = gsw.stability.Nsquared(SA,CT,p)
    
    mld = depth[np.argmax(N2)]
    E = N2/9.832*1000000
    mean_E = np.mean(E)
    #df = pd.DataFrame(data=E,index=depth[:-1])
    return mld,mean_E#,df

def Get_MLD2(i):
#Venables and Moore, 2010
#大于10米的密度 0.05的深度为混合层深度
    depth = data_sum[i][:,0]
    density = data_sum[i][:,3]
    if np.min(depth) <10:
        j = np.where(depth==10)
    else :
        j = 0
    for i in range(len(depth)):
        if depth[i] > 10:
            if density[i] - density[j] >= 0.05:
                mld = depth[i]
                break
    return mld

def Get_aver200(i):
    #CTD 0 1 2 5 MVP 1 3 5 
    depth = np.where(data_sum[i][:,1] <200)
    depth = list(depth)[0][10:]
    t =  np.mean(data_sum[i][depth,3])
    s =  np.mean(data_sum[i][depth,5])
#    do =  np.mean(data_sum[i][depth,5]) /36
    return t,s#,do

#计算mld 
file_dir = 'D:/Refresh/data/CHINARE-36/全水深MVP下上/'
stationnames = read_CTDdata.get_stationname(file_dir)
data_sum = read_CTDdata.get_data_mvp(file_dir)
stations = len(stationnames)

df = pd.DataFrame(np.zeros(shape=(stations,2)),
                  columns = ['MLD_depth','stability100'],
                  index = stationnames)
for i in range(stations):
    #df.iloc[i] = Get_MLD1(i)
    df.iloc[i] = Get_MLD1_mvp(i)




#32次
#df.loc['DA-06'][1] = 0.815207867
#df.loc['D2-03'][1] = 2.718069735

    
#print( stats.pearsonr(x,df['MLD_depth_D']))
#plt.scatter(df['MLD_depth_D'],x,c=df['QI'])
#plt.colorbar()
    
#计算温盐 200米平均值
#file_dir = 'D:/Refresh/data/CHINARE-36/全水深CTD/'
#stationnames = read_CTDdata.get_stationname(file_dir)
#data_sum = read_CTDdata.get_data(file_dir)
#stations = len(stationnames)
#
#
#df = pd.DataFrame(np.zeros(shape=(stations,3)),
#                  columns = ['T','S','DO'],
#                  index = stationnames)
#for i in range(stations):
#    df.iloc[i] = Get_aver200(i)   
#    
#    
#file_dir = 'D:/Refresh/data/CHINARE-36/全水深MVP/'
#stationnames = read_CTDdata.get_stationname(file_dir)
#data_sum = read_CTDdata.get_data_mvp(file_dir)
#stations = len(stationnames)
#
#df = pd.DataFrame(np.zeros(shape=(stations,2)),
#                  columns = ['T','S'],
#                  index = stationnames)
#for i in range(stations):
#    df.iloc[i] = Get_aver200(i)   