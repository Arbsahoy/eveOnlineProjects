# https://requests.readthedocs.io/en/master/user/install/#install
#import is bringing in libaries to help us use more simple coding teq.
import requests
import json
import mysql.connector
#cnx (connection short hand for the above lib. this allows python to attach to mySQL server)
cnx = mysql.connector.connect(user='admin', password='',
                              host='127.0.0.1',
                              database='sys')
#Being connected to mySQL clear out table data
cursor = cnx.cursor()
cursor.execute('TRUNCATE sys.1DQ1marketData')
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

#template for insert
insert="insert into sys.`1dq1marketdata` values(%(duration)s,	%(is_buy_order)s,	%(issued)s,	%(location_id)s,	%(min_volume)s,	%(order_id)s,	%(price)s,	%(range)s,	%(type_id)s,	%(volume_remain)s,	%(volume_total)s)" 

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


cnx.commit()
cursor.close()
cnx.close()