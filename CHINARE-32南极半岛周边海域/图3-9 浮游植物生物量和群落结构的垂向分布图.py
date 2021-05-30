# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 22:32:48 2019

@author: Administrator
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

def getChar(number):
    factor, moder = divmod(number, 26) # 26 字母个数
    modChar = chr(moder + 97)          # 65 -> 'A' 97 ->'a'
    if factor != 0:
        modChar = getChar(factor-1) + modChar # factor - 1 : 商为有效值时起始数为 1 而余数是 0
    return modChar

def stack_hist(df,stationnames,tchla_max,columns,indexs,df_density,area):
    for i in range(indexs):
        for j in range(columns):
            ax = plt.subplot(gs[i,j])
            d = columns * i + j
            depth = df.loc[stationnames[d],'depth']  
            value = df.loc[stationnames[d],:].T.values 
            v1=np.sum(value[[1,2,3,4,5,6],:],axis=0) 
            v2=np.sum(value[[1,2,3,4,5],:],axis=0)
            v3=np.sum(value[[1,2,3,4],:],axis=0)
            v4=np.sum(value[[1,2,3],:],axis=0) 
            v5=np.sum(value[[1,2],:],axis=0)
            v6=np.sum(value[[1],:],axis=0)
        
            ax.barh(depth,v1,color="#009e74",height=8)
            ax.barh(depth,v2,color="#f0e442",height=8)
            ax.barh(depth,v3,color="#55b5e9",height=8)
            ax.barh(depth,v4,color="#0071b2",height=8)
            ax.barh(depth,v5,color="#cc7aa7",height=8)
            ax.barh(depth,v6,color="#d55c00",height=8)

            #加字 
            font={'size':12,'weight':'normal'}
            text = 'Station : ' + stationnames[d]+'\nRegion : '+area[j]+'\nMLD : ' +\
                    str(mld[stationnames[d]]) +' m'
            ax.text(0.02,180,text,fontdict=font)
            s = getChar(d)
            ax.text(0.63,23,s,fontdict=font)
            if j != 0:
                ax.set_yticks(())
            else:
                ax.set_yticks((0,25,50,100,200))
                ax.set_ylabel('Depth/m',fontdict=font)
            if i != 1:
                ax.set_xticks(())
            else:
                ax.set_xticks((0.0,0.2,0.4,0.6))
                ax.set_xlabel('Chlorophyll a/mg·$\mathregular{m^{-3}}$',fontdict=font)

            ax.set_ylim((-10,210))
            ax.set_xlim((0,tchla_max))
            ax.invert_yaxis()   #Y轴反向 
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
    #        ax.xaxis.set_ticks_position('top')
            if i== 0 and j == 2:
                ax.legend(['Greenflagellates','Cryptophytes','P. antarctica',
                       'Cyanobacteria','Dinoflagellates','Diatoms'],
                            ncol=1,framealpha=0.3,
                            fontsize=6,loc='lower right')  #设置图例    
            
            #画密度分布图 8。14不能再subplot里嵌套小图 8。15twiny
            ax1 = ax.twiny()
            series = df_density[stationnames[d]]
            ax1.plot(np.array(series), series.index, 'k')
            ax1.set_xlim(26.9,27.8)
            if i != 0:
                ax1.set_xticks(())
            else:
                ax1.set_xticks((27.1,27.6))
                ax1.set_xlabel('Density/Kg·$\mathregular{m^{-3}}$',fontdict=font)
#            ax1.set_ylabel('y')
            


df_chemtax = pd.read_excel('D:/Refresh/data/CHINARE-32/CHEMTAX结果/6.29.xlsx',
                           sheet_name='Sheet1').set_index('Sample')
df_density = pd.read_excel('D:/Refresh/py36/色素数据处理/站位200米内密度变化.xlsx',
                           sheet_name='Sheet1')
df_mld = pd.read_excel('D:/Refresh/data/CHINARE-32/水柱积分藻种数据.xlsx',
                           sheet_name='Sheet2全').set_index('station')
mld = df_mld['MLD/m']
stationnames = ['D1-10','D3-03','D5-06',
                     'D2-06','D3-05','D6-03']
df = df_chemtax.loc[stationnames]
old_indexs,stationnames = list(df.index),[]
for index in old_indexs:
    if index not in stationnames:
        stationnames.append(index)
#    stationnames = list(set(df.index)) #不会保留原始顺序
columns,indexs = 3,2
plt.rcParams['figure.figsize'] = (9,6)
plt.subplots_adjust(wspace=0.05,hspace=0.05)
gs = gridspec.GridSpec(indexs,columns)
df_tchla =df['Diatoms']+df[ 'Dinoflagellates-1']+df['Cyanobacteria']+\
    df['Phaeocystisantarctica']+df[ 'Cryptophytes']+df['Greenflagellates']
tchla_max = np.max(df_tchla)
area=['Ⅰ','Ⅱ','Ⅲ']
stack_hist(df,stationnames,tchla_max,columns,indexs,df_density,area) 
fig_name = 'D:/Refresh/data/CHINARE-32/pic/CHEMTAX藻种分布/文章用/Region123.png' 
plt.savefig(fig_name,bbox_inches='tight',dpi=1000,pad_inches=0.1)

plt.show()     