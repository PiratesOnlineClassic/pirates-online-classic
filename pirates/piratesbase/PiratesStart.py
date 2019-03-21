from pandac.PandaModules import loadPrcFile

import PiratesPreloader
print 'PiratesStart: Starting the game.'
import __builtin__
import os

if __debug__:
    loadPrcFile('config/general.prc')
    loadPrcFile('config/dev.prc')

    if os.path.exists('config/personal.prc'):
        loadPrcFile('config/personal.prc')

class game:
    name = 'pirates'
    process = 'client'

__builtin__.game = game()
import time
import os
import sys
import random
import __builtin__
import gc
gc.enable()

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
from pandac.PandaModules import *
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
rolloverSound = base.loadSfx('audio/sfx_gui_click_08.mp3')
rolloverSound.setVolume(0.5)
DirectGuiGlobals.setDefaultRolloverSound(rolloverSound)
clickSound = base.loadSfx('audio/sfx_gui_click_22.mp3')
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
searchPath = DSearchPath()
if not launcher.isDummy():
    searchPath.appendDirectory(Filename('etc'))
    searchPath.appendDirectory(Filename('.'))
else:
    searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$PIRATES/src/configfiles')))
    searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$OTP/src/configfiles')))
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
        run()
    

