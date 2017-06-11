
class ColorText():
# colors in console
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	@staticmethod
	def getColoredText(msg, color=None):
		"""
        	Returns:
		colored msg, if colors are enabled in config and a color is provided for msg
		msg, otherwise
		"""
		if color:
			msg = color + msg + ColorText.ENDC
		return msg
