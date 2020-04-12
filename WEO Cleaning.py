# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:52:33 2020

@author: 12607
"""

import pandas as pd
from functools import reduce
this_is_the_path = "C:\\Users\\12607\\Desktop\\WEO.csv"
data = pd.read_csv(this_is_the_path)

data.drop(["Subject Descriptor","WEO Country Code", "ISO", "Subject Notes", "Country/Series-specific Notes", "Units", "Scale", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024" , "Estimates Start After"],axis=1, inplace=True)

data2 = pd.melt(data, id_vars=["WEO Subject Code", "Country"], 
                  var_name="Year", value_name="Value")

data2.rename(columns = {'WEO Subject Code':'WEO_SC'}, inplace = True)

data2 = data2[["Year", "Country", "Value", "WEO_SC", ]]

data3 = data2.replace(to_replace ="Vietnam", value ="Viet Nam")
data3 = data2.replace(to_replace ="Venezuela", value ="Venezuela, Bolivarian Republic of")
data3 = data2.replace(to_replace ="Tanzania", value ="Tanzania, United Republic of")
data3 = data2.replace(to_replace ="Taiwan Province of China", value ="Taiwan, Province of China")
data3 = data2.replace(to_replace ="Syria", value ="Syrian Arab Republic")
data3 = data2.replace(to_replace ="Slovak Republic", value ="Slovakia")
data3 = data2.replace(to_replace ="São Tomé and Príncipe", value ="Sao Tome and Principe")
data3 = data2.replace(to_replace ="Russia", value ="Russian Federation")
data3 = data2.replace(to_replace ="Moldova", value ="Moldova, Republic of")
data3 = data2.replace(to_replace ="Micronesia", value ="Micronesia, Federated States of")
data3 = data2.replace(to_replace ="Macao SAR", value ="Macao")
data3 = data2.replace(to_replace ="Lao P.D.R.", value ="Lao People's Democratic Republic")
data3 = data2.replace(to_replace ="Kyrgyz Republic", value ="Kyrgyzstan")
data3 = data2.replace(to_replace ="Korea", value ="Micronesia, Federated States of")
data3 = data2.replace(to_replace ="Islamic Republic of Iran", value ="Iran, Islamic Republic of")
data3 = data2.replace(to_replace ="Hong Kong SAR", value ="Hong Kong")
data3 = data2.replace(to_replace ="Democratic Republic of the Congo", value ="Congo")
data3 = data2.replace(to_replace ="Czech Republic", value ="Czechia")
data3 = data2.replace(to_replace ="Bolivia", value ="Bolivia, Plurinational State of")

print(data3)

NGDP_R = data3[data3.WEO_SC == 'NGDP_R']
NGDP_R.drop(["WEO_SC"],axis=1, inplace=True)
NGDP_R.rename(columns = {'Value':'NGDP_R'}, inplace = True)


NGDP_RPCH = data3[data3.WEO_SC == 'NGDP_RPCH']
NGDP_RPCH.drop(["WEO_SC"],axis=1, inplace=True)
NGDP_RPCH.rename(columns = {'Value':'NGDP_RPCH'}, inplace = True)

PPPEX = data3[data3.WEO_SC == 'PPPEX']
PPPEX.drop(["WEO_SC"],axis=1, inplace=True)
PPPEX.rename(columns = {'Value':'PPPEX'}, inplace = True)

PPPSH = data3[data3.WEO_SC == 'PPPSH']
PPPSH.drop(["WEO_SC"],axis=1, inplace=True)
PPPSH.rename(columns = {'Value':'PPPSH'}, inplace = True)

FLIBOR6 = data3[data3.WEO_SC == 'FLIBOR6']
FLIBOR6.drop(["WEO_SC"],axis=1, inplace=True)
FLIBOR6.rename(columns = {'Value':'FLIBOR6'}, inplace = True)

TM_RPCH = data3[data3.WEO_SC == 'TM_RPCH']
TM_RPCH.drop(["WEO_SC"],axis=1, inplace=True)
TM_RPCH.rename(columns = {'Value':'TM_RPCH'}, inplace = True)

TX_RPCH = data3[data3.WEO_SC == 'TX_RPCH']
TX_RPCH.drop(["WEO_SC"],axis=1, inplace=True)
TX_RPCH.rename(columns = {'Value':'TX_RPCH'}, inplace = True)

LUR = data3[data3.WEO_SC == 'LUR']
LUR.drop(["WEO_SC"],axis=1, inplace=True)
LUR.rename(columns = {'Value':'LUR'}, inplace = True)

LE = data3[data3.WEO_SC == 'LE']
LE.drop(["WEO_SC"],axis=1, inplace=True)
LE.rename(columns = {'Value':'LE'}, inplace = True)

LP = data3[data3.WEO_SC == 'LP']
LP.drop(["WEO_SC"],axis=1, inplace=True)
LP.rename(columns = {'Value':'LP'}, inplace = True)

GGXONLB_NGDP = data3[data3.WEO_SC == 'GGXONLB_NGDP']
GGXONLB_NGDP.drop(["WEO_SC"],axis=1, inplace=True)
GGXONLB_NGDP.rename(columns = {'Value':'GGXONLB_NGDP'}, inplace = True)

NGDP_FY = data3[data3.WEO_SC == 'NGDP_FY']
NGDP_FY.drop(["WEO_SC"],axis=1, inplace=True)
NGDP_FY.rename(columns = {'Value':'NGDP_FY'}, inplace = True)

data_frames = [NGDP_R, NGDP_RPCH, PPPEX, PPPSH, FLIBOR6, TM_RPCH, TX_RPCH, LUR, LE, LP, GGXONLB_NGDP, NGDP_FY ]

weo_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Country', 'Year'],
                                            how='outer'), data_frames)

weo_merged.to_csv('weo_merged.csv', index = False)