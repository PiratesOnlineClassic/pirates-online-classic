from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from otp.ai.MagicWordGlobal import *
from pirates.weather.WeatherManagerBase import WeatherManagerBase
from pirates.weather import WeatherGlobals
import random

class DistributedWeatherManagerAI(DistributedObjectAI, WeatherManagerBase):
	notify = directNotify.newCategory('DistributedWeatherManagerAI')

	def __init__(self, air):
		DistributedObjectAI.__init__(self, air)
		WeatherManagerBase.__init__(self)
		self.currentWeatherId = config.GetInt('starting-weather', WeatherGlobals.WEATHER_CLEAR)
		start, end = WeatherGlobals.getWeatherDuration(self.currentWeatherId)
		self.currentDuration = random.randint(start, end) * 60 
		self.maxWeatherPickAttempts = config.GetInt('max-weather-pick-attempts', 5)
		self.weatherTaskTime = 15
		self.isPaused = False
		self.windSpeed = 1

	def announceGenerate(self):
		DistributedObjectAI.announceGenerate(self)
		if self.advancedWeather:
			self.weatherHandlerTask()
			self.runWeather = taskMgr.doMethodLater(self.weatherTaskTime, self.weatherHandlerTask, 'runWeather')
		self.notify.info("Starting with initial weather of \"%s\" for a duration of %s seconds" % (WeatherGlobals.getNameFromWeather(self.currentWeatherId), self.currentDuration))

	def delete(self):
		DistributedObjectAI.delete(self)
		if hasattr(self, 'runWeather'):
			taskMgr.remove(self.runWeather)

	def getCurrentWeather(self):
		return self.currentWeatherId

	def pickStartingWeather(self):
		if not self.advancedWeather:
		    return
		return self.chooseRandomWeather()

	def weatherHandlerTask(self, task = None):
		if self.isPaused:
			return Task.again

		if self.currentDuration <= 0:
			choosen = self.currentWeatherId
			attempts = 0
			while choosen == self.currentWeatherId  or attempts >= self.maxWeatherPickAttempts:
				choosen = self.chooseRandomWeather()
				attempts+=1

			if (attempts >= self.maxWeatherPickAttempts):
				choosen = self.defaultWeather
				self.notify.info("Failed to pick random weather in alloted attempt count. Defaulting to \"%s\"" % WeatherGlobals.getNameFromWeather(choosen))

			weatherInfo = WeatherGlobals.WEATHER_STATES[choosen]
			self.currentDuration = random.randint(5, 10) * 60
			self.d_setWeatherState(choosen)
		else:
			self.currentDuration -= self.weatherTaskTime

		return Task.again

	def chooseRandomWeather(self, ignoreValidation=False):
		good = False
		choosen = WeatherGlobals.WEATHER_CLEAR
		attempts = 0
		while (good == False or attempts >= 20):
			choosen = random.randint(0, WeatherGlobals.END_WEATHER_ID)
			good = self.canRunWeather(choosen) or ignoreValidation
			attempts+=1
		if (attempts >= 20):
			self.notify.warning("Failed to pick random weather in the allotted attempt count. Defaulting to \"%s\"" % WeatherGlobals.getNameFromWeather(choosen))
		return choosen

	def canRunWeather(self, weatherId):
        if not weatherId in WeatherGlobals.WEATHER_STATES:
            return

		weatherInfo = WeatherGlobals.WEATHER_STATES[weatherId]
		canRun = True

		if 'configOptions' in weatherInfo:
			for option in weatherInfo['configOptions']:
				key, default = option
				if not config.GetBool(key, default):
					canRun = False
					break

		if 'conflictHolidays' in weatherInfo:
			newsManager = self.air.newsManager
			for holiday in weatherInfo['conflictHolidays']:
				if newsManager.isHolidayActive(holiday):
					canRun = False
					break

		return canRun

	def setWeatherState(self, weatherId):
		self.notify.debug("Setting weather state to (%s) \"%s\"" % (weatherId, WeatherGlobals.getNameFromWeather(weatherId)))
		self.currentWeatherId = weatherId

		# Tell the UberDOG about our weather!
		if hasattr(self.air, 'districtTracker'):
			self.air.districtTracker.sendDistrictStatusQuery()

	def d_setWeatherState(self, weatherId):
		self.sendUpdate("setWeatherState", [weatherId])

	def b_setWeatherState(self, weatherId):
		self.setWeatherState(weatherId)
		self.d_setWeatherState(weatherId)

	def getWeatherState(self):
		return self.currentWeatherId

	def setIsPaused(self, isPaused):
		self.isPaused = isPaused

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def weatherReady():
    return "Weather Ready: %s" % str(config.GetBool('advanced-weather', False))

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, int])
def setWeather(weatherId, duration):
	if weatherId not in WeatherGlobals.WEATHER_STATES:
		return "Invalid weather id."
	if not config.GetBool('advanced-weather', False):
		return "Weather is not enabled."
	if not simbase.air.weatherManager.canRunWeather(weatherId):
		return "That weather is currently unavailable."
	weatherName = WeatherGlobals.getNameFromWeather(weatherId)
	simbase.air.weatherManager.currentDuration = duration * 60
	simbase.air.weatherManager.d_setWeatherState(weatherId)
	return "Set weather id to (%s) \"%s\" for %s seconds" % (weatherId, weatherName, duration * 60)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def getWeather():
	weatherMgr = simbase.air.weatherManager
	return "Current Weather \"%s\" for a duration of \"%s\" seconds" % (WeatherGlobals.WEATHER_STATES[weatherMgr.currentWeatherId]['name'], weatherMgr.currentDuration)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def validWeather(weatherId):
	if weatherId not in WeatherGlobals.WEATHER_STATES:
		return "Invalid weather id."
	valid = weatherMgr.canRunWeather(weatherId)
	if not config.GetBool('advanced-weather', False) and weatherId != WeatherGlobals.WEATHER_CLEAR:
		valid = False
	weatherMgr = simbase.air.weatherManager
	return "Weather (%s) \"%s\". Valid: %s" % (weatherId, WeatherGlobals.getNameFromWeather(weatherId), valid)