# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 10:48:59 2020

@author: lthompson8
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 14:25:46 2020

@author: lthompson8
"""
#%% 1. Import packages
import numpy as np
import pandas as pd
import glob
import os
import zipfile
import re
import shutil
import csv
import matplotlib.pyplot as plt
#%% 2. Designate Working Directory 
os.getcwd()
#create parent directory
parentdirectory = 'C:\\Users\\lthompson8\\python2020summer\\FinalProject'
os.chdir(parentdirectory)
os.getcwd()

#%% 3. File download. Looks like I may have to use and API or token if I want to download directly from box.

#for now, will manually download to skip this issue, and proceed with zipped folder (assuming that I can get to this step with code in the future)
#url = "https://unl.app.box.com/folder/79735107810"

#%% 4. Concatenate into DF from zipped file and remove headers from each individual file.

###################USER INPUTS########################
zipfpath = 'C:\\Users\\lthompson8\\python2020summer\\FinalProject\\Rulo_5SW.zip' ##populate this field with your zip file location!!
startdate = '2020-01-01' #populate this with your chosen start date!!
enddate = '2020-07-06' #populate this with your chosen end date!!
######################################################


def openSoilByDate(zipfpath, startdate, enddate):
    '''
    open zip and read files within the range of the starting date and ending date
    preferable, controllable
    '''
    dfs = []
    with zipfile.ZipFile(zipfpath) as z:     #   z.infolist()
        filenames = [f.filename for f in z.infolist()]
        for d in pd.date_range(startdate, enddate, freq='D'):
            toOpen = 'Rulo_5SW/Rulo_5SW_soil_{:%Y%m%d}_0703.csv'.format(d)
            if toOpen in filenames:
                # check if the file exists in the zip
                with z.open(toOpen) as f:
                    dfs.append(pd.read_csv(f, header=0, skiprows=1).iloc[2:])
    return pd.concat(dfs).reset_index(drop=True)

soil = openSoilByDate(zipfpath, startdate, enddate)

def openAglByDate(zipfpath, startdate, enddate):
    '''
    open zip and read files within the range of the starting date and ending date
    preferable, controllable
    '''
    dfs = []
    with zipfile.ZipFile(zipfpath) as z:     #   z.infolist()
        filenames = [f.filename for f in z.infolist()]
        for d in pd.date_range(startdate, enddate, freq='D'):
            toOpen = 'Rulo_5SW/Rulo_5SW_agl_{:%Y%m%d}_0703.csv'.format(d)
            if toOpen in filenames:
                # check if the file exists in the zip
                with z.open(toOpen) as f:
                    dfs.append(pd.read_csv(f, header=0, skiprows=1).iloc[2:])
    return pd.concat(dfs).reset_index(drop=True)

agl = openAglByDate(zipfpath, startdate, enddate)

#this still gives me the error about dtypes but seems to work

# def openAllExisting(zipfpath):
#     '''
#     passively open all files. may open some files you don't want and make cleaning up more difficult
#     '''
    
#     soil2 = []
#     agl2 = []
#     with zipfile.ZipFile(zipfpath) as z:     #   
#         for f in z.infolist():
#             fname = f.filename
#             if fname.endswith('csv'):
#                 # check if it is a CSV file then open it
#                 with z.open(fname) as f:
#                     df = pd.read_csv(f, header=0, skiprows=1).iloc[2:]
#                 if 'soil' in fname:
#                     soil.append(df)
#                 if 'agl' in fname:
#                     agl.append(df)

#     return pd.concat(agl2).reset_index(drop=True), pd.concat(soil2).reset_index(drop=True)
# agl2, soil2 = openAllExisting('C:\\Users\\lthompson8\\python2020summer\\FinalProject\\Rulo_5SW.zip')
# print(agl2)
# print(soil2)

#%% 5. Convert dataframe dtypes to correct pandas types of datetime and numeric
soil.info()
soil['TIMESTAMP'] = pd.to_datetime(soil['TIMESTAMP'], errors='coerce')
soil['Ms_veg_5cm'] = pd.to_numeric(soil['Ms_veg_5cm'], errors='coerce')
soil['Ms_veg_10cm'] = pd.to_numeric(soil['Ms_veg_10cm'], errors='coerce')
soil['Ms_veg_20cm'] = pd.to_numeric(soil['Ms_veg_20cm'], errors='coerce')
soil['Ms_veg_50cm'] = pd.to_numeric(soil['Ms_veg_50cm'], errors='coerce')
soil['Ms_veg_100cm'] = pd.to_numeric(soil['Ms_veg_100cm'], errors='coerce')
soil['Ts_veg_5cm'] = pd.to_numeric(soil['Ts_veg_5cm'], errors='coerce')
soil['Ts_veg_10cm'] = pd.to_numeric(soil['Ts_veg_10cm'], errors='coerce')
soil['Ts_veg_20cm'] = pd.to_numeric(soil['Ts_veg_20cm'], errors='coerce')
soil['Ts_veg_50cm'] = pd.to_numeric(soil['Ts_veg_50cm'], errors='coerce')
soil['Ts_veg_100cm'] = pd.to_numeric(soil['Ts_veg_100cm'], errors='coerce')
soil['RECORD'] = pd.to_numeric(soil['RECORD'], errors='coerce')
soil.info()
#set the TIMESTAMP as index
soil = soil.set_index(['TIMESTAMP'])

#agl has many datetime columns. will convert all at once, but have it ignore ones that don't work (which will be time columns)
agl.info()
agl = agl.apply(pd.to_numeric, errors='ignore')
#now need to go and apply datetime to the time column that I care about.
agl['TIMESTAMP'] = pd.to_datetime(agl['TIMESTAMP'], errors='coerce')
agl.info()
#solar did not convert. Manually change this one and coerce for NAs
agl['Solar_2m_Avg'] = pd.to_numeric(agl['Solar_2m_Avg'], errors='coerce')
agl.info()
#rest of the date time columns could be changed to datetime too, but for now will leave as object as I don't think I will use them.
#set the TIMESTAMP as index
agl = agl.set_index(['TIMESTAMP'])

#%% 6. summarize stats
#from concatenated dataset, need to summarize stats by hour, day, month, year, etc.
#pick which to summarize

#for AGL data was recorded by minute. Will summarize key variables into hourly, daily, monthly, annual

#AGL Hourly Stats
AGLHourlyStats = pd.DataFrame(columns=['MinT','MaxT','MeanT','MinRH','MaxRH','MeanRH','AvgWindSpd','MaxGust','MinSolar','MaxSolar','MeanSolar','AvgSoilT','RainSum'])
AGLHourlyStats.MinT = agl.TaMin_2m.resample('H').min()
AGLHourlyStats.MaxT = agl.TaMax_2m.resample('H').max()
AGLHourlyStats.MeanT = agl.Ta_2m_Avg.resample('H').mean()
AGLHourlyStats.MinRH = agl.RHMin_2m.resample('H').min()
AGLHourlyStats.MaxRH = agl.RHMax_2m.resample('H').max()
AGLHourlyStats.MeanRH = agl.RH_2m_Avg.resample('H').mean()
AGLHourlyStats.AvgWindSpd = agl.WndAveSpd_3m.resample('H').mean()
AGLHourlyStats.MaxGust = agl.WndMaxSpd5s_3m.resample('H').max()
AGLHourlyStats.MinSolar = agl.Solar_2m_Avg.resample('H').min()
AGLHourlyStats.MaxSolar = agl.Solar_2m_Avg.resample('H').max()
AGLHourlyStats.MeanSolar = agl.Solar_2m_Avg.resample('H').mean()
AGLHourlyStats.AvgSoilT = agl.TsMax_bare_10cm.resample('H').mean()
AGLHourlyStats.RainSum = agl.Rain_1m_Tot.resample('H').sum()
print(AGLHourlyStats)

#AGL Daily Stats
AGLDailyStats = pd.DataFrame(columns=['MinT','MaxT','MeanT','MinRH','MaxRH','MeanRH','AvgWindSpd','MaxGust','MinSolar','MaxSolar','MeanSolar','AvgSoilT','RainSum'])
AGLDailyStats.MinT = agl.TaMin_2m.resample('D').min()
AGLDailyStats.MaxT = agl.TaMax_2m.resample('D').max()
AGLDailyStats.MeanT = agl.Ta_2m_Avg.resample('D').mean()
AGLDailyStats.MinRH = agl.RHMin_2m.resample('D').min()
AGLDailyStats.MaxRH = agl.RHMax_2m.resample('D').max()
AGLDailyStats.MeanRH = agl.RH_2m_Avg.resample('D').mean()
AGLDailyStats.AvgWindSpd = agl.WndAveSpd_3m.resample('D').mean()
AGLDailyStats.MaxGust = agl.WndMaxSpd5s_3m.resample('D').max()
AGLDailyStats.MinSolar = agl.Solar_2m_Avg.resample('D').min()
AGLDailyStats.MaxSolar = agl.Solar_2m_Avg.resample('D').max()
AGLDailyStats.MeanSolar = agl.Solar_2m_Avg.resample('D').mean()
AGLDailyStats.AvgSoilT = agl.TsMax_bare_10cm.resample('D').mean()
AGLDailyStats.RainSum = agl.Rain_1m_Tot.resample('D').sum()
print(AGLDailyStats)

#AGL Monthly Stats
AGLMonthlyStats = pd.DataFrame(columns=['MinT','MaxT','MeanT','MinRH','MaxRH','MeanRH','AvgWindSpd','MaxGust','MinSolar','MaxSolar','MeanSolar','AvgSoilT','RainSum'])
AGLMonthlyStats.MinT = agl.TaMin_2m.resample('M').min()
AGLMonthlyStats.MaxT = agl.TaMax_2m.resample('M').max()
AGLMonthlyStats.MeanT = agl.Ta_2m_Avg.resample('M').mean()
AGLMonthlyStats.MinRH = agl.RHMin_2m.resample('M').min()
AGLMonthlyStats.MaxRH = agl.RHMax_2m.resample('M').max()
AGLMonthlyStats.MeanRH = agl.RH_2m_Avg.resample('M').mean()
AGLMonthlyStats.AvgWindSpd = agl.WndAveSpd_3m.resample('M').mean()
AGLMonthlyStats.MaxGust = agl.WndMaxSpd5s_3m.resample('M').max()
AGLMonthlyStats.MinSolar = agl.Solar_2m_Avg.resample('M').min()
AGLMonthlyStats.MaxSolar = agl.Solar_2m_Avg.resample('M').max()
AGLMonthlyStats.MeanSolar = agl.Solar_2m_Avg.resample('M').mean()
AGLMonthlyStats.AvgSoilT = agl.TsMax_bare_10cm.resample('M').mean()
AGLMonthlyStats.RainSum = agl.Rain_1m_Tot.resample('M').sum()
print(AGLMonthlyStats)

#AGL Annual Stats
AGLAnnualStats = pd.DataFrame(columns=['MinT','MaxT','MeanT','MinRH','MaxRH','MeanRH','AvgWindSpd','MaxGust','MinSolar','MaxSolar','MeanSolar','AvgSoilT','RainSum'])
AGLAnnualStats.MinT = agl.TaMin_2m.resample('Y').min()
AGLAnnualStats.MaxT = agl.TaMax_2m.resample('Y').max()
AGLAnnualStats.MeanT = agl.Ta_2m_Avg.resample('Y').mean()
AGLAnnualStats.MinRH = agl.RHMin_2m.resample('Y').min()
AGLAnnualStats.MaxRH = agl.RHMax_2m.resample('Y').max()
AGLAnnualStats.MeanRH = agl.RH_2m_Avg.resample('Y').mean()
AGLAnnualStats.AvgWindSpd = agl.WndAveSpd_3m.resample('Y').mean()
AGLAnnualStats.MaxGust = agl.WndMaxSpd5s_3m.resample('Y').max()
AGLAnnualStats.MinSolar = agl.Solar_2m_Avg.resample('Y').min()
AGLAnnualStats.MaxSolar = agl.Solar_2m_Avg.resample('Y').max()
AGLAnnualStats.MeanSolar = agl.Solar_2m_Avg.resample('Y').mean()
AGLAnnualStats.AvgSoilT = agl.TsMax_bare_10cm.resample('Y').mean()
AGLAnnualStats.RainSum = agl.Rain_1m_Tot.resample('Y').sum()
print(AGLAnnualStats)

#Soil is moisture in hourly. Summarize into daily, monthly, and annual. #min, max, avg
#Soil Hourly Stats
SoilHourlyStats = pd.DataFrame(columns=['Avg_Ms_veg_5cm','Max_Ms_veg_5cm','Min_Ms_veg_5cm','Avg_Ms_veg_10cm','Max_Ms_veg_10cm','Min_Ms_veg_10cm','Avg_Ms_veg_20cm','Max_Ms_veg_20cm','Min_Ms_veg_20cm','Avg_Ms_veg_50cm','Max_Ms_veg_50cm','Min_Ms_veg_50cm','Avg_Ms_veg_100cm','Max_Ms_veg_100cm','Min_Ms_veg_100cm','Avg_Ts_veg_5cm','Max_Ts_veg_5cm','Min_Ts_veg_5cm','Avg_Ts_veg_10cm','Max_Ts_veg_10cm','Min_Ts_veg_10cm','Avg_Ts_veg_20cm','Max_Ts_veg_20cm','Min_Ts_veg_20cm','Avg_Ts_veg_50cm','Max_Ts_veg_50cm','Min_Ts_veg_50cm','Avg_Ts_veg_100cm','Max_Ts_veg_100cm','Min_Ts_veg_100cm'])
SoilHourlyStats.Avg_Ms_veg_5cm = soil.Ms_veg_5cm.resample('H').mean()
SoilHourlyStats.Max_Ms_veg_5cm = soil.Ms_veg_5cm.resample('H').max()
SoilHourlyStats.Min_Ms_veg_5cm = soil.Ms_veg_5cm.resample('H').min()
SoilHourlyStats.Avg_Ms_veg_10cm = soil.Ms_veg_10cm.resample('H').mean()
SoilHourlyStats.Max_Ms_veg_10cm = soil.Ms_veg_10cm.resample('H').max()
SoilHourlyStats.Min_Ms_veg_10cm = soil.Ms_veg_10cm.resample('H').min()
SoilHourlyStats.Avg_Ms_veg_20cm = soil.Ms_veg_20cm.resample('H').mean()
SoilHourlyStats.Max_Ms_veg_20cm = soil.Ms_veg_20cm.resample('H').max()
SoilHourlyStats.Min_Ms_veg_20cm = soil.Ms_veg_20cm.resample('H').min()
SoilHourlyStats.Avg_Ms_veg_50cm = soil.Ms_veg_50cm.resample('H').mean()
SoilHourlyStats.Max_Ms_veg_50cm = soil.Ms_veg_50cm.resample('H').max()
SoilHourlyStats.Min_Ms_veg_50cm = soil.Ms_veg_50cm.resample('H').min()
SoilHourlyStats.Avg_Ms_veg_100cm = soil.Ms_veg_100cm.resample('H').mean()
SoilHourlyStats.Max_Ms_veg_100cm = soil.Ms_veg_100cm.resample('H').max()
SoilHourlyStats.Min_Ms_veg_100cm = soil.Ms_veg_100cm.resample('H').min()
SoilHourlyStats.Avg_Ts_veg_5cm = soil.Ts_veg_5cm.resample('H').mean()
SoilHourlyStats.Max_Ts_veg_5cm = soil.Ts_veg_5cm.resample('H').max()
SoilHourlyStats.Min_Ts_veg_5cm = soil.Ts_veg_5cm.resample('H').min()
SoilHourlyStats.Avg_Ts_veg_10cm = soil.Ts_veg_10cm.resample('H').mean()
SoilHourlyStats.Max_Ts_veg_10cm = soil.Ts_veg_10cm.resample('H').max()
SoilHourlyStats.Min_Ts_veg_10cm = soil.Ts_veg_10cm.resample('H').min()
SoilHourlyStats.Avg_Ts_veg_20cm = soil.Ts_veg_20cm.resample('H').mean()
SoilHourlyStats.Max_Ts_veg_20cm = soil.Ts_veg_20cm.resample('H').max()
SoilHourlyStats.Min_Ts_veg_20cm = soil.Ts_veg_20cm.resample('H').min()
SoilHourlyStats.Avg_Ts_veg_50cm = soil.Ts_veg_50cm.resample('H').mean()
SoilHourlyStats.Max_Ts_veg_50cm = soil.Ts_veg_50cm.resample('H').max()
SoilHourlyStats.Min_Ts_veg_50cm = soil.Ts_veg_50cm.resample('H').min()
SoilHourlyStats.Avg_Ts_veg_100cm = soil.Ts_veg_100cm.resample('H').mean()
SoilHourlyStats.Max_Ts_veg_100cm = soil.Ts_veg_100cm.resample('H').max()
SoilHourlyStats.Min_Ts_veg_100cm = soil.Ts_veg_100cm.resample('H').min()
print(SoilHourlyStats)
# this may not make sense as giving max, min, and average should be the same as it was reported at this time scale originally.
#Soil Daily Stats
SoilDailyStats = pd.DataFrame(columns=['Avg_Ms_veg_5cm','Max_Ms_veg_5cm','Min_Ms_veg_5cm','Avg_Ms_veg_10cm','Max_Ms_veg_10cm','Min_Ms_veg_10cm','Avg_Ms_veg_20cm','Max_Ms_veg_20cm','Min_Ms_veg_20cm','Avg_Ms_veg_50cm','Max_Ms_veg_50cm','Min_Ms_veg_50cm','Avg_Ms_veg_100cm','Max_Ms_veg_100cm','Min_Ms_veg_100cm','Avg_Ts_veg_5cm','Max_Ts_veg_5cm','Min_Ts_veg_5cm','Avg_Ts_veg_10cm','Max_Ts_veg_10cm','Min_Ts_veg_10cm','Avg_Ts_veg_20cm','Max_Ts_veg_20cm','Min_Ts_veg_20cm','Avg_Ts_veg_50cm','Max_Ts_veg_50cm','Min_Ts_veg_50cm','Avg_Ts_veg_100cm','Max_Ts_veg_100cm','Min_Ts_veg_100cm'])
SoilDailyStats.Avg_Ms_veg_5cm = soil.Ms_veg_5cm.resample('D').mean()
SoilDailyStats.Max_Ms_veg_5cm = soil.Ms_veg_5cm.resample('D').max()
SoilDailyStats.Min_Ms_veg_5cm = soil.Ms_veg_5cm.resample('D').min()
SoilDailyStats.Avg_Ms_veg_10cm = soil.Ms_veg_10cm.resample('D').mean()
SoilDailyStats.Max_Ms_veg_10cm = soil.Ms_veg_10cm.resample('D').max()
SoilDailyStats.Min_Ms_veg_10cm = soil.Ms_veg_10cm.resample('D').min()
SoilDailyStats.Avg_Ms_veg_20cm = soil.Ms_veg_20cm.resample('D').mean()
SoilDailyStats.Max_Ms_veg_20cm = soil.Ms_veg_20cm.resample('D').max()
SoilDailyStats.Min_Ms_veg_20cm = soil.Ms_veg_20cm.resample('D').min()
SoilDailyStats.Avg_Ms_veg_50cm = soil.Ms_veg_50cm.resample('D').mean()
SoilDailyStats.Max_Ms_veg_50cm = soil.Ms_veg_50cm.resample('D').max()
SoilDailyStats.Min_Ms_veg_50cm = soil.Ms_veg_50cm.resample('D').min()
SoilDailyStats.Avg_Ms_veg_100cm = soil.Ms_veg_100cm.resample('D').mean()
SoilDailyStats.Max_Ms_veg_100cm = soil.Ms_veg_100cm.resample('D').max()
SoilDailyStats.Min_Ms_veg_100cm = soil.Ms_veg_100cm.resample('D').min()
SoilDailyStats.Avg_Ts_veg_5cm = soil.Ts_veg_5cm.resample('D').mean()
SoilDailyStats.Max_Ts_veg_5cm = soil.Ts_veg_5cm.resample('D').max()
SoilDailyStats.Min_Ts_veg_5cm = soil.Ts_veg_5cm.resample('D').min()
SoilDailyStats.Avg_Ts_veg_10cm = soil.Ts_veg_10cm.resample('D').mean()
SoilDailyStats.Max_Ts_veg_10cm = soil.Ts_veg_10cm.resample('D').max()
SoilDailyStats.Min_Ts_veg_10cm = soil.Ts_veg_10cm.resample('D').min()
SoilDailyStats.Avg_Ts_veg_20cm = soil.Ts_veg_20cm.resample('D').mean()
SoilDailyStats.Max_Ts_veg_20cm = soil.Ts_veg_20cm.resample('D').max()
SoilDailyStats.Min_Ts_veg_20cm = soil.Ts_veg_20cm.resample('D').min()
SoilDailyStats.Avg_Ts_veg_50cm = soil.Ts_veg_50cm.resample('D').mean()
SoilDailyStats.Max_Ts_veg_50cm = soil.Ts_veg_50cm.resample('D').max()
SoilDailyStats.Min_Ts_veg_50cm = soil.Ts_veg_50cm.resample('D').min()
SoilDailyStats.Avg_Ts_veg_100cm = soil.Ts_veg_100cm.resample('D').mean()
SoilDailyStats.Max_Ts_veg_100cm = soil.Ts_veg_100cm.resample('D').max()
SoilDailyStats.Min_Ts_veg_100cm = soil.Ts_veg_100cm.resample('D').min()
print(SoilDailyStats)

#Soil Monthly Stats
SoilMonthlyStats = pd.DataFrame(columns=['Avg_Ms_veg_5cm','Max_Ms_veg_5cm','Min_Ms_veg_5cm','Avg_Ms_veg_10cm','Max_Ms_veg_10cm','Min_Ms_veg_10cm','Avg_Ms_veg_20cm','Max_Ms_veg_20cm','Min_Ms_veg_20cm','Avg_Ms_veg_50cm','Max_Ms_veg_50cm','Min_Ms_veg_50cm','Avg_Ms_veg_100cm','Max_Ms_veg_100cm','Min_Ms_veg_100cm','Avg_Ts_veg_5cm','Max_Ts_veg_5cm','Min_Ts_veg_5cm','Avg_Ts_veg_10cm','Max_Ts_veg_10cm','Min_Ts_veg_10cm','Avg_Ts_veg_20cm','Max_Ts_veg_20cm','Min_Ts_veg_20cm','Avg_Ts_veg_50cm','Max_Ts_veg_50cm','Min_Ts_veg_50cm','Avg_Ts_veg_100cm','Max_Ts_veg_100cm','Min_Ts_veg_100cm'])
SoilMonthlyStats.Avg_Ms_veg_5cm = soil.Ms_veg_5cm.resample('M').mean()
SoilMonthlyStats.Max_Ms_veg_5cm = soil.Ms_veg_5cm.resample('M').max()
SoilMonthlyStats.Min_Ms_veg_5cm = soil.Ms_veg_5cm.resample('M').min()
SoilMonthlyStats.Avg_Ms_veg_10cm = soil.Ms_veg_10cm.resample('M').mean()
SoilMonthlyStats.Max_Ms_veg_10cm = soil.Ms_veg_10cm.resample('M').max()
SoilMonthlyStats.Min_Ms_veg_10cm = soil.Ms_veg_10cm.resample('M').min()
SoilMonthlyStats.Avg_Ms_veg_20cm = soil.Ms_veg_20cm.resample('M').mean()
SoilMonthlyStats.Max_Ms_veg_20cm = soil.Ms_veg_20cm.resample('M').max()
SoilMonthlyStats.Min_Ms_veg_20cm = soil.Ms_veg_20cm.resample('M').min()
SoilMonthlyStats.Avg_Ms_veg_50cm = soil.Ms_veg_50cm.resample('M').mean()
SoilMonthlyStats.Max_Ms_veg_50cm = soil.Ms_veg_50cm.resample('M').max()
SoilMonthlyStats.Min_Ms_veg_50cm = soil.Ms_veg_50cm.resample('M').min()
SoilMonthlyStats.Avg_Ms_veg_100cm = soil.Ms_veg_100cm.resample('M').mean()
SoilMonthlyStats.Max_Ms_veg_100cm = soil.Ms_veg_100cm.resample('M').max()
SoilMonthlyStats.Min_Ms_veg_100cm = soil.Ms_veg_100cm.resample('M').min()
SoilMonthlyStats.Avg_Ts_veg_5cm = soil.Ts_veg_5cm.resample('M').mean()
SoilMonthlyStats.Max_Ts_veg_5cm = soil.Ts_veg_5cm.resample('M').max()
SoilMonthlyStats.Min_Ts_veg_5cm = soil.Ts_veg_5cm.resample('M').min()
SoilMonthlyStats.Avg_Ts_veg_10cm = soil.Ts_veg_10cm.resample('M').mean()
SoilMonthlyStats.Max_Ts_veg_10cm = soil.Ts_veg_10cm.resample('M').max()
SoilMonthlyStats.Min_Ts_veg_10cm = soil.Ts_veg_10cm.resample('M').min()
SoilMonthlyStats.Avg_Ts_veg_20cm = soil.Ts_veg_20cm.resample('M').mean()
SoilMonthlyStats.Max_Ts_veg_20cm = soil.Ts_veg_20cm.resample('M').max()
SoilMonthlyStats.Min_Ts_veg_20cm = soil.Ts_veg_20cm.resample('M').min()
SoilMonthlyStats.Avg_Ts_veg_50cm = soil.Ts_veg_50cm.resample('M').mean()
SoilMonthlyStats.Max_Ts_veg_50cm = soil.Ts_veg_50cm.resample('M').max()
SoilMonthlyStats.Min_Ts_veg_50cm = soil.Ts_veg_50cm.resample('M').min()
SoilMonthlyStats.Avg_Ts_veg_100cm = soil.Ts_veg_100cm.resample('M').mean()
SoilMonthlyStats.Max_Ts_veg_100cm = soil.Ts_veg_100cm.resample('M').max()
SoilMonthlyStats.Min_Ts_veg_100cm = soil.Ts_veg_100cm.resample('M').min()
print(SoilMonthlyStats)

#Soil Annual Stats
SoilAnnualStats = pd.DataFrame(columns=['Avg_Ms_veg_5cm','Max_Ms_veg_5cm','Min_Ms_veg_5cm','Avg_Ms_veg_10cm','Max_Ms_veg_10cm','Min_Ms_veg_10cm','Avg_Ms_veg_20cm','Max_Ms_veg_20cm','Min_Ms_veg_20cm','Avg_Ms_veg_50cm','Max_Ms_veg_50cm','Min_Ms_veg_50cm','Avg_Ms_veg_100cm','Max_Ms_veg_100cm','Min_Ms_veg_100cm','Avg_Ts_veg_5cm','Max_Ts_veg_5cm','Min_Ts_veg_5cm','Avg_Ts_veg_10cm','Max_Ts_veg_10cm','Min_Ts_veg_10cm','Avg_Ts_veg_20cm','Max_Ts_veg_20cm','Min_Ts_veg_20cm','Avg_Ts_veg_50cm','Max_Ts_veg_50cm','Min_Ts_veg_50cm','Avg_Ts_veg_100cm','Max_Ts_veg_100cm','Min_Ts_veg_100cm'])
SoilAnnualStats.Avg_Ms_veg_5cm = soil.Ms_veg_5cm.resample('Y').mean()
SoilAnnualStats.Max_Ms_veg_5cm = soil.Ms_veg_5cm.resample('Y').max()
SoilAnnualStats.Min_Ms_veg_5cm = soil.Ms_veg_5cm.resample('Y').min()
SoilAnnualStats.Avg_Ms_veg_10cm = soil.Ms_veg_10cm.resample('Y').mean()
SoilAnnualStats.Max_Ms_veg_10cm = soil.Ms_veg_10cm.resample('Y').max()
SoilAnnualStats.Min_Ms_veg_10cm = soil.Ms_veg_10cm.resample('Y').min()
SoilAnnualStats.Avg_Ms_veg_20cm = soil.Ms_veg_20cm.resample('Y').mean()
SoilAnnualStats.Max_Ms_veg_20cm = soil.Ms_veg_20cm.resample('Y').max()
SoilAnnualStats.Min_Ms_veg_20cm = soil.Ms_veg_20cm.resample('Y').min()
SoilAnnualStats.Avg_Ms_veg_50cm = soil.Ms_veg_50cm.resample('Y').mean()
SoilAnnualStats.Max_Ms_veg_50cm = soil.Ms_veg_50cm.resample('Y').max()
SoilAnnualStats.Min_Ms_veg_50cm = soil.Ms_veg_50cm.resample('Y').min()
SoilAnnualStats.Avg_Ms_veg_100cm = soil.Ms_veg_100cm.resample('Y').mean()
SoilAnnualStats.Max_Ms_veg_100cm = soil.Ms_veg_100cm.resample('Y').max()
SoilAnnualStats.Min_Ms_veg_100cm = soil.Ms_veg_100cm.resample('Y').min()
SoilAnnualStats.Avg_Ts_veg_5cm = soil.Ts_veg_5cm.resample('Y').mean()
SoilAnnualStats.Max_Ts_veg_5cm = soil.Ts_veg_5cm.resample('Y').max()
SoilAnnualStats.Min_Ts_veg_5cm = soil.Ts_veg_5cm.resample('Y').min()
SoilAnnualStats.Avg_Ts_veg_10cm = soil.Ts_veg_10cm.resample('Y').mean()
SoilAnnualStats.Max_Ts_veg_10cm = soil.Ts_veg_10cm.resample('Y').max()
SoilAnnualStats.Min_Ts_veg_10cm = soil.Ts_veg_10cm.resample('Y').min()
SoilAnnualStats.Avg_Ts_veg_20cm = soil.Ts_veg_20cm.resample('Y').mean()
SoilAnnualStats.Max_Ts_veg_20cm = soil.Ts_veg_20cm.resample('Y').max()
SoilAnnualStats.Min_Ts_veg_20cm = soil.Ts_veg_20cm.resample('Y').min()
SoilAnnualStats.Avg_Ts_veg_50cm = soil.Ts_veg_50cm.resample('Y').mean()
SoilAnnualStats.Max_Ts_veg_50cm = soil.Ts_veg_50cm.resample('Y').max()
SoilAnnualStats.Min_Ts_veg_50cm = soil.Ts_veg_50cm.resample('Y').min()
SoilAnnualStats.Avg_Ts_veg_100cm = soil.Ts_veg_100cm.resample('Y').mean()
SoilAnnualStats.Max_Ts_veg_100cm = soil.Ts_veg_100cm.resample('Y').max()
SoilAnnualStats.Min_Ts_veg_100cm = soil.Ts_veg_100cm.resample('Y').min()
print(SoilAnnualStats)


AGLHourlyStats.info()
AGLDailyStats.info()
AGLMonthlyStats.info()
AGLAnnualStats.info()
SoilHourlyStats.info()
SoilDailyStats.info()
SoilMonthlyStats.info()
SoilAnnualStats.info()
#%% 7. give options for english or SI units.
#the original way is in SI. Need to convert all columns to English Units

#for AGL:
#MinT, MaxT, MeanT, soiltemp are in degrees celcius. These columns need (x°C × 1.8) + 32 = y°F
#relative humidity is in percent. it can stay the same.
#wind speed and gusts are in m/s, change to mph.
#solar, leave as is, as there isn't really an English unit for this.
#Rain - in mm. change to in. mm/25.4 = in
AGLHourlyStatsEnglish = pd.DataFrame(columns=['MinT','MaxT','MeanT','MinRH','MaxRH','MeanRH','AvgWindSpd','MaxGust','MinSolar','MaxSolar','MeanSolar','AvgSoilT','RainSum'])
print(AGLHourlyStatsEnglish)
AGLHourlyStatsEnglish['MinT']=(AGLHourlyStats['MinT']*1.8)+32
AGLHourlyStatsEnglish['MaxT']=(AGLHourlyStats['MaxT']*1.8)+32
AGLHourlyStatsEnglish['MeanT']=(AGLHourlyStats['MeanT']*1.8)+32
AGLHourlyStatsEnglish['AvgSoilT']=(AGLHourlyStats['AvgSoilT']*1.8)+32
AGLHourlyStatsEnglish['RainSum']=(AGLHourlyStats['RainSum']/25.4)
AGLHourlyStatsEnglish['AvgWindSpd']=(AGLHourlyStats['AvgWindSpd']*2.237)
AGLHourlyStatsEnglish['MaxGust']=(AGLHourlyStats['MaxGust']*2.237)
AGLHourlyStatsEnglish['MinRH']=(AGLHourlyStats['MinRH'])
AGLHourlyStatsEnglish['MaxRH']=(AGLHourlyStats['MaxRH'])
AGLHourlyStatsEnglish['MeanRH']=(AGLHourlyStats['MeanRH'])
AGLHourlyStatsEnglish['MinSolar']=(AGLHourlyStats['MinSolar'])
AGLHourlyStatsEnglish['MaxSolar']=(AGLHourlyStats['MaxSolar'])
AGLHourlyStatsEnglish['MeanSolar']=(AGLHourlyStats['MeanSolar'])

AGLDailyStatsEnglish = pd.DataFrame(columns=['MinT','MaxT','MeanT','MinRH','MaxRH','MeanRH','AvgWindSpd','MaxGust','MinSolar','MaxSolar','MeanSolar','AvgSoilT','RainSum'])
print(AGLDailyStatsEnglish)
AGLDailyStatsEnglish['MinT']=(AGLDailyStats['MinT']*1.8)+32
AGLDailyStatsEnglish['MaxT']=(AGLDailyStats['MaxT']*1.8)+32
AGLDailyStatsEnglish['MeanT']=(AGLDailyStats['MeanT']*1.8)+32
AGLDailyStatsEnglish['AvgSoilT']=(AGLDailyStats['AvgSoilT']*1.8)+32
AGLDailyStatsEnglish['RainSum']=(AGLDailyStats['RainSum']/25.4)
AGLDailyStatsEnglish['AvgWindSpd']=(AGLDailyStats['AvgWindSpd']*2.237)
AGLDailyStatsEnglish['MaxGust']=(AGLDailyStats['MaxGust']*2.237)
AGLDailyStatsEnglish['MinRH']=(AGLDailyStats['MinRH'])
AGLDailyStatsEnglish['MaxRH']=(AGLDailyStats['MaxRH'])
AGLDailyStatsEnglish['MeanRH']=(AGLDailyStats['MeanRH'])
AGLDailyStatsEnglish['MinSolar']=(AGLDailyStats['MinSolar'])
AGLDailyStatsEnglish['MaxSolar']=(AGLDailyStats['MaxSolar'])
AGLDailyStatsEnglish['MeanSolar']=(AGLDailyStats['MeanSolar'])

AGLMonthlyStatsEnglish = pd.DataFrame(columns=['MinT','MaxT','MeanT','MinRH','MaxRH','MeanRH','AvgWindSpd','MaxGust','MinSolar','MaxSolar','MeanSolar','AvgSoilT','RainSum'])
print(AGLMonthlyStatsEnglish)
AGLMonthlyStatsEnglish['MinT']=(AGLMonthlyStats['MinT']*1.8)+32
AGLMonthlyStatsEnglish['MaxT']=(AGLMonthlyStats['MaxT']*1.8)+32
AGLMonthlyStatsEnglish['MeanT']=(AGLMonthlyStats['MeanT']*1.8)+32
AGLMonthlyStatsEnglish['AvgSoilT']=(AGLMonthlyStats['AvgSoilT']*1.8)+32
AGLMonthlyStatsEnglish['RainSum']=(AGLMonthlyStats['RainSum']/25.4)
AGLMonthlyStatsEnglish['AvgWindSpd']=(AGLMonthlyStats['AvgWindSpd']*2.237)
AGLMonthlyStatsEnglish['MaxGust']=(AGLMonthlyStats['MaxGust']*2.237)
AGLMonthlyStatsEnglish['MinRH']=(AGLMonthlyStats['MinRH'])
AGLMonthlyStatsEnglish['MaxRH']=(AGLMonthlyStats['MaxRH'])
AGLMonthlyStatsEnglish['MeanRH']=(AGLMonthlyStats['MeanRH'])
AGLMonthlyStatsEnglish['MinSolar']=(AGLMonthlyStats['MinSolar'])
AGLMonthlyStatsEnglish['MaxSolar']=(AGLMonthlyStats['MaxSolar'])
AGLMonthlyStatsEnglish['MeanSolar']=(AGLMonthlyStats['MeanSolar'])


AGLAnnualStatsEnglish = pd.DataFrame(columns=['MinT','MaxT','MeanT','MinRH','MaxRH','MeanRH','AvgWindSpd','MaxGust','MinSolar','MaxSolar','MeanSolar','AvgSoilT','RainSum'])
print(AGLAnnualStatsEnglish)
AGLAnnualStatsEnglish['MinT']=(AGLAnnualStats['MinT']*1.8)+32
AGLAnnualStatsEnglish['MaxT']=(AGLAnnualStats['MaxT']*1.8)+32
AGLAnnualStatsEnglish['MeanT']=(AGLAnnualStats['MeanT']*1.8)+32
AGLAnnualStatsEnglish['AvgSoilT']=(AGLAnnualStats['AvgSoilT']*1.8)+32
AGLAnnualStatsEnglish['RainSum']=(AGLAnnualStats['RainSum']/25.4)
AGLAnnualStatsEnglish['AvgWindSpd']=(AGLAnnualStats['AvgWindSpd']*2.237)
AGLAnnualStatsEnglish['MaxGust']=(AGLAnnualStats['MaxGust']*2.237)
AGLAnnualStatsEnglish['MinRH']=(AGLAnnualStats['MinRH'])
AGLAnnualStatsEnglish['MaxRH']=(AGLAnnualStats['MaxRH'])
AGLAnnualStatsEnglish['MeanRH']=(AGLAnnualStats['MeanRH'])
AGLAnnualStatsEnglish['MinSolar']=(AGLAnnualStats['MinSolar'])
AGLAnnualStatsEnglish['MaxSolar']=(AGLAnnualStats['MaxSolar'])
AGLAnnualStatsEnglish['MeanSolar']=(AGLAnnualStats['MeanSolar'])

AGLHourlyStats.info()
AGLMonthlyStats.info()
AGLDailyStats.info()
AGLAnnualStats.info()

#convert soil to English Units. Moisture is in mV. millivolts. Not water content. Will look at this more later.
SoilHourlyStats
SoilDailyStats
SoilMonthlyStats.info()
SoilAnnualStats
#%% 8. Create CSV exports for all options (hourly, daily, monthly, annual) X (english or SI)
#at this point, will omit the soil dataset from interface options
#full soil data csv export
dirPath = r'C:\Users\lthompson8\python2020summer\FinalProject'
fileName = 'Rulo_soil_Data_bydate_combined.csv'
fullPath = os.path.join(dirPath, fileName)
print(fullPath)
soil.to_csv(fullPath, index=False)
#full agl data csv export
dirPath = r'C:\Users\lthompson8\python2020summer\FinalProject'
fileName = 'Rulo_agl_Data_bydate_combined.csv'
fullPath = os.path.join(dirPath, fileName)
print(fullPath)
agl.to_csv(fullPath, index=False)

##################################################################
#######These are the 8 options defined by 2 radial buttons########
##################################################################

#daily AGL English
fileName = 'DailyAGLRulo_English.csv'
fullPath = os.path.join(parentdirectory, fileName)
print(fullPath)
AGLDailyStatsEnglish.to_csv(fullPath, float_format='%.2f')

#monthly AGL English
fileName = 'MonthlyAGLRulo_English.csv'
fullPath = os.path.join(parentdirectory, fileName)
print(fullPath)
AGLMonthlyStatsEnglish.to_csv(fullPath, float_format='%.2f')

#Hourly AGL English
fileName = 'HourlyAGLRulo_English.csv'
fullPath = os.path.join(parentdirectory, fileName)
print(fullPath)
AGLHourlyStatsEnglish.to_csv(fullPath, float_format='%.2f')

#annual AGL English
fileName = 'AnnualAGLRulo_English.csv'
fullPath = os.path.join(parentdirectory, fileName)
print(fullPath)
AGLAnnualStatsEnglish.to_csv(fullPath, float_format='%.2f')

#Daily AGL SI
fileName = 'DailyAGLRulo_SI.csv'
fullPath = os.path.join(parentdirectory, fileName)
print(fullPath)
AGLDailyStats.to_csv(fullPath, float_format='%.2f')

#Monthly AGL SI
fileName = 'MonthlyAGLRulo_SI.csv'
fullPath = os.path.join(parentdirectory, fileName)
print(fullPath)
AGLMonthlyStats.to_csv(fullPath, float_format='%.2f')

#Hourly AGL SI
fileName = 'HourlyAGLRulo_SI.csv'
fullPath = os.path.join(parentdirectory, fileName)
print(fullPath)
AGLHourlyStats.to_csv(fullPath, float_format='%.2f')

#Annual AGL SI
fileName = 'AnnualAGLRulo_SI.csv'
fullPath = os.path.join(parentdirectory, fileName)
print(fullPath)
AGLAnnualStats.to_csv(fullPath, float_format='%.2f')

#%% 9. create plots to visualize key items
#visualize key items
AGLMonthlyStats.info()

#hourly temperature - SI
fig, ax = plt.subplots()  # Create a figure and an axes.
plt.plot(AGLHourlyStats.index, AGLHourlyStats.MeanT, label='mean temperature')  # Plot some data on the axes.
plt.plot(AGLHourlyStats.index, AGLHourlyStats.MinT, label='min temperature')  # Plot more data on the axes...
plt.plot(AGLHourlyStats.index, AGLHourlyStats.MaxT, label='max temperature')  # ... and some more.
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Temperature - C')  # Add a y-label to the axes.
plt.title('Hourly Temperature Plot - C')
plt.legend()  # Add a legend.

#monthly temperature - SI
fig, ax = plt.subplots()  # Create a figure and an axes.
plt.plot(AGLMonthlyStats.index, AGLMonthlyStats.MeanT, label='mean temperature')  # Plot some data on the axes.
plt.plot(AGLMonthlyStats.index, AGLMonthlyStats.MinT, label='min temperature')  # Plot more data on the axes...
plt.plot(AGLMonthlyStats.index, AGLMonthlyStats.MaxT, label='max temperature')  # ... and some more.
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Temperature - C')  # Add a y-label to the axes.
plt.title('Monthly Temperature Plot - C')
plt.legend()  # Add a legend.

#Daily temperature- SI
fig, ax = plt.subplots()  # Create a figure and an axes.
plt.plot(AGLDailyStats.index, AGLDailyStats.MeanT, label='mean temperature')  # Plot some data on the axes.
plt.plot(AGLDailyStats.index, AGLDailyStats.MinT, label='min temperature')  # Plot more data on the axes...
plt.plot(AGLDailyStats.index, AGLDailyStats.MaxT, label='max temperature')  # ... and some more.
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Temperature - C')  # Add a y-label to the axes.
plt.title('Daily Temperature Plot - C')
plt.legend()  # Add a legend.

#annual temperature - SI
fig, ax = plt.subplots()  # Create a figure and an axes.
plt.plot(AGLAnnualStats.index, AGLAnnualStats.MeanT, label='mean temperature')  # Plot some data on the axes.
plt.plot(AGLAnnualStats.index, AGLAnnualStats.MinT, label='min temperature')  # Plot more data on the axes...
plt.plot(AGLAnnualStats.index, AGLAnnualStats.MaxT, label='max temperature')  # ... and some more.
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Temperature - C')  # Add a y-label to the axes.
plt.title('Annual Temperature Plot - C')
plt.legend()  # Add a legend.

#Annual rainfall - SI
fig, ax = plt.subplots()  # Create a figure and an axes.
rects1 = ax.bar(AGLAnnualStats.index, AGLAnnualStats.RainSum, label='rain (mm)')
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Rain (mm)')  # Add a y-label to the axes.
plt.title('Annual Rainfall Plot (mm)')

#Monthly rainfall - SI
fig, ax = plt.subplots()  # Create a figure and an axes.
rects1 = ax.bar(AGLMonthlyStats.index, AGLMonthlyStats.RainSum, label='rain (mm)')
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Rain (mm)')  # Add a y-label to the axes.
plt.title('Monthly Rainfall Plot (mm)')

#Daily rainfall - SI
fig, ax = plt.subplots()  # Create a figure and an axes.
rects1 = ax.bar(AGLDailyStats.index, AGLDailyStats.RainSum, label='rain (mm)')
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Rain (mm)')  # Add a y-label to the axes.
plt.title('Daily Rainfall Plot (mm)')

#Hourly rainfall - SI
fig, ax = plt.subplots()  # Create a figure and an axes.
rects1 = ax.bar(AGLHourlyStats.index, AGLHourlyStats.RainSum, label='rain (mm)')
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Rain (mm)')  # Add a y-label to the axes.
plt.title('Hourly Rainfall Plot (mm)')



#hourly temperature - English
fig, ax = plt.subplots()  # Create a figure and an axes.
plt.plot(AGLHourlyStatsEnglish.index, AGLHourlyStatsEnglish.MeanT, label='mean temperature')  # Plot some data on the axes.
plt.plot(AGLHourlyStatsEnglish.index, AGLHourlyStatsEnglish.MinT, label='min temperature')  # Plot more data on the axes...
plt.plot(AGLHourlyStatsEnglish.index, AGLHourlyStatsEnglish.MaxT, label='max temperature')  # ... and some more.
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Temperature - F')  # Add a y-label to the axes.
plt.title('Hourly Temperature Plot - F')
plt.legend()  # Add a legend.

#monthly temperature - English
fig, ax = plt.subplots()  # Create a figure and an axes.
plt.plot(AGLMonthlyStatsEnglish.index, AGLMonthlyStatsEnglish.MeanT, label='mean temperature')  # Plot some data on the axes.
plt.plot(AGLMonthlyStatsEnglish.index, AGLMonthlyStatsEnglish.MinT, label='min temperature')  # Plot more data on the axes...
plt.plot(AGLMonthlyStatsEnglish.index, AGLMonthlyStatsEnglish.MaxT, label='max temperature')  # ... and some more.
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Temperature - F')  # Add a y-label to the axes.
plt.title('Monthly Temperature Plot - F')
plt.legend()  # Add a legend.

#Daily temperature- English
fig, ax = plt.subplots()  # Create a figure and an axes.
plt.plot(AGLDailyStatsEnglish.index, AGLDailyStatsEnglish.MeanT, label='mean temperature')  # Plot some data on the axes.
plt.plot(AGLDailyStatsEnglish.index, AGLDailyStatsEnglish.MinT, label='min temperature')  # Plot more data on the axes...
plt.plot(AGLDailyStatsEnglish.index, AGLDailyStatsEnglish.MaxT, label='max temperature')  # ... and some more.
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Temperature - F')  # Add a y-label to the axes.
plt.title('Daily Temperature Plot - F')
plt.legend()  # Add a legend.

#annual temperature - English
fig, ax = plt.subplots()  # Create a figure and an axes.
plt.plot(AGLAnnualStatsEnglish.index, AGLAnnualStatsEnglish.MeanT, label='mean temperature')  # Plot some data on the axes.
plt.plot(AGLAnnualStatsEnglish.index, AGLAnnualStatsEnglish.MinT, label='min temperature')  # Plot more data on the axes...
plt.plot(AGLAnnualStatsEnglish.index, AGLAnnualStatsEnglish.MaxT, label='max temperature')  # ... and some more.
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Temperature - F')  # Add a y-label to the axes.
plt.title('Annual Temperature Plot - F')
plt.legend()  # Add a legend.




#Annual rainfall - English
fig, ax = plt.subplots()  # Create a figure and an axes.
rects1 = ax.bar(AGLAnnualStatsEnglish.index, AGLAnnualStatsEnglish.RainSum, label='rain (in)')
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Rain (in)')  # Add a y-label to the axes.
plt.title('Annual Rainfall Plot (in)')

#Monthly rainfall - English
fig, ax = plt.subplots()  # Create a figure and an axes.
rects1 = ax.bar(AGLMonthlyStatsEnglish.index, AGLMonthlyStatsEnglish.RainSum, label='rain (in)')
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Rain (in)')  # Add a y-label to the axes.
plt.title('Monthly Rainfall Plot (in)')

#Daily rainfall - English
fig, ax = plt.subplots()  # Create a figure and an axes.
rects1 = ax.bar(AGLDailyStatsEnglish.index, AGLDailyStatsEnglish.RainSum, label='rain (in)')
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Rain (in)')  # Add a y-label to the axes.
plt.title('Daily Rainfall Plot (in)')

#Hourly rainfall - English
fig, ax = plt.subplots()  # Create a figure and an axes.
rects1 = ax.bar(AGLHourlyStatsEnglish.index, AGLHourlyStatsEnglish.RainSum, label='rain (in)')
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Rain (in)')  # Add a y-label to the axes.
plt.title('Hourly Rainfall Plot (in)')

















AGLAnnualStatsEnglish.info()
#Daily windspeed and gusts- English
fig, ax = plt.subplots(1,1, figsize=(25,4))  # Create a figure and an axes.
plt.plot(AGLDailyStatsEnglish.index, AGLDailyStatsEnglish.AvgWindSpd, label='Wind Speed (mph)')  # Plot some data on the axes.
plt.plot(AGLDailyStatsEnglish.index, AGLDailyStatsEnglish.MaxGust, label='Gusts (mph)')  # Plot more data on the axes...
plt.xlabel('Date-Time')  # Add an x-label to the axes.
plt.ylabel('Wind (mph)')  # Add a y-label to the axes.
plt.title('Wind Speed and Gusts')
plt.legend()  # Add a legend.




#%% 10. need to rethink user interface given what I create here and how to best access.
#add radial for SI vs English
#download CSV by hourly, daily, monthly, yearly
#view temperature or rainfall graph by hourly, daily, monthly, or yearly
