from .SCColorScheme import SCColorScheme

class SCSettings:
    
    def __init__(self, eventPrefix, whisperMode = 0, colorScheme = None, submenuOverlap = 2.0 / 3, topLevelOverlap = None):
        self.eventPrefix = eventPrefix
        self.whisperMode = whisperMode
        if colorScheme is None:
            colorScheme = SCColorScheme()
        
        self.colorScheme = colorScheme
        self.submenuOverlap = submenuOverlap
        self.topLevelOverlap = topLevelOverlap


