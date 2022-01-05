# this module is to look at Fuzzworks for an updated SDE. If new - download, delete old, unzip, then bring into a new table. If not - bring current SDE into a table.
import requests #url tools
from datetime import datetime #time tools
import os.path #check if file exsists
import bz2 #zip reader
import pandas as pd #duh pandas
#fetch URL
url = 'https://www.fuzzwork.co.uk/dump/latest/invTypes.csv.bz2'
#Get that URL
r1 = requests.get(url)
#make the string as datetime for compairing.
datetime_r1 = datetime.strptime(r1.headers['Last-Modified'], "%a, %d %b %Y %H:%M:%S %Z")
#program save path
save_path = "C:\\Users\\dbink\\Desktop\\Arbs Ahoy's AEET\\"
#make a file that notates when the last update was to make sure we are grabbing most up to date from Fuzzworks.
invTypesLastModifiedDateExists = os.path.isfile(save_path+"invTypesDate.txt")
#if doesn't exsist, make one and write the details. 
if not invTypesLastModifiedDateExists:
    with open(save_path+"invTypesDate.txt",'w'): pass

invTypesWriteDateToText = open(save_path+"invTypesDate.txt", "w")

invTypesWriteDateToText.write(r1.headers['Last-Modified'])
#read .txt to get time date
invTypesWriteDateToText = open(save_path+"invTypesDate.txt", "r")
#convert string into datetime
datetime_r2 = datetime.strptime(invTypesWriteDateToText.read(), "%a, %d %b %Y %H:%M:%S %Z")
#if datetime_r1 is greater than or equal to datetime_r2, up to date and read the file. If not, update file and read new. 
if datetime_r1 >= datetime_r2:
    print("invTypes is Up to Date.")
    open(save_path+"invType.csv.bz2","r")
    dfinvType = pd.read_csv(save_path+"invType.csv.bz2")
else:
    print("invType Updating.....")
    os.remove(save_path+"invType.csv.bz2")
    open(save_path+"invType.csv.bz2","wb").write(r1.content)
    dfinvType = pd.read_csv(save_path+"invType.csv.bz2")


