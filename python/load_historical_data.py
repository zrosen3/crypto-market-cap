#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file loads in historical return data which I will use to model stock performance over time. The source for the historical stock performance data
comes from. This dataset was compiled by the NYU stern school of business and can be downloaded here: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html.

"""
#load necessary libraries 
import pandas as pd
import os

#read in data
df = pd.read_excel(r'../data/Input/histretSP.xls', sheet_name='Returns by year', header = 17, nrows = 94)

#modify column names
df.columns = df.columns.str.replace('\&| ', '_', regex = True)
df.columns = df.columns.str.replace('\(|\)|\.', '', regex = True)
df.columns = df.columns.str.replace('_', '_', regex = True)
df.columns = df.columns.str.replace('\!', '1', regex = True)
df.columns = df.columns.str.replace('[0-9]$', '', regex = True)
df.columns = df.columns.str.replace('\-month', '_month', regex = True)
df.columns = df.columns.str.replace('\-year', '_year', regex = True)
df.columns = df.columns.str.replace("_\-_", "-", regex = True)
df.columns = df.columns.str.replace("T_Bill_Real", "tbill", regex= True)
df.columns.values[1:6] = "annual_returns_" + df.columns.values[1:6]
df.columns.values[6:11] = "value_100_invested_1928_" + df.columns.values[6:11]
df.columns.values[11:15] = "annual_risk_premium_" + df.columns.values[11:15]
df.columns.values[16:] = "annual_real_returns_" + df.columns.values[16:]
df.columns = df.columns.str.replace('_+', '_', regex = True)
df = df.rename(columns=str.lower)
df.columns = df.columns.str.replace("10_year_tbonds", "us_t_bond", regex = True)
df.columns = df.columns.str.replace("baa_corp_bonds", "baa_corporate_bond", regex = True)
df = df.append({"year":2022}, ignore_index = True)

#investigate data frame properties
print(df.columns)
print(df.shape)
print(df.dtypes) #confirm that all data types are numeric
print(df.isnull().sum()) #all missing data are in the historical risk premium column,

#export processed data
df.to_excel(r'../data/Output/Returns dataset.xlsx', sheet_name = "r.data", index = False)





