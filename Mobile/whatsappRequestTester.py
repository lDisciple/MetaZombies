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
def getUserStatus(user):
	data = post({'command':'getUserStatus','userID':user})
	jsonObj = json.loads(data)
	userdata = jsonObj['0']
	print(userdata['USERNAME']+" ["+userdata['USERID'] + "]: " + userdata['STATUS'] +  " (" + userdata['HUMANSCORE'] + "/" + userdata['ZOMBIESCORE'] + ")");

data = post({'command':'claim','userID':'be74486','code':'qu79jmn9','password':'#EDC4rfv'})
print(data)
"""
data = "\t"+post({'command':'getLeaderboard'})
jd = json.loads(data)
print(jd)
text = ""
text+= ("*Zombie Leaderboard:*\n")
count = 1
for key in jd['zombies']:
	text+= ("%-4s%-25s%s\n" % (str(count)+".",key['USERNAME']+":",key['ZOMBIESCORE']))
	count += 1
count=0
text+= ("\n*Human Leaderboard:*\n")
for key in jd['humans']:
	text+= ("%-4s%-25s%s\n" % (str(count)+".",key['USERNAME']+":",key['HUMANSCORE']))
	count += 1
print(text)
"""
"""
print('User status')
getUserStatus('be74486')
data = post({'command':'getUserData'})
jsonObj = json.loads(data)
print ("User data")
for record in [x for x in jsonObj if x != 'success']:
	recordData = jsonObj[record]
	print("\t"+recordData['USERNAME'] + " " + recordData['USERID'] + " +27" + recordData['CELLNUMBER'][1:] + " " + recordData['STUDENTNUMBER'])
#curl -H "Content-Type: application/json" -X POST -d '{"command":"getLeaderboard"}' http://localhost/whatsapp_requests.php
print('Claim:')
print("\t"+post({'command':'claim','userID':'be74486','code':'abcdefg'}))
print('Claim: bad code')
print("\t"+post({'command':'claim','userID':'be74486','code':'abcefg'}))
print('Claim: bad id')
print("\t"+post({'command':'claim','userID':'b4486','code':'abcdefg'}))
print('Leaderboard')
print("\t"+post({'command':'getLeaderboard'}))
print('Kill')
getUserStatus('be74486')
getUserStatus('0853e70')
print("Kill\t"+post({'command':'kill','victimID':'0853e70','killerID':'be74486'}))
getUserStatus('be74486')
getUserStatus('0853e70')
print("Revive\t"+post({'command':'claim','userID':'0853e70','code':'12345'}))
getUserStatus('be74486')
getUserStatus('0853e70')
print()
"""
#INSERT INTO `Claims`('id',`type`, `claimValue`, `timeStart`, `timeValid`, `usesRemaining`) VALUES ('abcdefg',0,100,1500,36000,15)
#INSERT INTO `metazomb_MetazombiesDB`.`Claims` (`ID`, `type`, `claimValue`, `timeStart`, `timeValid`, `usesRemaining`) VALUES ('abcdefg', '0', '100', CURRENT_TIMESTAMP, '10000', '15');