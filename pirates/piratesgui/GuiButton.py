import copy

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from direct.task.Task import Task
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame


class GuiButton(DirectButton):
    
    notify = directNotify.newCategory('GuiButton')
    genericButton = None

    def __init__(self, parent=None, hotkeys=(), hotkeyLabel=None, helpText='', helpPos=(0, 0, 0), helpDelay=PiratesGuiGlobals.HelpPopupTime, helpColorOff=False, helpLeftAlign=False, **kw):
        self.loadGui()
        self.helpBox = None
        self.helpWatcher = None
        self.canRepositon = False
        optiondefs = (
         (
          'relief', None, None), ('pos', (0, 0, 0), None), ('image', GuiButton.genericButton, None), ('image_scale', (0.24, 0.22, 0.22), None), ('image_pos', (0, 0, 0), None), ('pressEffect', 0, None), ('text', '', None), ('text_font', PiratesGlobals.getInterfaceFont(), None), ('text_scale', PiratesGuiGlobals.TextScaleLarge, None), ('text0_fg', PiratesGuiGlobals.TextFG2, None), ('text1_fg', PiratesGuiGlobals.TextFG2, None), ('text2_fg', PiratesGuiGlobals.TextFG2, None), ('text3_fg', PiratesGuiGlobals.TextFG3, None), ('text_shadow', PiratesGuiGlobals.TextShadow, None), ('text_pos', (0, -0.01), None), ('text_wordwrap', 8, None), ('text_align', TextNode.ACenter, None), ('textMayChange', 1, None), ('helpText', helpText, self.helpTextUpdated), ('helpPos', helpPos, self.setHelpPos), ('helpDelay', helpDelay, None), ('helpColorOff', helpColorOff, None), ('helpLeftAlign', helpLeftAlign, None), ('helpBin', 'gui-popup', None), ('helpBinSort', 0, None), ('helpOpaque', 0, None), ('canReposition', False, None), ('sortOrder', 100, None), ('baseImage', None, None), ('selected', False, None), ('selectedImage', GuiButton.genericButton, None), ('state', DGG.NORMAL, self.setState))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent=parent, **kw)
        self.initialiseoptions(GuiButton)
        self.hotkeys = ()
        self.setupHotkeys(hotkeys, hotkeyLabel, self['command'], self['extraArgs'])
        return

    def destroy(self):
        self.hideDetails()
        if self.helpWatcher:
            self.helpWatcher.unbind(DGG.WITHIN)
            self.helpWatcher.unbind(DGG.WITHOUT)
            self.helpWatcher.destroy()
            self.helpWatcher = None
        self.ignoreAll()
        DirectButton.destroy(self)
        return

    def loadGui(self):
        if GuiButton.genericButton:
            return
        gui = loader.loadModel('models/gui/toplevel_gui')
        GuiButton.genericButton = (gui.find('**/generic_button'), gui.find('**/generic_button_down'), gui.find('**/generic_button_over'), gui.find('**/generic_button_disabled'))

    def setupHotkeys(self, hotkeys, hotkeyLabel, command, extraArgs):
        if self.hotkeys:
            self.ignoreHotkeys()
            self.hotkeyLabel.destroy()
        self.hotkeys = hotkeys
        if self.hotkeys:
            self.hotkeyLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=hotkeyLabel, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0.092,
                                                                                                                                                                                                                     0.01), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1)
            self.acceptHotkeys(self.hotkeys, command, extraArgs)
        return

    def ignoreHotkeys(self):
        if self.hotkeys:
            for hotkey in self.hotkeys:
                self.ignore(hotkey)

    def acceptHotkeys(self, hotkeys, command, extraArgs):
        if self.hotkeys:
            for hotkey in self.hotkeys:
                self.accept(hotkey, command, extraArgs + [hotkey])

    def createHelpWatcher(self):
        if self['helpOpaque']:
            self.bind(DGG.ENTER, self.waitShowDetails)
            self.bind(DGG.EXIT, self.hideDetails)
        else:
            w = self.getWidth()
            h = self.getHeight()
            pos = self.__discoverHelpWatcherPos()
            frameSize = self['frameSize'] or self.getBounds()
            self.helpWatcher = DirectFrame(parent=self, relief=base.config.GetBool('show-helpwatchers', 0), state=DGG.NORMAL, frameColor=(1,
                                                                                                                                          1,
                                                                                                                                          0,
                                                                                                                                          0.5), frameSize=frameSize, sortOrder=self['sortOrder'] - 1)
            self.helpWatcher.wrtReparentTo(self.getParent())
            self.reparentTo(self.getParent())
            self.helpWatcher.bind(DGG.WITHIN, self.waitShowDetails)
            self.helpWatcher.bind(DGG.WITHOUT, self.hideDetails)

    def __discoverHelpWatcherPos(self):
        w = self.getWidth()
        h = self.getHeight()
        bounds = self['frameSize'] or self.getBounds()
        pos = Vec3(bounds[0] + w / 2, 0, bounds[2] + h / 2)
        return pos

    def resetHelpWatcher(self):
        if self.helpWatcher:
            self.helpWatcher.setPos(self, 0, 0, 0)

    def createHelpBox(self):
        if not self.helpWatcher:
            self.createHelpWatcher()
        helpLabel = DirectLabel(relief=None, state=DGG.DISABLED, text=self['helpText'], text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG1, text_wordwrap=12, text_shadow=(0,
                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                  1), textMayChange=0, sortOrder=91)
        height = helpLabel.getHeight()
        width = helpLabel.getWidth() + 0.05
        if self['helpLeftAlign']:
            fs = [
             0.0, width, -height, 0.045]
            pos = [width / 2.0, 0, -0.01]
        else:
            fs = [
             0.25 - width, 0.25, -height, 0.045]
            pos = [0.25 - width / 2.0, 0, -0.01]
        self.helpBox = BorderFrame(parent=self, state=DGG.DISABLED, frameSize=(fs[0], fs[1], fs[2], fs[3]), suffix='_f', pos=self['helpPos'], sortOrder=90)
        helpLabel.reparentTo(self.helpBox)
        helpLabel.setPos(pos[0], pos[1], pos[2])
        self.helpBox.hide()
        self.helpBox.setClipPlaneOff()
        pos = self.helpBox.getPos(aspect2d)
        x = min(pos[0], base.a2dRight - width)
        z = max(pos[2], base.a2dBottom - height)
        self.helpBox.setPos(aspect2d, x, 0, z)
        if self['helpColorOff']:
            self.helpBox.setColorOff()
        else:
            self.helpBox.flattenLight()
        if self['helpBin']:
            self.helpBox.setBin(self['helpBin'], self['helpBinSort'])
        return

    def helpTextUpdated(self):
        if self.helpBox and self.helpBox['text'] != self['helpText']:
            self.helpBox.destroy()
            self.createHelpBox()
        else:
            if self['helpText']:
                self.createHelpBox()

    def setHelpPos(self):
        if self.helpBox:
            self.helpTextUpdated()

    def waitShowDetails(self, event):
        try:
            self['helpDelay']
        except AttributeError:
            return
        else:
            if not self.helpBox:
                self.createHelpBox()
            if self['helpDelay']:
                self.hideDetails()
                taskMgr.doMethodLater(self['helpDelay'], self.helpBox.show, 'helpInfoTask-%s' % self.getName(), extraArgs=[])
            self.helpBox.show()

    def hideDetails(self, event=None):
        taskMgr.remove('helpInfoTask-%s' % self.getName())
        if self.helpBox and not self.helpBox.isEmpty():
            self.helpBox.hide()

    def setImage(self):
        DirectButton.setImage(self)
        if not self['baseImage']:
            self['baseImage'] = self['image']

    def setSelected(self):
        if self['selected']:
            self['image'] = self['selectedImage']
        else:
            self['image'] = self['baseImage']

    def setPos(self, *args, **kw):
        DirectButton.setPos(self, *args, **kw)

    def setX(self, *args, **kw):
        DirectButton.setX(self, *args, **kw)

    def setY(self, *args, **kw):
        DirectButton.setY(self, *args, **kw)

    def setZ(self, *args, **kw):
        DirectButton.setZ(self, *args, **kw)

    def setState(self):
        DirectButton.setState(self)
        if self.helpWatcher:
            self.helpWatcher['state'] = self['state']

    def removeNode(self):
        DirectButton.removeNode(self)
        if self.helpWatcher:
            self.helpWatcher.removeNode()

    def remove(self):
        DirectButton.remove(self)
        if self.helpWatcher:
            self.helpWatcher.removeNode()

    def detachNode(self):
        DirectButton.detachNode(self)
        if self.helpWatcher:
            self.helpWatcher.detachNode()

    def hide(self):
        DirectButton.hide(self)
        if self.helpWatcher:
            self.helpWatcher.hide()

    def show(self):
        DirectButton.show(self)
        if self.helpWatcher:
            self.helpWatcher.show()

    def stash(self):
        DirectButton.stash(self)
        if self.helpWatcher:
            self.helpWatcher.stash()

    def unstash(self):
        DirectButton.unstash(self)
        self.reparentTo(self.getParent(), sort=self['sortOrder'])
        if self.helpWatcher:
            self.helpWatcher.unstash()
            self.helpWatcher.reparentTo(self.helpWatcher.getParent(), sort=self.helpWatcher['sortOrder'])
