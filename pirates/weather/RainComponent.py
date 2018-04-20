from pirates.effects.RainMist import RainMist
from pirates.effects.RainDrops import RainDrops
from pirates.effects.RainSplashes import RainSplashes
from pirates.effects.RainSplashes2 import RainSplashes2
from pirates.weather.WeatherComponentBase import WeatherComponentBase

class RainComponent(WeatherComponentBase):

	def __init__(self, weatherMgr):
		WeatherComponentBase.__init__(self, weatherMgr)
		self.rainDrops = None
		self.rainMist = None
		self.rainSplashes = None
		self.rainSplashes2 = None
		self.wetnessLerp = None

	def startEffect(self):
		self.rainDrops = RainDrops(base.camera)
		self.rainDrops.reparentTo(render)
		self.rainDrops.startLoop()

		self.rainMist = RainMist(base.camera)
		self.rainMist.reparentTo(render)
		self.rainMist.startLoop()

		self.rainSplashes = RainSplashes(base.camera)
		self.rainSplashes.reparentTo(render)
		self.rainSplashes.startLoop()

		self.rainSplashes2 = RainSplashes2(base.camera)
		self.rainSplashes2.reparentTo(render)
		self.rainSplashes2.startLoop()		

	def stopEffect(self):
		if self.rainDrops:
			self.rainDrops.stopLoop()
			self.rainDrops.destroy()
			self.rainDrops = None

		if self.rainMist:
			self.rainMist.stopLoop()
			self.rainMist.destroy()
			self.rainMist = None

		if self.rainSplashes:
			self.rainSplashes.stopLoop()
			self.rainSplashes.destroy()
			self.rainSplashes = None

		if self.rainSplashes2:
			self.rainSplashes2.stopLoop()
			self.rainSplashes2.destroy()
			self.rainSplashes2 = None


