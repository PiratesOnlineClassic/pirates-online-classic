import __builtin__
import os
import sys
import random
import gc
import time
import glob

gc.enable()

from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal

from pirates.piratesbase import PiratesPreloader
from pirates.piratesbase import ClassicLogger

if __debug__:
    loadPrcFile('config/general.prc')
    loadPrcFile('config/dev.prc')

    if os.path.exists('config/personal.prc'):
        loadPrcFile('config/personal.prc')

vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
    vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

for file in glob.glob('resources/*.mf'):
    mf = Multifile()
    mf.openReadWrite(Filename(file))
    names = mf.getSubfileNames()
    for name in names:
        ext = os.path.splitext(name)[1]
        if ext not in ['.jpg', '.jpeg', '.ogg', '.rgb']:
            mf.removeSubfile(name)

    vfs.mount(mf, Filename('/'), 0)

class game:
    name = 'pirates'
    process = 'client'

__builtin__.game = game()

notify = DirectNotifyGlobal.directNotify.newCategory('PiratesStart')
notify.setInfo(True)

notify.info('Starting the game...')

try:
    launcher
except:
    notify.info('Creating PiratesDummyLauncher...')
    from pirates.launcher.PiratesDummyLauncher import PiratesDummyLauncher
    launcher = PiratesDummyLauncher()
    __builtin__.launcher = launcher

from direct.gui import DirectGuiGlobals
from pirates.piratesbase import PiratesGlobals
DirectGuiGlobals.setDefaultFontFunc(PiratesGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
from pirates.piratesbase import PiratesBase
PiratesBase.PiratesBase()
from direct.showbase.ShowBaseGlobal import *

if base.config.GetBool('want-preloader', False):
    base.preloader = PiratesPreloader.PiratesPreloader()

if not base.win:
    notify.error('Unable to open window; aborting...')

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
notify.info('ServerVersion: %s' % serverVersion)
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

autoRun = ConfigVariableBool('pirates-auto-run', True)

if autoRun:
    try:
        base.run()
    except SystemExit:
        raise
    except:
        from direct.showbase import PythonUtil
        print PythonUtil.describeException()
        raise
