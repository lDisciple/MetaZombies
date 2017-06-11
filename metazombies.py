from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.common.tools			       import Jid
from stackThread import StackThread
from inputInterrupt import InputInterrupt
import signal
import os
import sys
import time

def acknowledgeMessageDelivery(stackThread, ackID):
	newContents = ""
	fIn = open(os.getcwd() + "/UndeliveredMessages.txt","r")
	for line in fIn:
		if not line.startswith(ackID) and len(line) > 1:
			newContents += line
	fIn.close()
	fOut = open(os.getcwd() + "/UndeliveredMessages.txt","w")
	fOut.write(newContents.strip())
	fOut.close()

def doCommand(stackThread,command, showErrors = True):
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
		if showErrors:
			errorFile.write("Failed: " + command + " Reason: No such command\n")
	
def doFileCommands(stackThread):
	commandFiles = os.listdir(os.getcwd() + "/TODO")
	for fileName in commandFiles:
		if "task" in fileName:
			f = open(os.getcwd() + "/TODO/" + fileName,"r")
			for line in f:
				doCommand(stackThread1,line)
			os.rename(os.getcwd() + "/TODO/" + fileName,os.getcwd() + "/TODO/" + fileName.replace("task","completed"))
			f.close()

def interruptHandler(signum, frame):
	raise InputInterrupt()

####################################
#Main
####################################

stackThread1 = StackThread()
stackThread1.start()
commands = {
		"select" : stackThread1.selectContact,
		"send" : stackThread1.sendMessage,
		"check" : stackThread1.findUnreadContacts,
		"open" : stackThread1.openNewChat,
		"listContacts" : stackThread1.listContacts,
		"removeGroupParticipant" : stackThread1.removeGroupParticipant,
		"resetSize" : stackThread1.resetSize,
		"checkFor" : stackThread1.checkFor,
		"hoverOver" : stackThread1.hoverOver,
		"click" : stackThread1.clickElement
	}

errorFile = open(os.getcwd() + "/errors.txt", "a")
signal.signal(signal.SIGALRM,interruptHandler)
command = ""
while not stackThread1.isConnected():
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		command = "stop"
print("Enter your commands:")
while command != "stop":
	try:
		command = "";
		doFileCommands(stackThread1)
		signal.alarm(1)#Signal to stop input() after 1 second
		try:
			command = input()
			signal.pause()
		except InputInterrupt:
			True
		if command:
			doCommand(stackThread1,command, showErrors = False)
		time.sleep(1)	
	except KeyboardInterrupt:
	#Stop and wait for the final signal to hit
		command = "stop"
		try:
			signal.pause()
		except InputInterrupt:
			True
stackThread1.disconnect()
stackThread1.join()
errorFile.close()