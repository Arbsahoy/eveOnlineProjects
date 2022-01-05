# https://requests.readthedocs.io/en/master/user/install/#install
#import is bringing in libaries to help us use more simple coding teq.
import requests
import json
import mysql.connector
import time #To time things because it looks good
from datetime import datetime
dateTimeObj = datetime.now()

superStartTime = time.time()
timeStart = time.time()
#cnx (connection short hand for the above lib. this allows python to attach to mySQL server)
cnx = mysql.connector.connect(user='admin', password='',
                              host='127.0.0.1',
                              database='sys')
cursor = cnx.cursor()

#Connect to ESI and get refresh token
url = "https://login.eveonline.com/oauth/token"
body = "grant_type=refresh_token&refresh_token="
headers = {
"Content-type":"application/x-www-form-urlencoded",
"User-Agent":"",
"Authorization":"Basic =="
}

response = requests.post(url, 
                        data = body,
                        headers = headers,
                       )
token = json.loads(response.content)
print("using refresh token: " + token["access_token"])

structure = 1030049082711
#while loop in python, len(length)page == (is equal to) 1000
n = 1
page = []

timeEnd = time.time()

print("Connected to SQL, Refresh Token Received.", timeEnd-timeStart)

cursor.execute('TRUNCATE sys.marketdata1dq1')

timeStart = time.time()

#template for insert
insert="insert into sys.`marketdata1dq1` values(%(duration)s,	%(is_buy_order)s,	%(issued)s,	%(location_id)s,	%(min_volume)s,	%(order_id)s,	%(price)s,	%(range)s,	%(type_id)s,	%(volume_remain)s,	%(volume_total)s, DEFAULT)" 

while(n == 1 or len(page) == 1000):
  url = f'https://esi.evetech.net/latest/markets/structures/{structure}/?datasource=tranquility&page={n}&token={token["access_token"]}'
  headers = {
    "Accept": "application/json"
  }
  response = requests.get(url,headers=headers)
  page = json.loads(response.content)
  print(f'retrieved page {n} with {len(page)} items')
  #for each item in page assign it to it and run and execute "it" 
  for it in page:
    cursor.execute(insert,it)
  n=n+1

timeEnd = time.time()

print("Paged collection completed: ", timeEnd-timeStart)

timeStart = time.time()

cursor.execute('''CREATE TABLE IF NOT EXISTS material1dq1(
	typeID INT NOT NULL,
	materialTypeID INT NOT NULL,
    groupID INT NOT NULL,
    categoryID INT NOT NULL, 
    split FLOAT,
    ttl FLOAT 
)''')

timeEnd = time.time()

print('SQL1 cmd completed: ',timeEnd-timeStart)

timeStart = time.time()

cursor.execute('TRUNCATE TABLE material1dq1')

timeEnd = time.time()

print('SQL2 cmd completed: ',timeEnd-timeStart)

timeStart = time.time()

cursor.execute('''INSERT INTO material1dq1(typeID, materialTypeID, groupID, categoryID, split, ttl)

SELECT 
	invtypematerials.typeID , invtypematerials.materialTypeID , invtypes.groupID as groupID, invtypes.categoryID , 
	(ROUND(ifnull(MAX(buyOrders.price),0)+ifnull(MIN(sellOrders.price),0))/2) as split ,
    ROUND(invtypematerials.quantity * .55)*(ROUND(ifnull(MAX(buyOrders.price),0)+ifnull(MIN(sellOrders.price),0))/2) as ttl
    
FROM invtypematerials

LEFT JOIN (SELECT * FROM marketdata1dq1 WHERE is_buy_order = 0) sellOrders 
ON invtypematerials.materialTypeID = sellOrders.type_id

LEFT JOIN (SELECT * FROM marketdata1dq1 WHERE is_buy_order = 1) buyOrders 
ON invtypematerials.materialTypeID = buyOrders.type_id

LEFT JOIN (SELECT invtypes.typeID, invtypes.groupid , categoryID.categoryID  FROM invtypes

LEFT JOIN (select * from invgroups) categoryID
ON invtypes.groupID = categoryID.groupID) invtypes
ON invtypes.typeID = invtypematerials.typeID

GROUP BY
invtypematerials.PKEY''')

timeEnd = time.time()

print('SQL3 cmd completed: ',timeEnd-timeStart)

timeStart = time.time()

cursor.execute('''CREATE TABLE IF NOT EXISTS 
reprocessing1dq1(
	typeID INT NOT NULL, 
    groupID INT NOT NULL, 
    catagoryID INT NOT NULL, 
    typeName VARCHAR(100),
    qty INT,
    sell FLOAT,
    uID VARCHAR(50))''')

timeEnd = time.time()

print('SQL4 cmd completed: ',timeEnd-timeStart)

timeStart = time.time()

cursor.execute('TRUNCATE TABLE reprocessing1dq1')

timeEnd = time.time()

print('SQL5 cmd completed: ',timeEnd-timeStart)

timeStart = time.time()

cursor.execute('''INSERT INTO reprocessing1dq1(typeID,groupID,catagoryID,typeName,qty,sell,uID)
SELECT 
watchlist1dq1.typeID, watchlist1dq1.groupID, watchlist1dq1.catagoryID, watchlist1dq1.typeName, sellOrders.volume_remain as qty, sellOrders.price AS sell, CONCAT(type_ID, "X", sellOrders.price) as uID
FROM 
watchlist1dq1 

LEFT JOIN (SELECT * FROM marketdata1dq1 WHERE is_buy_order = 0) sellOrders 
ON watchlist1dq1.typeid = sellOrders.type_id''')

timeEnd = time.time()

print('SQL6 cmd completed: ',timeEnd-timeStart)



cnx.commit()
cursor.close()
cnx.close()
superEndTime = time.time()
print('Python reached end of script: ', superEndTime-superStartTime)
