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

class StackThread(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self._URL = "https://web.whatsapp.com/"
		self._DRIVER_PATH = '/home/jonathan/python/Whatsapp/WebWhatsapp/geckodriver'
		self._isConnected = False
		self._driver = None

	def run(self):
		try:
			col = ColorText.getColoredText
			print("Starting stack.loop")
			self._isConnected = False
			self._driver = webdriver.Firefox(executable_path=self._DRIVER_PATH)
			self._driver.get(self._URL)
			while True:
				isConnected = input(col("Phone connected? y/n: \n>", ColorText.HEADER))
				if isConnected.lower() == 'y':
					break
			self._isConnected = True
			#self._driver.set_window_size(1366, 100000)
			assert "WhatsApp" in self._driver.title
		except KeyboardInterrupt:
			sys.exit("Startup ended. Press ctrl+C again.")

	def isConnected(self):
		return self._isConnected

	def disconnect(self):
		self._driver.quit()

	def resetSize(self):
		self._driver.set_window_size(1366, 100000)
	
	def sendMessage(self,contact,message, showText = True):
		self.selectContact(contact,False)
		messageArea = self._driver.find_element(By.XPATH, "//*[@id='main']//div[@class='input']")
		messageArea.click()
		messageArea.send_keys(message)
		try:
			compose = self._driver.find_element(By.XPATH, "//*[@id='main']//button[@class='icon icon-send compose-btn-send']")
			compose.click()
		except selenium.common.exceptions.NoSuchElementException:
			if showText:
				print("No message entered")
	def sendBroadcast(self,phoneNumbers,message):
		numberList = phoneNumbers.split(",")
		True
	
	def selectContact(self,name, showText = True):
		searchIcon = self._driver.find_element(By.XPATH, '//*[@id="side"]//div[@class="icon icon-search"]')
		searchBox = self._driver.find_element(By.XPATH, '//*[@id="side"]//input')
		searchBox.clear()
		searchIcon.click()
		searchBox.send_keys(name)
		searchBox.send_keys(Keys.RETURN)
		backButton = self._driver.find_element(By.XPATH, '//*[@id="side"]//div[@class="icon icon-back-blue"]')
		if backButton.is_enabled():
			backButton.click()
		try:
			contactTitle = self._driver.find_element(By.XPATH, '//*[@id="main"]//span[@class="emojitext ellipsify"]')
			if showText:
				print(contactTitle.text + " selected")
		except selenium.common.exceptions.NoSuchElementException:	
			if showText:
				print("No contact selected")

	def findUnreadContacts(self, showText = True):
		prevContactTitle = ""
		try:
			prevContactTitle = self._driver.find_element(By.XPATH, '//*[@id="main"]//span[@class="emojitext ellipsify"]').text
			if showText:
				print(prevContactTitle + " selected")
		except selenium.common.exceptions.NoSuchElementException:	
			if showText:
				print("No contact selected - keeping last recieved")
		unreadContacts = self._driver.find_elements(By.XPATH, "//*[@id='side']/div[@id='pane-side']//span[@class='icon-meta unread-count']")
		for contact in unreadContacts:
			contact.click()
		if len(prevContactTitle) != 0:
			self.selectContact(prevContactTitle,showText)
	
	def openNewChat(self, contact,showText = True):
		newChatButton = self._driver.find_element(By.XPATH, "//div[@id='side']//button[@class='icon icon-chat']")
		newChatButton.click()
		contactButton = self._driver.find_element(By.XPATH, "//span[@class='pane pane-one']//div[@class='chat-title']//span[@title='" + contact + "']")
		contactButton.click()

	def listContacts(self):
		newChatButton = self._driver.find_element(By.XPATH, "//div[@id='side']//button[@class='icon icon-chat']")
		newChatButton.click()
		contactButtons = self._driver.find_elements(By.XPATH, "//span[@class='pane pane-one']//div[@class='chat-title']")
		print(str(len(contactButtons)) + " contacts found.")
		for chatBtn in contactButtons:
			print(chatBtn.text)
		backButton = self._driver.find_element(By.XPATH, "//span[@class='pane pane-one']//span[@class='icon btn-close-drawer icon-back-light']")
		backButton.click()	

	def checkFor(self,path):
		try:
			we = self._driver.find_element(By.XPATH, path)
			print("Found")
			return True
		except selenium.common.exceptions.NoSuchElementException:
			print("Not found")
			return False

	def hoverOver(self,path):
		we = self._driver.find_element(By.XPATH, path)
		actions = ActionChains(self._driver);
		actions.move_to_element(we).perform();

	def clickElement(self,path):
		we = self._driver.find_element(By.XPATH, path)
		we.click()

	def waitForAndClick(self,path):
		visible = False	
		while not visible:
			try:
				we = self._driver.find_element(By.XPATH, path)
				we.click()
				visible = True
				time.sleep(0.01)
			except selenium.common.exceptions.NoSuchElementException:
				False
	
	def removeGroupParticipant(self,group,contact):
		self.selectContact(group)
		header = self._driver.find_element(By.XPATH, "//div[@id='main']//div[@class='chat-main']/h2[@class='chat-title']")
		header.click()
		##try:
		#Hover over contact
		contactPath = "//*[@class='pane pane-three']//*[@class='chat-body']//*[@title='" + contact + "']//ancestor::div[@class='chat-body']"
		isHovering = False
		self.hoverOver(contactPath)		
		while not isHovering:
			try:
				#Click options arrow when appears
				self.hoverOver(contactPath)
				optArrow = self._driver.find_element(By.XPATH, (contactPath+"//span[@class='icon icon-down btn-context']"))
				optArrow.click()
				isHovering = True
				time.sleep(0.01)
			except selenium.common.exceptions.NoSuchElementException:
				False
		#click Remove in dropdown
		print("clicking dropdown")
		self.waitForAndClick("//div[@class='dropdown']//*[@title='Remove']")
		#Confirm REMOVE in popup
		print("clicking popup")
		self.waitForAndClick("//div[@class='popup']//button[@class='btn-plain btn-default popup-controls-item']")
		#close side pane
		print("returning to normal")
		closeBtn = self._driver.find_element(By.XPATH, "//div[@class='header-close']//button")
		#except selenium.common.exceptions.NoSuchElementException:
		#	print("Not a group/Contact not found")

	
