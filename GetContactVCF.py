import threading
import urllib
import urllib.parse
import urllib.error
import urllib.request
import urllib.response
import json
import time
import os

def post(rawData):
	jsondata = json.dumps(rawData)
	url = urllib.request.Request("https://metazombies.ml/whatsapp_requests.php",jsondata.encode())
	url.add_header("Content-Type","application/json")
	data = urllib.request.urlopen(url, timeout=10).read().decode('utf8', 'ignore')
	return data
data = post({'command':'getUserData','password':'#EDC4rfv'})
print(data)
jsonObj = json.loads(data)
del jsonObj['success']
for key in jsonObj:
	user = jsonObj[key]
	print('BEGIN:VCARD')
	print('VERSION:2.1')
	print("N:;{};;;".format(user['USERID']))
	print("FN:{}".format(user['USERID']))
	print("TEL;CELL:{}".format(user['CELLNUMBER']))
	print('END:VCARD')

