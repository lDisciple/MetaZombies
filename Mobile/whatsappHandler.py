import sched
import sys
import threading
import time
from colorText import ColorText

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException as WebDriverException

class WhatsappHandler(threading.Thread):

	def __init__(self,geckoPath):
		threading.Thread.__init__(self)
		self._URL = "https://web.whatsapp.com/"
		self._DRIVER_PATH = geckoPath
		self._isConnected = False
		self._isReady = False
		self._driver = None
		self._commands = []
		self._lastMessageIDs = {}

	def run(self):
		try:
			col = ColorText.getColoredText
			#print("Starting stack.loop")
			print("Starting Web.Whatsapp")
			 #Setup the browser
			self._isConnected = False
			self._driver = webdriver.Firefox(executable_path=self._DRIVER_PATH)
			self._driver.get(self._URL)
			while True:
				isConnected = input(col("Phone connected? y/n: \n>", ColorText.HEADER))
				if isConnected.lower() == 'y':
					break
			self._isConnected = True
			self._driver.set_window_size(1366, 10000)
			while True:
				resized = input(col("Is the window resized? y/n: \n>", ColorText.HEADER))
				if resized.lower() == 'y':
					break
				else:
					self._driver.set_window_size(1366, 100000)
			assert "WhatsApp" in self._driver.title
			 #Get ready for new messages
			print("Setting up...")
			self.getStartingMessages()
			self._isReady = True
		except KeyboardInterrupt:
			sys.exit("Startup ended. Press ctrl+C again.")
#Thread management commands
	def isConnected(self):
		return self._isConnected

	def isReady(self):
		return self._isReady

	def stop(self):
		self._driver.quit()
		self._isConnected = False

	def getCommands(self):
		ret = self._commands
		self._commands = []
		return ret

	def resetSize(self):
		self._driver.set_window_size(1366, 100000)
#Whatsapp Functional commands

	def addGroupParticipant(self,group,contact):
		#Select Group
		self.selectContact(group,False)
		#Click header 
		self.waitForAndClick("//div[@id='main']//*[@class='chat-title']")
		#Click add participant
		self.waitForAndClick("//div[@class='app three']//div[@title='Add participant']/div")
		#Select input field and input contact name & enter
		self.waitForAndClick("//div[@class='popup-body']//button")
		inputArea = self._driver.find_element(By.XPATH, "//div[@class='popup-contents']//input")
		if '+27' in contact:
			contact = contact[3:]
		inputArea.send_keys(contact)
		self.waitForAndClick("//div[@class='popup-contents']//div[@class='chat-main']/div[@class='chat-title']")
		if self.checkFor("//div[@id='app']//div[@class='popup-contents']//div[contains(@class,'first infinite-list-item')]//div[@class='chat-body']",False):
			self.waitForAndClick("//div[@id='app']//div[@class='popup-contents']//div[contains(@class,'first infinite-list-item')]//div[@class='chat-body']")
		#Confirm
		self.waitForAndClick("//div[@class='popup']//button[contains(@class,'btn-default')]",timeout = 2)
		if self.checkFor("//div[@class='popup-contents']//span[contains(@class,'icon btn')]",False):
			self.waitForAndClick("//div[@class='popup-contents']//span[contains(@class,'icon btn')]")
		#Close side pane, select old contact
		self.waitForAndClick("//body/div[@id='app']//header[@class='pane-header']//button")
	
	def selectContactAt(self, num):
		chatbody = self._driver.find_element(By.XPATH, "//div[@id='side']//div[@class='chatlist infinite-list']/div[@class='infinite-list-viewport']/div[1]")
		style = chatbody.get_attribute("style")
		height = int(style[style.index("height: ")+8:style.index("px")])
		yPos = str(height*int(num))
		if self.checkFor("//div[@id='side']//div[@class='infinite-list-viewport']/div[contains(@style,'0px, "+yPos+"px,')]//div[@class='chat-body']",False):
			contactPane = self._driver.find_element(By.XPATH, "//div[@id='side']//div[@class='infinite-list-viewport']/div[contains(@style,'0px, "+yPos+"px,')]//div[@class='chat-body']")
			contactPane.click()

	def sendToSelected(self,message):
		if self.checkFor("//*[@id='main']//div[@class='input']",False):
			#Enter text into input of selected contact
			messageArea = self._driver.find_element(By.XPATH, "//*[@id='main']//div[@class='input']")
			messageArea.click()
			messageArea.send_keys(message)
			#Click send button if available (Wont be if no text entered)
			try:
				compose = self._driver.find_element(By.XPATH, "//*[@id='main']//button[contains(@class,'compose-btn-send')]")
				compose.click()
			except selenium.common.exceptions.NoSuchElementException:
					if showText:
						print("No message entered")

		def sendMessage(self,contact,message, showText = True):
			contact = contact.split('\n')[0].strip()
			isNum = False
		if '+27' in contact:
			contact = contact[3:]
			isNum = True
		self.selectContact(contact,False)
		#Test if contact is selected
		selected = False
		try:
			contactTitle = self._driver.find_element(By.XPATH, '//*[@id="main"]//span[@class="emojitext ellipsify"]')
			if contact in contactTitle.text.replace(" ",""):
				selected = True
				
		except selenium.common.exceptions.NoSuchElementException:	
			selected = False
		if selected:
			#Enter text into input of selected contact
			messageArea = self._driver.find_element(By.XPATH, "//*[@id='main']//div[@class='input']")
			messageArea.click()
			for part in message.split("\n"):
				messageArea.send_keys(part)
				ActionChains(self._driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
			#Click send button if available (Wont be if no text entered)
			try:
				compose = self._driver.find_element(By.XPATH, "//*[@id='main']//button[contains(@class,'compose-btn-send')]")
				compose.click()
			except selenium.common.exceptions.NoSuchElementException:
				if showText:
					print("No message entered")

	def selectContact(self,name, showText = True):
		name.strip()
		#Get search box input area
		searchBox = self._driver.find_element(By.XPATH, '//*[@id="side"]//input')
		searchBox.clear()
		#Get focus of search bar
		searchIcon = self._driver.find_element(By.XPATH, '//*[@id="side"]//div[@class="icon icon-search"]')
		searchIcon.click()
		#Enter contact name into search box
		searchBox.send_keys(name)
		searchBox.send_keys(Keys.RETURN)
		#Click the back button if available to reset to start state
		backButton = self._driver.find_element(By.XPATH, '//*[@id="side"]//div[@class="icon icon-back-blue"]')
		if backButton.is_enabled():
			backButton.click()
		#Find out new contacts real title
		try:
			contactTitle = self._driver.find_element(By.XPATH, '//*[@id="main"]//span[@class="emojitext ellipsify"]')
			if showText:
				print(contactTitle.text + " selected")
		except selenium.common.exceptions.NoSuchElementException:	
			if showText:
				print("No contact selected")

	def sendMessage(self,contact,message, showText = True):
		self.selectContact(contact,False)
		found = False
		if '+27' in contact:
			contact = contact[3:]
		#Enter text into input of selected contact
		try:
			contactTitle = self._driver.find_element(By.XPATH, '//*[@id="main"]//span[@class="emojitext ellipsify"]')
			found = contact in contactTitle.text.replace(" ","")
		except selenium.common.exceptions.NoSuchElementException:	
			found = False
		print(str(contact) + " " + contactTitle.text)
		if found:
			messageArea = self._driver.find_element(By.XPATH, "//*[@id='main']//div[@class='input']")
			messageArea.click()
			for part in message.split("\n"):
				messageArea.send_keys(part)
				ActionChains(self._driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
			#Click send button if available (Wont be if no text entered)
			try:
				compose = self._driver.find_element(By.XPATH, "//*[@id='main']//button[contains(@class,'compose-btn-send')]")
				compose.click()
			except selenium.common.exceptions.NoSuchElementException:
				if showText:
					print("No message entered")

	def getStartingMessages(self):
		#Get active contacts (Assume no archived and deleted have no messagse)
		contacts = self._driver.find_elements(By.XPATH, "//div[@id='side']//div[@class='chat-title']")
		for contactElement in contacts:
			#Get contact data and messsage list
			contactName = contactElement.text
			contactElement.click()
			messageList = self._driver.find_elements(By.XPATH, '//*[@id="main"]//div[contains(@class, "message-text")]')
			#Add last message if there is else none.
			if len(messageList) > 0:
				self._lastMessageIDs[contactName] = messageList[len(messageList)-1].get_attribute("data-id")
			else:
				self._lastMessageIDs[contactName] = ""
			

	def checkForMessages(self, showText = True):
		if self._isConnected:
			prevContactTitle = ""
			#Get currently selected contacts title
			try:
				prevContactTitle = self._driver.find_element(By.XPATH, '//*[@id="main"]//span[@class="emojitext ellipsify"]').text
			except selenium.common.exceptions.NoSuchElementException:	
				if showText:
					print("No contact selected - keeping last recieved")
			#Get contacts with unread messages
			unreadContacts = self._driver.find_elements(By.XPATH, "//*[@id='side']/div[@id='pane-side']//span[contains(@class,'unread-count')]")
			for contact in unreadContacts:
				#Select and focus on contact and get message list and name
				contact.click()
				inputBox = self._driver.find_element(By.XPATH, "//div[@id='app']//div[@class='input']")
				inputBox.click()
				messageList = self._driver.find_elements(By.XPATH, '//*[@id="main"]//div[contains(@class, "message-text")]')
				contactName = self._driver.find_element(By.XPATH, '//*[@id="main"]//span[@class="emojitext ellipsify"]').text
				#Add contact to lastMessageIDs if new
				if not contactName in self._lastMessageIDs:
					self._lastMessageIDs[contactName] = ""
				#Read messages from new to old until reach last read message
				for message in reversed(messageList):
					lastMessage = message
					if str(message.get_attribute("data-id")) == self._lastMessageIDs[contactName]:
						break
					if message.get_attribute("data-id")[:5] == 'false':
						comms = message.text.split(" ")
						comms.insert(1,contactName.replace(" ",""))
						retCommand = " ".join(comms)
						self._commands.insert(0,retCommand)
				self._lastMessageIDs[contactName] = messageList[-1].get_attribute("data-id")
					
	
	def openNewChat(self, contact,showText = True):
		#Click new chat button,find contact and select it (Not persistent till message sent)
		newChatButton = self._driver.find_element(By.XPATH, "//div[@id='side']//button[@class='icon icon-chat']")
		newChatButton.click()
		contactButton = self._driver.find_element(By.XPATH, "//span[@class='pane pane-one']//div[@class='chat-title']//span[@title='" + contact + "']")
		contactButton.click()

	def listContacts(self):
		#Open new chat pane
		newChatButton = self._driver.find_element(By.XPATH, "//div[@id='side']//button[@class='icon icon-chat']")
		newChatButton.click()
		#Get all listed contacts
		contactButtons = self._driver.find_elements(By.XPATH, "//span[@class='pane pane-one']//div[@class='chat-title']")
		print(str(len(contactButtons)) + " contacts found.")
		for chatBtn in contactButtons:
			print(chatBtn.text)
		#Reset state
		backButton = self._driver.find_element(By.XPATH, "//span[@class='pane pane-one']//span[@class='icon btn-close-drawer icon-back-light']")
		backButton.click()	

	def removeGroupParticipant(self,group,contact,showText = True):
		self.selectContact(group)
		header = self._driver.find_element(By.XPATH, "//div[@id='main']//div[@class='chat-main']/h2[@class='chat-title']")
		header.click()
		try:
			#Hover over contact
			if '+27' in contact:
				contact = contact[3:]
			contactPath = "//*[@class='pane pane-three']//*[@class='chat-body']//*[contains(@title,'" + contact + "')]//ancestor::div[@class='chat-body']"
			isHovering = False
			self.hoverOver(contactPath)	
			attempts = 0	
			while not isHovering and attempts < 20:
				try:
					#Click options arrow when appears
					self.hoverOver(contactPath)
					optArrow = self._driver.find_element(By.XPATH, (contactPath+"//div[contains(@class,'btn-context')]"))
					optArrow.click()
					isHovering = True
					time.sleep(0.01)
				except selenium.common.exceptions.NoSuchElementException:
					False
				attempts += 1
			if attempts < 20:
				#click Remove in dropdown
				if showText:
					print("clicking dropdown")
				self.waitForAndClick("//div[@class='dropdown']//*[@title='Remove']")
				#Confirm REMOVE in popup
				if showText:
					print("clicking popup")
				self.waitForAndClick("//div[@class='popup']//button[@class='btn-plain btn-default popup-controls-item']")
				#close side pane
				if showText:
					print("returning to normal")
				closeBtn = self._driver.find_element(By.XPATH, "//div[@class='header-close']//button")
		except selenium.common.exceptions.NoSuchElementException:
			print("Not a group/Contact not found")

#Basic Whatsapp manuvering commands

	def hoverOver(self,path):
		we = self._driver.find_element(By.XPATH, path)
		actions = ActionChains(self._driver);
		actions.move_to_element(we).perform();

	def clickElement(self,path):
		we = self._driver.find_element(By.XPATH, path)
		we.click()

	def waitForAndClick(self,path,timeout = 5):
		visible = False
		startTime = int(time.time())
		while not visible:
			try:
				we = self._driver.find_element(By.XPATH, path)
				we.click()
				visible = True
				time.sleep(0.01)
			except selenium.common.exceptions.NoSuchElementException:
				visible =  startTime + timeout < time.time()

	
#Browser-based commands
	
	def checkFor(self,path, showText = True):
		try:
			we = self._driver.find_element(By.XPATH, path)
			if showText:
				print("Found")
			return True
		except selenium.common.exceptions.NoSuchElementException:
			if showText:
				print("Not found")
			return False
	
	def printElementsAt(self,path):
		wes = self._driver.find_elements(By.XPATH, path)
		print(str(len(wes)))
		for we in wes:
			print(str(we))
