# https://requests.readthedocs.io/en/master/user/install/#install
#import is bringing in libaries to help us use more simple coding teq.
import requests
import json
import mysql.connector
import time
import urllib
from datetime import datetime
dateTimeObj = datetime.now()

timestampStr = dateTimeObj.strftime("%d-%b (%H:%M:%S.%f)")

#cnx (connection short hand for the above lib. this allows python to attach to mySQL server)
cnx = mysql.connector.connect(user='admin', password='',
                              host='127.0.0.1',
                              database='sys')
cursor = cnx.cursor()

#Connect to ESI and get refresh token - Alpha Token
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
print("Using refresh token: " + token["access_token"])

characterID = 2116122920

url = f'https://esi.evetech.net/latest/characters/{characterID}/wallet/transactions/?datasource=tranquility&token={token["access_token"]}'
headers = {
    "Accept": "application/json"
  }

insert = "INSERT IGNORE INTO sys.maggieswallet VALUES(%(client_id)s, %(date)s, %(is_buy)s, %(is_personal)s, %(journal_ref_id)s, %(location_id)s, %(quantity)s, %(transaction_id)s, %(type_id)s, %(unit_price)s)"

response = requests.get(url,headers=headers)
page = json.loads(response.content)

for it in page:
  cursor.execute(insert,it)

cnx.commit()

cursor.close()
cnx.close()