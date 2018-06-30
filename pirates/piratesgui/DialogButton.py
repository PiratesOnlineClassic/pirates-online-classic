# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.DialogButton
from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesgui import GuiButton, PiratesGuiGlobals


class DialogButton(GuiButton.GuiButton):

    yesGeom = None
    noGeom = None
    arrowGeom = None
    BLANK = 0
    YES = 1
    NO = 2
    LEFT = 3
    RIGHT = 4

    def __init__(self, parent, buttonStyle=BLANK, **kw):
        if not DialogButton.yesGeom:
            gui = loader.loadModelCopy('models/gui/toplevel_gui')
            DialogButton.yesGeom = gui.find('**/generic_check')
            DialogButton.noGeom = gui.find('**/generic_x')
            DialogButton.arrowGeom = gui.find('**/generic_arrow')
        optiondefs = (('buttonStyle', buttonStyle,
                       None), ('text_fg', PiratesGuiGlobals.TextFG1, None),
                      ('text_shadow', PiratesGuiGlobals.TextShadow, None))
        if buttonStyle == DialogButton.BLANK:
            optiondefs += (('geom', None, None),
                           ('text_scale', PiratesGuiGlobals.TextScaleLarge,
                            None), ('text_pos', (0.0, -0.012), None))
        else:
            if buttonStyle == DialogButton.YES:
                optiondefs += (('geom', self.yesGeom,
                                None), ('geom_scale', 0.5,
                                        None), ('geom_pos', (-0.06, 0, 0),
                                                None),
                               ('geom0_color',
                                PiratesGuiGlobals.ButtonColor6[0], None),
                               ('geom1_color',
                                PiratesGuiGlobals.ButtonColor6[1], None),
                               ('geom2_color',
                                PiratesGuiGlobals.ButtonColor6[2],
                                None), ('geom3_color',
                                        PiratesGuiGlobals.ButtonColor6[3],
                                        None), ('text', 'Yes', None),
                               ('text_scale', PiratesGuiGlobals.TextScaleLarge,
                                None), ('text_pos', (0.04, -0.015), None))
            else:
                if buttonStyle == DialogButton.NO:
                    optiondefs += (('geom', self.noGeom,
                                    None), ('geom_scale', 0.5,
                                            None), ('geom_pos', (-0.06, 0, 0),
                                                    None),
                                   ('geom0_color',
                                    PiratesGuiGlobals.ButtonColor3[0], None),
                                   ('geom1_color',
                                    PiratesGuiGlobals.ButtonColor3[1], None),
                                   ('geom2_color',
                                    PiratesGuiGlobals.ButtonColor3[2],
                                    None), ('geom3_color',
                                            PiratesGuiGlobals.ButtonColor3[3],
                                            None), ('text', 'No', None),
                                   ('text_scale',
                                    PiratesGuiGlobals.TextScaleLarge,
                                    None), ('text_pos', (0.04, -0.012), None))
                else:
                    if buttonStyle == DialogButton.LEFT:
                        optiondefs += (('geom', self.arrowGeom,
                                        None), ('geom_scale', 0.5,
                                                None), ('geom_pos', (-0.06, 0,
                                                                     0), None),
                                       ('geom0_color',
                                        PiratesGuiGlobals.TextFG1, None),
                                       ('geom1_color',
                                        PiratesGuiGlobals.TextFG1, None),
                                       ('geom2_color',
                                        PiratesGuiGlobals.TextFG1,
                                        None), ('geom3_color',
                                                PiratesGuiGlobals.TextFG1,
                                                None), ('text', 'Back', None),
                                       ('text_scale',
                                        PiratesGuiGlobals.TextScaleLarge,
                                        None), ('text_pos', (0.04, -0.012),
                                                None))
                    else:
                        optiondefs += (('geom', self.arrowGeom,
                                        None), ('geom_scale', (-0.5, 0.5, 0.5),
                                                None), ('geom_pos', (0.06, 0,
                                                                     0), None),
                                       ('geom0_color',
                                        PiratesGuiGlobals.TextFG1, None),
                                       ('geom1_color',
                                        PiratesGuiGlobals.TextFG1, None),
                                       ('geom2_color',
                                        PiratesGuiGlobals.TextFG1,
                                        None), ('geom3_color',
                                                PiratesGuiGlobals.TextFG1,
                                                None), ('text', 'Next', None),
                                       ('text_scale',
                                        PiratesGuiGlobals.TextScaleLarge,
                                        None), ('text_pos', (-0.04, -0.012),
                                                None))
        self.defineoptions(kw, optiondefs)
        GuiButton.GuiButton.__init__(self, parent=parent, **kw)
        self.initialiseoptions(DialogButton)
        return


# okay decompiling .\pirates\piratesgui\DialogButton.pyc
