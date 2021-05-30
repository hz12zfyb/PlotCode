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

def stack_hist(df,stationnames,tchla_max,columns,indexs,time):
    for i in range(indexs):
        for j in range(columns):
            ax = plt.subplot(gs[i,j])
            d = columns * i + j
            depth = df.loc[stationnames[d],'depth']  
            value = df.loc[stationnames[d],:].T.values 
            v1=np.sum(value[[1,2,3,4,5,6,7],:],axis=0) 
            v2=np.sum(value[[1,2,3,4,5,6],:],axis=0) 
            v3=np.sum(value[[1,2,3,4,5],:],axis=0)
            v4=np.sum(value[[1,2,3,4],:],axis=0)
            v5=np.sum(value[[1,2,3],:],axis=0) 
            v6=np.sum(value[[1,2],:],axis=0)
            v7=np.sum(value[[1],:],axis=0)
        
            ax.barh(depth,v1,color="#009e74",height=8)
            ax.barh(depth,v2,color="#f0e442",height=8)
            ax.barh(depth,v3,color="#55b5e9",height=8)
            ax.barh(depth,v4,color="#0071b2",height=8)
            ax.barh(depth,v5,color="#cc7aa7",height=8)
            ax.barh(depth,v6,color="#d55c00",height=8)
            ax.barh(depth,v7,color="#5c00d5",height=8)

            #加字 
            font={'size':12,'weight':'normal'}
            text = 'Station : ' + stationnames[d] +'\nMLD : ' +\
                    str(mld[stationnames[d]]) +' m\nIce free days : '+\
                    str(time[j])+' days'
            ax.text(1.5,200,text,fontdict=font)
            s = getChar(d)
            ax.text(2.7,15,s,fontdict=font)
            
            if j != 0:
                ax.set_yticks(())
            else:
                ax.set_yticks((0,25,50,75,100,200))
                ax.set_ylabel('Depth/m ',fontdict=font)
            
            ax.set_xticks((0.0,1.0,2.0,3.0))                
            ax.xaxis.set_ticks_position('top')
            ax.set_ylim((-10,210))
            ax.set_xlim((0,tchla_max))
            ax.invert_yaxis()   #Y轴反向 
            ax.spines['right'].set_color('none')
            ax.spines['bottom'].set_color('none')
   
            if i== 0 and j == 1:
                ax.text(0.6,5,'Chlorophyll a/mg·$\mathregular{m^{-3}}$',fontdict=font)
                ax.legend(['P. antarctica (low Fe)','P. antarctica (high Fe)','Dinoflagellate','Diatoms-B',
                       'Diatoms-A','Cryptophytes','Chlorophytes'],
                            ncol=1,framealpha=0.3,
                            fontsize=12,loc='right')  #设置图例  upper center  
            
            #画密度分布图 8。14不能再subplot里嵌套小图 8。15twiny
#            ax1 = ax.twiny()
#            series = df_density[stationnames[d]]
#            ax1.plot(np.array(series), series.index, 'k')
#            ax1.set_xlim(26.9,27.8)
#            if i != 0:
#                ax1.set_xticks(())
#            else:
#                ax1.set_xticks((27.1,27.6))
#                ax1.set_xlabel('Density/Kg·$\mathregular{m^{-3}}$',fontdict=font)
#            ax1.set_ylabel('y')
            #画营养盐分布图
            ax1 = plt.subplot(gs[i+1,j])#ax.twiny()
            nutrition_depth = df_nutrition.loc[stationnames[d],'Depth [m]']
            n_value = df_nutrition.loc[stationnames[d],'NO3 [μmol/L]']
            p_value = df_nutrition.loc[stationnames[d],'PO4 [μmol/L]']
            si_value = df_nutrition.loc[stationnames[d],'Si [μmol/L]']
            
            ax1.plot(n_value,nutrition_depth, 'r.-')
#            ax1.plot(p_value,nutrition_depth, 'y.-')
            ax1.plot(si_value,nutrition_depth, 'b.-')
            ax1.set_xlim(0,80)
            ax1.invert_yaxis()
            ax1.xaxis.set_ticks_position('top')
#            ax1.spines['right'].set_color('none')
#            ax1.spines['bottom'].set_color('none')
            ax1.text(72,25,getChar(d+3),fontdict=font)
            if j != 0:
                ax1.set_yticks(())
            else:
                ax1.set_yticks((0,25,50,75,100,200))
                ax1.set_ylabel('Depth / m',fontdict=font)
            ax2 = ax1.twiny()
            ax2.plot(p_value,nutrition_depth, 'y.-')
            ax2.set_xlim(0,5)
            if i== 0 and j == 1:
                ax1.set_xlabel('Nutrition concentration/μmol·$\mathregular{L^{-1}}$',fontdict=font)
            if i== 0 and j == 2:
                ax1.legend(['Nitrate','Silicate'],
                            ncol=1,framealpha=0.3,
                            fontsize=12,loc='lower right')
                ax2.legend(['Phosphate'],
                            ncol=1,framealpha=0.3,
                            fontsize=12,loc='upper right') 
                   
plt.rcParams['font.sans-serif'] = ['Times New Roman']  
df_chemtax = pd.read_excel('D:/Refresh/data/CHINARE-35/CHEMTAX结果/4.23-wright2010.xlsx',
                           sheet_name='Sheet1').set_index('Sample')
#df_density = pd.read_excel('D:/Refresh/py36/色素数据处理/站位200米内密度变化.xlsx',
#                           sheet_name='Sheet1')
df_mld = pd.read_excel('D:/Refresh/data/CHINARE-35/水柱积分藻种数据.xlsx',
                           sheet_name='Sheet1').set_index('Station')
df_nutrition = pd.read_excel('D:/Refresh/data/CHINARE-35/data_all.xlsx',
                           sheet_name='Sheet1').set_index('Station')
mld = df_mld['MLD/m']
stationnames = ['A9-08','A8-08','A7-10']
df = df_chemtax.loc[stationnames]
old_indexs,stationnames = list(df.index),[]
for index in old_indexs:
    if index not in stationnames:
        stationnames.append(index)
#    stationnames = list(set(df.index)) #不会保留原始顺序
columns,indexs = 3,1
plt.rcParams['figure.figsize'] = (12,8)
plt.subplots_adjust(wspace=0.05,hspace=0.05)
gs = gridspec.GridSpec(indexs+1,columns)
df_tchla =df['Chloro']+df['Crypto']+df['Diat1']+\
    df['Diat2']+df[ 'Dino1']+df['Hapt6HiFe']+df['Hapt6LoFe']
tchla_max = np.max(df_tchla)
time = ['4','20','76']
stack_hist(df,stationnames,tchla_max,columns,indexs,time) 
fig_name = 'D:/Refresh/data/CHINARE-35/pic/CHEMTAX藻种分布/三个典型站位-english.png' 
plt.savefig(fig_name,bbox_inches='tight',dpi=1000,pad_inches=0.3)

plt.show()     