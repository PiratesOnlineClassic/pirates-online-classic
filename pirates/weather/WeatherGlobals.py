from pirates.ai import HolidayGlobals
from pirates.piratesbase import TODGlobals

from pirates.weather.RainComponent import RainComponent

WEATHER_CLEAR = 0
WEATHER_RAIN = 1
END_WEATHER_ID = 1

WEATHER_STATES = {
    WEATHER_CLEAR: {
        'name': "Clear",
        'configOptions': {},
        'holidayOverides': {},
        'conflictHolidays': {},
        'weatherComponents': {},
        'weatherDuration': (5, 10),
        'cloudStateOverride': None
    },
    WEATHER_RAIN: {
        'name': "Rain",
        'configOptions': {
            ("want-weather-rain", True)
        },
        'holidays': {},
        'conflictHolidays': {},
        'weatherComponents': {
            RainComponent
        },
        'weatherDuration': (5, 10),
    }
}

def getNameFromWeather(weatherId):
    if weatherId not in WEATHER_STATES:
        return "Unknown"
    return WEATHER_STATES[weatherId]['name']

def getWeatherDuration(weatherId):
    if weatherId not in WEATHER_STATES:
        return (0, 0)
    return WEATHER_STATES[weatherId]['weatherDuration']