# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:26:32 2019

@author: Administrator
"""

import matplotlib.pyplot as plt
import numpy as np 
from libtiff import  TIFF
import matplotlib as mpl
import matplotlib.colors as col
import matplotlib.cm as cm
import math,os
import netCDF4 as ne 
import matplotlib.pylab as p
from matplotlib.mlab import griddata



def log_n(a,logn):
    shape_a = a.shape
    b = np.zeros_like(a.reshape(-1))
    for i in range(len(a)):
        b[i] = math.log(a[i],logn)
    return b.reshape(shape_a)

def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def inter_data(x,y,z,n):
    lon_left,lon_right = np.min(x),np.max(x)
    lat_bottom,lat_top = np.min(y),np.max(y)
    xi, yi = p.meshgrid(p.linspace(lon_left,lon_right,n),
                        p.linspace(lat_bottom,lat_top,n))
    zi = griddata(x,y,z,xi,yi,interp='nn')
    return xi,yi,zi

def loadtif():
    file_name = 'D:/Refresh/data/ETOPO1/ETOPO1_Ice_c_geotiff.tif '   #冰架数据
    tif = TIFF.open(filename=file_name,mode='r')
    image =  tif.read_image()[::-1,:]
    print ('西经W南纬S为- 水深为-')
    return image

def quadratic(y):
    a,b,c = 17.634 ,41.164 ,-139.71-y
    p=b*b-4*a*c
    x=(-b+math.sqrt(p))/(2*a)
    return x

def contourf (image,lon1,lon2,lat1,lat2):  #纯白colorbar
    a = (image.shape[1]-1)/2
    b = (image.shape[0]-1)/2
    c = a/180
    x1 = np.int(np.round( lon1 *c + a,decimals=0))
    x2 = np.int(np.round( lon2 *c + a,decimals=0))
    y1 = np.int(np.round( lat1 *c + b,decimals=0))
    y2 = np.int(np.round( lat2 *c + b,decimals=0))
    image_plt =  - image[y1:y2,x1:x2]
    lon = np.linspace(lon1,lon2,num=x2-x1)
    lat = np.linspace(lat1,lat2,num=y2-y1)
    lon_num,lat_num = 6 , 6
    lon_name = lon_tran(lon1,lon2,lon_num)
    lat_name = lat_tran(lat1,lat2,lat_num)
    plt.xticks(np.linspace(lon1,lon2,num=lon_num),lon_name)
    plt.yticks(np.linspace(lat1,lat2,num=lat_num),lat_name)

    for i in range(y2-y1):
        for j in range(x2-x1):
            if image_plt[i,j] > 0:
                image_plt[i,j] = quadratic(image_plt[i,j])
            else:
                continue
    image_plt = np.ma.array(image_plt, mask=image_plt > 0)  #加mask
   #image_plt = -np.log10(-image_plt[:,:])
    plt.gca().patch.set_color('.25')  #设定mask颜色
    colors = ['#d0bfb1','#d5c9bc','#d8cfc3','#d5d2c6',
          '#cad3ca','#bad3cf','#afd2d4','#a4cfda',
          '#a1c6e0','#9ab9e2','#8face7','#82a1ec',
          '#8397f0','#8891f2','#8c89f4','#9485f3','#9881f3'] #odv colorbar
    colors = ['#FFFFFF','#FFFFFF'] #纯白colorbar
    cmap2 = col.LinearSegmentedColormap.from_list('odv',colors)    #定义odv的colorbar
   #extra arguments are N=256, gamma=1.0
    cm.register_cmap(cmap=cmap2)
    norm = mpl.colors.Normalize(vmin=0, vmax=17)
    plt.contourf(lon,lat,image_plt, 17, cmap='odv',norm=norm)  #odv Grey 
   #plt.contour(lon,lat,image_plt,10,colors='k')

def contourf_re(image,lon1,lon2,lat1,lat2):  #纯白colorbar
    a = (image.shape[1]-1)/2
    b = (image.shape[0]-1)/2
    c = a/180
    x1 = np.int(np.round( lon1 *c + a,decimals=0))
    x2 = np.int(np.round( lon2 *c + a,decimals=0))
    y1 = np.int(np.round( lat1 *c + b,decimals=0))
    y2 = np.int(np.round( lat2 *c + b,decimals=0))
    image_plt =  - image[y1:y2,x1:x2]
    lon = np.linspace(lon1,lon2,num=x2-x1)
    lat = np.linspace(lat1,lat2,num=y2-y1)
    lon_num,lat_num = 6 , 6
    lon_name = lon_tran(lon1,lon2,lon_num)
    lat_name = lat_tran(lat1,lat2,lat_num)
    plt.xticks(np.linspace(lon1,lon2,num=lon_num),lon_name)
    plt.yticks(np.linspace(lat1,lat2,num=lat_num),lat_name)

    for i in range(y2-y1):
        for j in range(x2-x1):
            if image_plt[i,j] > 0:
                image_plt[i,j] = quadratic(image_plt[i,j])
            else:
                continue
    image_plt = np.ma.array(image_plt, mask=image_plt > 0)  #加mask
   #image_plt = -np.log10(-image_plt[:,:])
    plt.gca().patch.set_color('1')  #设定mask颜色
    colors = ['#d0bfb1','#d5c9bc','#d8cfc3','#d5d2c6',
          '#cad3ca','#bad3cf','#afd2d4','#a4cfda',
          '#a1c6e0','#9ab9e2','#8face7','#82a1ec',
          '#8397f0','#8891f2','#8c89f4','#9485f3','#9881f3'] #odv colorbar
    colors = ['#7F7F7F','#7F7F7F'] #纯灰colorbar
    cmap2 = col.LinearSegmentedColormap.from_list('odv',colors)    #定义odv的colorbar
   #extra arguments are N=256, gamma=1.0
    cm.register_cmap(cmap=cmap2)

    plt.contourf(lon,lat,image_plt, 17, cmap='odv')  #odv Grey 
   #plt.contour(lon,lat,image_plt,10,colors='k')
    
       
def contourf_area (image,lon1,lon2,lat1,lat2,colorbar): #odv colorbar
    colors = ['#d0bfb1','#d5c9bc','#d8cfc3','#d5d2c6',
          '#cad3ca','#bad3cf','#afd2d4','#a4cfda',
          '#a1c6e0','#9ab9e2','#8face7','#82a1ec',
          '#8397f0','#8891f2','#8c89f4','#9485f3','#9881f3'] #odv colorbar
    #colors = ['#FFFFFF','#FFFFFF'] #纯白colorbar
    cmap2 = col.LinearSegmentedColormap.from_list('odv',colors)    #定义odv的colorbar
    #extra arguments are N=256, gamma=1.0
    cm.register_cmap(cmap=cmap2)
    a = (image.shape[1]-1)/2
    b = (image.shape[0]-1)/2
    c = a/180
    x1 = np.int(np.round( lon1 *c + a,decimals=0))
    x2 = np.int(np.round( lon2 *c + a,decimals=0))
    y1 = np.int(np.round( lat1 *c + b,decimals=0))
    y2 = np.int(np.round( lat2 *c + b,decimals=0))
    image_plt =  - image[y1:y2,x1:x2]
    lon = np.linspace(lon1,lon2,num=x2-x1)
    lat = np.linspace(lat1,lat2,num=y2-y1)
    lon_num,lat_num = 6 , 6
    lon_name = lon_tran(lon1,lon2,lon_num)
    lat_name = lat_tran(lat1,lat2,lat_num)
    plt.xticks(np.linspace(lon1,lon2,num=lon_num),lon_name)
    plt.yticks(np.linspace(lat1,lat2,num=lat_num),lat_name)

    for i in range(y2-y1):
        for j in range(x2-x1):
            if image_plt[i,j] > 0:
                image_plt[i,j] = quadratic(image_plt[i,j])
            else:
                continue
    image_plt = np.ma.array(image_plt, mask=image_plt < 0)  #加mask
    plt.gca().patch.set_color('.5')  #设定mask颜色

    norm = mpl.colors.Normalize(vmin=0, vmax=17)
    plt.contourf(lon,lat,image_plt, 17, cmap='odv',norm=norm)  #odv Grey
    
    if colorbar == 1:
        cb = plt.colorbar()
        cb.set_ticklabels(['0 m','100 m','500 m','1000 m','1500 m',\
                           '2500 m','3500 m','4500 m','5500 m']) 

def lat_tran(lat_bottom,lat_top,n):
    lat = np.linspace(lat_bottom,lat_top,num=n,endpoint=True)
    lat_name = []
    for i in range(len(lat)):
        if lat[i] < 0:
            lat_name.append(str(np.abs(lat[i])) +'°S')
        else:
            lat_name.append(str(np.abs(lat[i])) +'°N')
    return lat_name

def lon_tran(lon_left,lon_right,n):
    lon = np.linspace(lon_left,lon_right,num=n,endpoint=True)
    lon_name = []
    for i in range(len(lon)):
        if lon[i] < 0:
            lon_name.append(str(np.abs(lon[i])) + '°W')
        else :
            lon_name.append(str(np.abs(lon[i])) + '°E')
    return lon_name

def float2per(value):
    value_per = []
    for i in range(len(value)):
        per = str(np.round(value[i]*100,2))
        value_per.append(per + '%')
    return value_per

def file_name(file_dir,file_postfix):   
    L=[]   
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            if os.path.splitext(file)[1] == file_postfix:  
                L.append(os.path.join(root, file)) 
    return L
                
def to_mask(array,fill_value):
    array = np.squeeze(array)
    return np.ma.array(array, mask=array ==fill_value)

def getChar(number):
    factor, moder = divmod(number, 26) # 26 字母个数
    modChar = chr(moder + 97)          # 65 -> 'A' 97 ->'a'
    if factor != 0:
        modChar = getChar(factor-1) + modChar 
        # factor - 1 : 商为有效值时起始数为 1 而余数是 0
    return modChar

def lon_180_360(x):
    y = np.zeros_like(x)
    for i in range(len(x)):
        if x[i]>180:
            y[i] = -(360 - x[i])
        else:
            y[i] = x[i]
    return y

def read_nc_data(file_name,lon_lat_var_name,area):      
    nc = ne.Dataset(file_name)
    print('经纬度范围为',area)
    print('经度数据从小到大  纬度数据从大到小 value[lat,lon]')
    lon_pre,lat_pre,value_pre = nc.variables[lon_lat_var_name[0]][:],\
                                nc.variables[lon_lat_var_name[1]][:],\
                                nc.variables[lon_lat_var_name[2]][:]
    #数据清洗
    if value_pre.shape[0] != lat_pre.shape[0]:
        value_pre_lonlat = np.rollaxis(value_pre,axis=1)
    elif value_pre.shape[0] == lat_pre.shape[0]:
        value_pre_lonlat = np.rollaxis(value_pre,axis=0)#不变
    else:
        print('读取nc数据意料之外的错误')
    if lon_pre[0] - lon_pre[-1] > 0:
        lon_pre = lon_pre[::-1]
        value_pre_lonlat = value_pre_lonlat[::-1,:]
    if lat_pre[0] - lat_pre[-1] < 0:
        lat_pre = lat_pre[::-1]
        value_pre_lonlat = value_pre_lonlat[:,::-1]
    #数据聚焦    
    X1 = int(np.where(lon_pre < area[0])[0][-1]) #-61
    X2 = int(np.where(lon_pre > area[1])[0][0]) #-44
    Y1 = int(np.where(lat_pre < area[2])[0][0])#-64
    Y2 = int(np.where(lat_pre > area[3])[0][-1])#-59
    
    lon,lat = np.meshgrid(lon_pre[X1:X2],lat_pre[Y2:Y1])
    value = value_pre_lonlat[Y2:Y1,X1:X2]
    return lon,lat,value      