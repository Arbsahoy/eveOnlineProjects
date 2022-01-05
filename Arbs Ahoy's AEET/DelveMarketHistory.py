# https://requests.readthedocs.io/en/master/user/install/#install
#import is bringing in libaries to help us use more simple coding teq.
import requests
import json
import mysql.connector
from datetime import datetime
#cnx (connection short hand for the above lib. this allows python to attach to mySQL server)
cnx = mysql.connector.connect(user='admin', password='',
                              host='127.0.0.1',
                              database='sys')
cursor = cnx.cursor()

#no key is needed to grab esi data as this is a public API

#region = 10000060


#template for insert
insert="insert into sys.`regionhistory1dq1` values(%(average)s,%(date)s,%(highest)s,%(lowest)s,%(order_count)s,%(volume)s)" 

for x in [34,35,36,37]:
  url = f'https://esi.evetech.net/latest/markets/10000060/history/?datasource=tranquility&type_id={x}'
  headers = {
    "Accept": "application/json"
  }
  response = requests.get(url,headers=headers)
  page = json.loads(response.content)
cursor.executemany(insert,page)


cnx.commit()
cursor.close()
cnx.close()
dateTimeObj = datetime.now()
print(dateTimeObj)