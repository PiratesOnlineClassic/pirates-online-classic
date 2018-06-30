# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.CheckButton
from direct.gui.DirectButton import *
from panda3d.core import *


class CheckButton(DirectButton):

    def __init__(self, parent=None, **kw):
        toplevel_gui = loader.loadModel('models/gui/toplevel_gui')
        generic_box = toplevel_gui.find('**/generic_box')
        generic_box_over = toplevel_gui.find('**/generic_box_over')
        optiondefs = (('geom', None, None), ('value', False, self.setValue),
                      ('checkedGeom', toplevel_gui.find('**/generic_check'),
                       None), ('image', (generic_box, generic_box,
                                         generic_box_over, generic_box),
                               None), ('image_scale', 0.6, None))
        self.oldValue = False
        self.quiet = True
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        self.initialiseoptions(CheckButton)
        self.quiet = False
        return

    def commandFunc(self, event):
        self['value'] = not self['value']

    def setQuiet(self, value):
        self.quiet = True
        self['value'] = value
        self.quiet = False

    def setValue(self):
        if self['value']:
            self['geom'] = self['checkedGeom']
        else:
            self['geom'] = None
        self.setGeom()
        if self.oldValue ^ self['value']:
            self.oldValue = self['value']
            if self['command'] and not self.quiet:
                args = [int(self['value'])] + self['extraArgs']
                self['command'](*args)
        return


# okay decompiling .\pirates\piratesgui\CheckButton.pyc
