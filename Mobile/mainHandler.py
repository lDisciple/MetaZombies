from whatsappHandler import WhatsappHandler
from inputHandler import InputHandler
import os
import time
import networkHandler as server


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
	fileName = os.listdir(os.getcwd() + "/TODO/task_queue_" + str(time.time()))
	f = open(fileName,"w")
	f.write(command)
	f.close()

def addCommandsToQueue(commands):
	fileName = os.listdir(os.getcwd() + "/TODO/task_queue_" + str(time.time()))
	f = open(fileName,"w")
	for command in commands:
		f.write(command)
	f.close()
	
"""
Method for handling commands coming from Whatsapp
"""
def handleOutgoingCommand(whatsappHandler,networkHandler,logFile,command):
	#Args[0] is the command and after is the parameters
	args = command.replace("  "," ").split(" ")
	if args[0].lower() in phoneCommands:
		try:
			phoneCommands[args[0]](*tuple(args[1:]))
			logFile.write("[TRANSFERRED] " + command)
		except TypeError as error:
			handler.sendMessage(args[1],"That's not how that command works, type 'help' for more info.")
			logFile.write("[ERROR] " + command + " \n\tReason: Incorrect usage of phone command: " + error.args[0] + "\n")
	else:
		handler.sendMessage(args[1],"That command does not exist, type 'help' for more info.")
		logFile.write("[ERROR] " + command + " \n\tReason: No such phone command\n")
	print(command)
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
			logFile.write("[SUCCESS] " + command)
		except TypeError as error:
			print(error)
			logFile.write("[ERROR] " + command + " \n\tReason: Incorrect usage of command: " + error.args[0] + "\n")
	else:
		if args[0] != "stop":
			print("No such command exists")
			logFile.write("[ERROR] " + command + " \n\tReason: No such command\n")

	

#########################################
#	    ~~~Command Setup~~~		#
#########################################
whatsappHandler = WhatsappHandler(config["GeckoDriverPath"])
serverConn = networkHandler.NetworkHandler()

def kill(userID, killerName, successful, handler = whatsappHandler):
	if successful:
		handler.sendMessage(userID,"You have been killed by " + serverConn.getUsername(killerID)+
			"\nWelcome to the walking dead. Time to find a revive or feed off the living.\n"+
			+"If you need help on how to be a zombie type 'info'")
		handler.sendMessage(userID,"Well done! You killed " + serverConn.getUsername(userID))
		addCommandToQueue("addGroupParticipant~~" + config["ZombieGroupName"] + "~~" + userID)
	else:
		handler.sendMessage(userID,"Could not kill that user.\n"
			+"Remember you cannot kill the dead!\n"
			+"Try again on the website if this problem persists.")

	
def package(userID, successful,handler = whatsappHandler):
	if successful:
		handler.sendMessage(userID,"You claimed a package!")
	else:
		handler.sendMessage(userID,"Your claim failed, the package is probably empty...\n"
			+"Try claim it on the website if the problem persists.")

def revive(userID, successful, handler = whatsappHandler):
	if successful:
		handler.sendMessage(userID,"It's Alive!!!\n"
			+"Well done you claimed a revive!")	
		addCommandToQueue("removeGroupParticipant~~" + config["ZombieGroupName"] + "~~" + userID)
	else:
		handler.sendMessage(userID,"Your claim failed, someone probably beat you to that revive...\n"
			+"Try claim it on the website if the problem persists.")

def news(text,handler = whatsappHandler):
	handler.selectContactAt(config["GeneralBroadcastIndex"])
	handler.sendToSelected(text)

def zednews(text,handler = whatsappHandler):
	handler.sendMessage(config["ZombieGroupName"],text)

def sendToAdmin(userID, text,handler = whatsappHandler):
	handler.sendMessage(config["AdminGroupName"],userID + " - " + text)

def endGame(handler = whatsappHandler):
	handler.selectContactAt(config["GeneralBroadcastIndex"])
	handler.sendToSelected("Metazombies is finished!!!")
	addCommandToQueue("stop")

def sendHelp(userID ,handler = whatsappHandler):
	handler.sendMessage(userID,"Help page")#TODO Finish help

def registerUser(userID ,handler = whatsappHandler):
	handler.sendMessage(userID,"It's Alive!!!\n"
			+"Well done you claimed a revive!")#TODO Finish

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
		"getAt" : whatsappHandler.printElementsAt,
		"addGroupParticipant" : whatsappHandler.addGroupParticipant,
		"selectAt" : whatsappHandler.selectContactAt,
	#PHP commands [Whatsapp API] - Need Users ID as parameter, possibly code
		"kill": kill,
		"package": package,
		"revive": revive,
		"news": news,
		"zednews": zednews,
		"sendToAdmin" : sendToAdmin,
		"endGame": endGame
	}

phoneCommands = {
		"kill" : serverConn.claim,
		"claim" : serverConn.claim,

		"help" : sendHelp,
		"info" : sendHelp,

		"score" : serverConn.getLeaderboard,
		"scores" : serverConn.getLeaderboard,
		"leaderboard" : serverConn.getLeaderboard,

		"contact" : sendToAdmin,
		"complain" : sendToAdmin,
		"admin" : sendToAdmin,

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
	logFile = open(os.getcwd() + "/log.txt", "a")
	running = True
	while running:
		try:
			#Check for incoming commands
			incomingCommands = inputHandler.getInput() + getFileCommands()
			for command in incomingCommands:
				running = running and command != "stop"
				handleIncomingCommand(whatsappHandler,command)
				time.sleep(0.1)
			#Check for outgoing commands
			outgoingCommands = whatsappHandler.getCommands()
			for command in outgoingCommands:
				running = running and command != "stop"
				handleOutgoingCommand(whatsappHandler,serverConn,command)
				time.sleep(0.1)
			time.sleep(1)
			#Check for new messages
			whatsappHandler.checkForMessages(False)
			time.sleep(1)
		except KeyboardInterrupt:
			running = False
	#Clean up
	whatsappHandler.stop()
	inputHandler.stop()
	print("Press Enter to exit")


