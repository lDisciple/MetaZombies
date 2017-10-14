from whatsappHandler import WhatsappHandler
from inputHandler import InputHandler
import os
import time
import networkHandler as server
import json


#########################################
#	   ~~~Setup Config~~~		#
#########################################
cfgFile = open(os.getcwd() + "/Config.cfg", "r")
config = {}
for line in cfgFile:
	parts = line.strip().split("=")
	config[parts[0]] = parts[1]

#########################################
#	   ~~~Input Handling~~~		#
#########################################
"""
Looks in the TODO directory and gets commands from files with the prefix "Task_"
Then returns the list for processing
"""
def getFileCommands():
	commandFiles = os.listdir(os.getcwd() + "/TODO")
	commands = []
	for fileName in commandFiles:
		if "task" in fileName:
			f = open(os.getcwd() + "/TODO/" + fileName,"r")
			for line in f:
				commands.append(line)
			os.rename(os.getcwd() + "/TODO/" + fileName,os.getcwd() + "/TODO/" + fileName.replace("task","completed"))
			f.close()
	return commands
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
	
"""
Method for handling commands coming from Whatsapp
"""
def handleOutgoingCommand(whatsappHandler,networkHandler,logFile,command):
	args = command.strip().replace("  "," ").split(" ")
	#Args[0] is the command and after is the parameters
	if not 'Metazombies' in args[1] and not 'Horde' in args[1] and not 'Requests' in args[1]:
		if args[0].lower() in phoneCommands:
			try:
				reply = phoneCommands[args[0].lower()](*tuple(args[1:]))
				if reply != None:
					whatsappHandler.sendMessage(args[1],reply)
				logFile.write("[TRANSFERRED] " + command+"\n")
			except (TypeError,ValueError) as error:
				whatsappHandler.sendMessage(args[1],"That's not how that command works, type 'help' for more info.")
				logFile.write("[ERROR] " + command + " \n\tReason: Incorrect usage of phone command: " + error.args[0] + "\n")
		else:
			whatsappHandler.sendMessage(args[1],"That command does not exist, type 'help' for more info.")
			logFile.write("[ERROR] " + command + " \n\tReason: No such phone command\n")
"""
Method for handling commands coming from TODO directory or command line.
Commands can be found in the commands list
Format: <CommandName>~~<arg1>~~<arg2>~~...
"""
def handleIncomingCommand(whatsappHandler, logFile, command):
	#Args[0] is the command and after is the parameters
	args = command.split("~~")
	if args[0] in commands:
		try:
			commands[args[0]](*tuple(args[1:]))
			logFile.write("[SUCCESS] " + command+"\n")
		except TypeError as error:
			print(error)
			logFile.write("[ERROR] " + command + " \n\tReason: Incorrect usage of command: " + error.args[0] + "\n")
	else:
		if args[0].lower() != "stop":
			print("No such command exists " + args[0].lower())
			logFile.write("[ERROR] " + command + " \n\tReason: No such command\n")

	

#########################################
#	    ~~~Command Setup~~~		#
#########################################
whatsappHandler = WhatsappHandler(config["GeckoDriverPath"])
serverConn = server.NetworkHandler(config["phpUrl"],config["phpPassword"])

def sendMessage(userID,text,handler = whatsappHandler):
	userID = '+27'+serverConn.getCellphone(userID)[1:]
	handler.sendMessage(userID,text)

def kill(userID, killerID, handler = whatsappHandler):
	sendMessage(userID,"You have been killed by " + serverConn.getUsername(killerID)+
		"\nWelcome to the walking dead. Time to find a revive or feed off the living.\n"
		+"If you need help on how to be a zombie check out the rules at www.metazombies.tk")
	sendMessage(killerID,"Well done! You killed " + serverConn.getUsername(userID))
	handler.addGroupParticipant(config["ZombieGroupName"],userID)

	
def package(userID, claimID,handler = whatsappHandler):
	sendMessage(userID,"You claimed {}*****!".format(claimID[:2]))

		
def sendLeaderboard(userID,data,handler = whatsappHandler):
	jsondata = json.loads(data)
	text = ""
	text+= ("*Zombie Leaderboard:*\n")
	count = 1
	for key in jsondata['zombies']:
		text+= ("%-4s%s\n%15s\n" % (str(count)+".",key['USERNAME']+":",key['ZOMBIESCORE']))
		count += 1
	count=1
	text+= ("\n*Human Leaderboard:*\n")
	for key in jsondata['humans']:
		text+= ("%-4s%s\n%8s\n" % (str(count)+".",key['USERNAME']+":",key['HUMANSCORE']))
		count += 1
	count=1
	text+= ("\n*Sections Leaderboard:*\n")
	for key in jsondata['sections']:
		text+= ("%-4s%s\n%8s\n" % (str(count)+".",key['SECTIONNAME']+":",key['SCORE']))
		count += 1
	sendMessage(userID,text)	
	
def sendStatus(userID,data,handler = whatsappHandler):
	jsondata = json.loads(data)['0']
	text = ""
	text += "*{}*\n".format(jsondata['USERNAME'])
	text += "{}\n".format(jsondata['STUDENTNUMBER'])
	text += "{} ({})\n".format(jsondata['USERID'],jsondata['STATUS'])
	if jsondata['STATUS'] == 'human':
		text += "{} hearts left.\n".format(jsondata['HEARTS'])
		timeLeft = int(jsondata['NEXTHEART'])
		text+= "{}hr min{}\n".format(int(timeLeft/3600),int((timeLeft%3600)/60))
	text += "_Zombie Score:_\n" 
	text += " "+jsondata['ZOMBIESCORE']+"\n"
	text += "_Human Score:_\n" 
	text += " "+jsondata['HUMANSCORE']+"\n"
	sendMessage(userID,text)




def revive(userID, handler = whatsappHandler):
	sendMessage(userID,"It's Alive!!!\n"
		+"Well done you claimed a revive!")	
	#handler.removeGroupParticipant(config["ZombieGroupName"] ,userID,False)

def userDied(userID, handler = whatsappHandler):
	sendMessage(userID,"You have starved... But not to fear, zombie-kind took pity on you and you have joined their ranks." +
		"\nWelcome to the walking dead. Time to find a revive or feed off the living.\n"
		+"If you need help on how to be a zombie read the rules at www.metazombies.tk")
	handler.addGroupParticipant(config["ZombieGroupName"],userID)

def news(text,handler = whatsappHandler):
	handler.selectContactAt(config["GeneralBroadcastIndex"])
	handler.sendToSelected(text)

def zednews(text,handler = whatsappHandler):
	sendMessage(config["ZombieGroupName"],text)

def sendToAdmin(userID,handler = whatsappHandler):
	#handler.sendMessage(config["AdminGroupName"],serverConn.getCellphone(userID) + " - " + text)
	sendMessage(userID,"Your contact has been sent to the admins. Please wait for them to get back to you.")
	sendMessage(config["AdminGroupName"],"+27"+serverConn.getCellphone(userID)[1:] + " needs help.")

def endGame(handler = whatsappHandler):
	handler.selectContactAt(config["GeneralBroadcastIndex"])
	handler.sendToSelected("Metazombies is finished!!!")
	addCommandToQueue("stop")

def sendHelp(userID ,handler = whatsappHandler):
	sendMessage(userID,"*Welcome To MetaZombie Mobile!*\n"
		+"To use this platform all you have to do is send a command to this contact.\n\n"
		+"*Commands:*\n"
		+"_Info:_\n Sends this help message\n"
		+"_Kill [Users ID]:_\n This will kill the user with the ID given in place of [Users ID]\n"
		+"_Claim [Claim ID]:_\n This will claim the package with the ID given in place of [Claim ID] (e.g. revive code or health code.)\n"
		+"_Scores:_\n Sends through the current scoreboard.\n"
		+"_Status:_\n This will send through your current health and overall status.\n"
		+"_Survivors:_\n Sends back a list fo the living.\n"
		+"_Contact:_\n This will request an admin to contact you.\n\n"
		+"Note do not send too many commands too quickly or they may be ignored.\n"
		)

def sendLiving(userID,data):
	jsondata = json.loads(data);
	text = ""
	for key in jsondata:
		text += key['USERNAME']+"\n"
	sendMessage(userID,"*Survivors:*\n"+text)

def registerUser(userID ,handler = whatsappHandler):
	handler.sendMessage(userID,"Welcome to Metazombies Whatsapp!\n Type 'info' for help on how to use Metazombies Mobile")
	handler.addGroupParticipant('Metazombies News',userID)

commands = {
	#Direct commands
		"select" : whatsappHandler.selectContact,
		"send" : whatsappHandler.sendMessage,
		"open" : whatsappHandler.openNewChat,
		"listContacts" : whatsappHandler.listContacts,
		"removeGroupParticipant" : whatsappHandler.removeGroupParticipant,
		"resetSize" : whatsappHandler.resetSize,
		"checkFor" : whatsappHandler.checkFor,
		"hoverOver" : whatsappHandler.hoverOver,
		"click" : whatsappHandler.clickElement,
		"check" : whatsappHandler.checkForMessages,
		"getAt" : whatsappHandler.printElementsAt,
		"addGroupParticipant" : whatsappHandler.addGroupParticipant,
		"selectAt" : whatsappHandler.selectContactAt,
	#PHP commands [Whatsapp API] - Need Users ID as parameter, possibly code
		"kill": kill,
		"claim": package,
		"revive": revive,
		"die": userDied,
		"news": news,
		"zednews": zednews,
		"sendToAdmin" : sendToAdmin,
		"endGame": endGame,
		"sendstatus": sendStatus,
		"sendleaderboard": sendLeaderboard,
		"sendliving" : sendLiving
	}

phoneCommands = {
		"kill" : serverConn.kill,
		"claim" : serverConn.claim,

		"help" : sendHelp,
		"info" : sendHelp,

		"score" : serverConn.getLeaderboard,
		"scores" : serverConn.getLeaderboard,
		"leaderboard" : serverConn.getLeaderboard,

		"contact" : sendToAdmin,
		"complain" : sendToAdmin,
		"admin" : sendToAdmin,
		
		"survivors" : serverConn.getLiving,

		"status" : serverConn.getStatus,
		"start" : registerUser
	}

#########################################
#	   	~~~Main~~~		#
#########################################
if __name__ == '__main__':
	# 1. Start whatsapp web handler (Uses commandline for confirmation)
	whatsappHandler.start()
	while not whatsappHandler.isReady():
		time.sleep(1)
	# 2. Start waiting for commandline commands
	inputHandler = InputHandler()
	inputHandler.start()
	# 3. Start network handler (Long Polling)
	serverConn.start()

	logFile = open(os.getcwd() + "/log.txt", "a")
	running = True

	
	while running:
		try:
			#Check for incoming commands
			incomingCommands =  getFileCommands() + serverConn.getCommands()
			for command in incomingCommands:
				handleIncomingCommand(whatsappHandler,logFile,command)
				time.sleep(0.1)
			#Check for input commands
			inputCommands = inputHandler.getInput()
			for command in inputCommands:
				running = running and command != "stop"
				handleIncomingCommand(whatsappHandler,logFile,command)
				time.sleep(0.1)
			#Check for outgoing commands
			outgoingCommands = whatsappHandler.getCommands()
			for command in outgoingCommands:
				handleOutgoingCommand(whatsappHandler,serverConn,logFile,command)
				time.sleep(0.1)
			time.sleep(1)
			#Check for new messages
			whatsappHandler.checkForMessages(False)
			time.sleep(1)
			logFile.flush()
		except KeyboardInterrupt:
			running = False
	#Clean up
	logFile.close()
	whatsappHandler.stop()
	inputHandler.stop()
	serverConn.stop()
	print("Press Enter to exit")


