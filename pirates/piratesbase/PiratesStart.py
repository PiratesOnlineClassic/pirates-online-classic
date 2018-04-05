import __builtin__
import os
import sys
import random
import gc
import time
import PiratesPreloader
import ClassicLogger
from panda3d.core import *

gc.disable()

if __debug__:
    loadPrcFile('config/general.prc')
    loadPrcFile('config/dev.prc')

print 'PiratesStart: Starting the game.'

class game:
    __module__ = __name__
    name = 'pirates'
    process = 'client'

__builtin__.game = game()

try:
    launcher
except:
    print 'Creating PiratesDummyLauncher'
    from pirates.launcher.PiratesDummyLauncher import PiratesDummyLauncher
    launcher = PiratesDummyLauncher()
    __builtin__.launcher = launcher

from direct.gui import DirectGuiGlobals
import PiratesGlobals
DirectGuiGlobals.setDefaultFontFunc(PiratesGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
import PiratesBase
PiratesBase.PiratesBase()
from direct.showbase.ShowBaseGlobal import *

if base.config.GetBool('want-preloader', 0):
    base.preloader = PiratesPreloader.PiratesPreloader()

if base.win == None:
    print 'Unable to open window; aborting.'
    sys.exit()

launcher.setPandaErrorCode(0)
launcher.setPandaWindowOpen()
base.sfxPlayer.setCutoffDistance(500.0)
rolloverSound = base.loader.loadSfx('audio/sfx_gui_click_08.mp3')
rolloverSound.setVolume(0.5)
DirectGuiGlobals.setDefaultRolloverSound(rolloverSound)
clickSound = base.loader.loadSfx('audio/sfx_gui_click_22.mp3')
DirectGuiGlobals.setDefaultClickSound(clickSound)
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModelOnce('models/gui/panel_parchment'))
clearColor = Vec4(0.0, 0.0, 0.0, 1.0)
base.win.setClearColor(clearColor)
from pirates.shader.Hdr import *
hdr = Hdr()
from pirates.seapatch.Reflection import Reflection
Reflection.initialize(render)
serverVersion = base.config.GetString('server-version', 'no_version_set')
print 'serverVersion: ', serverVersion
from pirates.distributed import PiratesClientRepository
cr = PiratesClientRepository.PiratesClientRepository(serverVersion, launcher)
base.initNametagGlobals()
base.startShow(cr)
from otp.distributed import OtpDoGlobals
from pirates.piratesbase import UserFunnel
UserFunnel.logSubmit(1, 'CLIENT_OPENS')
UserFunnel.logSubmit(0, 'CLIENT_OPENS')

if base.config.GetBool('want-portal-cull', 0):
    base.cam.node().setCullCenter(base.camera)
    base.graphicsEngine.setPortalCull(1)

if base.options:
    base.options.options_to_config()
    base.options.setRuntimeOptions()
    if launcher.isDummy():
        base.run()
