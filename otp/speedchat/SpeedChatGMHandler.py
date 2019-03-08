from pandac.PandaModules import *
from direct.showbase import DirectObject
from otp.otpbase import OTPLocalizer

class SpeedChatGMHandler(DirectObject.DirectObject):
    scStructure = None
    scList = {}
    
    def __init__(self):
        if SpeedChatGMHandler.scStructure is None:
            self.generateSCStructure()

    def generateSCStructure(self):
        SpeedChatGMHandler.scStructure = [OTPLocalizer.PSCMenuGM]
        numGMPhrases = base.config.GetInt('num-gm-phrases', 0)
        for i in range(0, numGMPhrases):
            phrase = base.config.GetString('gm-phrase-%d' % i, '')
            if phrase != '':
                idx = 'gm%d' % i
                SpeedChatGMHandler.scList[idx] = phrase
                SpeedChatGMHandler.scStructure.append(idx)

    def getStructure(self):
        return SpeedChatGMHandler.scStructure

    def getPhrase(self, id):
        return SpeedChatGMHandler.scList[id]


