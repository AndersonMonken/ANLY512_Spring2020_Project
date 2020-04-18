#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 07:18:28 2020

@author: vidarithchan
"""

from datetime import datetime, date, time
import pandas_datareader as pdr
from pandas_datareader import wb
import pandas as pd
import pycountry


# import wb_data_raw

filepath = "/Users/vidarithchan/Desktop/MSAnalytics/ANALY 502/data.csv"

wb_data_raw = pd.read_csv(filepath)


# FIXING COUNTRY NAME
pycountries = [country.name for country in pycountry.countries]

# Seeing what countries I have in the wb_data_raw

WBcountries = sorted(list(set(wb_data_raw.country)))

Same = sorted(list(set(WBcountries).intersection(set(pycountries))))
WB_Only = sorted(list(set(WBcountries) - set(pycountries)))
Py_Only = sorted(list(set(pycountries) - set(WBcountries)))

comparisondf = pd.DataFrame({'Same': pd.Series(Same),
                             'Merged_Only': pd.Series(WB_Only),
                             'Py_Only': pd.Series(Py_Only)})

comparisondf.to_csv('comp_local.csv')


# Other country names need to be updated to match current official names

update_dic = {'Bahamas, The':'Bahamas','Bolivia':'Bolivia, Plurinational State of',
          'British Virgin Islands':'British Indian Ocean Territory',
          'Congo, Dem. Rep.':'Congo, The Democratic Republic of the',
          'Congo, Rep.':'Congo','Czech Republic':'Czechia','Egypt, Arab Rep.':'Egypt',
          'Gambia, The':'Gambia','Hong Kong SAR, China':'Hong Kong','Iran, Islamic Rep.':'Iran, Islamic Republic of',
          'Korea, Dem. People‚Äôs Rep.':"Korea, Democratic People's Republic of",
          'Korea, Rep.':'Korea, Republic of','Kyrgyz Republic':'Kyrgyzstan',
          'Lao PDR':"Lao People's Democratic Republic",'Macao SAR, China':'Macao',
          'Moldova':'Moldova, Republic of','Slovak Republic':'Slovakia',
          'Tanzania':'Tanzania, United Republic of','Venezuela, RB':'Venezuela, Bolivarian Republic of',
          'Vietnam':'Viet Nam','Virgin Islands (U.S.)':'Virgin Islands, U.S.','Yemen, Rep.':'Yemen'}


# Replace names with new names in dictionary:
wb_data_raw = wb_data_raw.replace({"country": update_dic})

# Find country names that are in the WB data but NOT in the pycountry module.
wb_countries_after_matching = set(sorted(list(set(wb_data_raw.country)))) - set(pycountries)

# Take out unmatched countries from the WB data.
wb_data_raw = wb_data_raw[~wb_data_raw.country.isin(wb_countries_after_matching)]

# 2019 data are mostly blank as of April 2020. Remove it.

	
# Get names of indexes for which column Age has value 30
indexNames = wb_data_raw[ wb_data_raw['year'] == 2019 ].index
 
# Delete these row indexes from dataFrame
wb_data_raw.drop(indexNames , inplace=True) 


# Rename column names.
wb_data_raw = wb_data_raw.rename(columns={'NY.GDP.PCAP.KD':'gdp_percap','NV.AGR.TOTL.ZS':'agripercent_gdp',
           'SL.AGR.EMPL.ZS':'agg_empl_agri_perc','SP.RUR.TOTL.ZS':'rural_pop_tot',
           'SP.POP.TOTL':'totalpop','IT.CEL.SETS.P2':'mobilesub_per100peeps',
           'NV.IND.MANF.KD.ZG':'manuf_added_percent_gdp','ST.INT.ARVL':'intl_tourist_arrival',
           'SP.DYN.LE00.IN':'total_life_exp','SP.DYN.LE00.FE.IN':'life_exp_fe',
           'SP.DYN.LE00.MA.IN':'life_exp_male'})

### CLEANING DATA

wb_data_raw.dtypes # finding data type for each column in the wb data. 

wb_data_raw.isnull().sum()

# replace missing values:

#wb_data_raw = wb_data_raw.fillna(wb_data_raw.mean()) 
    # one way to do it but it might not be right given the time series time frame but fine for now.

# All the life-expectancy variables: 
    
#wb_data_raw['total_life_exp'] = wb_data_raw['total_life_exp'].fillna(wb_data_raw['total_life_exp'].mean())
#
#wb_data_raw['life_exp_fe'] = wb_data_raw['total_life_fe'].fillna(wb_data_raw['total_life_fe'].mean())
#
#wb_data_raw['total_life_male'] = wb_data_raw['total_life_male'].fillna(wb_data_raw.groupby['total_life_male'].mean())

#wb_data_raw["total_life_exp"] = wb_data_raw.groupby("country").transform(lambda x: x.fillna(x.mean()))

wb_data_raw['total_life_exp'] = wb_data_raw['total_life_exp'].fillna(wb_data_raw.groupby('country')['total_life_exp'].transform('mean'))

wb_data_raw['life_exp_fe'] = wb_data_raw['life_exp_fe'].fillna(wb_data_raw.groupby('country')['life_exp_fe'].transform('mean'))

wb_data_raw['life_exp_male'] = wb_data_raw['life_exp_male'].fillna(wb_data_raw.groupby('country')['life_exp_male'].transform('mean'))

wb_data_raw['intl_tourist_arrival'] = wb_data_raw['intl_tourist_arrival'].fillna(wb_data_raw.groupby('country')['intl_tourist_arrival'].transform('mean'))

wb_data_raw['mobilesub_per100peeps'] = wb_data_raw['mobilesub_per100peeps'].fillna(wb_data_raw.groupby('country')['mobilesub_per100peeps'].transform('mean'))

wb_data_raw['totalpop'] = wb_data_raw['totalpop'].fillna(wb_data_raw.groupby('country')['totalpop'].transform('mean'))

wb_data_raw['rural_pop_tot'] = wb_data_raw['rural_pop_tot'].fillna(wb_data_raw.groupby('country')['rural_pop_tot'].transform('mean'))

wb_data_raw['agg_empl_agri_perc'] = wb_data_raw['agg_empl_agri_perc'].fillna(wb_data_raw.groupby('country')['agg_empl_agri_perc'].transform('mean'))

wb_data_raw['agripercent_gdp'] = wb_data_raw['agripercent_gdp'].fillna(wb_data_raw.groupby('country')['agripercent_gdp'].transform('mean'))

wb_data_raw['gdp_percap'] = wb_data_raw['gdp_percap'].fillna(wb_data_raw.groupby('country')['gdp_percap'].transform('mean'))


# There are still some missing values. That is because some of these countries do not have any values for any years. 
# Because these are country-specific cases, it is not right to fill in the mean. gdp_percap of the world is not for country X.
# I am going to remove all the missing values from the entire dataset. 

# Before I do that, I will need to drop two variables from the dataset. 

wb_data_raw.drop(["SL.TLF.CACT.ZS", "manuf_added_percent_gdp"], axis = 1, inplace = True) 

wb_data_final = wb_data_raw.dropna()

wb_data_final.isnull().sum()

# write data to the folder
wb_data_final.to_csv('worldbank_data_final.csv')



























































