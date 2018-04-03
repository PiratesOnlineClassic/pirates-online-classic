# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.MapPage
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pirates.piratesbase import PLocalizer, PiratesGlobals
from pirates.piratesgui import InventoryPage, BorderFrame, ShardPanel, PiratesGuiGlobals, GuiButton
from pirates.piratesgui.DownloadBlockerPanel import DownloadBlockerPanel
from pirates.map.WorldMap import WorldMap

class MapPage(InventoryPage.InventoryPage):
    __module__ = __name__

    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(MapPage)
        self.shardPanel = None
        self.worldMap = None
        self.gear = None
        self.portOfCall = ''
        self.portOfCallLabel = None
        self.portOfCallButton = None
        self.worldButton = None
        self.islandButton = None
        self.townButton = None
        self.clipPlane = None
        self.mode = 0
        self.createPortOfCall()
        self.createWorldMap()
        self.createFrontOrnament()
        self.createShardPanel()
        self.hide()
        return

    def destroy(self):
        InventoryPage.InventoryPage.destroy(self)
        self.shardPanel = None
        self.gear = None
        self.worldMap = None
        self.portOfCallLabel = None
        self.portOfCallButton = None
        self.worldButton = None
        self.islandButton = None
        self.townButton = None
        self.clipPlane = None
        return

    def show(self, *args, **kwargs):
        super(self.__class__, self).show(*args, **kwargs)
        self.switchMode(self.mode, True)

    def slideOpenCallback(self):
        self.worldMap.resetArcBall()
        self.worldMap.rotateAvatarToCenter()

    def hide(self, *args, **kwargs):
        super(self.__class__, self).hide(*args, **kwargs)
        self.switchMode(-1)

    def slideCloseCallback(self):
        self.shardPanel.hideIfShown()

    def createPortOfCall(self):
        if self.portOfCallLabel:
            self.portOfCallLabel.destroy()
        if self.portOfCallButton:
            self.portOfCallButton.destroy()
        compassGui = loader.loadModel('models/gui/compass_gui')
        topGui = loader.loadModel('models/gui/toplevel_gui')
        teleportIcon = topGui.find('**/treasure_w_b_slot_empty').copyTo(NodePath(''))
        compassGui.find('**/compass_icon_objective_green').copyTo(teleportIcon)
        teleportIcon.flattenStrong()
        self.portOfCallLabel = DirectLabel(parent=self, text='', text_font=PiratesGlobals.getPirateOutlineFont(), text_scale=0.045, text_fg=PiratesGuiGlobals.TextFG2, textMayChange=1, pos=(0.55,
                                                                                                                                                                                             0,
                                                                                                                                                                                             0.08))
        self.portOfCallButton = GuiButton.GuiButton(parent=self, pos=(0.54, 0, 0.015), scale=0.85, text='Return', text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.033, -0.014), textMayChange=1, image3_color=(0.8,
                                                                                                                                                                                                                        0.8,
                                                                                                                                                                                                                        0.8,
                                                                                                                                                                                                                        1), geom=teleportIcon, geom_pos=(-0.065, 0, 0), geom_scale=0.2, command=self.handlePortOfCall)

    def createFrontOrnament(self):
        geom = loader.loadModel('models/gui/gui_map_window')
        geom.reparentTo(self)
        geom.setPos(0.54, 0, 0.725)
        geom.setScale(0.32)
        geom.flattenStrong()

    def createMapButtons(self, gui):
        z = 1.1
        self.worldButton = DirectButton(parent=self, relief=None, geom=(gui.find('**/topgui_icon_map_chart'), gui.find('**/topgui_icon_map_chart'), gui.find('**/topgui_icon_map_chart_over'), gui.find('**/topgui_icon_map_chart')), geom_scale=0.5, pos=(0.34, 0, z), command=self.switchMode, extraArgs=[0])
        self.islandButton = DirectButton(parent=self, relief=None, geom=(gui.find('**/topgui_icon_map_island'), gui.find('**/topgui_icon_map_island'), gui.find('**/topgui_icon_map_island_over'), gui.find('**/topgui_icon_map_island')), geom_scale=0.5, pos=(0.55, 0, z), command=self.switchMode, extraArgs=[1])
        self.townButton = DirectButton(parent=self, relief=None, geom=(gui.find('**/topgui_icon_map_town'), gui.find('**/topgui_icon_map_town'), gui.find('**/topgui_icon_map_town_over'), gui.find('**/topgui_icon_map_town')), geom_scale=0.5, pos=(0.76, 0, z), command=self.switchMode, extraArgs=[2])
        self.pointer = DirectFrame(parent=self, relief=None, state=DGG.DISABLED, image=gui.find('**/topgui_icon_map_pointer'), scale=0.5, pos=(0.34, 0, z - 0.07))
        return

    def createWorldMap(self):
        self.worldMap = WorldMap(parent=self, state=DGG.NORMAL, pos=(0.55, 0, 0.62), scale=0.47)
        if __dev__ and 0:

            def changeMouseMode():
                self.worldMap.mapBall.rMode += 1
                self.worldMap.mapBall.rMode %= 2
                self.mouseModeLabel['text'] = `(self.worldMap.mapBall.rMode)`

            self.mouseModeButton = DirectButton(parent=self, text='MouseMode', scale=0.065, pos=(0.25,
                                                                                                 0,
                                                                                                 0.09), command=changeMouseMode)
            self.mouseModeLabel = DirectLabel(parent=self, scale=0.075, pos=(0.5, 0,
                                                                             0.087), text=`(self.worldMap.mapBall.rMode)`, text_fg=(1,
                                                                                                                                    1,
                                                                                                                                    1,
                                                                                                                                    1), textMayChange=1)

    def createShardPanel(self):
        if self.shardPanel:
            self.shardPanel.destroy()
            self.clearClipPlane()
        if self.gear:
            self.gear.detachNode()
        gui = loader.loadModelCopy('models/gui/gui_map_window_drawer')
        gui.reparentTo(self)
        gui.setPos(0.55, 0, 0.725)
        gui.setScale(0.32)
        self.gear = gui.find('**/gear')
        self.gear.wrtReparentTo(self)
        gui.detachNode()
        self.shardPanel = ShardPanel.ShardPanel(parent=self, relief=None, gear=self.gear)
        self.clipPlane = self.attachNewNode(PlaneNode('clip'))
        self.clipPlane.node().setPlane(Plane(0, 0, -1, 0))
        self.clipPlane.setPos(0, 0, 1.35)
        self.setClipPlane(self.clipPlane)
        if __dev__ and 0:

            def showShardList():
                self.shardPanel.show()
                self.shardButton['text'] = 'Hide Shards'
                self.shardButton['command'] = hideShardList

            def hideShardList():
                self.shardPanel.hide()
                self.shardButton['text'] = 'Show Shards'
                self.shardButton['command'] = showShardList

            self.shardButton = DirectButton(parent=self, text='Show Shards', scale=0.065, pos=(0.75,
                                                                                               0,
                                                                                               0.09), command=showShardList, textMayChange=1)
        return

    def switchMode(self, mode, force=False):
        if force:
            self.mode = -1
        if self.mode != mode:
            if mode >= 0:
                xPos = (0.34, 0.55, 0.76)
            if self.mode == 0:
                self.worldMap.disable()
                self.worldMap.hide()
            else:
                if self.mode == 1:
                    pass
                else:
                    if self.mode == 2:
                        pass
            if mode == 0:
                self.worldMap.enable()
                self.worldMap.show()
            elif mode == 1:
                pass
            elif mode == 2:
                pass
        if mode >= 0:
            self.mode = mode

    def updateTeleportIsland(self, teleportToken, amt):
        self.worldMap.updateTeleportIsland(teleportToken)

    def setReturnIsland(self, islandUid):
        self.worldMap.setReturnIsland(islandUid)
        self.setPortOfCall(islandUid)

    def setCurrentIsland(self, islandUid):
        self.worldMap.setCurrentIsland(islandUid)

    def setPortOfCall(self, islandUid):
        self.portOfCall = islandUid
        self.worldMap.setPortOfCall(self.portOfCall)
        if self.portOfCall:
            self.portOfCallLabel.show()
            self.portOfCallButton.show()
            islandName = PLocalizer.LocationNames.get(islandUid)
            if islandName:
                self.portOfCallLabel['text'] = '%s: %s' % (PLocalizer.PortOfCall, islandName)
            else:
                self.portOfCallLabel['text'] = '%s: %s' % (PLocalizer.PortOfCall, 'Unknown Island')
        else:
            self.portOfCallLabel.hide()
            self.portOfCallButton.hide()
            self.portOfCallLabel['text'] = '%s:' % PLocalizer.PortOfCall

    def handlePortOfCall(self):
        if self.portOfCall:
            if launcher.canLeaveFirstIsland():
                base.cr.teleportMgr.requestTeleportToIsland(self.portOfCall)
            else:
                localAvatar.guiMgr.showDownloadBlocker(DownloadBlockerPanel.Reasons.TELEPORT)

    def addQuestDart(self, questId, worldPos):
        return self.worldMap.addQuestDart(questId, worldPos)

    def updateQuestDart(self, questId, worldPos):
        return self.worldMap.updateQuestDart(questId, worldPos)

    def removeQuestDart(self, questId):
        return self.worldMap.removeQuestDart(questId)

    def addLocalAvDart(self, worldPos=Vec3(0)):
        return self.worldMap.addLocalAvDart(worldPos)

    def updateLocalAvDart(self, worldPos):
        return self.worldMap.updateLocalAvDart(worldPos)

    def addIsland(self, name, islandUid, modelPath, pos, h):
        return self.worldMap.addIsland(name, islandUid, modelPath, pos, h)

    def updateIsland(self, name, worldPos=None, rotation=None):
        return self.worldMap.updateIsland(name, worldPos, rotation)

    def removeIsland(self, name):
        return self.worldMap.removeIsland(name)

    def addOceanArea(self, name, areaUid, pos1, pos2):
        self.worldMap.addOceanArea(name, areaUid, pos1, pos2)

    def addShip(self, shipInfo, worldPos):
        self.worldMap.addShip(shipInfo, worldPos)

    def removeShip(self, shipDoId):
        self.worldMap.removeShip(shipDoId)
# okay decompiling .\pirates\piratesgui\MapPage.pyc
