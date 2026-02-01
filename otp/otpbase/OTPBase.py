from . import OTPRender
import time

from otp.ai.MagicWordGlobal import *

from direct.showbase.ShowBase import ShowBase

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


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def fps():
    """
    Toggle frame rate meter on or off.
    """

    base.setFrameRateMeter(not base.frameRateMeter)
    return 'Toggled framerate meter.'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def showAvIds():
    """
    Show avId in Nametags.
    """

    messenger.send('nameTagShowAvId')
    return 'Enabled avId nametags.'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def showNames():
    """
    Remove avIds in Nametags.
    """

    messenger.send('nameTagShowName')
    return 'Disabled avId nametags.'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def showAccess():
    """
    Returns the access of the current localAvatar.
    """

    target = spellbook.getTarget()
    return "Access level: %d" % target.getAdminAccess()

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def toggle2d():
    """
    Toggles visibility of all aspect2d nodes
    """

    if aspect2d.isHidden():
        aspect2d.show()
    else:
        aspect2d.hide()

    return 'Toggled aspect2d.'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def placer():
    """
    Toggles the direct placer.
    """

    base.camera.place()
    return 'Toggled placer.'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def explorer():
    """
    Toggles the direct explorer.
    """

    base.render.explore()
    return 'Toggled explorer.'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def analyze():
    """
    Returns a string of analytic scenegraph data
    """

    render.analyze()
    return "Toggled scenegraph analyze."
