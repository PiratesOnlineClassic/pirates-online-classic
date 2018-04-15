from pandac.PandaModules import *
from direct.distributed import DistributedNode
from direct.distributed import DistributedObject
from direct.showbase.PythonUtil import Functor, report
from direct.actor import Actor
from pirates.world import WorldGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.effects import EnvironmentEffects
from pirates.effects import SwampEffects
from pirates.effects import ForestEffects
from pirates.effects import CaveEffects
from pirates.piratesbase import TimeOfDayManager, TODGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import UserFunnel
from pirates.tutorial import ChatTutorial
from pirates.tutorial import ChatTutorialAlt
from pirates.tutorial import CrewTutorial
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionHandlerEvent
from pirates.quest.QuestConstants import LocationIds
from pirates.chat.PiratesChatManager import PiratesChatManager
from pirates.seapatch.SeaPatch import SeaPatch
from pirates.seapatch.Reflection import Reflection
from pirates.seapatch.Water import IslandWaterParameters
from pirates.swamp.Swamp import Swamp
from pirates.ai import HolidayGlobals
import time

class DistributedGameArea(DistributedNode.DistributedNode):
    notify = directNotify.newCategory('DistributedGameArea')

    def __init__(self, cr):
        DistributedNode.DistributedNode.__init__(self, cr)
        NodePath.__init__(self, 'GameArea')
        self.uniqueId = ''
        self.geom = None
        self.funnelDisplayName = None
        self.previousDisplayName = None
        self.__onOffState = False
        self.gameFSM = None
        self.links = []
        self.pendingSetupConnector = {}
        self.connectors = {}
        self.connectorInterests = set()
        self.envEffects = None
        self.spawnTriggers = []
        self.blockerColls = []
        self.islandWaterParameters = None
        self.swamp_water = None
        self.entryTime = [None, 0]
        self.timeCheck = 0

    def __repr__(self):
        return '%s (%s)' % (DistributedNode.DistributedNode.__repr__(self), self.getName())

    def disable(self):
        taskMgr.remove('showEnterMessage')
        DistributedNode.DistributedNode.disable(self)
        if self.geom:
            self.geom.removeNode()

        self.unloadConnectors()
        for request in self.pendingSetupConnector.itervalues():
            self.cr.relatedObjectMgr.abortRequest(request)

        self.pendingSetupConnector = {}

    def delete(self):
        for trigger in self.spawnTriggers:
            trigger.removeNode()

        del self.spawnTriggers
        del self.connectors
        del self.links
        if self.envEffects:
            self.envEffects.delete()
            self.envEffects = None

        DistributedNode.DistributedNode.delete(self)
        if self.islandWaterParameters:
            del self.islandWaterParameters

        if self.swamp_water:
            self.swamp_water.delete()
            del self.swamp_water

    def setLocation(self, parentId, zoneId, teleport = 0):
        DistributedObject.DistributedObject.setLocation(self, parentId, zoneId)
        if parentId != 0:
            parentObj = self.cr.doId2do.get(parentId)
            self.reparentTo(parentObj)

    def setName(self, name):
        self.name = name

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def handleChildArrive(self, childObj, zoneId):
        DistributedNode.DistributedNode.handleChildArrive(self, childObj, zoneId)
        if childObj.isLocal():
            childObj.refreshActiveQuestStep()

    def setUniqueId(self, uid):
        if self.uniqueId != '':
            self.cr.uidMgr.removeUid(self.uniqueId)

        self.uniqueId = uid
        self.cr.uidMgr.addUid(self.uniqueId, self.getDoId())

    def getUniqueId(self):
        return self.uniqueId

    def loadModel(self):
        pass

    @report(types = ['frameCount', 'args'], dConfigParam = ['want-jail-report'])
    def setLinks(self, links):
        for link in links:
            (areaNode, connId, areaUid, connParent, connZone, connNode, connWorld, connWorldZone) = link
            self.links.append([
                connId,
                connParent,
                connZone])

            def setupConnector(connector):
                connector.interior = self
                self.connectors[connector.doId] = connector
                request = self.pendingSetupConnector.pop(connector.doId, None)
                if not request:
                    pass

            connector = self.cr.doId2do.get(connId)
            if connector:
                self.pendingSetupConnector[connId] = None
                setupConnector(connector)

            elif connId:
                if connId in self.pendingSetupConnector:
                    request = self.pendingSetupConnector.pop(connId)
                    self.cr.relatedObjectMgr.abortRequest(request)

                request = self.cr.relatedObjectMgr.requestObjects([
                    connId], eachCallback = setupConnector)
                self.pendingSetupConnector[connId] = request

    @report(types = ['frameCount', 'args'], dConfigParam = ['want-jail-report', 'want-teleport-report'])
    def loadConnectors(self):
        for link in self.links:
            if link:
                connectorId = link[0]
                if connectorId not in self.connectorInterests:
                    self.connectorInterests.add(connectorId)
                    parentId = link[1]
                    zoneId = link[2]
                    connectorEvent = 'connector-%s' % connectorId
                    self.acceptOnce(connectorEvent, self.reparentConnector,
                                    extraArgs = [connectorId])
                    localAvatar.setInterest(parentId, zoneId,
                                            ['Connectors-%s' % self.doId],
                                            connectorEvent)

                self.reparentConnector(connectorId)

    @report(types = ['frameCount', 'args'], dConfigParam = ['want-jail-report', 'want-teleport-report'])
    def unloadConnectors(self):
        for (connectorId, connector) in self.connectors.iteritems():
            if connector:
                connector.setLoadedArea(None)
                connector.turnOff()

        self.connectors = {}
        localAvatar.clearInterestNamed('connectorInterestCleared', [
            'Connectors-%s' % self.doId])
        self.connectorInterests = set()

    @report(types = ['frameCount', 'args'], dConfigParam = ['want-jail-report', 'want-teleport-report'])
    def reparentConnector(self, connectorId):
        connector = self.cr.doId2do.get(connectorId)
        if connector:
            self.connectors[connectorId] = connector
            if connector.dclass.getName() == 'DistributedGATunnel':
                connector.reparentConnectorToArea(self)

            if self.__onOffState:
                connector.turnOn()
            else:
                connector.turnOff()

    @report(types = ['frameCount', 'args'], dConfigParam = ['want-jail-report', 'want-teleport-report'])
    def handleEnterGameArea(self, collEntry = None):
        if localAvatar.style.getTutorial() == PiratesGlobals.TUT_CHAPTER3_STARTED:
            if localAvatar.chatMgr.noChat:
                ct = ChatTutorialAlt.ChatTutorialAlt()
            else:
                ct = ChatTutorial.ChatTutorial()

        taskMgr.doMethodLater(1, self.showEnterMessage, 'showEnterMessage')
        UserFunnel.logSubmit(0, 'ENTERING_' + str(self.funnelDisplayName))
        UserFunnel.logSubmit(1, 'ENTERING_' + str(self.funnelDisplayName))
        displayName = PLocalizer.LocationNames.get(self.uniqueId)
        base.setLocationCode(displayName)
        self.storeLocationTime(self.funnelDisplayName, time.time())

    def storeLocationTime(self, loc, time):
        if loc == self.entryTime[0]:
            if self.entryTime[1] == 0:
                self.entryTime[1] = time
            return
        else:
            self.entryTime = [
                loc,
                time]

    def readLocationTime(self):
        return self.entryTime[1]

    def showEnterMessage(self, task):
        displayName = PLocalizer.LocationNames.get(self.uniqueId)
        self.displayGameAreaName(displayName)
        localAvatar.guiMgr.radarGui.showLocation(self.uniqueId)

    @report(types = ['frameCount', 'args'], dConfigParam = [ 'want-jail-report', 'want-teleport-report'])
    def handleExitGameArea(self, collEntry = None):
        UserFunnel.logSubmit(0, 'EXITING_' + str(self.funnelDisplayName))
        UserFunnel.logSubmit(1, 'EXITING_' + str(self.funnelDisplayName))
        self.previousDisplayName = None
        displayName = str(self.funnelDisplayName)
        timeSpent = int(time.time()) - int(self.readLocationTime())
        if int(self.timeCheck) + 1 == int(timeSpent) or int(self.timeCheck) - 1 == int(timeSpent) or int(self.timeCheck) == int(timeSpent):
            pass
        else:
            base.cr.centralLogger.writeClientEvent('EXITING_AREA|%s|%d' % (displayName, timeSpent))
            self.timeCheck = timeSpent

    def displayGameAreaName(self, displayName):
        self.funnelDisplayName = displayName
        if self.previousDisplayName != displayName:
            self.previousDisplayName = displayName
            base.localAvatar.guiMgr.createTitle(displayName, PiratesGuiGlobals.TextFG2)

    def setPlayerBarrier(self, isOn):
        pass

    def setupCannonballLandColl(self, collNode, mask, index):
        if collNode and not collNode.isEmpty():
            collNode.node().setCollideMask(mask)
            collNode.setTag('objType', str(PiratesGlobals.COLL_LAND))
            collNode.setTag('groundCode', str(index))
            collNode.setTag('groundId', str(self.doId))

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        pass

    def startCustomEffects(self, interior = True):
        if self.envEffects:
            self.envEffects.delete()
            self.envEffects = None

        if 'swamp' in self.modelPath:
            self.envEffects = SwampEffects.SwampEffects(self, self.modelPath)
            base.musicMgr.request('swamp')
        elif 'jungle' in self.modelPath:
            self.envEffects = ForestEffects.ForestEffects(self, self.modelPath)
            base.musicMgr.request('jungle')
        elif 'cave' in self.modelPath:
            self.envEffects = CaveEffects.CaveEffects(self, self.modelPath)
            base.musicMgr.request('cave')
        elif self.uniqueId == '1189479168.0sdnaik0':
            r = Reflection.getGlobalReflection()
            saintPatricksDay = base.saintPatricksDay
            water = SeaPatch(self, reflection = r, saintPatricksDay = saintPatricksDay)
            water.loadSeaPatchFile('out.spf')
            self.water = water
            self.initializeIslandWaterParameters()
            base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_DEFAULT)
        else:
            self.envEffects = EnvironmentEffects.EnvironmentEffects(self, self.modelPath)
            if interior:
                self.cr.timeOfDayManager.request('NoLighting')

            for holidayId in self.cr.newsManager.holidayIdList:
                holidayName = HolidayGlobals.getHolidayName(holidayId)
                self.envEffects.loadHolidayEffects(holidayName)

    def stopCustomEffects(self):
        if self.envEffects:
            self.envEffects.delete()
            self.envEffects = None

        if 'swamp' in self.modelPath:
            base.musicMgr.requestFadeOut('swamp')
        elif 'jungle' in self.modelPath:
            base.musicMgr.requestFadeOut('jungle')
        elif 'cave' in self.modelPath:
            base.musicMgr.requestFadeOut('cave')
        elif self.uniqueId == '1189479168.0sdnaik0':
            self.water.delete()
            self.water = None

    def updateAvReturnLocation(self, av, uniqueId):
        pass

    @report(types = ['frameCount', 'args'], dConfigParam = ['want-jail-report', 'want-teleport-report'])
    def quickLoadOtherSide(self):
        connector = self.connectors.get(localAvatar.lastConnectorId)
        if connector:
            connector.quickLoadOtherSide()

    def addSpawnTriggers(self, triggerSpheres):
        for (x, y, z, triggerRadius, spawnPtId) in triggerSpheres:
            objectSphere = CollisionSphere(x, y, z, triggerRadius)
            objectName = uniqueName('spawnTriggerSphere')
            objectSphere.setTangible(0)
            objectSphereNode = CollisionNode(objectName)
            objectSphereNode.addSolid(objectSphere)
            objectSphereNode.setIntoCollideMask(PiratesGlobals.WallBitmask)
            objectSphereNodePath = self.attachNewNode(objectSphereNode)
            self.accept('enter' + objectName, self.handleEnterSphere, extraArgs = [
                spawnPtId])
            self.spawnTriggers.append(objectSphereNodePath)

    def handleEnterSphere(self, spawnPtId, entry):
        if base.localAvatar:
            if hasattr(base.localAvatar, 'getDoId'):
                doId = base.localAvatar.getDoId()
                self.sendUpdate('spawnNPC', [
                    spawnPtId,
                    doId])

    def initBlockers(self, geom):
        self.disableBlockers = False
        if base.config.GetBool('disable-blockers', False):
            self.disableBlockers = True

        blockerColls = geom.findAllMatches('**/blocker_*')
        interior = False
        if not blockerColls.isEmpty():
            if blockerColls[0].getName().find('_i') != -1:
                interior = True

            for i in range(0, blockerColls.getNumPaths()):
                self.blockerColls.append(blockerColls[i])
                if self.disableBlockers:
                    blockerColls[i].stash()

        if interior:
            self.accept('enterblocker_1_i', self.handleInteriorBlockerCollision)
        else:
            self.accept('enterblocker_1', self.handleBlockerCollision)
            self.accept('enterblocker_0', self.handleBlockerCollision)

    def stashSpecificBlocker(self, name):
        self.ignore('enter' + name)
        for blocker in self.blockerColls:
            if blocker.getName() == name:
                blocker.stash()

    def stashAllBlockers(self):
        self.ignore('enterblocker_1_i')
        self.ignore('enterblocker_1')
        self.ignore('enterblocker_0')
        for blocker in self.blockerColls:
            blocker.stash()

    def handleInteriorBlockerCollision(self, entry):
        questId = localAvatar.activeQuestId
        if base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_CUTLASS:
            questId = 'c2_visit_will_turner'
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.QuestStrings[questId]['blockerMessage'])
        else:
            self.stashAllBlockers()

    def handleBlockerCollision(self, entry):
        questId = localAvatar.activeQuestId
        if base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_CUTLASS:
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.QuestStrings[questId]['description'])
        elif base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_KILLED_1_SKELETON:
            questId = 'c2.2defeatSkeletons'
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.QuestStrings[questId]['blockerMessage'])
        elif base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_COMPASS:
            questId = 'c2_visit_tia_dalma'
            self.stashSpecificBlocker('blocker_0')
            if entry.getIntoNodePath().getName() != 'blocker_0':
                localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.QuestStrings[questId]['blockerMessage'])

        else:
            self.stashAllBlockers()

    @report(types = ['frameCount'], dConfigParam = 'want-connector-report')
    def turnOn(self, av = None):
        self.__onOffState = True
        for (id, connector) in self.connectors.iteritems():
            if connector:
                connector.turnOn()

    @report(types = ['frameCount'], dConfigParam = 'want-connector-report')
    def turnOff(self):
        self.__onOffState = False
        for (id, connector) in self.connectors.iteritems():
            if connector:
                connector.turnOff()

    def getOnOffState(self):
        return self.__onOffState

    def getTeleportDestPosH(self, index = 0):
        pt = self._getTunnelSpawnPos(index)
        return (pt[0], pt[1], pt[2], 0)

    def _getTunnelSpawnPos(self, index = 0):
        connectorNodes = self.findAllMatches('**/portal_exterior*') + self.findAllMatches('**/portal_interior*')
        return self.getRelativePoint(connectorNodes[index % len(connectorNodes)], Point3(40, 0, 0))

    def initializeIslandWaterParameters(self):
        debug = False
        island_water_parameters = IslandWaterParameters()
        world_position = self.getPos(render)
        world_x_offset = world_position[0]
        world_y_offset = world_position[1]
        world_z_offset = world_position[2]
        if debug:
            print self, '=', self.getName()
            print 'GAME AREA X OFF, Y OFF, Z OFF = ', world_x_offset, world_y_offset, world_z_offset

        model = self.geom.find('**/water_color')
        if model and model.isEmpty() == False:
            if debug:
                print 'WATER COLOR X OFF, Y OFF, Z OFF = ', world_x_offset, world_y_offset, world_z_offset

            model.hide()
            min_point = Point3(0)
            max_point = Point3(0)
            model.calcTightBounds(min_point, max_point)
            size = max_point - min_point
            if self.getH() == 180 or self.getH() == -180:
                x = -min_point[0] + world_x_offset
                y = -min_point[1] + world_y_offset
                x_size = -size[0]
                y_size = -size[1]
            else:
                x = min_point[0] + world_x_offset
                y = min_point[1] + world_y_offset
                x_size = size[0]
                y_size = size[1]
            island_water_parameters.map_x_origin = x
            island_water_parameters.map_y_origin = y
            island_water_parameters.map_x_scale = x_size
            island_water_parameters.map_y_scale = y_size
            if debug:
                print 'X, Y, X SIZE, Y SIZE = ', min_point[0], min_point[1], x_size, y_size

            texture = model.findTexture('*')
            if texture:
                island_water_parameters.water_color_texture = texture
                if debug:
                    print 'WATER COLOR TEXTURE', texture

        elif debug:
            print '*** water_color NODE NOT FOUND'

        model = self.geom.find('**/water_alpha')
        if model and model.isEmpty() == False:
            if debug:
                print 'WATER ALPHA X OFF, Y OFF, Z OFF = ', world_x_offset, world_y_offset, world_z_offset

            model.hide()
            min_point = Point3(0)
            max_point = Point3(0)
            model.calcTightBounds(min_point, max_point)
            size = max_point - min_point
            if self.getH() == 180 or self.getH() == -180:
                x = -min_point[0] + world_x_offset
                y = -min_point[1] + world_y_offset
                x_size = -size[0]
                y_size = -size[1]
            else:
                x = min_point[0] + world_x_offset
                y = min_point[1] + world_y_offset
                x_size = size[0]
                y_size = size[1]
            island_water_parameters.alpha_map_x_origin = x
            island_water_parameters.alpha_map_y_origin = y
            island_water_parameters.alpha_map_x_scale = x_size
            island_water_parameters.alpha_map_y_scale = y_size
            if debug:
                print 'ALPHA X, Y, X SIZE, Y SIZE = ', min_point[0], min_point[1], x_size, y_size

            texture = model.findTexture('*')
            if texture:
                island_water_parameters.water_alpha_texture = texture
                if debug:
                    print 'WATER ALPHA TEXTURE', texture

        elif debug:
            print '*** water_alpha NODE NOT FOUND'

        use_shader = False
        if base.config.GetBool('want-shaders', 1) and base.win and base.win.getGsg() and base.win.getGsg().getShaderModel() >= GraphicsStateGuardian.SM20:
            use_shader = True

        model_ns = self.geom.find('**/water_swamp_ns')
        if model_ns and model_ns.isEmpty() == False:
            if use_shader:
                model_ns.hide()
            else:
                model_ns.show()
                model = model_ns
                model.setBin('water', 1)
                parent = model.getParent()
                model.detachNode()
                stencil_one_node_path = NodePath('stencil_one')
                stencil_one_node_path.reparentTo(parent)
                model.instanceTo(stencil_one_node_path)
                mask = 0xFFFFFFFFL
                stencil_one = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, mask, mask)
                stencil_one_node_path.setAttrib(stencil_one, 100)
                stencil_one_node_path.setDepthTest(0)

        model_alpha_texture = None
        model_alpha = self.geom.find('**/water_alpha_swamp')
        if model_alpha and model_alpha.isEmpty() == False:
            model_alpha_texture = model_alpha.findTexture('*')
            model_alpha.hide()
            if debug:
                print 'model_alpha_texture', model_alpha_texture

            if False:
                texture = model_alpha_texture
                card_x_size = 0.5
                card_y_size = 0.5
                card = CardMaker('test_texture_card')
                card.setFrame(-card_x_size, card_x_size, -card_y_size, card_y_size)
                card_node_path = NodePath(card.generate())
                card_node_path.setTexture(texture, 1)
                card_node_path.node().setBounds(OmniBoundingVolume())
                card_node_path.node().setFinal(1)
                card_node_path.reparentTo(render2d)

        else:
            model_alpha = None
        model = self.geom.find('**/water_color_swamp')
        if model and model.isEmpty() == False:
            if use_shader:
                model.show()
                model_texture = model.findTexture('*')
                if debug:
                    print 'WATER COLOR SWAMP X OFF, Y OFF, Z OFF = ', world_x_offset, world_y_offset, world_z_offset

                parent = model.getParent()
                model.detachNode()
                stencil_one_node_path = NodePath('stencil_one')
                stencil_one_node_path.reparentTo(parent)
                model.instanceTo(stencil_one_node_path)
                mask = 0xFFFFFFFFL
                stencil_one = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, mask, mask)
                stencil_one_node_path.setAttrib(stencil_one, 100)
                stencil_one_node_path.setDepthTest(0)
                min_point = Point3(0)
                max_point = Point3(0)
                model.calcTightBounds(min_point, max_point)
                size = max_point - min_point
                x = min_point[0] + world_x_offset
                y = min_point[1] + world_y_offset
                x_size = size[0]
                y_size = size[1]
                if debug:
                    print 'min_point', min_point
                    print 'max_point', max_point
                    print 'size', size
                    print 'x y', x, y

                island_water_parameters.swamp_map_x_origin = x
                island_water_parameters.swamp_map_y_origin = y
                island_water_parameters.swamp_map_x_scale = x_size
                island_water_parameters.swamp_map_y_scale = y_size
                if debug:
                    print 'X, Y, X SIZE, Y SIZE = ', min_point[0], min_point[1], x_size, y_size

                texture = model.findTexture('*')
                if texture:
                    island_water_parameters.swamp_water_color_texture = texture
                    if debug:
                        print 'SWAMP WATER COLOR TEXTURE', texture

                water_color_file_path = island_water_parameters.default_water_color_file_path
                alpha_texture_file_path = island_water_parameters.default_water_alpha_file_path
                opacity_texture_file_path = None
                shader_file_path = 'models/swamps/cuba_swamp001_2X.cg'
                reflection = Reflection.getGlobalReflection()
                self.swamp_water = Swamp(None, None, reflection, model, shader_file_path)
                island_water_parameters.swamp_water = self.swamp_water
                unload_previous_texture = True
                self.swamp_water.set_water_color_texture(water_color_file_path, unload_previous_texture, model_texture)
                self.swamp_water.set_water_alpha_texture(alpha_texture_file_path, unload_previous_texture, model_alpha_texture)
                self.swamp_water.set_wrap_or_clamp(True)
                r = 37.0
                g = 62.0
                b = 40.0
                self.swamp_water.water_r = r
                self.swamp_water.water_g = g
                self.swamp_water.water_b = b
                island_water_parameters.swamp_color_r = r
                island_water_parameters.swamp_color_g = g
                island_water_parameters.swamp_color_b = b
                x = 0.0
                y = 1.0
                speed = 3.2000000000000002
                island_water_parameters.swamp_direction_x = x
                island_water_parameters.swamp_direction_y = y
                island_water_parameters.swamp_speed = speed
                self.swamp_water.update_water_direction_and_speed(x, y, speed)
            else:
                model.hide()
        elif debug:
            print '*** water_color_swamp NODE NOT FOUND'

        self.islandWaterParameters = island_water_parameters

    def getLevel(self):
        return 1
