from direct.showbase.ShowBase import ShowBase
import OTPRender
import time

class OTPBase(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)
        self.wantNametags = self.config.GetBool('want-nametags', 1)
        self.slowCloseShard = self.config.GetBool('slow-close-shard', 0)
        self.slowCloseShardDelay = self.config.GetFloat('slow-close-shard-delay', 10.0)
        self.fillShardsToIdealPop = self.config.GetBool('fill-shards-to-ideal-pop', 1)
        self.wantDynamicShadows = 1
        self.gameOptionsCode = ''
        self.locationCode = ''
        self.locationCodeChanged = time.time()
        if base.cam:
            base.cam.node().setCameraMask(OTPRender.MainCameraBitmask)
    
    def getShardPopLimits(self):
        return (300, 600, 1200)

    def setLocationCode(self, locationCode):
        if locationCode != self.locationCode:
            self.locationCode = locationCode
            self.locationCodeChanged = time.time()


