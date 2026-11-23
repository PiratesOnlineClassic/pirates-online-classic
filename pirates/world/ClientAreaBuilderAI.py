from panda3d.core import *

from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.GridParent import GridParent

from pirates.quest.QuestConstants import LocationIds
from pirates.leveleditor import ObjectList
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.ship import ShipGlobals
from pirates.tutorial import TutorialGlobals
from pirates.world import WorldGlobals


class ClientAreaBuilderAI(DirectObject):
    notify = directNotify.newCategory('ClientAreaBuilderAI')

    def __init__(self, air, parent):
        self.air = air
        self.parent = parent
        self.objectList = {}

    def getIslands(self):
        from pirates.world.DistributedIslandAI import DistributedIslandAI
        return self.findObjectsOfClass(DistributedIslandAI)

    def findObjectsOfClass(self, objectClass):
        objects = []
        for object in list(self.objectList.values()):
            if isinstance(object, objectClass):
                objects.append(object)

        return objects

    def addObject(self, object, uniqueId=None):
        self.air.uidMgr.addUid(uniqueId or object.getUniqueId(), object.doId)
        self.objectList[object.doId] = object

    def removeObject(self, object, uniqueId=None):
        uid = uniqueId or object.getUniqueId()
        registeredId = self.air.uidMgr.getDoId(uid)
        if registeredId is None or registeredId == object.doId:
            self.air.uidMgr.removeUid(uid)
        del self.objectList[object.doId]

    def getObject(self, doId=None, uniqueId=None):
        for object in list(self.objectList.values()):
            if object.doId == doId or object.getUniqueId() == uniqueId:
                return object

        return None

    def deleteObject(self, doId):
        object = self.objectList.get(doId)
        if not object:
            return

        self.removeObject(object)
        object.requestDelete()

    def broadcastObjectPosition(self, object):
        if not object:
            return

        object.d_setPos(*object.getPos())
        object.d_setHpr(*object.getHpr())

    def parentObjectToCell(self, object, zoneId=None, parent=None):
        if not object:
            return

        parent = parent or self.parent
        if zoneId is None:
            zoneId = parent.getZoneFromXYZ(object.getPos())

        cell = GridParent.getCellOrigin(parent, zoneId)
        originalPos = object.getPos()

        object.reparentTo(cell)
        object.setPos(parent, originalPos)

        self.broadcastObjectPosition(object)

    def isChildObject(self, objKey, parentUid):
        return self.air.worldCreator.getObjectParentUid(objKey) != parentUid

    def setObjectTruePosHpr(self, object, objKey, parentUid, objectData):
        objectPos = objectData.get('Pos', Point3(0, 0, 0))
        objectHpr = objectData.get('Hpr', Point3(0, 0, 0))
        if not self.isChildObject(objKey, parentUid):
            object.setPos(objectPos)
            object.setHpr(objectHpr)
            return object

        parentData = self.air.worldCreator.getObjectDataByUid(parentUid)
        if parentData is None or parentData.get('Type') == 'Island':
            object.setPos(objectPos)
            object.setHpr(objectHpr)
            return object

        parentObject = NodePath('psuedo-%s' % parentUid)
        parentObject.setPos(parentData.get('Pos', Point3(0, 0, 0)))
        parentObject.setHpr(parentData.get('Hpr', Point3(0, 0, 0)))

        object.setPos(parentObject, objectPos)
        object.setHpr(parentObject, objectHpr)
        return object

    def getObjectTruePosAndParent(self, objKey, parentUid, objectData):
        if self.isChildObject(objKey, parentUid):
            parentData = self.air.worldCreator.getObjectDataByUid(parentUid)
            if parentData['Type'] == 'Island':
                return objectData.get('Pos'), NodePath('')

            parentObject = NodePath('psuedo-%s' % parentUid)
            if not 'GridPos' in objectData:
                parentObject.setPos(parentData.get('Pos', Point3(0, 0, 0)))

            parentObject.setHpr(parentData.get('Hpr', Point3(0, 0, 0)))
            objectPos = objectData.get('GridPos', objectData.get('Pos', Point3(0, 0, 0)))
            return objectPos, parentObject

        return objectData.get('Pos'), NodePath('')

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None
        if objType == ObjectList.AREA_TYPE_ISLAND:
            newObj = self.createIsland(objectData, parent, parentUid, objKey, dynamic)
        elif (objType == ObjectList.AREA_TYPE_SHIP_PART
              and objKey == TutorialGlobals.STUMPY_BOAT_UID
              and objectData.get('Category') == 'InterceptorTutorial'
              and self.parent.getFileName() == WorldGlobals.PiratesTutorialSceneFileBase):
            newObj = self.createTutorialShip(objectData, objKey)
        else:
            if not parent or not hasattr(parent, 'builder'):
                parent = self.air.uidMgr.justGetMeMeObject(parentUid)
                if not parent or parent == self.parent:
                    return newObj

            newObj = parent.builder.createObject(objType, objectData, parent, parentUid, objKey, dynamic)

        return newObj

    def createTutorialShip(self, objectData, objKey):
        from pirates.ship.TutorialShipAI import TutorialShipAI

        oceanGrid = getattr(self.parent, 'oceanGrid', None)
        if not oceanGrid:
            raise RuntimeError('Cannot create tutorial ship %s without an ocean grid' % objKey)

        shipClass = ShipGlobals.STUMPY_SHIP
        shipConfig = ShipGlobals.getShipConfig(shipClass)
        hullConfig = ShipGlobals.getHullConfig(shipClass)
        if not shipConfig or not hullConfig:
            raise RuntimeError('Cannot create tutorial ship %s without ship configuration' % objKey)

        self.air.worldCreator.movementLinkManager.registerMovementLinkData(
            self.parent.getUniqueId())
        ship = TutorialShipAI(self.air)
        ship.setUniqueId(objKey)
        ship.setShipClass(shipClass)
        ship.setBaseTeam(PiratesGlobals.teamStr2TeamId(
            objectData.get('Team', PiratesGlobals.PLAYER_TEAM_STR), ShipGlobals.PLAYER_TEAM))
        ship.setLevel(ShipGlobals.getShipLevel(shipClass))
        ship.setNPCship(1)
        ship.setIsBoardable(1)
        ship.setIsFlagship(bool(objectData.get('Flagship', False)))
        ship.setMaxHp(shipConfig['setMaxHp'][0])
        ship.setHp(shipConfig['setHp'][0])
        ship.setMaxSp(hullConfig['setMaxSp'][0])
        ship.setSp(hullConfig['setSp'][0])
        ship.setHullCondition(1 << 7)

        pos = objectData.get('Pos', (0, 0, 0))
        hpr = objectData.get('Hpr', (0, 0, 0))
        zoneId = oceanGrid.getZoneFromXYZ(pos)
        ship.setTutorialAuthoredPose(oceanGrid, pos, hpr)
        oceanGrid.generateChildWithRequired(ship, zoneId)
        ship.setPos(oceanGrid, *pos)
        ship.setHpr(oceanGrid, *hpr)
        oceanGrid.addObjectToOceanGrid(ship)
        ship.sendCurrentPosition()
        ship.startPosHprBroadcast()
        ship.b_setGameState(objectData.get('Start State', 'Idle'), 0)
        self.addObject(ship)

        stumpy = self.createTutorialStumpy(ship)
        ship.setTutorialStumpy(stumpy, self)

        return ship

    def createTutorialStumpy(self, ship):
        from pirates.battle import EnemyGlobals
        from pirates.leveleditor import NPCList
        from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
        from pirates.pirate import AvatarTypes

        dnaId = '1153439632.21darren'
        dna = NPCList.NPC_LIST.get(dnaId)
        if not dna or NPCList.NPC_LIST.get(dnaId + '_type') != 'Townsperson':
            raise RuntimeError('Cannot create tutorial Stumpy without townsperson DNA')

        stumpy = DistributedNPCTownfolkAI(self.air)
        stumpy.setUniqueId(TutorialGlobals.STUMPY_UID)
        stumpy.setDNAId(dnaId)
        stumpy.setName(dna[NPCList.setName])
        stumpy.setAvatarType(AvatarTypes.Commoner)
        stumpy.setTeam(PiratesGlobals.VILLAGER_TEAM)
        stumpy.setCollisionMode(PiratesGlobals.COLL_MODE_FLOORS_CL)

        pos = (0, -1.2, 9)
        hpr = (180, 0, 0)
        stumpy.setPos(pos)
        stumpy.setHpr(hpr)
        stumpy.setScale(1)
        stumpy.setSpawnPos(pos)
        stumpy.setInitZ(pos[2])

        aggroInfo = EnemyGlobals.determineAggroInfo(None)
        stumpy.setAggroMode(aggroInfo[0])
        stumpy.setAggroRadius(aggroInfo[1])

        level = EnemyGlobals.getRandomEnemyLevel(AvatarTypes.Commoner)
        hp, mojo = EnemyGlobals.getEnemyStats(AvatarTypes.Commoner, level)
        stumpy.setLevel(level)
        stumpy.setMaxHp(hp)
        stumpy.setHp(hp, True)
        stumpy.setMaxMojo(mojo)
        stumpy.setMojo(mojo)
        stumpy.setAnimSet('default')
        stumpy.setStartState('Idle')
        stumpy.setAmbush(False)

        ship.generateChildWithRequired(stumpy, PiratesGlobals.ShipZoneOnDeck)
        self.addObject(stumpy)
        stumpy.setPos(ship, *pos)
        stumpy.setHpr(ship, *hpr)
        stumpy.d_setInitZ(stumpy.getZ())
        stumpy.d_setSpawnIn()
        stumpy.b_setGameState(stumpy.getStartState())
        return stumpy

    def createIsland(self, objectData, parent, parentUid, objKey, dynamic):
        from pirates.world.DistributedIslandAI import DistributedIslandAI
        islandWorldData = self.air.worldCreator.getIslandWorldDataByUid(objKey)
        if not islandWorldData:
            self.notify.warning('Failed to generate island: %s' % objKey)
            return

        (x, y, z) = islandWorldData.get('Pos', (0, 0, 0))
        (h, p, r) = islandWorldData.get('Hpr', (0, 0, 0))

        island = DistributedIslandAI(self.air)
        if self.parent.getType() == PiratesGlobals.INSTANCE_TM:
            island.cellWidth = WorldGlobals.ISLAND_TM_CELL_SIZE
            island.gridRadius = WorldGlobals.ISLAND_TM_GRID_RADIUS
        island.setUniqueId(objKey)
        island.setName(PLocalizer.LocationNames.get(objKey, ''))
        island.setFileName(islandWorldData.get('File', ''))
        island.setIslandTransform(x, y, z, h)
        island.setModelPath(islandWorldData['Visual']['Model'])
        island.setScale(objectData.get('Scale', (1, 1, 1)))
        island.setUndockable(objectData.get('Undockable', False))

        portCollisionSpheres = []
        if 'Objects' in islandWorldData:
            for obj in list(islandWorldData['Objects'].values()):
                objType = obj.get('Type')
                if objType == 'LOD Sphere':
                    sphereCenter = obj['Pos']
                    island.setZoneSphereSize(*obj['Radi'])
                    island.setZoneSphereCenter(sphereCenter[0], sphereCenter[1])
                elif objType == ObjectList.PORT_COLLISION or objType == 'Port Collision Sphere':
                    # World data stores port blockers as scaled spheres in island-local space.
                    pos = obj.get('Pos', (0, 0, 0))
                    scale = obj.get('Scale', (1, 1, 1))
                    radius = scale[0] if scale else 0
                    if radius > 0:
                        portCollisionSpheres.append({
                            'pos': (pos[0], pos[1], pos[2] if len(pos) > 2 else 0),
                            'radius': radius,
                            'name': obj.get('Name', ''),
                        })

        if portCollisionSpheres:
            island.setPortCollisionSpheres(portCollisionSpheres)

        self.notify.debug('Generated island %s (%s)' % (island.getName(), objKey))
        self.parent.generateChildWithRequired(island, PiratesGlobals.IslandAvailableZoneStart)
        self.addObject(island)
        self.air.worldCreator.linkManager.registerLinkData(objKey)
        self.air.worldCreator.movementLinkManager.registerMovementLinkData(objKey)
        return island
