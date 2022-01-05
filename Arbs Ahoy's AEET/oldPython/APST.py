#Imports to make the tool work
import sys
sys.path.append('/root/EveOnline/SDE')
import mapDenormalize as mD #to get the area of interest
import pandas as pd #to get dataframes to do analysis with
import time as t #to time thing for a chance to make measureable optimizations
import mysql.connector #to connect to mySQL server
import datetime as dt #so I can convert my strings by time segments
import numpy as np
import scipy.stats as stats
import datetime as dt
import h5py

apstSuperStartTime = t.time()

#cnx (connection short hand for the above lib. this allows python to attach to mySQL server)
#cnx = mysql.connector.connect(user='vsserver', password='Stamp-Daisy9-Countless',
#                              host='192.168.1.13',
#                              database='sys')
#cursor = cnx.cursor()
#print("Connected to the SQL Server.")

dfmd = mD.dfmapDenormalize #make a short hand variable so it's easier to type

regionName = dfmd.loc[(dfmd['groupID'] == 3 ) & (dfmd['itemID'] < 11000000)] #focus in on group 3 (regions) where itemID is less than a limit (as regions have lower ID's)
systemName = dfmd.loc[(dfmd['groupID'] == 5 ) & (dfmd['itemID'] < 40000001) & (dfmd['itemID'] > 29999999)]

#fancy print me regions Names
print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
for name in regionName['itemName']:
    print(name)
print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

#store which contellation user wants to look at
whichRegion = input('Which constellation do you want to spy on? (case sensitive): ')
print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

#store the constellation of interest
desiredRegionID = regionName['itemID'].loc[regionName['itemName'] == whichRegion]

#systems of interest  
systemsOfInterest = systemName.merge(desiredRegionID, how='right', left_on='regionID', right_on='itemID').drop(columns=['itemID_y', 'orbitID', 'x', 'y', 'z', 'radius', 'celestialIndex', 'orbitIndex']).rename(columns={"itemID_x" : "itemID"})

#Math Section! 

#system jump performance removing the old jump performance in favor of a pre-mathed to increase performance. 
playfileSuperStartTime = t.time()
print(".")

shipJumps = pd.read_hdf('/root/EveOnline/Spy/HDF5/shipjump', mode='r')
print("..")

systemsOfInterest = pd.read_csv('/root/EveOnline/SDE/CSV/systemOfInterestDelve.csv')
print("...")

mergedList = systemsOfInterest.merge(shipJumps, how='left', left_on='itemID', right_on='system_id').set_index('itemID')
print("....")

del mergedList['system_id']
print(".....")

systemAverage = mergedList.groupby('itemID')['ship_jumps'].mean()
print("......")

systemSTD = mergedList.groupby('itemID')['ship_jumps'].std()
print(".......")

mergedListavg = mergedList.merge(systemAverage, how='left', on='itemID').rename(columns={'ship_jumps_x' : 'shipJumps', 'ship_jumps_y' : 'sysJumpAVG'})
print("........")

mergedListstd = mergedListavg.merge(systemSTD, how='left', on='itemID').rename(columns={'ship_jumps' : 'SysSTD'})
print(".........")

mergedListstd['zScore'] = (mergedListstd['shipJumps']-mergedListstd['sysJumpAVG'])/mergedListstd['SysSTD']
print("..........")

mergedListstd['percentile'] = pd.to_numeric(stats.norm.cdf(abs(mergedListstd['zScore'])))
print("...........")

mergedListstd['day'] = mergedListstd['timestamp'].dt.dayofweek
print("............")

mergedListstd['hour'] = mergedListstd['timestamp'].dt.hour
print(".............")

mergedListstd['timestamp'] = mergedListstd['timestamp'].apply(lambda _: dt.datetime.strftime(_,"%a %H:%M"))
print("..............")

mergedListstd.to_hdf('/root/EveOnline/Spy/HDF5/shipJumpMetrics', key='mergedListstd', mode='a', append=True, format='table')

#ship jump last hour, this will be the max timestamp, timedelta not needed, just read sql select * from sysjumps where datetime = datetime.max(); this is old, I now need to figure out how to do this with HDF5
#ship average popular time, need to get zscore and then I need to determine what a popular time is, is it 70% more than the std? 
#ship jump trending



#sys sov for last hour
#sys owned by last hour
#sys sov trend
#sys last hour vul start

#ship kills last hour (player ships, npc, pods)
#ship kills avg
#ship kill std. dev.
#ship kill trending



print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')


#closing statements
#cnx.commit()
#cursor.close()
#cnx.close()

apstSuperEndTime = t.time()
print('APST script completed in: ', apstSuperEndTime-mD.mapDenormalizeStartTime, " seconds.")
