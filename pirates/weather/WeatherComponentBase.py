
class WeatherComponentBase:

	def __init__(self, weatherMgr):
		self.weatherMgr = weatherMgr

	def destroy(self):
		self.stopEffect()

	def enterIndoors(self):
		self.stopEffect()

	def exitIndoors(self):
		self.startEffect()

	def startEffect(self):
		pass

	def stopEffect(self):
		pass