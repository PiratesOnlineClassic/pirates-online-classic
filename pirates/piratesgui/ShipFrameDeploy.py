# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ShipFrameDeploy
from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesbase import Freebooter, PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ShipFrameSelect import ShipFrameSelect
from pirates.piratesgui.ShipSnapshot import ShipSnapshot
from pirates.ship import ShipGlobals


class ShipFrameDeploy(ShipFrameSelect):

    def __init__(self, parent, **kw):
        optiondefs = (('avatarName', '', None),)
        self.defineoptions(kw, optiondefs)
        ShipFrameSelect.__init__(self, parent, **kw)
        self.initialiseoptions(ShipFrameDeploy)
        return

    def enableStats(self,
                    shipName='',
                    shipClass=0,
                    mastInfo=[],
                    hp=0,
                    sp=0,
                    cargo=0,
                    crew=0,
                    time=0):
        hullInfo = ShipGlobals.getHullStats(shipClass)
        self.shipClass = shipClass
        self.snapShot = ShipSnapshot(
            self,
            None,
            self['siegeTeam'],
            shipName,
            shipClass,
            mastInfo,
            hp,
            hullInfo['maxHp'],
            sp,
            hullInfo['maxSp'],
            cargo,
            hullInfo['maxCargo'],
            crew,
            hullInfo['maxCrew'],
            time,
            pos=self['snapShotPos'])
        typeStr = self['avatarName']
        if self['shipType'] is ShipFrameSelect.STBand:
            self.button['text'] = PLocalizer.BoardShip
        else:
            if self['shipType'] is ShipFrameSelect.STGuild:
                self.button['text'] = PLocalizer.BoardShip
            else:
                if self['shipType'] is ShipFrameSelect.STFriend:
                    self.button['text'] = PLocalizer.BoardShip
                else:
                    if self['shipType'] is ShipFrameSelect.STPublic:
                        self.button['text'] = PLocalizer.BoardShip
                    else:
                        typeStr = ''
        stateStr = PLocalizer.ShipAtSea
        if hp <= 0:
            self.button['state'] = DGG.DISABLED
            stateStr = '\x01red\x01%s\x02' % (PLocalizer.ShipSunk,)
            self['shipColorScale'] = VBase4(0.8, 0.3, 0.3, 1)
        else:
            if crew >= hullInfo['maxCrew']:
                self.button['state'] = DGG.DISABLED
                stateStr = '\x01red\x01%s\x02' % (PLocalizer.ShipFull,)
                self['shipColorScale'] = VBase4(0.4, 0.4, 0.4, 1)
            else:
                self.button['state'] = DGG.NORMAL
        if typeStr:
            self.typeLabel['text'] = '\x01smallCaps\x01(%s)\x02' % typeStr
        return

    def enableStatsOV(self, shipOV):
        self.snapShot = ShipSnapshot(
            self, shipOV, self['siegeTeam'], pos=self['snapShotPos'])
        typeStr = ''
        if self['siegeTeam']:
            hp = shipOV.maxHp
            sp = shipOV.maxSp
        else:
            hp = shipOV.Hp
            sp = shipOV.Sp
        if hp <= 0:
            self.button['state'] = DGG.DISABLED
            self.button['text'] = PLocalizer.DeployShip
            stateStr = '\x01Ired\x01%s\x02' % PLocalizer.ShipSunk
            self['shipColorScale'] = VBase4(1, 0.4, 0.4, 1)
            self.button['image3_color'] = VBase4(
                *PiratesGuiGlobals.ButtonColor3[2])
            self.button['geom3_color'] = VBase4(0.4, 0.4, 0.4, 0.4)
            self.button['text3_color'] = VBase4(0.4, 0.4, 0.4, 0.4)
            self.button['helpText'] = PLocalizer.ShipSunk
        else:
            if len(shipOV.crew) >= shipOV.maxCrew:
                self.button['state'] = DGG.DISABLED
                self.button['text'] = PLocalizer.BoardShip
                self.button['helpText'] = PLocalizer.ShipFull
                stateStr = '\x01red\x01%s\x02' % (PLocalizer.ShipFull,)
                self['shipColorScale'] = VBase4(0.4, 0.4, 0.4, 1)
            else:
                if localAvatar.getActiveShipId(
                ) and shipOV.doId != localAvatar.getActiveShipId():
                    self.button['state'] = DGG.DISABLED
                    self.button['text'] = PLocalizer.DeployShip
                    self.button['helpText'] = PLocalizer.OtherShipOut
                    stateStr = '\x01Ired\x01%s\x02' % PLocalizer.OtherShipOut
                    self['shipColorScale'] = VBase4(0.4, 0.4, 0.4, 1)
                else:
                    if shipOV.state in 'Off':
                        self.button['state'] = DGG.NORMAL
                        self.button['text'] = PLocalizer.DeployShip
                        stateStr = PLocalizer.ShipInBottle
                        self.button['helpText'] = PLocalizer.ShipInBottle
                    else:
                        self.button['state'] = DGG.NORMAL
                        self.button['text'] = PLocalizer.BoardShip
                        stateStr = PLocalizer.ShipAtSea
                        self.button['helpText'] = PLocalizer.ShipAtSea
        if not Freebooter.getPaidStatus(
                base.localAvatar.getDoId()
        ) and shipOV.shipClass != ShipGlobals.INTERCEPTORL1 and shipOV.shipClass != ShipGlobals.MERCHANTL1:
            self.button['command'] = base.localAvatar.guiMgr.showNonPayer
            self.button['extraArgs'] = ['Restricted_ShipFrame_Deploy', 3]
            self.button['text'] = PLocalizer.Locked
            subgui = loader.loadModel('models/gui/toplevel_gui')
            if subgui:
                self.button['geom'] = subgui.find('**/subscribers_lock')
                self.button['geom_scale'] = 0.2
                self.button['geom_color'] = Vec4(0.7, 0.7, 0.7, 1.0)
                subgui.removeNode()
        if typeStr:
            self.typeLabel['text'] = '\x01smallCaps\x01(%s)\x02' % typeStr

    def addCrewMemberName(self, name):
        if name not in self.snapShot['crewNames']:
            self.snapShot['crewNames'] += [name]


# okay decompiling .\pirates\piratesgui\ShipFrameDeploy.pyc
