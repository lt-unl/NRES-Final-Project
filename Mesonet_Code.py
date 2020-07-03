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

#%% 2. Designate Working Directory 
os.getcwd()
#create parent directory
parentdirectory = 'C:\\Users\\lthompson8\\python2020summer\\FinalProject'
os.chdir(parentdirectory)
os.getcwd()

#%% 3. File download. Looks like I may have to use and API or token if I want to download directly from box.

#for now, will manually download to skip this issue, and proceed with zipped folder (assuming that I can get to this step with code in the future)
#url = "https://unl.app.box.com/folder/79735107810"

#%% 4. Unzip file to new folder named 'temp_csv' in working directory
# Create a ZipFile Object and load zip in it
file_name="Rulo_5SW.zip"
with ZipFile(file_name, 'r') as zipObj:
   # Get a list of all archived file names from the zip
   listOfFileNames = zipObj.namelist()
   # Iterate over the file names
   for fileName in listOfFileNames:
       # Check filename endswith csv
       if fileName.endswith('.csv'):
           # Extract a single file from zip
           zipObj.extract(fileName, 'temp_csv')

# opening the zip file in READ mode 
with ZipFile(file_name, 'r') as zip: 
    # printing all the contents of the zip file 
    zip.printdir() 

#%% 5. Sorting files into folders. 
#Each day, 2 datasets are created:
    #agl is above ground measurements and contains 35 columns and readings every minute
    #soil is soil measurements and contains 12 columns and readings every hour
    
#will need to extract agl files to one folder -> RuloAGL
dirname = 'C:\\Users\\lthompson8\\python2020summer\\FinalProject\\temp_csv'
os.chdir(dirname)
for root, dirs, files in os.walk(dirname):
    for fname in files:
        # Match a string starting with 7 digits followed by everything else.
        # Capture each part in a group so we can access them later.
        match_object = re.match('(Rulo_5SW_agl)(.*)$', fname)
        if match_object is None:
            # The regular expression did not match, ignore the file.
            continue

        # Form the new directory path using the number from the regular expression and the current root.
        new_dir = os.path.join(root, match_object.group(1))
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)

        new_file_path = os.path.join(new_dir, fname)

        old_file_path = os.path.join(root, fname)
        shutil.move(old_file_path, new_file_path)
agl_file_path = 'C:\\Users\\lthompson8\\python2020summer\\FinalProject\\temp_csv\\Rulo_5SW\\Rulo_5SW_agl\\Rulo_5SW_agl'
#will extract soil files to another folder -> RuloSoil
for root, dirs, files in os.walk(dirname):
    for fname in files:
        # Match a string starting with 7 digits followed by everything else.
        # Capture each part in a group so we can access them later.
        match_object = re.match('(Rulo_5SW_soil)(.*)$', fname)
        if match_object is None:
            # The regular expression did not match, ignore the file.
            continue

        # Form the new directory path using the number from the regular expression and the current root.
        new_dir = os.path.join(root, match_object.group(1))
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)

        new_file_path = os.path.join(new_dir, fname)

        old_file_path = os.path.join(root, fname)
        shutil.move(old_file_path, new_file_path)
soil_file_path = 'C:\\Users\\lthompson8\\python2020summer\\FinalProject\\temp_csv\\Rulo_5SW\\Rulo_5SW_soil'

#%% 6. Append/Concatenate files for soil
#move to directory with soil
os.chdir(soil_file_path)
#start with soil data

#%% 6.a - append CSV files to one combined file with pandas.
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f)for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_soil_test1.csv", index = False, encoding='utf-8-sig')
#appears first 4 columns were lost when combining.
#WHY?

#%% 6.b - trying something different - not using Pandas
#create header with column names
soil_csv_header = 'Timestamp,Record Number,Ms Veg 5 cm,Ms Veg 10 cm,Ms Veg 20 cm,Ms Veg 50 cm,Ms Veg 100 cm,Ts Veg 5 cm,Ts Veg 10 cm,Ts Veg 20 cm,Ts Veg 50 cm,Ts Veg 100 cm'
csv_out = 'combined_soil_test3.csv'

csv_dir = os.getcwd()

dir_tree = os.walk(csv_dir)
for dirpath, dirnames, filenames in dir_tree:
   pass

csv_list = []
for file in filenames:
   if file.endswith('.csv'):
      csv_list.append(file)

csv_merge = open(csv_out, 'w')
csv_merge.write(soil_csv_header)
csv_merge.write('\n')

for file in csv_list:
   csv_in = open(file)
   for line in csv_in:
      if line.startswith(soil_csv_header):
         continue
      csv_merge.write(line)
   csv_in.close()
   csv_merge.close()
print('Verify consolidated CSV file : ' + csv_out)

#initial records do not print all columns. Later on in dates all columns are printed. WHY???

#%% 6.c - try another approach

#import csv files from folder
path = r'C:\\Users\\lthompson8\\python2020summer\\FinalProject\\temp_csv\\Rulo_5SW\\Rulo_5SW_soil'
allFiles = glob.glob(path + "/*.csv")
allFiles.sort()  # glob lacks reliable ordering, so impose your own if output order matters
with open('combined_soil_test4.csv', 'wb') as outfile:
    for i, fname in enumerate(allFiles):
        with open(fname, 'rb') as infile:
            if i != 0:
                infile.readline()  # Throw away header on all but first file
            # Block copy rest of file from input to output without parsing
            shutil.copyfileobj(infile, outfile)
            print(fname + " has been imported.")
#combined, but headers are still on each file and it has been combined with only 8 columns

#%% 6.d 
os.makedirs('headerRemoved', exist_ok=True)
  
# loop through every file in the current working directory.
for csvFilename in os.listdir('.'):
    if not csvFilename.endswith('.csv'):
        continue # skip non-csv files
    print('Removing header from ' + csvFilename + '...')  
    targetFilename = os.path.join('headerRemoved', csvFilename)
    with open(csvFilename) as ifo, open(targetFilename, "w") as ofo:
        ifo.readline()
        shutil.copyfileobj(ifo, ofo)

#%% 6.e
os.makedirs('headerRemoved', exist_ok=True)
  
# loop through every file in the current working directory.
for csvFilename in os.listdir('.'):
    if not csvFilename.endswith('.csv'):
        continue # skip non-csv files
    print('Removing header from ' + csvFilename + '...')  
#read the csv file in (skipping header rows)
    csvRows = []
    csvFileObj = open(csvFilename)
    readerObj = csv.reader(csvFileObj)
    for row in readerObj:
        if readerObj.line_num ==1:
            continue #skip first row
        csvRows.append(row)
    csvFileObj.close()
#wrtie out the csv file
    csvFileObj = open(os.path.join('headerRemoved', csvFilename), 'w', newline='')
    csvWriter = csv.writer(csvFileObj)
    for row in csvRows:
        csvWriter.writerow(row)
    csvFileObj.close()
    
    
        
#%% 7. Append/Concatenate files for AGL
os.chdir(agl_file_path)
#append CSV files to one combined file.

#%% 7.a - try with pandas
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f)for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_agl_test1.csv", index = False, encoding='utf-8-sig')
#does not work.

#%% 7.b - try without pandas
#create header with column names
agl_csv_header = 'Timestamp,Record Number,T 2m avg C,T 2m max C,T 2m max time,T 2m min C,T 2m min time,RH 2m avg %,RH 2m max %,RH 2m max time,RH 2m min %,RH 2m min time,DP 2m avg C,DP 2m max C,DP 2m max time,DP 2m min C,DP 2m min time,HeatIndex 2m avg,HeatIndex 2m max C,HeatIndex 2m max time,WindChill 2m avg C,WindChill 2m min C,WindChill 2m min time,WindSpd 3m avg mpers,WingVecMag 3m avg mpers,WindDir 3m avg,WindDirAvg 3m SD,WindMaxSpd5s 3m mpers,WindMaxSpd5s 3m time,WindMax 5s Dir 3m,PresAvg 1pnt 5m mb,PresMax 1pnt 5m mb,PresMaxTime 1pnt 5m,PresMin 1pnt 5m mb,PresMinTime 1pnt 5m,Solar 2m Avg Wpermsquared,Rain 1m total mm,Ts bare 10cm avg,Ts bare 10cm max,Ts bare 10cm max time,Ts bare 10cm min,Ts bare 10cm min time,BattVolts min,LithBatt min,employee num'
csv_out = 'combined_agl_test3.csv'

csv_dir = os.getcwd()

dir_tree = os.walk(csv_dir)
for dirpath, dirnames, filenames in dir_tree:
   pass

csv_list = []
for file in filenames:
   if file.endswith('.csv'):
      csv_list.append(file)

csv_merge = open(csv_out, 'w')
csv_merge.write(agl_csv_header)
csv_merge.write('\n')

for file in csv_list:
   csv_in = open(file)
   for line in csv_in:
      if line.startswith(agl_csv_header):
         continue
      csv_merge.write(line)
   csv_in.close()
   csv_merge.close()
print('Verify consolidated CSV file : ' + csv_out)

#puts headers on and writes file, but doesn't merge together files...

#files have not appended correctly ... appears issue is unknown data type in most columns. Will need to specify dtype option on import??
#pandas is trying to guess the dtype. apparently uses a lot of memory and was not successful.
#need to assign for each of 45 columns - something like the below...
#but - don't think the csv files have column names assigned yet. Would be better if I could call by position of column...
dtype={'TS': str}
dtype={'RN': float}


#df = pd.read_csv(data, dtype={'Col_A': str,'Col_B':int64})





#%% 7. remove headers from appearing in each file...
#should this be done to each csv before or after concatenating??
#can I/should I do this for all files initially? before combining? if so, how?
#example codes below

#example 1
file='C:\\Users\\lthompson8\\python2020summer\\FinalProject\\temp_csv\\Rulo_5SW\\Rulo_5SW_soil\Rulo_5SW_soil_20200622_0703.csv'
df = pd.read_csv(file, skiprows=3, delimiter='\t', header=0, names=['Timestamp','Record Number','Ms Veg 5 cm','Ms Veg 10 cm','Ms Veg 20 cm','Ms Veg 50 cm','Ms Veg 100 cm','Ts Veg 5 cm','Ts Veg 10 cm','Ts Veg 20 cm','Ts Veg 50 cm','Ts Veg 100 cm'])
print(df)


#example 2
df = pd.read_csv(file, skiprows=range(0,4), sep='\n', names=['Timestamp','Record Number','Ms Veg 5 cm','Ms Veg 10 cm','Ms Veg 20 cm','Ms Veg 50 cm','Ms Veg 100 cm','Ts Veg 5 cm','Ts Veg 10 cm','Ts Veg 20 cm','Ts Veg 50 cm','Ts Veg 100 cm'])

skiprows=range(0,3)
#%% 8. summarize stats
#from concatenated dataset, need to summarize stats by hour, day, month, year, etc.
#pick which to summarize

#%% 9. give options for english or SI units.

#%% 10. create plots to visualize key items
#visualize key items