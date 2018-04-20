from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordGlobal import *
from pirates.piratesbase import TODGlobals
from pirates.weather.WeatherManagerBase import WeatherManagerBase
from pirates.weather import WeatherGlobals

class DistributedWeatherManager(DistributedObject, WeatherManagerBase):
    notify = directNotify.newCategory('DistributedTimeOfDayManager')
    notify.setInfo(True)

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        WeatherManagerBase.__init__(self)
        self.currentWeatherId = WeatherGlobals.WEATHER_CLEAR
        self.currentComponents = []
        self.indoors = False

    def generate(self):
        self.cr.weatherManager = self
        DistributedObject.generate(self)
        self.accept('enterIndoors', self.enterIndoors)
        self.accept('exitIndoors', self.exitIndoors)

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

    def disable(self):
        DistributedObject.disable(self)
        if self.cr.weatherManager == self:
            self.cr.weatherManager = None

    def delete(self):
        for component in self.currentComponents:
            self.despawnComponent(component)
        DistributedObject.delete(self)

    def enterIndoors(self, todSettings = None):
        self.notify.info("Player entered indoors")
        self.indoors = True
        for component in self.currentComponents:
            component.enterIndoors()

    def exitIndoors(self):
        self.notify.info("Player exited indoors")
        self.indoors = False
        for component in self.currentComponents:
            component.exitIndoors()

    def spawnComponent(self, component, autoStart=True):
        weatherComp = component(self)
        if autoStart:
            weatherComp.startEffect()
        self.currentComponents.append(weatherComp)

    def despawnComponent(self, component):
        if component not in self.currentComponents:
            return
        component.stopEffect()
        component.destroy()
        self.currentComponents.remove(component)
        del component

    def setWeatherState(self, weatherId):
        if not weatherId in WeatherGlobals.WEATHER_STATES:
            self.notify.warning("Received invalid weather Id '%s'" % weatherId)
            return

        if not self.advancedWeather:
            return

        self.notify.info("Changing weather to Id '%s'" % weatherId)
        self.currentWeatherId = weatherId
        weatherState = WeatherGlobals.WEATHER_STATES[weatherId]

        #Set Weather components
        for oldComponent in self.currentComponents:
            self.despawnComponent(oldComponent)

        if 'weatherComponents' in weatherState:
            weatherComponents = weatherState['weatherComponents']
            for component in weatherComponents:
                self.spawnComponent(component, not self.indoors)