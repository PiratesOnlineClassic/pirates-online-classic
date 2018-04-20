
class WeatherManagerBase:

    def __init__(self):
        self.advancedWeather = config.GetBool('advanced-weather', False)