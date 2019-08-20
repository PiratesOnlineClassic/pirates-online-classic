from direct.directnotify.DirectNotifyGlobal import directNotify

from pirates.world.GameAreaBuilderAI import GameAreaBuilderAI
from pirates.leveleditor import ObjectList
from pirates.leveleditor import WorldDataGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.world.DistributedCellDoorAI import DistributedCellDoorAI
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from pirates.minigame.DistributedHoldemTableAI import DistributedHoldemTableAI
from pirates.minigame.DistributedBlackjackTableAI import DistributedBlackjackTableAI
from pirates.minigame.Distributed7StudTableAI import Distributed7StudTableAI
from pirates.minigame.DistributedBishopsHandTableAI import DistributedBishopsHandTableAI
from pirates.minigame.DistributedLiarsDiceAI import DistributedLiarsDiceAI


class InteriorAreaBuilderAI(GameAreaBuilderAI):
    notify = directNotify.newCategory('InteriorAreaBuilderAI')

    def __init__(self, air, parent):
        GameAreaBuilderAI.__init__(self, air, parent)

        self.wantJailCellDoors = config.GetBool('want-jail-cell-doors', True)
        self.wantParlorGames = config.GetBool('want-parlor-games', True)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None
        if objType == ObjectList.DOOR_LOCATOR_NODE and self.wantDoorLocatorNodes:
            newObj = self.createDoorLocatorNode(parent, parentUid, objKey, objectData)
        elif objType == ObjectList.LOCATOR_NODE and self.wantConnectorLocatorNodes:
            newObj = self.createConnectorLocatorNode(parent, parentUid, objKey, objectData)
        elif objType == 'Jail Cell Door' and self.wantJailCellDoors:
            newObj = self.createCellDoor(parent, parentUid, objKey, objectData)
        elif objType == 'Parlor Game' and self.wantParlorGames:
            newObj = self.createParlorTable(objectData, parent, parentUid, objKey)
        else:
            newObj = GameAreaBuilderAI.createObject(self, objType, objectData, parent, parentUid,
                objKey, dynamic, parentIsObj, fileName, actualParentObj)

        return newObj

    def createDoorLocatorNode(self, parent, parentUid, objKey, objectData):
        from pirates.world.DistributedInteriorDoorAI import DistributedInteriorDoorAI

        doorLocatorNode = DistributedInteriorDoorAI(self.air)
        doorLocatorNode.setUniqueId(objKey)
        doorLocatorNode.setPos(objectData.get('Pos', (0, 0, 0)))
        doorLocatorNode.setHpr(objectData.get('Hpr', (0, 0, 0)))
        doorLocatorNode.setScale(objectData.get('Scale', (1, 1, 1)))
        doorLocatorNode.setInteriorId(self.parent.doId, self.parent.parentId, self.parent.zoneId)

        if not self.parent.getInteriorFrontDoor():
            self.parent.setInteriorFrontDoor(doorLocatorNode)
            exteriorDoor = self.parent.getExteriorFrontDoor()
        else:
            doorLocatorNode.setDoorIndex(1)
            self.parent.setInteriorBackDoor(doorLocatorNode)
            exteriorDoor = self.parent.getExteriorBackDoor()

        if not exteriorDoor:
            self.notify.debug('Cannot generate interior door %s, '
                'cant find other exterior door!' % objKey)

            return

        exteriorWorld = self.parent.getParentObj()
        if not exteriorWorld:
            self.notify.debug('Cannot create interior door %s, '
                'for exterior with no parent!' % objKey)

            return

        exterior = exteriorDoor.getParentObj()
        if not exterior:
            self.notify.debug('Cannot create interior door %s, '
                'no exterior found!' % objKey)

            return

        doorLocatorNode.setBuildingUid(exteriorDoor.getBuildingUid())
        doorLocatorNode.setOtherDoor(exteriorDoor)
        doorLocatorNode.setExteriorId(exterior.doId, exteriorWorld.doId, exterior.zoneId)
        doorLocatorNode.setBuildingDoorId(exteriorDoor.doId)

        zoneId = self.parent.getZoneFromXYZ(doorLocatorNode.getPos())
        self.parent.generateChildWithRequired(doorLocatorNode, zoneId)
        exteriorDoor.setOtherDoor(doorLocatorNode)
        self.addObject(doorLocatorNode)

        # update the game area's links
        links = self.parent.getLinks()
        links.append(['', doorLocatorNode.doId, '', self.parent.parentId, self.parent.zoneId, '',
            exteriorWorld.parentId, exteriorWorld.zoneId])

        self.parent.b_setLinks(links)
        return doorLocatorNode

    def createConnectorLocatorNode(self, parent, parentUid, objKey, objectData):
        locatorName = objectData.get('Name', '')
        if 'interior' not in locatorName:
            return

        self.air.worldCreator.locatorManager.addLocator(parentUid, objKey, objectData)

    def createCellDoor(self, parent, parentUid, objKey, objectData):
        cellDoor = DistributedCellDoorAI(self.air)
        cellDoor.setUniqueId(objKey)
        cellDoor.setPos(objectData.get('Pos', (0, 0, 0)))
        cellDoor.setHpr(objectData.get('Hpr', (0, 0, 0)))
        cellDoor.setScale(objectData.get('Scale', (1, 1, 1)))
        cellDoor.setCellIndex(objectData.get('Cell Index', 0))

        zoneId = self.parent.getZoneFromXYZ(cellDoor.getPos())
        self.parent.generateChildWithRequired(cellDoor, zoneId)
        #self.parentObjectToCell(cellDoor, zoneId)

        self.addObject(cellDoor)
        self.parent.addCellDoor(cellDoor)
        return cellDoor

    def createParlorTable(self, objectData, parent, parentUid, objKey):
        tableCls = None
        gameType = objectData.get('Category', 'Unknown')
        if gameType == 'Holdem':
            tableCls = DistributedHoldemTableAI
        elif gameType == 'Blackjack':
            tableCls = DistributedBlackjackTableAI
        elif gameType == '7Stud':
            tableCls = Distributed7StudTableAI
        elif gameType == 'Bishops':
            tableCls = DistributedBishopsHandTableAI
        elif gameTable == 'LiarsDice':
            tableCls = DistributedLiarsDiceAI
        else:
            self.notify.warning('Failed to generate Parlor Table %s; %s is not a valid game type' % (objKey, gameType))
            return

        gameTable = tableCls(self.air)
        gameTable.setUniqueId(objKey)
        gameTable.setPos(objectData.get('Pos', (0, 0, 0)))
        gameTable.setHpr(objectData.get('Hpr', (0, 0, 0)))
        gameTable.setScale(objectData.get('Scale', 1))
        gameTable.generatePlayers()

        if hasattr(gameTable, 'setGameType'):
            gameTable.setGameType(gameType)

        if hasattr(gameTable, 'setBetMultiplier'):
            gameTable.setBetMultiplier(int(objectData.get('BetMultiplier', '1')))

        zoneId = self.parent.getZoneFromXYZ(gameTable.getPos())
        self.parent.generateChildWithRequired(gameTable, zoneId)
        self.parentObjectToCell(gameTable, zoneId)
        self.addObject(gameTable)
        return gameTable
