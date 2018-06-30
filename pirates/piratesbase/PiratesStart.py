import __builtin__
import os
import sys
import random
import gc
import time

from pirates.piratesbase import PiratesPreloader
from pirates.piratesbase import ClassicLogger
from panda3d.core import *

gc.enable()

if __debug__:
    loadPrcFile('config/general.prc')
    loadPrcFile('config/dev.prc')
    if os.path.exists('config/personal.prc'):
        loadPrcFile('config/personal.prc')

print 'PiratesStart: Starting the game.'


class game:

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
from pirates.piratesbase import PiratesGlobals
DirectGuiGlobals.setDefaultFontFunc(PiratesGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
from pirates.piratesbase import PiratesBase
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
DirectGuiGlobals.setDefaultDialogGeom(
    loader.loadModelOnce('models/gui/panel_parchment'))
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

if __debug__ and base.config.GetBool('want-debug-injector', False):

    def openInjector_wx():
        import wx
        from direct.stdpy import threading, thread

        def __inject_wx(_):
            code = textbox.GetValue()
            exec (code, globals())

        app = wx.App(redirect=False)

        frame = wx.Frame(
            None,
            title="POC Injector",
            size=(640, 420),
            style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
        panel = wx.Panel(frame)
        button = wx.Button(
            parent=panel, id=-1, label="Inject", size=(50, 20), pos=(295, 0))
        global textbox
        textbox = wx.TextCtrl(
            parent=panel,
            id=-1,
            pos=(20, 22),
            size=(600, 340),
            style=wx.TE_MULTILINE)
        frame.Bind(wx.EVT_BUTTON, __inject_wx, button)

        frame.Show()
        app.SetTopWindow(frame)

        textbox.AppendText(
            "# Welcome to the Pirates Online Classic Debug Injector! #")

        __builtin__.injectorThread = threading.Thread(target=app.MainLoop)
        __builtin__.injectorThread.start()

    openInjector_wx()
    __builtin__.devInjectorOpen = True
    UserFunnel.logSubmit(1, 'DEV_INJECTOR_OPENS')
    UserFunnel.logSubmit(0, 'DEV_INJECTOR_OPENS')

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
