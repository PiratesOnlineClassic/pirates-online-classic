# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.RadioButton
from direct.gui.DirectButton import *
from panda3d.core import *


class RadioButton(DirectButton):
    

    def __init__(self, parent=None, **kw):
        gui_main = loader.loadModel('models/gui/gui_main')
        icon_sphere = gui_main.find('**/icon_sphere')
        icon_torus = gui_main.find('**/icon_torus')
        icon_torus_over = gui_main.find('**/icon_torus_over')
        gui_main.removeNode()
        optiondefs = (
         ('geom', None, None), ('checkedGeom', icon_sphere, None), ('image', (icon_torus, icon_torus, icon_torus_over, icon_torus), None), ('geom_color', VBase4(1, 1, 1, 1), None), ('image_scale', 1.4, None), ('variable', [], None), ('value', [], None), ('others', [], None), ('relief', None, None), ('isChecked', False, None))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        self.initialiseoptions(RadioButton)
        needToCheck = True
        if len(self['value']) == len(self['variable']) != 0:
            for i in range(len(self['value'])):
                if self['variable'][i] != self['value'][i]:
                    needToCheck = False
                    break

        if needToCheck:
            self.check(False)
        return

    def commandFunc(self, event):
        self.check()

    def check(self, fCommand=True):
        if len(self['value']) == len(self['variable']) != 0:
            for i in range(len(self['value'])):
                self['variable'][i] = self['value'][i]

        self['isChecked'] = True
        self['geom'] = self['checkedGeom']
        for other in self['others']:
            if other != self:
                other.uncheck()

        if fCommand and self['command']:
            apply(self['command'], [self['value']] + self['extraArgs'])

    def setOthers(self, others):
        self['others'] = others

    def uncheck(self):
        self['isChecked'] = False
        self['geom'] = None
        return
# okay decompiling .\pirates\piratesgui\RadioButton.pyc
