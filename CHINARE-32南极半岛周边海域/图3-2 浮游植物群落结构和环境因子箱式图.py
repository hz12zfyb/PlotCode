# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:55:43 2019

@author: Administrator
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os,sys
sys.path.append('D:/Refresh/py36')
import support_pie
import numpy as np


#设定调色盘
color = ['#d55c00', '#cc7aa7', '#0071b2', '#55b5e9',
         '#f0e442', '#009e74'] #藻种colorbar
#color = ['#0071b2','#d55c00','#cc7aa7'] #label colorbar
sns.set_palette( color )
plt.subplots_adjust(wspace=0.45,hspace=0.27)
plt.rcParams['figure.figsize'] = (9,12)

def getChar(number):
    factor, moder = divmod(number, 26) # 26 字母个数
    modChar = chr(moder + 97)          # 65 -> 'A' 97 ->'a'
    if factor != 0:
        modChar = getChar(factor-1) + modChar # factor - 1 : 商为有效值时起始数为 1 而余数是 0
    return modChar

#读取数据
df = pd.read_excel('D:/Refresh/data/CHINARE-32/水柱积分藻种数据.xlsx',
                   sheet_name='Sheet2全').set_index('station')

#new 12
parameters=['Diatoms','P.antarctica', 'Green flagellates',
            'PAR/E·$\mathregular{m^{-2}}$·$\mathregular{day^{-1}}$',
            'MLD/m','Zeu/m',
            'Temperature/℃', 'Salinity/psu',
            'Chlorophyll a/mg $\mathregular{m^{-3}}$',
            'Nitrate/μmol·$\mathregular{L^{-1}}$',
            'Phosphate /μmol·$\mathregular{L^{-1}}$',
            'Silicate/μmol·$\mathregular{L^{-1}}$'
            ]
for i in range(12):
    plt.subplot(4,3,i+1)    
    sns.boxplot( x='Region',
             y=parameters[i],
             data=df, 
             orient='v')
    ymin,ymax = plt.ylim()
    y_loc = 0.9*(ymax-ymin)+ymin
    s_range = getChar(i)
    plt.text(2.2,y_loc,s_range,fontsize=14)
    if i <=2:
#        plt.xticks(())
        yticks = np.array(plt.yticks()[0][1:])
        per_name = support_pie.float2per(yticks)
        plt.yticks(yticks,per_name)

fig_name ='D:/Refresh/data/CHINARE-32/pic/'+'分区域藻种和光和环境因子箱式图.png'
plt.savefig(fig_name,bbox_inches='tight',dpi=1000,pad_inches=0.1)