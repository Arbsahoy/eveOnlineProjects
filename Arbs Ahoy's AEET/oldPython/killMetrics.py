#Imports to make the tool work
import sys
sys.path.append('/root/homeProjects/EveOnline/SDE')
import mapDenormalize as mD #to get the area of interest
import pandas as pd #to get dataframes to do analysis with
import time as t #to time thing for a chance to make measureable optimizations
import datetime as dt #so I can convert my strings by time segments
import numpy as np
import scipy.stats as stats
import h5py
from functools import reduce

apstSuperStartTime = t.time()

'''To be removed because this is going to be a called meteric, it'll be asked in APST.py
'''
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

#timer
playfileSuperStartTime = t.time()

#read the kill hdf5
shipKills = pd.read_hdf('/root/homeProjects/EveOnline/Spy/HDF5/shipkill', mode='r')

#merge the selected region of interest
mergedList = systemsOfInterest.merge(shipKills, how='left', left_on='itemID', right_on='system_id').set_index('itemID')

#delete the extreous information
del mergedList['system_id']

#set timestamp to MM/DD/YY HH:MM:00:00
mergedList['timestamp'] = mergedList['timestamp'].dt.strftime('%Y-%m-%d %H:%M:00:00')

#max time stamp
maxtime = mergedList['timestamp'].max()

#get the average of all the metrics by itemID

#-=-=-=-#
npcAverage = pd.DataFrame(pd.Series(mergedList.groupby('itemID')['npc_kills'].mean()))

shipAverage = pd.DataFrame(pd.Series(mergedList.groupby('itemID')['ship_kills'].mean()))

podAverage = pd.DataFrame(pd.Series(mergedList.groupby('itemID')['pod_kills'].mean()))

npcSTD = pd.DataFrame(pd.Series(mergedList.groupby('itemID')['npc_kills'].std()))

shipSTD = pd.DataFrame(pd.Series(mergedList.groupby('itemID')['ship_kills'].std()))

podSTD = pd.DataFrame(pd.Series(mergedList.groupby('itemID')['pod_kills'].std()))

latestShipKill = mergedList['ship_kills'].loc[mergedList['timestamp'] == maxtime].groupby('itemID')

#latestNpcKill

#latestPodKill
#-=-=-=-#

everything = [npcAverage,shipAverage,podAverage,npcSTD,shipSTD,podSTD]

protoMerge = reduce(lambda  left,right: pd.merge(left,right,on=['itemID'], how='left'), everything)

finalMerge = protoMerge.rename(columns={'npc_kills_x' : 'npcKillAvg', 'ship_kills_x' : 'shipKillAvg' , 'pod_kills_x' : 'podKillAvg', 'npc_kills_y' : 'npcKillStd', 'ship_kills_y' : 'shipKillStd', 'pod_kills_y' : 'podKillStd'})

print(finalMerge)