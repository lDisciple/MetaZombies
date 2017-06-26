import threading
import urllib
import urllib.parse
import urllib.error
import urllib.request
import urllib.response
import json

def getUsername(userID):
	return "Bob"






class NetworkHandler(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self._commands = []

	def run(self):
		True
		#Long poll for updates

	def sendRequest(self):
		True#TODO Finish stub

	def parseUpdates(self):
		True#TODO Finish stub

	def getLeaderboard(self,userID):
		True #TODO Finish stub

	def getStatus(self,userID):
		True #TODO Finish stub

	def claim(self,userID, claimID):
		True #TODO Finish stub

	def getCommands(self):
		ret = self._commands
		self._commands = []
		return ret
		
if __name__ == '__main__':
	#net = NetworkHandler()
	#net.start()
	#net.claim("1","2")
	#POST
	#data = json.dumps({'password':'password','command':'kill'})
	#url = urllib.request.Request("https://metazombies.000webhostapp.com/whatsapp_test.php",data.encode())
	#url.add_header("Content-Type","application/json")
	#data = urllib.request.urlopen(url).read().decode('utf8', 'ignore')
	#print(data)
