class InputInterrupt(RuntimeError):
	def __init__(self):
		self.args = "Interrupt for stdin blocking"