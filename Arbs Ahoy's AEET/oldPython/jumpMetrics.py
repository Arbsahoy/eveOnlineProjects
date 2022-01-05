import sys
sys.path.append('/root/EveOnline/SDE')
import pandas as pd #to get dataframes to do analysis with
import time as t #to time thing for a chance to make measureable optimizations
import numpy as np
import scipy.stats as stats
import datetime as dt
import h5py

playfileSuperStartTime = t.time()
print(".")

shipJumps = pd.read_hdf('/root/EveOnline/Spy/HDF5/shipjump', mode='r')
print("..")

#systemsOfInterest = pd.read_csv('/root/EveOnline/SDE/CSV/systemOfInterestDelve.csv')
#print("...")

#mergedList = systemsOfInterest.merge(shipJumps, how='left', left_on='itemID', right_on='system_id').set_index('itemID')
#print("....")

#del mergedList['system_id']
#print(".....")

systemAverage = shipJumps.groupby('system_id')['ship_jumps'].mean()
print("......")

systemSTD = shipJumps.groupby('system_id')['ship_jumps'].std()
print(".......")

mergedListavg = shipJumps.merge(systemAverage, how='left', on='system_id').rename(columns={'ship_jumps_x' : 'shipJumps', 'ship_jumps_y' : 'sysJumpAVG'})
print("........")

mergedListstd = mergedListavg.merge(systemSTD, how='left', on='system_id').rename(columns={'ship_jumps' : 'SysSTD'})
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
print(mergedListstd)
#mergedListstd.to_hdf('/root/EveOnline/Spy/HDF5/shipJumpMetrics', key='mergedListstd', mode='a', append=True, format='table')
