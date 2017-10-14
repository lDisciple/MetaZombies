import threading
import urllib
import urllib.parse
import urllib.error
import urllib.request
import urllib.response
import json
import time
import os
"""
Method to add a new TODO file with command in it
"""
def addCommandToQueue(command):
	fileName = os.getcwd() + "/TODO/task_queue_" + str(time.time())
	f = open(fileName,"w")
	f.write(command)
	f.close()

def addCommandsToQueue(commands):
	fileName = os.getcwd() + "/TODO/task_queue_" + str(time.time())
	f = open(fileName,"w")
	for command in commands:
		f.write(command)
	f.close()
	

class NetworkHandler(threading.Thread):
	def __init__(self,url,password):
		threading.Thread.__init__(self)
		self._commands = []
		self._url = url
		self._password = password
		self._running = False
		self._userdata = {}
		self._splitter = "/%%:"
	
	def run(self):
		self._running = True
		#Long poll for updates
		while self._running:
			try:
				updates = self.post({'command':'getUpdates'})
				jdata = json.loads(updates)
				for update in jdata:
					self._commands.append(update['command'].strip())
			except:
				pass
			time.sleep(3)

	def post(self,rawData):
			rawData['password'] = self._password
			data = json.dumps(rawData)
			url = urllib.request.Request(self._url,data.encode())
			url.add_header("Content-Type","application/json")
			data = urllib.request.urlopen(url, timeout=10).read().decode('utf8', 'ignore')
			return data
	def loadUserData(self):
		if os.path.exists(os.getcwd() + "/userdata.txt")==False:#Download if absent
			self.downloadUserData()	
		#Load File
		f = open(os.getcwd() + "/userdata.txt","r")
		line = f.readline()
		while len(line) > 0:
			details = line.split(self._splitter)
			self._userdata[details[0]] = {'username':details[1],'studentnum':details[2],'cellphone':details[3]}
			line = f.readline()
		f.close()

	def downloadUserData(self):
		userDataJson = self.getUserData()
		userMap = json.loads(userDataJson)
		toWrite = ""
		for user in userMap:
			if user != 'success':
				details = userMap[user]
				toWrite += "{1}{0}{2}{0}{3}{0}{4}\n".format(self._splitter,details['USERID'],details['USERNAME'],details['STUDENTNUMBER'],details['CELLNUMBER'])
		newFile = open(os.getcwd() + "/userdata.txt","w")
		newFile.write(toWrite)
		newFile.close()

	def getUserDetail(self,userID,detail):
		if len(self._userdata) == 0:#Check if file loaded
			self.loadUserData()
		if not userID in self._userdata:#If user doesnt exist and old file then redownload
			self.downloadUserData()
		if not userID in self._userdata:#If user doesnt exist
			return userID
		else:#User exists
			return self._userdata[userID][detail]

	def findValue(self,m,val,detail):
		found = False
		for key in m:
			if val in m[key][detail]:
				found = True
		return found

	def findUserDetails(self,value,detail):
		if len(self._userdata) == 0:#Check if file loaded
			self.loadUserData()
		if not self.findValue(self._userdata,value,detail):#If user doesnt exist and old file then redownload
			self.downloadUserData()
		if not self.findValue(self._userdata,value,detail):#If user doesnt exist
			return "Unknown("+userID+")"
		else:#User exists
			for key in self._userdata:
				if value in self._userdata[key][detail]:
					return key
		return 'unknown'


	

	def getUsername(self,userID):
		return self.getUserDetail(userID,'username')
	def getCellphone(self,userID):
		return self.getUserDetail(userID,'cellphone')
	def getStudentNumber(self,userID):
		return self.getUserDetail(userID,'studentnum')
	def getUserIDByCell(self,cell):
		return self.findUserDetails(cell,'cellphone')
	def getLeaderboard(self,userID):
		data = self.post({'command':'getLeaderboard'})
		jsondata = json.loads(data);
		if not jsondata['success']:
			addCommandToQueue("send~~"+ self.sanitiseUserID(userID) +"~~Could not load the leaderboard."
			+" Try the website if the problem persists.")
		else:
			addCommandToQueue("sendleaderboard~~"+ userID +"~~" + data)
	def sanitiseUserID(self,userID):
			if '+27' in userID:
				userID = "0"+userID[3:]
				userID = self.getUserIDByCell(userID)
			if userID == 'unknown':
				self.addCommandToQueue("send~~"+ userID +"~~Could not find your user code. Please use the website.")
				userID = 'a385cac'
			return userID

	def getStatus(self,userID):
		data = self.post({'command':'getUserStatus','userID':self.sanitiseUserID(userID)})
		jsondata = json.loads(data);
		if jsondata['success'] != True:
			addCommandToQueue("send~~"+ userID +"~~Error: Could not get your details."
			+" Try the website if the problem persists.")
		else:
			addCommandToQueue("sendstatus~~"+ userID +"~~"+data)

	def getUserData(self):
		return self.post({'command':'getUserData'})
	
	def kill(self,userID, victimID):
		data = self.post({'command':'kill','killerID':self.sanitiseUserID(userID),'victimID':self.sanitiseUserID(victimID)})
		jsondata = json.loads(data);
		if not jsondata['success']:
			addCommandToQueue("send~~"+ userID +"~~Could not kill that user."
			+jsondata['reason']
			+". Try the website if the problem persists.")
	
	
	def claim(self,userID, claimID):
		data = self.post({'command':'claim','userID':self.sanitiseUserID(userID),'code':claimID})
		jsondata = json.loads(data);
		if not jsondata['success']:
			addCommandToQueue("send~~"+ userID +"~~Your claim failed, " + jsondata['reason']
			+". Try claim it on the website if the problem persists.")

	def getLiving(self,userID):
		data = self.post({'command':'getLiving'})
		addCommandToQueue("sendliving~~"+ userID +"~~"+data)
	
	def stop(self):
		self._running = False

	def getCommands(self):
		ret = self._commands
		self._commands = []	
		return ret

	
		
if __name__ == '__main__':
	cfgFile = open(os.getcwd() + "/Config.cfg", "r")
	config = {}
	for line in cfgFile:
		parts = line.strip().split("=")
		config[parts[0]] = parts[1]
	net = NetworkHandler(config['phpUrl'],config['phpPassword'])
	net.start()
	print(net.getUserIDByCell('845810628'))
	
