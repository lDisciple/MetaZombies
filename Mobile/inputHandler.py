import threading
import time

"""
Requests input through threading to prevent blocking.
Input can be retrieved
"""
class InputHandler(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self._inputtedText = []
		self._running = False

	def run(self):
		text = ""
		self._running = True
		print("Enter your commands:")
		while self._running:
			try:
				text = "";
				text = input()
				if len(text) > 0:
					self._inputtedText.append(text)	
			except KeyboardInterrupt:
				self._running = False
	"""
	Retrieve input
	"""
	def getInput(self):
		ret = self._inputtedText
		self._inputtedText = []
		return ret
	"""
	Prevent another input call (current one will block closing of thread)
	"""
	def stop(self):
		self._running = False