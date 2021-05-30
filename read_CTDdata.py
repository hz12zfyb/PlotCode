# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 19:36:46 2019

@author: Administrator
"""

import os 
import numpy as np
from itertools import islice 
import chardet 
import time
import pandas as pd

def get_stationname(file_dir):
    stationnames =[]
    for files in os.walk(file_dir):
        print('')           
    for i in range(len(files[2])):
        file = files[2][i][:-4]
        stationnames.append(file)
    return stationnames

def get_stationname2(file_dir):
    stationnames =[]
    for files in os.walk(file_dir):
        print('')           
    for i in range(len(files[2])):
        file = files[2][i][:-4]
        stationnames.append(file)
    return stationnames

def get_data(file_dir): #全水深
    stationnames = []
    data_sum = []
    nico = 9
    #参数数量32次为20 33次为43 34次为47 35次为22 36次为9 362次为43
    dropline = 331
    #32次为341 33，34，362次为0 35次为345 36次为331
    for files in os.walk(file_dir):
        print('')
    for i in range(len(files[2])):
        file = files[2][i][:-4]
        stationnames.append(file)   
    for i in range(len(stationnames)):
        file_name = file_dir + files[2][i]
        encoding_way=chardet.detect(open(file_name,mode='rb').read())   #'encoding': 'ISO-8859-1'
        f = open(file_name,'r+',encoding=encoding_way['encoding'])
        counts = len(f.readlines()) - dropline
        count = 0
        data = np.zeros(shape=(counts,nico))
        for line in islice(open(file_name,'r+',encoding = encoding_way['encoding']),dropline,None):
            seris = list(filter(None, line.split(' ')))#32次分隔为' '，36次为','' '，362次为'\t'
            if len(seris) == nico:
                for j in range(nico):
                    if j in [13,14] and float(seris[j]) < 0:
                        data[count,j] = data[count-1,j]
                    elif j == 9 and float(seris[j] )< 0.000001:
                        data[count,j] = data[count-1,j]
                    else:
                        data[count,j] = seris[j]
                count += 1
        data_sum.append(data[:count,:])    
    return data_sum

def get_data_mvp(file_dir): #36次全水深MVP
    stationnames = []
    data = 0
    data_sum = []
    nico = 13
    #参数数量 36次为13
    dropline = 63
    #36次为63
    for files in os.walk(file_dir):
        print('') 
    for i in range(len(files[2])):
        file = files[2][i][:-4]
        stationnames.append(file)   
    for i in range(len(stationnames)):
        file_name = file_dir + files[2][i]
        encoding_way=chardet.detect(open(file_name,mode='rb').read())   #'encoding': 'ISO-8859-1'
        f = open(file_name,'r+',encoding=encoding_way['encoding'])
        counts = len(f.readlines()) - dropline
        count = 0
        data = np.zeros(shape=(counts,nico))
        for line in islice(open(file_name,'r+',encoding = encoding_way['encoding']),dropline,None):
            seris = list(filter(None, line.split(',')))
            for j in range(nico):
                data[count,j] = seris[j]
            count += 1

        df = pd.DataFrame(data)
        df['depth'] = np.round(df[1],0)
#        df.groupby(by='depth')
        df.sort_values('depth')
        df[1] = df['depth']
        data_sum.append(np.array(df.groupby(by='depth').mean()))   
        
    return data_sum

def get_data2(file_dir): #32次采水层 
    dropline = 263
    stationnames = []
    data = 0
    data_sum = []
    for files in os.walk(file_dir):
        print('') 
    for i in range(len(files[2])):
        file = files[2][i][:-4]
        stationnames.append(file)   
    for i in range(len(stationnames)):
        file_name = file_dir + files[2][i]
        encoding_way=chardet.detect(open(file_name,mode='rb').read())   #'encoding': 'ISO-8859-1'
        f = open(file_name,'r+',encoding=encoding_way['encoding'])
        counts =int((len(f.readlines()) - dropline)/2)
        count = 0
        data = np.zeros(shape=(counts,2)) #32次
        for line in islice(open(file_name,'r+',encoding = encoding_way['encoding']),dropline,None):
            seris = list(filter(None, line.split(' ')))
            print(seris)
            if len(seris) == 15: 
                for j in range(10):
                    data[count,j] = seris[j+4]
                count += 1
            else:
                continue
        data_sum.append(data)
    return data_sum
    
def get_data36(file_dir): #36次采水层
    dropline = 268
    stationnames = []
    data = 0
    data_sum = []
    for files in os.walk(file_dir):
        print('') 
    for i in range(len(files[2])):
        file = files[2][i][0:-4]
        stationnames.append(file)   
    for i in range(len(stationnames)):
        file_name = file_dir + files[2][i]
        encoding_way=chardet.detect(open(file_name,mode='rb').read())   #'encoding': 'ISO-8859-1'
        f = open(file_name,'r+',encoding=encoding_way['encoding'])
        counts =int((len(f.readlines()) - dropline)/2)
        count = 0
        data = np.zeros(shape=(counts,3)) #只要温盐深
        for line in islice(open(file_name,'r+',encoding = encoding_way['encoding']),dropline,None):
            seris = list(filter(None, line.split(' ')))
            if len(seris) == 13: 
                data[count] = seris[7:10]
                count += 1
            else:
                continue
        data_sum.append(data)
    return data_sum



#start = time.time()
#stationnames = get_stationname()
#data_sum = get_data(341)
#end = time.time()
#print (end-start)

