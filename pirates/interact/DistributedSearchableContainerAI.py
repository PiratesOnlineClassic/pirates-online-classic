from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedSearchableContainerAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSearchableContainerAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.color = [1.0, 1.0, 1.0, 1.0]
        self.scale = [1, 1, 1]
        self.searchTime = 0.0
        self.currentUser = None

    def handleRequestInteraction(self, avatar, interactType, instant):
        searchAvailable = config.GetBool('always-allow-searching', False) #TODO: input from questing

        if searchAvailable and self.currentUser is None:
            self.currentUser = avatar
            taskMgr.doMethodLater(self.searchTime, self.__searchTask, '%s-avatarSearchTask-%s' % 
                (self.doId, avatar.doId))

            self.sendUpdateToAvatarId(avatar.doId, 'startSearching', [])
            return self.ACCEPT

        return self.DENY

    def handleRequestExit(self, avatar):
        if avatar != self.currentUser:
            self.notify.warning('Failed to request handle exist; Avatar is not current interactor')

            self.air.logPotentialHacker(
                message='Received handleRequestExist from a different avatar then is currently digging!',
                currentAvatarId=self.currentUser.doId,
                requestedAvatarId=avatar.doId
            )
            return

        self.currentUser = None

    def __searchTask(self, task):

        if not self.currentUser:
            return task.done

        questProgress = 1 #TODO: add proper quest value

        self.sendUpdateToAvatarId(self.currentUser.doId, 'stopSearching', [questProgress])
        self.currentUser = None

        return task.done

    def setSearchTime(self, searchTime):
        self.searchTime = searchTime

    def d_setSearchTime(self, searchTime):
        self.sendUpdate('setSearchTime', [searchTime])

    def b_setSearchTime(self, searchTime):
        self.setSearchTime(searchTime)
        self.d_setSearchTime(searchTime)

    def getSearchTime(self):
        return self.searchTime

    def setType(self, searchType):
        self.type = searchType

    def d_setType(self, searchType):
        self.sendUpdate('setType', [searchType])

    def b_setType(self, searchType):
        self.setType(searchType)
        self.d_setType(searchType)

    def getType(self):
        return self.type

    def setScale(self, scale):
        self.scale = scale

    def d_setScale(self, scale):
        self.sendUpdate('setScale', [scale])

    def b_setScale(self, scale):
        self.setScale(scale)
        self.d_setScale(scale)

    def getScale(self):
        return self.scale

    def setContainerColor(self, color):
        self.color = color

    def d_setContainerColor(self, color):
        self.sendUpdate('setContainerColor', color)

    def b_setContainerColor(self, color):
        self.setContainerColor(color)
        self.d_setContainerColor(color)

    def getContainerColor(self):
        return self.color

    def setSphereScale(self, sphereScale):
        self.sphereScale = sphereScale

    def d_setSphereScale(self, sphereScale):
        self.sendUpdate('setSphereScale', [sphereScale])

    def b_setSphereScale(self, sphereScale):
        self.setSphereScale(sphereScale)
        self.d_setSphereScale(sphereScale)

    def getSphereScale(self):
        return self.sphereScale

    