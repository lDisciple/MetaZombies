from whatsappHandler import WhatsappHandler
from inputHandler import InputHandler
import os
import time

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
Method for handling commands coming from Whatsapp
"""
def handleOutgoingCommand(whatsappHandler,command, showErrors = True):
	True#TODO Finish stub	
"""
Method for handling commands coming from TODO directory or command line.
Commands can be found in the commands list
Format: <CommandName>~~<arg1>~~<arg2>~~...
"""
def handleIncomingCommand(whatsappHandler,command, showErrors = True):
	#Args[0] is the command and after is the parameters
	args = command.split("~~")
	if args[0] in commands:
		try:
			commands[args[0]](*tuple(args[1:]))
		except TypeError as error:
			print(error)
			if showErrors:
				errorFile.write("Failed: " + command + " Reason: Incorrect usage of command: " + error.args[0] + "\n")
	else:
		if args[0] != "stop":
			print("No such command exists")
		if showErrors:
			errorFile.write("Failed: " + command + " Reason: No such command\n")

#########################################
#		~~~Main~~~		#
#########################################
whatsappHandler = WhatsappHandler()
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
		"check" : whatsappHandler.checkForMessages
	}

if __name__ == '__main__':
	# 1. Start whatsapp web handler (Uses commandline for confirmation)
	whatsappHandler.start()
	while not whatsappHandler.isReady():
		time.sleep(1)
	# 2. Start waiting for commandline commands
	inputHandler = InputHandler()
	inputHandler.start()
	errorFile = open(os.getcwd() + "/errors.txt", "a")#TODO judge usefulness
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
				handleOutgoingCommand(whatsappHandler,command)
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

