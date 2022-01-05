# this module is to look at Fuzzworks for an updated SDE. If new - download, delete old, unzip, then bring into a new table. If not - bring current SDE into a table.

import requests #url tools
from datetime import datetime #time tools
import os.path #check if file exsists
import bz2 #zip reader
import pandas as pd #duh pandas
import numpy as np #numpy for math pandas can't use

#fetch URL
url = 'https://www.fuzzwork.co.uk/dump/latest/invTypeMaterials.csv.bz2'

#Get that URL
r1 = requests.get(url)

#make the string as datetime for compairing.
datetime_r1 = datetime.strptime(r1.headers['Last-Modified'], "%a, %d %b %Y %H:%M:%S %Z")

#program save path
save_path = "C:\\Users\\dbink\\Desktop\\Arbs Ahoy's AEET\\"

#make a file that notates when the last update was to make sure we are grabbing most up to date from Fuzzworks.
invTypeMaterialsLastModifiedDateExists = os.path.isfile(save_path+"invTypeMaterialsDate.txt")

#if doesn't exsist, make one and write the details. 
if not invTypeMaterialsLastModifiedDateExists:
    with open(save_path+"invTypeMaterialsDate.txt",'w'): pass

invTypeMaterialsWriteDateToText = open(save_path+"invTypeMaterialsDate.txt", "w")

invTypeMaterialsWriteDateToText.write(r1.headers['Last-Modified'])

#making the material list
dfinvTypeMaterials = ()

#read .txt to get time date
invTypeMaterialsWriteDateToText = open(save_path+"invTypeMaterialsDate.txt", "r")

#convert string into datetime
datetime_r2 = datetime.strptime(invTypeMaterialsWriteDateToText.read(), "%a, %d %b %Y %H:%M:%S %Z")

#if datetime_r1 is greater than or equal to datetime_r2, up to date and read the file. If not, update file and read new. 
if datetime_r1 >= datetime_r2:
    print("invTypeMaterials is Up to Date.")
    open(save_path+"invTypeMaterials.csv.bz2","r")
    dfinvTypeMaterials = pd.read_csv(save_path+"invTypeMaterials.csv.bz2")
else:
    print("invTypeMaterials Updating.....")
    os.remove(save_path+"invTypeMaterials.csv.bz2")
    open(save_path+"invTypeMaterials.csv.bz2","wb").write(r1.content)
    dfinvTypeMaterials = pd.read_csv(save_path+"invTypeMaterials.csv.bz2")

#adjusts qty to line up with pricing
dfinvTypeMaterials['quantity'] = (.55 * dfinvTypeMaterials['quantity']).apply(np.ceil)

print('invTypeMaterials loaded...')