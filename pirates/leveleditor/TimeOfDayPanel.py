# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.leveleditor.TimeOfDayPanel
import pprint
import tkColorChooser
from Tkinter import *

import Pmw
from direct.directtools.DirectUtil import getTkColorString
from direct.gui import DirectGuiGlobals as DGG
from direct.showbase.TkGlobal import *
from direct.tkwidgets import Dial, Floater, Slider, Valuator, VectorWidgets
from direct.tkwidgets.AppShell import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer as PL
from pirates.piratesbase import TODGlobals


class TimeOfDayPanel(AppShell):
    
    appname = 'Time Of Day Panel'
    appversion = '1.0'
    copyright = 'Copyright 2006 Walt Disney Internet Group.' + ' All Rights Reserved'
    contactname = 'Joe Shochet'
    contactphone = '(818) 623-3912'
    contactemail = 'joe.shochet@disney.com'
    frameWidth = 480
    frameHeight = 950
    usecommandarea = 0
    usestatusarea = 0

    def __init__(self, todMgr, parent=None, **kw):
        self.todMgr = todMgr
        self.accept('timeOfDayChange', self.updateTod)
        DGG.INITOPT = Pmw.INITOPT
        optiondefs = (('title', self.appname, None),)
        self.defineoptions(kw, optiondefs)
        AppShell.__init__(self, parent)
        self.initialiseoptions(TimeOfDayPanel)
        self.editor = None
        return

    def setEditor(self, editor):
        self.editor = editor

    def onDestroy(self, event):
        if self.editor:
            self.editor.TODPanel = None
            self.editor.TODPanelLoaded = False
        self.ignoreAll()
        AppShell.onDestroy(self, event)
        return

    def updateTod(self, stateId, stateDuration, elapsedTime):
        self.todVar.set(stateId)
        fogColor = self.todMgr.fog.getColor()
        fogRange = self.todMgr.fog.getExpDensity()
        ambientColor = self.todMgr.alight.node().getColor()
        directionalColor = self.todMgr.dlight.node().getColor()
        self.fogColor.set((int(fogColor[0] * 255), int(fogColor[1] * 255), int(fogColor[2] * 255)))
        self.fogRange.set((fogRange,))
        self.ambientColor.set((int(ambientColor[0] * 255), int(ambientColor[1] * 255), int(ambientColor[2] * 255)))
        self.directionalColor.set((int(directionalColor[0] * 255), int(directionalColor[1] * 255), int(directionalColor[2] * 255)))

    def getTkColorFromVec4(self, v):
        return getTkColorString([int(v[0] * 255), int(v[1] * 255), int(v[2] * 255)])

    def createInterface(self):
        interior = self.interior()
        todFrame = Frame(interior, borderwidth=4, relief='raised')
        todLabel = Label(todFrame, text='TIME OF DAY', font=('MS Sans Serif', 14))
        printButton = Button(todFrame, text='PRINT', command=self.printSettings)
        texToggle = Button(todFrame, text='Toggle Textures', command=base.toggleTexture)
        todStateFrame = Frame(todFrame, borderwidth=2, relief='sunken')
        self.todVar = IntVar()
        self.todVar.set(self.todMgr.currentState)
        todDawn = Radiobutton(todStateFrame, text='Dawn', variable=self.todVar, value=PiratesGlobals.TOD_DAWN, command=self.changeTod)
        todDay = Radiobutton(todStateFrame, text='Day', variable=self.todVar, value=PiratesGlobals.TOD_DAY, command=self.changeTod)
        todDusk = Radiobutton(todStateFrame, text='Dusk', variable=self.todVar, value=PiratesGlobals.TOD_DUSK, command=self.changeTod)
        todNight = Radiobutton(todStateFrame, text='Night', variable=self.todVar, value=PiratesGlobals.TOD_NIGHT, command=self.changeTod)
        todStars = Radiobutton(todStateFrame, text='Stars', variable=self.todVar, value=PiratesGlobals.TOD_STARS, command=self.changeTod)
        todOff = Radiobutton(todStateFrame, text='TOD Off', variable=self.todVar, value=PiratesGlobals.TOD_OFF, command=self.changeTod)
        todDawn.pack(side=LEFT, fill=X, expand=0)
        todDay.pack(side=LEFT, fill=X, expand=0)
        todDusk.pack(side=LEFT, fill=X, expand=0)
        todNight.pack(side=LEFT, fill=X, expand=0)
        todStars.pack(side=LEFT, fill=X, expand=0)
        todOff.pack(side=LEFT, fill=X, expand=0)
        todCycleFrame = Frame(todFrame, borderwidth=2, relief='sunken')
        self.todCycleVar = IntVar()
        self.todCycleVar.set(int(self.todMgr.cycleDuration))
        todCycle0 = Radiobutton(todCycleFrame, text='Off', variable=self.todCycleVar, value=0, command=self.changeTod)
        todCycle1 = Radiobutton(todCycleFrame, text='30 sec', variable=self.todCycleVar, value=30, command=self.changeTod)
        todCycle2 = Radiobutton(todCycleFrame, text='2 min', variable=self.todCycleVar, value=120, command=self.changeTod)
        todCycle3 = Radiobutton(todCycleFrame, text='10 min', variable=self.todCycleVar, value=600, command=self.changeTod)
        todCycle0.pack(side=LEFT, fill=X, expand=0)
        todCycle1.pack(side=LEFT, fill=X, expand=0)
        todCycle2.pack(side=LEFT, fill=X, expand=0)
        todCycle3.pack(side=LEFT, fill=X, expand=0)
        todLabel.pack(fill=X, expand=0)
        printButton.pack(side=LEFT, fill=X, expand=0)
        texToggle.pack(side=RIGHT, fill=X, expand=0)
        todStateFrame.pack(fill=X, expand=0)
        todCycleFrame.pack(fill=X, expand=0)
        todFrame.pack(fill=BOTH, expand=1, pady=4)
        initialFogColor = self.todMgr.fog.getColor()
        fogFrame = Frame(interior, borderwidth=4, relief='raised')
        self.fogLabel = Label(fogFrame, text='FOG', font=('MS Sans Serif', 14))
        self.fogLabel['bg'] = self.getTkColorFromVec4(initialFogColor)
        self.fogColor = Valuator.ValuatorGroup(parent=fogFrame, dim=3, labels=['R', 'G', 'B'], value=[int(initialFogColor[0] * 255), int(initialFogColor[1] * 255), int(initialFogColor[2] * 255)], type='slider', valuator_style='full', valuator_min=0, valuator_max=255, valuator_resolution=1)
        self.fogColor['command'] = self.setFogColorVec

        def popupFogColorPicker():
            color = tkColorChooser.askcolor(parent=interior, initialcolor=(0, 0, 0))
            if color[0] is not None:
                self.fogColor.set((color[0][0], color[0][1], color[0][2]))
            return

        pButton = Button(fogFrame, text='Popup Color Picker', command=popupFogColorPicker)
        initialRange = self.todMgr.fog.getExpDensity()
        self.fogRange = Valuator.ValuatorGroup(parent=fogFrame, dim=1, labels=['Range'], value=[initialRange], type='slider', valuator_style='full', min=0.0, max=0.015, numDigits=6, resolution=1e-06)
        self.fogRange['command'] = self.setFogRangeVec
        self.fogLabel.pack(fill=X, expand=0)
        pButton.pack(fill=X, expand=0)
        self.fogColor.pack(fill=X, expand=0)
        self.fogRange.pack(fill=X, expand=0)
        fogFrame.pack(fill=BOTH, expand=1, pady=4)
        initialAmbientColor = self.todMgr.alight.node().getColor()
        ambientFrame = Frame(interior, borderwidth=4, relief='raised')
        self.ambientLabel = Label(ambientFrame, text='AMBIENT LIGHT', font=('MS Sans Serif',
                                                                            14))
        self.ambientLabel['bg'] = self.getTkColorFromVec4(initialAmbientColor)
        self.ambientColor = Valuator.ValuatorGroup(parent=ambientFrame, dim=3, labels=['R', 'G', 'B'], value=[int(initialAmbientColor[0] * 255), int(initialAmbientColor[1] * 255), int(initialAmbientColor[2] * 255)], type='slider', valuator_style='full', valuator_min=0, valuator_max=255, valuator_resolution=1)
        self.ambientColor['command'] = self.setAmbientColorVec

        def popupAmbientColorPicker():
            color = tkColorChooser.askcolor(parent=interior, initialcolor=(0, 0, 0))
            if color[0] is not None:
                self.ambientColor.set((color[0][0], color[0][1], color[0][2]))
            return

        pButton = Button(ambientFrame, text='Popup Color Picker', command=popupAmbientColorPicker)
        self.ambientLabel.pack(fill=X, expand=0)
        pButton.pack(fill=X, expand=0)
        self.ambientColor.pack(fill=X, expand=0)
        ambientFrame.pack(fill=BOTH, expand=1, pady=4)
        initialDirectionalColor = self.todMgr.dlight.node().getColor()
        directionalFrame = Frame(interior, borderwidth=4, relief='raised')
        self.directionalLabel = Label(directionalFrame, text='DIRECTIONAL LIGHT', font=('MS Sans Serif',
                                                                                        14))
        self.directionalLabel['bg'] = self.getTkColorFromVec4(initialDirectionalColor)
        self.directionalColor = Valuator.ValuatorGroup(parent=directionalFrame, dim=3, labels=['R', 'G', 'B'], value=[int(initialDirectionalColor[0] * 255), int(initialDirectionalColor[1] * 255), int(initialDirectionalColor[2] * 255)], type='slider', valuator_style='full', valuator_min=0, valuator_max=255, valuator_resolution=1)
        self.directionalColor['command'] = self.setDirectionalColorVec

        def popupDirectionalColorPicker():
            color = tkColorChooser.askcolor(parent=interior, initialcolor=(0, 0, 0))
            if color[0] is not None:
                self.directionalColor.set((color[0][0], color[0][1], color[0][2]))
            return

        pButton = Button(directionalFrame, text='Popup Color Picker', command=popupDirectionalColorPicker)
        self.directionalLabel.pack(fill=X, expand=0)
        pButton.pack(fill=X, expand=0)
        self.directionalColor.pack(fill=X, expand=0)
        directionalFrame.pack(fill=BOTH, expand=1, pady=4)

    def changeTod(self):
        tod = self.todVar.get()
        cycleDuration = self.todCycleVar.get()
        magicWord = '~tod %s %s' % (tod, cycleDuration)
        messenger.send('magicWord', [magicWord])
        if self.editor:
            self.editor.panel.skyState.set(self.todVar.get())
            if tod >= 0:
                self.editor.changeTimeOfDay()
            else:
                if self.editor and self.editor.TODPanelLoaded:
                    self.editor.objectMgr.canModifyCurrAttribs(edit=True)
                    self.editor.objectMgr.currEditedObjInfo.setTodModified(True)
                self.editor.disableTOD(fromTODPanel=True)

    def setFogColorVec(self, color):
        vColor = Vec4(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, 1)
        self.todMgr.fog.setColor(vColor)
        self.fogLabel['bg'] = getTkColorString(color)
        todState = self.todVar.get()
        TODGlobals.FogColors[self.todMgr.environment][todState] = vColor
        if self.editor and self.editor.TODPanelLoaded:
            self.editor.objectMgr.canModifyCurrAttribs(edit=True)
            self.editor.objectMgr.currEditedObjInfo.setTodModified(True)

    def setFogRangeVec(self, range):
        self.todMgr.fog.setExpDensity(range[0])
        todState = self.todVar.get()
        TODGlobals.FogExps[self.todMgr.environment][todState] = range[0]
        if self.editor and self.editor.TODPanelLoaded:
            self.editor.objectMgr.canModifyCurrAttribs(edit=True)
            self.editor.objectMgr.currEditedObjInfo.setTodModified(True)

    def setAmbientColorVec(self, color):
        vColor = Vec4(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, 1)
        self.todMgr.alight.node().setColor(vColor)
        self.ambientLabel['bg'] = getTkColorString(color)
        todState = self.todVar.get()
        TODGlobals.AmbientLightColors[self.todMgr.environment][todState] = vColor
        if self.editor and self.editor.TODPanelLoaded:
            self.editor.objectMgr.canModifyCurrAttribs(edit=True)
            self.editor.objectMgr.currEditedObjInfo.setTodModified(True)

    def setDirectionalColorVec(self, color):
        vColor = Vec4(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, 1)
        self.todMgr.dlight.node().setColor(vColor)
        self.directionalLabel['bg'] = getTkColorString(color)
        todState = self.todVar.get()
        TODGlobals.DirectionalLightColors[self.todMgr.environment][todState] = vColor
        if self.editor and self.editor.TODPanelLoaded:
            self.editor.objectMgr.canModifyCurrAttribs(edit=True)
            self.editor.objectMgr.currEditedObjInfo.setTodModified(True)

    def printSettings(self):
        print '# Fog Colors'
        print 'self.fogColors = ',
        pprint.pprint(TODGlobals.FogColors)
        print '# Fog Ranges'
        print 'self.fogExps = ',
        pprint.pprint(TODGlobals.FogExps)
        print '# Ambient Colors'
        print 'self.ambientLightColors = ',
        pprint.pprint(TODGlobals.AmbientLightColors)
        print '# Directional Colors'
        print 'self.directionalLightColors = ',
        pprint.pprint(TODGlobals.DirectionalLightColors)
# okay decompiling .\pirates\leveleditor\TimeOfDayPanel.pyc
