# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.RadarGui
from direct.fsm.FSM import FSM
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from .GuiTray import GuiTray
from pandac.PandaModules import *
from pirates.band.DistributedBandMember import DistributedBandMember
from pirates.piratesbase import PiratesGlobals, PLocalizer, TeamUtils
from pirates.world import OceanZone
from .RadarMap import RadarMap

RADAR_OBJ_TYPE_DEFAULT = 0
RADAR_OBJ_TYPE_LANDMARK = 1
RADAR_OBJ_TYPE_QUEST = 2
RADAR_OBJ_TYPE_SHIP = 3
RADAR_OBJ_TYPE_EXIT = 4
RADAR_OBJ_TYPE_TUTORIAL = 5

class RadarZoomFSM(FSM):
    __module__ = __name__
    notify = directNotify.newCategory('RadarZoomFSM')

    def __init__(self, radarGui):
        FSM.__init__(self, 'RadarZoom')
        self.radarGui = radarGui

    def destroy(self):
        self.cleanup()

    def enterOff(self, args=[]):
        collisionNode = self.radarGui.collSphereNodePath.getNode(0)
        collisionNode.setFromCollideMask(BitMask32.allOff())

    def enterZoom1(self, args=[]):
        self.radarGui.resetRadius(200.0)
        collisionNode = self.radarGui.collSphereNodePath.getNode(0)
        collisionNode.setFromCollideMask(PiratesGlobals.RadarAvatarBitmask)
        self.radarGui.lastZoom = 'Zoom1'

    def exitZoom1(self):
        pass

    def enterZoom2(self, args=[]):
        self.radarGui.resetRadius(1000.0)
        collisionNode = self.radarGui.collSphereNodePath.getNode(0)
        collisionNode.setFromCollideMask(PiratesGlobals.RadarAvatarBitmask | PiratesGlobals.RadarShipBitmask)
        self.radarGui.lastZoom = 'Zoom2'

    def exitZoom2(self):
        pass

    def enterZoom3(self, args=[]):
        self.radarGui.resetRadius(2500.0)
        collisionNode = self.radarGui.collSphereNodePath.getNode(0)
        collisionNode.setFromCollideMask(PiratesGlobals.RadarShipBitmask)
        self.radarGui.lastZoom = 'Zoom3'

    def exitZoom3(self):
        pass


class RadarGui(GuiTray, FSM):
    __module__ = __name__
    notify = directNotify.newCategory('RadarGui')

    def __init__(self, parent, av, radius=200.0, **kw):
        GuiTray.__init__(self, parent, 0.4, 0.4, **kw)
        FSM.__init__(self, 'RadarGui')
        self.initialiseoptions(RadarGui)
        self.av = av
        self.map = None
        self.radius = radius
        self.battleAvatarTubeRadius = 2.0
        self.lastZoom = 'Zoom1'
        guiScale = 0.15
        self.rWidth = (self.width - 0.1) / guiScale
        self.rHeight = (self.height - 0.1) / guiScale
        self.__normalizeWithRadius()
        self.relNode = render.attachNewNode('radarGuiRelNode')
        self.model = loader.loadModel('models/gui/compass_main')
        self.modelMisc = loader.loadModel('models/gui/compass_gui')
        self.zoomOutSfx = loader.loadSfx('audio/sfx_gui_zoom-io.mp3')
        self.zoomInSfx = loader.loadSfx('audio/sfx_gui_zoom-oi.mp3')
        self.guiTop = self.attachNewNode('compassGuiTop')
        self.guiTop.setScale(guiScale)
        self.guiTop.setPos(self.__dX, 0, self.__dZ)
        self.background = self.model.find('**/background')
        self.background.setColorScale(1, 1, 1, 0.6)
        if base.config.GetBool('want-radar-maps', 0):
            self.map = RadarMap(av=av, parent=self, relief=None, scale=(self.rWidth, 1, self.rHeight))
            self.map.setZoomScale(self.radius)
        self.frame = self.model.find('**/frame')
        self.dial = self.model.find('**/dial')
        self.north = loader.loadModel('models/gui/compass_north')
        self.north.setScale(0.75)
        self.north.setZ(1)
        self.north.reparentTo(self.dial)
        self.arrow = loader.loadModel('models/gui/compass_arrow')
        self.arrow.getChild(0).getChild(0).setHpr(90, 0, 90)
        self.arrow.getChild(0).getChild(0).setY(0.2)
        objectiveGrey = self.model.find('**/icon_objective_grey')
        objectiveGrey.copyTo(self.arrow)
        objectiveGrey.setScale(0.5)
        self.arrow.find('**/icon_objective_grey').setScale(0.8)
        self.rectangle = NodePath('rectangle')
        rectangleGeom = self.model.find('**/icon_rectangle_hollow')
        rectangleGeom.setHpr(90, 0, 0)
        rectangleGeom.reparentTo(self.rectangle)
        self.background.reparentTo(self.guiTop)
        if self.map:
            self.map.reparentTo(self.guiTop)
        self.frame.reparentTo(self.guiTop)
        self.dial.reparentTo(self.guiTop)
        self.objTop = self.guiTop.attachNewNode('compassObjTop')
        self.zoomInButton = DirectButton(parent=self, relief=None, scale=0.2, pos=(0.25,
                                                                                   0,
                                                                                   0.25), image=(self.model.find('**/zoomin_button'), self.model.find('**/zoomin_button'), self.model.find('**/zoomin_button_over')), command=self.zoomIn)
        self.zoomOutButton = DirectButton(parent=self, relief=None, scale=0.2, pos=(0.25,
                                                                                    0,
                                                                                    0.25), image=(self.model.find('**/zoomout_button'), self.model.find('**/zoomout_button'), self.model.find('**/zoomout_button_over')), command=self.zoomOut)
        self.zoomInButton.flattenStrong()
        self.zoomOutButton.flattenStrong()
        self.modelDict = {RADAR_OBJ_TYPE_DEFAULT: [self.model.find('**/icon_sphere'), None], RADAR_OBJ_TYPE_LANDMARK: [self.model.find('**/icon_square'), self.model.find('**/icon_square_hollow')], RADAR_OBJ_TYPE_QUEST: [self.model.find('**/icon_objective_grey'), self.arrow], RADAR_OBJ_TYPE_SHIP: [self.model.find('**/icon_ship'), None], RADAR_OBJ_TYPE_EXIT: [self.rectangle, self.rectangle]}
        self.la = self.modelDict[RADAR_OBJ_TYPE_DEFAULT][0].copyTo(self.objTop)
        self.la.setColorScale(1, 1, 1, 1)
        self.la.setPos(0, 0, 0)
        self.__radarObjects = {}
        self.__cachedRadarObjects = {}
        self.collSphereNodePath = None
        self.setupCollisions()
        self.detachNode()
        self.enterSphereEvent = 'enterradarSphere'
        self.exitSphereEvent = 'exitradarSphere'
        self.zoomFSM = RadarZoomFSM(self)
        self.effectIvals = []
        self.locationLabel = DirectLabel(parent=self, relief=None, text='', text_font=PiratesGlobals.getPirateOutlineFont(), text_fg=(1.0,
                                                                                                                                      1.0,
                                                                                                                                      1.0,
                                                                                                                                      1.0), text_shadow=(0,
                                                                                                                                                         0,
                                                                                                                                                         0,
                                                                                                                                                         1), text_scale=0.04, text_pos=(0.2, -0.025), text_wordwrap=7)
        self.locationLabel.hide()
        self.toggle()
        self.flashCleanupTasks = {}
        return

    def showLocation(self, locationUID):
        locText = PLocalizer.LocationNames.get(locationUID)
        if locText is not None:
            self.locationLabel['text'] = locText
            self.locationLabel.show()
        else:
            if base.localAvatar.ship:
                pos = base.localAvatar.ship.getPos(render)
                ocean = OceanZone.getOceanZone(pos[0], pos[1])
                oceanText = PLocalizer.LocationNames.get(ocean)
                if oceanText is None:
                    oceanText = PLocalizer.LoadingScreen_Ocean
                    self.locationLabel['text'] = oceanText
                    self.locationLabel.show()
            else:
                self.locationLabel.hide()
        return

    def hideLocationText(self):
        self.locationLabel.hide()

    def destroy(self):
        for currDoLater, ival in list(self.flashCleanupTasks.values()):
            taskMgr.remove(currDoLater)
            ival.finish()

        self.flashCleanupTasks = {}
        self.cleanupEffects()
        self.removeCollisions()
        taskMgr.remove('drawRadarTask')
        if self.map:
            self.map.clearAreaModel()
        GuiTray.destroy(self)
        self.zoomFSM.destroy()
        del self.zoomFSM
        self.modelMisc.removeNode()
        del self.modelMisc
        self.guiTop.removeNode()
        del self.guiTop
        del self.objTop
        del self.background
        if self.map:
            del self.map
        del self.frame
        del self.dial
        self.relNode.removeNode()
        del self.relNode
        del self.modelDict
        del self.zoomInButton
        del self.zoomOutButton
        loader.unloadSfx(self.zoomOutSfx)
        loader.unloadSfx(self.zoomInSfx)
        del self.zoomOutSfx
        del self.zoomInSfx
        self.locationLabel.destroy()
        del self.av

    def __normalizeWithRadius(self):
        self.__kX = 0.5 * self.rWidth / self.radius
        self.__kZ = 0.5 * self.rHeight / self.radius
        self.__dX = 0.5 * self.width
        self.__dZ = 0.5 * self.height

    def setupCollisions(self):
        sphereName = 'radarSphere'
        collSphere = CollisionSphere(0, 0, 0, self.radius - self.battleAvatarTubeRadius)
        collSphere.setTangible(0)
        collSphereNode = CollisionNode(sphereName)
        collSphereNode.addSolid(collSphere)
        collSphereNode.setFromCollideMask(BitMask32.allOff())
        collSphereNode.setIntoCollideMask(BitMask32.allOff())
        self.collSphereNodePath = self.av.attachNewNode(collSphereNode)
        self.collSphereNodePath.stash()
        self.collHandler = CollisionHandlerEvent()
        self.collHandler.addInPattern('enterradarSphere')
        self.collHandler.addOutPattern('exitradarSphere')
        base.cTrav.addCollider(self.collSphereNodePath, self.collHandler)

    def resetRadius(self, radius):
        if self.radius == radius:
            return
        self.radius = radius
        self.__normalizeWithRadius()
        collSphereNode = self.collSphereNodePath.getNode(0)
        collSphere = collSphereNode.modifySolid(0)
        collSphere.setRadius(self.radius - self.battleAvatarTubeRadius)
        if self.map:
            self.map.setZoomScale(self.radius)

    def removeCollisions(self):
        base.cTrav.removeCollider(self.collSphereNodePath)
        if self.collSphereNodePath:
            self.collSphereNodePath.detachNode()

    def radarObjectCollEnter(self, collEntry):
        radarObj = collEntry.getIntoNodePath()
        radarObjId = self.getObjIdFromCollNode(radarObj)
        objType = RADAR_OBJ_TYPE_DEFAULT
        self.addRadarObject(radarObjId, radarObj, objType)

    def getObjIdFromCollNode(self, radarObj):
        doIdStr = radarObj.getNetTag('avId')
        if doIdStr == '':
            doIdStr = radarObj.getNetTag('avIdStr')
            if doIdStr == '':
                return
            return doIdStr
        radarObjDoId = int(doIdStr)
        return radarObjDoId

    def radarObjectCollExit(self, collEntry):
        radarObj = collEntry.getIntoNodePath()
        radarObjId = self.getObjIdFromCollNode(radarObj)
        self.removeRadarObject(radarObjId)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def restoreCachedObject(self, objId, srcObjNode):
        self.__radarObjects[objId] = self.__cachedRadarObjects[objId]
        radarNode, outOfRangeNode = self.makeRadarNode(srcObjNode, self.__radarObjects[objId]['type'])
        self.__radarObjects[objId]['radarObjNode'] = radarNode
        self.__radarObjects[objId]['outOfRangeNode'] = outOfRangeNode
        self.__radarObjects[objId]['srcObjNode'] = srcObjNode
        del self.__cachedRadarObjects[objId]

    def restoreStickyCachedObjects(self):
        cachedKeys = list(self.__cachedRadarObjects.keys())
        for currObjKey in cachedKeys:
            if self.__cachedRadarObjects[currObjKey]['type'] != RADAR_OBJ_TYPE_DEFAULT or self.__cachedRadarObjects[currObjKey]['type'] != RADAR_OBJ_TYPE_EXIT:
                dummyObjNode = self.__cachedRadarObjects[currObjKey]['dummySrcObjNode']
                self.restoreCachedObject(currObjKey, dummyObjNode)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def addRadarObject(self, objId, radarObj, objType=RADAR_OBJ_TYPE_DEFAULT, dummySrcObjNode=None, teamId=None, enableUnconvert=False):
        if objId in self.__radarObjects:
            if objType != RADAR_OBJ_TYPE_DEFAULT:
                if objType == RADAR_OBJ_TYPE_TUTORIAL:
                    objType = RADAR_OBJ_TYPE_DEFAULT
                    self.convertRadarObject(objType, objId, teamId)
                else:
                    self.convertRadarObject(objType, objId, enableUnconvert=enableUnconvert)
            if radarObj == None:
                radarObj = self.__radarObjects[objId]['srcObjNode']
            self.updateObjRef(radarObj, objId, dummySrcObjNode=dummySrcObjNode)
        else:
            if objId in self.__cachedRadarObjects:
                if not radarObj:
                    radarObj = self.__cachedRadarObjects[objId]['dummySrcObjNode']
                self.restoreCachedObject(objId, radarObj)
                if objType != RADAR_OBJ_TYPE_DEFAULT:
                    if objType == RADAR_OBJ_TYPE_TUTORIAL:
                        objType = RADAR_OBJ_TYPE_DEFAULT
                    self.convertRadarObject(objType, objId, teamId)
            else:
                srcNode = radarObj
                if radarObj == None:
                    srcNode = dummySrcObjNode
                if objType == RADAR_OBJ_TYPE_TUTORIAL:
                    objType = RADAR_OBJ_TYPE_DEFAULT
                    radarNode, outOfRangeNode = self.makeRadarNode(srcNode, objType, objId, teamId=teamId)
                else:
                    radarNode, outOfRangeNode = self.makeRadarNode(srcNode, objType)
                newRadarObjInfo = {'type': objType, 'radarObjNode': radarNode, 'outOfRangeNode': outOfRangeNode, 'srcObjNode': srcNode, 'dummySrcObjNode': dummySrcObjNode}
                self.__radarObjects[objId] = newRadarObjInfo
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def removeRadarObject(self, objId, force=False):
        objInfo = self.__radarObjects.get(objId)
        if objInfo:
            if objInfo['type'] == RADAR_OBJ_TYPE_DEFAULT or objInfo['type'] == RADAR_OBJ_TYPE_EXIT or force:
                self.moveRadarObjToCache(objId, skipCache=force)
            else:
                self.updateObjRef(objInfo['dummySrcObjNode'], objId)

    def restoreRadarObject(self, objId):
        restoreResult = self.restoreOldInfo(objId)
        if restoreResult == False:
            self.moveRadarObjToCache(objId, skipCache=True)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def convertRadarObject(self, toType, objId, teamId=None, enableUnconvert=False):
        objectInfo = self.__radarObjects.get(objId)
        if objectInfo == None:
            return
        if objectInfo['type'] != toType:
            if enableUnconvert:
                objectInfo['oldInfo'] = {'type': objectInfo['type'], 'radarObjNode': objectInfo['radarObjNode'], 'outOfRangeNode': objectInfo['outOfRangeNode'], 'dummySrcObjNode': objectInfo['dummySrcObjNode']}
            objectInfo['type'] = toType
            objectInfo['radarObjNode'].hide()
            outOfRangeNode = objectInfo['outOfRangeNode']
            if outOfRangeNode:
                outOfRangeNode.hide()
            objectInfo['radarObjNode'], objectInfo['outOfRangeNode'] = self.makeRadarNode(objectInfo['srcObjNode'], toType, objId, teamId)
            if objectInfo['type'] == RADAR_OBJ_TYPE_DEFAULT:
                objectInfo['dummySrcObjNode'].hide()
                objectInfo['dummySrcObjNode'] = None
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def updateObjRef(self, object, objId, dummySrcObjNode=None):
        objectInfo = self.__radarObjects[objId]
        if dummySrcObjNode:
            objectInfo['dummySrcObjNode'] = dummySrcObjNode
        objectInfo['srcObjNode'] = object

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def addRadarObjectAtLoc(self, pos, objType=RADAR_OBJ_TYPE_DEFAULT, targetObjId=None, teamId=None, enableUnconvert=False):
        desiredRadarNode = render.attachNewNode('desiredRadarNode')
        desiredRadarNode.setPos(pos)
        self.addRadarObject(targetObjId, None, objType, dummySrcObjNode=desiredRadarNode, teamId=teamId, enableUnconvert=enableUnconvert)
        return

    def removeAllObjects(self):
        objects = list(self.__radarObjects.keys())
        for key in objects:
            self.moveRadarObjToCache(key)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def moveRadarObjToCache(self, objKey, skipCache=False):
        self.endFlashRadarObject(objKey)
        objInfo = self.__radarObjects.pop(objKey, None)
        objInfo['radarObjNode'].removeNode()
        outOfRangeNode = objInfo['outOfRangeNode']
        if outOfRangeNode:
            outOfRangeNode.removeNode()
        if objInfo['type'] != RADAR_OBJ_TYPE_DEFAULT and objInfo['type'] != RADAR_OBJ_TYPE_EXIT and skipCache == False:
            objInfo['radarObjNode'] = None
            objInfo['outOfRangeNode'] = None
            objInfo['srcObjNode'] = None
            self.__cachedRadarObjects[objKey] = objInfo
        else:
            if (objInfo['type'] == RADAR_OBJ_TYPE_DEFAULT or objInfo['type'] == RADAR_OBJ_TYPE_EXIT) and objInfo['dummySrcObjNode'] and not objInfo['dummySrcObjNode'].isEmpty():
                objInfo['dummySrcObjNode'].removeNode()
        return

    def clearCache(self):
        objects = list(self.__cachedRadarObjects.keys())
        for key in objects:
            objInfo = self.__cachedRadarObjects[key]
            objInfo['radarObjNode'].removeNode()
            outOfRangeNode = objInfo['outOfRangeNode']
            if outOfRangeNode:
                outOfRangeNode.removeNode()
            del self.__cachedRadarObjects[key]

    def printRadarObjects(self):
        print(self.__radarObjects)

    def getRadarObjects(self):
        return self.__radarObjects

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def makeRadarNode(self, obj, objType, objDoId=None, teamId=None):
        model = None
        outOfRangeNode = None
        camH = camera.getH(render)
        if objType != RADAR_OBJ_TYPE_QUEST and obj.getCollideMask().hasBitsInCommon(PiratesGlobals.RadarShipBitmask):
            modelDict = self.modelDict[RADAR_OBJ_TYPE_SHIP]
        else:
            modelDict = self.modelDict[objType]
        model = modelDict[0].copyTo(self.objTop)
        if modelDict[1]:
            outOfRangeNode = modelDict[1].copyTo(self.objTop)
        if objType == RADAR_OBJ_TYPE_DEFAULT:
            status = PiratesGlobals.NEUTRAL
            if teamId:
                status = TeamUtils.teamStatus(localAvatar.getTeam(), teamId)
            else:
                avId = objDoId or obj.getNetTag('avId')
                if avId:
                    avId = int(avId)
                    av = base.cr.doId2do.get(avId)
                    if av:
                        if DistributedBandMember.areSameCrew(localAvatar.doId, avId):
                            status = PiratesGlobals.CREW
                        else:
                            status = TeamUtils.friendOrFoe(localAvatar, av)
                    else:
                        return (
                         model, outOfRangeNode)
            if status == PiratesGlobals.ENEMY or status == PiratesGlobals.PVP_ENEMY:
                model.setColorScale(1.0, 0.1, 0.1, 0.6)
            elif status == PiratesGlobals.FRIEND or status == PiratesGlobals.PVP_FRIEND:
                model.setColorScale(0.1, 0.5, 1.0, 0.6)
            elif status == PiratesGlobals.CREW:
                model.setColorScale(0.9, 0.5, 0.95, 1)
            else:
                model.setColorScale(0.1, 1.0, 0.1, 0.6)
        else:
            if objType == RADAR_OBJ_TYPE_QUEST:
                model.setColorScale(1, 1, 0, 1)
                if outOfRangeNode:
                    outOfRangeNode.setColorScale(1, 1, 0, 1)
                    outOfRangeNode.setScale(0.75)
        x, z, relH, inRange = self.getXZHRelative(obj)
        model.setPos(x, 0, z)
        model.setR(relH)
        if outOfRangeNode:
            outOfRangeNode.setPos(x, 0, z)
            if outOfRangeNode.getName() == self.arrow.getName():
                arrow = outOfRangeNode.getChild(0)
                arrow.lookAt(x, 0, z)
        return (
         model, outOfRangeNode)

    def enterOn(self):
        self.collSphereNodePath.unstash()
        taskMgr.doMethodLater(0.1, self.draw, 'drawRadarTask')
        self.accept(self.enterSphereEvent, self.radarObjectCollEnter)
        self.accept(self.exitSphereEvent, self.radarObjectCollExit)
        self.accept('-', self.zoomOut)
        self.accept('=', self.zoomIn)
        self.accept('+', self.zoomIn)
        self.zoomFSM.request(self.lastZoom)
        self.reparentTo(base.a2dTopRight)
        self.restoreStickyCachedObjects()
        if self.map:
            self.map.startUpdateTask()

    def exitOn(self):
        if not self.collSphereNodePath.isSingleton():
            self.collSphereNodePath.stash()
        collisionNode = self.collSphereNodePath.getNode(0)
        if hasattr(self, 'zoomFSM'):
            self.zoomFSM.request('Off')
        self.ignore(self.enterSphereEvent)
        self.ignore(self.exitSphereEvent)
        self.ignore('-')
        self.ignore('=')
        self.ignore('+')
        taskMgr.remove('drawRadarTask')
        self.removeAllObjects()
        self.detachNode()
        if self.map:
            self.map.stopUpdateTask()

    def getXZHRelative(self, obj):
        self.relNode.setPos(self.av, 0, 0, 0)
        self.relNode.setHpr(render, 0, 0, 0)
        d = obj.getPos(self.relNode)
        h = obj.getH(self.relNode) + 90
        d.setZ(0.0)
        inRange = 1
        if d.length() > self.radius:
            inRange = 0
            dNorm = Vec3(d)
            dNorm.normalize()
            d = dNorm * self.radius
        dx = d[0] * self.__kX
        dz = d[1] * self.__kZ
        return (
         dx, dz, h, inRange)

    def draw(self, task):
        camH = camera.getH(render)
        for objId in self.__radarObjects:
            objInfo = self.__radarObjects[objId]
            objType = objInfo['type']
            radarNode = objInfo['radarObjNode']
            outOfRangeNode = objInfo['outOfRangeNode']
            srcObjNode = objInfo['srcObjNode']
            if srcObjNode:
                if srcObjNode.isEmpty():
                    self.moveRadarObjToCache(objId)
                    return Task.again
                if radarNode and not srcObjNode.getParent().isEmpty() and not srcObjNode.isEmpty():
                    dx, dz, relH, inRange = self.getXZHRelative(objInfo['srcObjNode'])
                    if inRange:
                        radarNode.setPos(dx, 0, dz)
                        if objType == RADAR_OBJ_TYPE_EXIT:
                            radarNode.getChild(0).lookAt(dx, 0, dz)
                            radarNode.getChild(0).getChild(0).setH(90)
                            outOfRangeNode.hide()
                        else:
                            radarNode.setR(-relH - 90)
                        radarNode.show()
                    else:
                        radarNode.hide()
                        if objType == RADAR_OBJ_TYPE_EXIT:
                            outOfRangeNode.show()
                            outOfRangeNode.getChild(0).getChild(0).setHpr(90, 0, 90)
                    if outOfRangeNode:
                        if objType == RADAR_OBJ_TYPE_QUEST:
                            basePiece = outOfRangeNode.find('**/icon_objective*')
                            if not basePiece.isEmpty():
                                inRange or basePiece.show()
                            else:
                                basePiece.hide()
                    child = outOfRangeNode.getChild(0)
                    child.lookAt(dx, 0, dz)
                    vec = VBase3(dx, 0, dz)
                    vec.normalize()
                    outOfRangeNode.setPos(vec[0], 0, vec[2])
                dummyNode = objInfo.get('dummySrcObjNode')
                if dummyNode and objInfo['srcObjNode'].compareTo(dummyNode) != 0:
                    dummyNode.setPos(objInfo['srcObjNode'].getPos(render))

        self.dial.setR(camH)
        self.north.setR(-camH)
        self.objTop.setR(camH)
        return Task.again

    def toggle(self, args=None):
        if self.state == 'Off':
            self.request('On')
        else:
            if self.state == 'On':
                self.request('Off')

    def toggleDisplay(self, useReceiveEffect=False, destPos=None):
        if self.isHidden() or useReceiveEffect:
            self.show()
            if useReceiveEffect:
                self.zoomFSM.request('Zoom1')
                if destPos:
                    self.resetRadius(50)
                    localAvatar.guiMgr.createReceiveEffect(self, explain=True)
                else:
                    localAvatar.guiMgr.radarGui.la.setColorScale(1, 1, 1, 1)
                    localAvatar.guiMgr.createReceiveEffect(self, explain=False)
        else:
            self.hide()

    def addEffectIval(self, ival):
        self.effectIvals.append(ival)

    def zoomIn(self):
        self.zoomInSfx.play()
        if self.zoomFSM.state == 'Off':
            self.zoomFSM.request('Zoom1')
        else:
            if self.zoomFSM.state == 'Zoom1':
                return
            else:
                if self.zoomFSM.state == 'Zoom2':
                    self.zoomFSM.request('Zoom1')
                else:
                    if self.zoomFSM.state == 'Zoom3':
                        self.zoomFSM.request('Zoom2')

    def zoomOut(self):
        self.zoomOutSfx.play()
        if self.zoomFSM.state == 'Off':
            self.zoomFSM.request('Zoom1')
        else:
            if self.zoomFSM.state == 'Zoom1':
                self.zoomFSM.request('Zoom2')
            else:
                if self.zoomFSM.state == 'Zoom2':
                    self.zoomFSM.request('Zoom3')
                else:
                    if self.zoomFSM.state == 'Zoom3':
                        return

    def loadMap(self, modelPath):
        if self.map:
            self.map.setAreaModel(modelPath)

    def unloadMap(self):
        if self.map:
            self.map.clearAreaModel()

    def getRadarObjNode(self, objId):
        radarObjInfo = self.__radarObjects.get(objId)
        if radarObjInfo == None:
            if self.map:
                uItem = self.map.getIconAV()
            uItem = None
        else:
            inNode = radarObjInfo['radarObjNode']
            outNode = radarObjInfo['outOfRangeNode']
            if inNode == None or inNode.isHidden():
                uItem = outNode
            else:
                uItem = inNode
            if outNode == None or outNode.isHidden():
                uItem = inNode
            else:
                uItem = outNode
        return uItem

    def flashRadarObject(self, objId, duration=None, scaleMin=Point3(0.5, 0.5, 0.5), scaleMax=Point3(1.0, 1.0, 1.0)):
        if duration != None and objId in self.flashCleanupTasks:
            task = self.flashCleanupTasks[objId][0]
            currentTime = taskMgr._TaskManager__getTime()
            task.delayTime = duration
            task.wakeTime = currentTime + duration
            return True
        uItem = self.getRadarObjNode(objId)
        if uItem == None or uItem.isEmpty():
            return False
        displayIval = Sequence(LerpScaleInterval(uItem, duration=0.5, scale=scaleMax, startScale=scaleMin, blendType='noBlend'), LerpScaleInterval(uItem, duration=0.5, scale=scaleMin, startScale=scaleMax, blendType='noBlend'))
        displayIval.loop()
        if duration == None:
            self.addEffectIval([displayIval, objId])
        else:
            self.flashCleanupTasks[objId] = [
             taskMgr.doMethodLater(duration, self.endFlashRadarObject, 'endRadarObjFlash-' + str(objId), extraArgs=[objId]), displayIval]
        self.addEffectIval(displayIval)
        return True

    def flashRadarObjectTimed(self, objId, duration=5.0, scaleMin=Point3(0.75, 0.75, 0.75), scaleMax=Point3(1.25, 1.25, 1.25)):
        self.flashRadarObject(objId, duration, scaleMin=scaleMin, scaleMax=scaleMax)

    def endFlashRadarObject(self, objId):
        flashInfo = self.flashCleanupTasks.pop(objId, None)
        if flashInfo:
            taskMgr.remove(flashInfo[0])
            flashInfo[1].finish()
            uItem = self.getRadarObjNode(objId)
            if uItem and not uItem.isEmpty():
                uItem.setScale(1.0, 1.0, 1.0)
        return Task.done

    def cleanupEffects(self):
        for currIval, currObjId in self.effectIvals:
            currIval.finish()
            uItem = self.getRadarObjNode(currObjId)
            if uItem and not uItem.isEmpty():
                uItem.setScale(1.0, 1.0, 1.0)

        self.effectIvals = []

    def refreshRadarObject(self, objId):
        if objId in self.__radarObjects:
            outOfRangeNode = self.__radarObjects[objId]['outOfRangeNode']
            dummySrcObjNode = self.__radarObjects[objId]['dummySrcObjNode']
            type = self.__radarObjects[objId]['type']
            radarObjNode = self.__radarObjects[objId]['radarObjNode']
            srcObjNode = self.__radarObjects[objId]['srcObjNode']
            self.removeRadarObject(objId)
            self.addRadarObject(objId, srcObjNode)

    def restoreOldInfo(self, objId):
        objectInfo = self.__radarObjects.get(objId)
        if not objectInfo:
            return True
        offRadar = objectInfo['srcObjNode'] is objectInfo['dummySrcObjNode'] and objectInfo['dummySrcObjNode'] != None
        if objectInfo and not offRadar:
            if 'oldInfo' in objectInfo:
                objectInfo['type'] = objectInfo['oldInfo']['type']
                radarObjNode = objectInfo.get('radarObjNode')
                if radarObjNode and not radarObjNode.isEmpty():
                    radarObjNode.removeNode()
                objectInfo['radarObjNode'] = objectInfo['oldInfo']['radarObjNode']
                radarObjNode = objectInfo.get('radarObjNode')
                radarObjNodeShown = False
                if radarObjNode and not radarObjNode.isEmpty():
                    radarObjNodeShown = True
                    radarObjNode.show()
                outOfRangeNode = objectInfo.get('outOfRangeNode')
                if outOfRangeNode and not outOfRangeNode.isEmpty():
                    outOfRangeNode.removeNode()
                objectInfo['outOfRangeNode'] = objectInfo['oldInfo']['outOfRangeNode']
                outOfRangeNode = objectInfo.get('outOfRangeNode')
                if outOfRangeNode and not outOfRangeNode.isEmpty():
                    outOfRangeNode.show()
                dummySrcObjNode = objectInfo.get('dummySrcObjNode')
                if dummySrcObjNode and not dummySrcObjNode.isEmpty():
                    dummySrcObjNode.removeNode()
                objectInfo['dummySrcObjNode'] = objectInfo['oldInfo']['dummySrcObjNode']
                if radarObjNodeShown == False and 'dummySrcObjNode' in objectInfo and objectInfo['dummySrcObjNode']:
                    objectInfo['dummySrcObjNode'].show()
                del objectInfo['oldInfo']
            else:
                self.convertRadarObject(RADAR_OBJ_TYPE_DEFAULT, objId)
            return True
        else:
            return False
        return
# okay decompiling .\pirates\piratesgui\RadarGui.pyc
