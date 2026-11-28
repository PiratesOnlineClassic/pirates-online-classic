from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.kraken.KrakenPartAI import KrakenPartAI
from pirates.kraken.GrabberGameFSMAI import GrabberGameFSMAI
from pirates.battle import EnemyGlobals


class GrabberTentacleAI(KrakenPartAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('GrabberTentacleAI')

    HpScale = 1.5

    # how often a grabbed avatar is squeezed and how hard
    SqueezeDelay = 2.0
    SqueezeDamageScale = 0.5

    # how many squeezes before we let the avatar go
    MaxSqueezes = 5

    def __init__(self, air):
        KrakenPartAI.__init__(self, air)

        self.locatorId = 0
        self.emerged = 0
        self.grabbedAvatarId = 0
        self.grabbedMast = 0
        self.numSqueezes = 0

    def createGameFSM(self):
        self.gameFSM = GrabberGameFSMAI(self.air, self)

    def delete(self):
        self.stopSqueeze()
        KrakenPartAI.delete(self)

    def setLocatorId(self, locatorId):
        self.locatorId = locatorId

    def d_setLocatorId(self, locatorId):
        self.sendUpdate('setLocatorId', [locatorId])

    def b_setLocatorId(self, locatorId):
        self.setLocatorId(locatorId)
        self.d_setLocatorId(locatorId)

    def getLocatorId(self):
        return self.locatorId

    def d_emerge(self, emerge):
        self.sendUpdate('emerge', [emerge])

    def emerge(self, emerge):
        self.d_emerge(emerge)
        self.b_setEmerged(emerge)

    def setEmerged(self, emerged):
        self.emerged = emerged

    def d_setEmerged(self, emerged):
        self.sendUpdate('setEmerged', [emerged])

    def b_setEmerged(self, emerged):
        self.setEmerged(emerged)
        self.d_setEmerged(emerged)

    def getEmerged(self):
        return self.emerged

    def d_grabAvatar(self, avId):
        self.sendUpdate('grabAvatar', [avId])

    def grabAvatar(self, avId):
        if avId == self.grabbedAvatarId:
            return

        self.d_grabAvatar(avId)
        self.b_setGrabbedAvatar(avId)
        if avId:
            self.startSqueeze()
        else:
            self.stopSqueeze()

    def releaseAvatar(self):
        if self.grabbedAvatarId:
            self.grabAvatar(0)

    def setGrabbedAvatar(self, avId):
        self.grabbedAvatarId = avId

    def d_setGrabbedAvatar(self, avId):
        self.sendUpdate('setGrabbedAvatar', [avId])

    def b_setGrabbedAvatar(self, avId):
        self.setGrabbedAvatar(avId)
        self.d_setGrabbedAvatar(avId)

    def getGrabbedAvatar(self):
        return self.grabbedAvatarId

    def getGrabbedAvatarObj(self):
        return self.air.doId2do.get(self.grabbedAvatarId)

    def d_grabMast(self, mast):
        self.sendUpdate('grabMast', [mast])

    def grabMast(self, mast):
        if mast == self.grabbedMast:
            return

        self.d_grabMast(mast)
        self.b_setGrabbedMast(mast)

    def releaseMast(self):
        if self.grabbedMast:
            self.grabMast(0)

    def setGrabbedMast(self, mast):
        self.grabbedMast = mast

    def d_setGrabbedMast(self, mast):
        self.sendUpdate('setGrabbedMast', [mast])

    def b_setGrabbedMast(self, mast):
        self.setGrabbedMast(mast)
        self.d_setGrabbedMast(mast)

    def getGrabbedMast(self):
        return self.grabbedMast

    def isBusy(self):
        return bool(self.grabbedAvatarId or self.grabbedMast)

    def releaseAll(self):
        self.releaseAvatar()
        self.releaseMast()

    def getSqueezeTaskName(self):
        return self.taskName('squeeze')

    def startSqueeze(self):
        self.stopSqueeze()
        self.numSqueezes = 0
        taskMgr.doMethodLater(self.SqueezeDelay, self.__squeeze, self.getSqueezeTaskName())

    def stopSqueeze(self):
        taskMgr.remove(self.getSqueezeTaskName())
        self.numSqueezes = 0

    def getSqueezeDamage(self):
        return max(1, int(EnemyGlobals.getMonsterDmg(self.level, self.SqueezeDamageScale)))

    def __squeeze(self, task):
        avatar = self.getGrabbedAvatarObj()
        kraken = self.getKraken()
        if not avatar or not kraken or self.isDead():
            self.releaseAvatar()
            return Task.done

        # the avatar managed to get off of the ship, let them go...
        if avatar.getShipId() != kraken.getShipId():
            self.releaseAvatar()
            return Task.done

        hp = avatar.getHp()[0]
        if hp <= 0:
            self.releaseAvatar()
            return Task.done

        avatar.b_setHp(max(0, hp - self.getSqueezeDamage()))

        self.numSqueezes += 1
        if self.numSqueezes >= self.MaxSqueezes:
            self.releaseAvatar()
            return Task.done

        return Task.again
