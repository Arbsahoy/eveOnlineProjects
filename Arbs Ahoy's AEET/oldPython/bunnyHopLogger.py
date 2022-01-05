import requests #for url getting.
import json #for reading json data.
import mysql.connector #to connect to the SQL server.
import time #to time things because.... I like to time things? 
import pandas as pd
import os #to delete files and stuffs

bunnyHopLoggerStartTime = time.time() #setting a start time for the script

#cnx (connection short hand for the above lib. this allows python to attach to mySQL server)
cnx = mysql.connector.connect(user='vsserver', password='',
                              host='192.168.1.13',
                              database='sys')
cursor = cnx.cursor()
print("Connected to MySQL")

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Get ship kills
start = time.time()
#template for SQL Query
insert = f"INSERT INTO sys.`shipkills` VALUES(%(npc_kills)s, %(pod_kills)s, %(ship_kills)s, %(system_id)s, DEFAULT)"

#url to fetch ship jumps by system ID
url='https://esi.evetech.net/latest/universe/system_kills/?datasource=tranquility'
headers = {
    "Accept": "application/json"
    }
response = requests.get(url,headers=headers)
shipkills = json.loads(response.content)
for data in shipkills:
    cursor.execute(insert,data)
print("Added new ship kill SQL data.")

shipKillSQLtoHDF5 = pd.read_sql("SELECT * FROM sys.shipkills", cnx)

if os.path.exists("/root/EveOnline/Spy/HDF5/shipkill") :
   os.remove("/root/EveOnline/Spy/HDF5/shipkill")

shipKillSQLtoHDF5.to_hdf('/root/EveOnline/Spy/HDF5/shipkill', key='shipKillSQLtoHDF5', mode='a', append=True, format='table')
print("Added new ship kill data to HDF5.")

end = time.time()
print("System Ship Kills Loaded into SQL:", end-start)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Get Sov Data
start = time.time()
#template for SQL Query
insert = f"INSERT INTO sys.`sov` VALUES(%(alliance_id)s, %(solar_system_id)s, %(structure_id)s, %(structure_type_id)s, %(vulnerability_occupancy_level)s, %(vulnerable_end_time)s, %(vulnerable_start_time)s, DEFAULT)"

#url to fetch ship jumps by system ID
url='https://esi.evetech.net/latest/sovereignty/structures/?datasource=tranquility'
headers = {
    "Accept": "application/json"
    }

response = requests.get(url,headers=headers)
sov = json.loads(response.content)
DEFAULT_OCCUPANCY = 0
for data in sov:
    data['vulnerability_occupancy_level'] = data.get('vulnerability_occupancy_level', DEFAULT_OCCUPANCY )
    data['vulnerable_end_time'] = data.get('vulnerable_end_time', DEFAULT_OCCUPANCY )
    data['vulnerable_start_time'] = data.get('vulnerable_start_time', DEFAULT_OCCUPANCY )
    cursor.execute(insert, data)
print("Added new sov SQL data")

sovSQLtoHDF5 = pd.read_sql("SELECT * FROM sys.sov", cnx)

if os.path.exists("/root/EveOnline/Spy/HDF5/sov") :
   os.remove("/root/EveOnline/Spy/HDF5/sov")

sovSQLtoHDF5.to_hdf('/root/EveOnline/Spy/HDF5/sov', key='sovSQLtoHDF5', mode='a', append=True, format='table')
print("Added new sov data to HDF5")

end = time.time()
print("Sov Data Loaded into SQL:", end-start)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Get Ship Jumps
start = time.time()

#template for SQL Query
insert = f"INSERT INTO sys.`shipjumps` VALUES(%(ship_jumps)s, %(system_id)s, DEFAULT)"

#url to fetch ship jumps by system ID
url='https://esi.evetech.net/latest/universe/system_jumps/?datasource=tranquility'
headers = {
    "Accept": "application/json"
    }

response = requests.get(url,headers=headers)
shipjumps = json.loads(response.content)
for data in shipjumps:
    cursor.execute(insert,data) 
print("Added new ship jump data SQL")

shipJumpSQLtoHDF5 = pd.read_sql("SELECT * FROM sys.shipjumps", cnx)
os.remove('/root/EveOnline/Spy/HDF5/shipjump')
shipJumpSQLtoHDF5.to_hdf('/root/EveOnline/Spy/HDF5/shipjump', key='shipJumpSQLtoHDF5', mode='a', append=True, format='table')
print("Added new ship jump data to HDF5")

end = time.time()
print("System Ship Jumps Loaded into SQL:", end-start)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-



#ending list of thing
cnx.commit()
cursor.close()
cnx.close()

bunnyHopLoggerEndTime = time.time()
print("total update time: ", bunnyHopLoggerEndTime-bunnyHopLoggerStartTime)
