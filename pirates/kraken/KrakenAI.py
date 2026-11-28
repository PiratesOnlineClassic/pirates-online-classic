import random

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.task import Task

from otp.ai.MagicWordGlobal import *

from pirates.kraken.GrabberTentacleAI import GrabberTentacleAI
from pirates.kraken.HolderTentacleAI import HolderTentacleAI
from pirates.kraken.KrakenBodyAI import KrakenBodyAI
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import AvatarTypes
from pirates.battle import EnemyGlobals
from pirates.ship import ShipGlobals


class KrakenAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenAI')

    MinLevel = 25
    MaxLevel = 50

    NumHolderTentacles = 4

    # how often the kraken thinks about what its tentacles should do
    AttackDelay = 3.0
    GrabAvatarChance = 0.35
    GrabMastChance = 0.15

    # damage done to the ship per tick for each tentacle wrapped around a mast
    ShipDamageScale = 0.25

    # gold given to every crew member when the kraken is defeated
    GoldScale = 10

    # how long it takes the kraken to sink back into the deep
    SubmergeDelay = 5.0

    # once the kraken has sunk it's ship it stays for the client's sink cutscene,
    # the doom tentacle drags the ship under (see DistributedShip.playSinkAnim),
    # we leave with the ship or once the ship has had long enough to sink...
    SinkShipTimeout = 30.0

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'KrakenAI')

        self.shipId = 0
        self.level = 0
        self.grabberTentacles = {}
        self.holderTentacles = []
        self.body = None

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        ship = self.getShip()
        if not ship:
            self.notify.warning('Kraken %d generated without a ship (%d)!' % (self.doId, self.shipId))
            self.requestDelete()
            return

        self.accept(ship.getDeleteEvent(), self.handleShipDeleted)
        self.accept(ship.uniqueName('shipSinking'), self.handleShipSinking)

        self.level = self.getLevelForShip(ship)
        self.createBody()
        self.createHolderTentacles()
        self.createGrabberTentacles()

        self.request('Attack')

    def delete(self):
        self.ignoreAll()
        self.stopAttack()
        taskMgr.remove(self.taskName('submerge'))
        taskMgr.remove(self.taskName('sinkShip'))
        FSM.cleanup(self)

        # the client expects the kraken to leave before it's parts do.
        for grabber in list(self.grabberTentacles.values()):
            grabber.requestDelete()

        for holder in self.holderTentacles:
            holder.requestDelete()

        if self.body:
            self.body.requestDelete()

        self.grabberTentacles = {}
        self.holderTentacles = []
        self.body = None
        DistributedObjectAI.delete(self)

    def setShipId(self, shipId):
        self.shipId = shipId

    def d_setShipId(self, shipId):
        self.sendUpdate('setShipId', [shipId])

    def b_setShipId(self, shipId):
        self.setShipId(shipId)
        self.d_setShipId(shipId)

    def getShipId(self):
        return self.shipId

    def getShip(self):
        return self.air.doId2do.get(self.shipId)

    def getLevel(self):
        return self.level

    def getLevelForShip(self, ship):
        level = config.GetInt('kraken-level', 0)
        if not level:
            level = ship.getLevel() or self.MinLevel

        return min(max(level, self.MinLevel), self.MaxLevel)

    @staticmethod
    def getNumGrabberLocators(shipClass):
        # the client mirrors each locator onto both sides of the ship
        return len(ShipGlobals.KrakenLocators.get(shipClass, ())) * 2

    def createPart(self, partCls, avatarType):
        part = partCls(self.air)
        part.setKrakenId(self.doId)
        part.setupPart(avatarType, self.level)
        return part

    def generatePart(self, part):
        ship = self.getShip()
        ship.generateChildWithRequired(part, self.zoneId)

    def createBody(self):
        self.body = self.createPart(KrakenBodyAI, AvatarTypes.KrakenBody)
        self.generatePart(self.body)

    @staticmethod
    def getHolderPosHprs(shipClass, numHolders):
        """
        The holders wrap the hull from below, bow and stern on either side of the ship,
        just outboard of the grabber locators (see DistributedShip.setupKrakenLocators)...
        """

        locators = ShipGlobals.KrakenLocators.get(shipClass, ())
        if not locators:
            return []

        sideX = max(locator[0][0] for locator in locators) + 30
        foreY = max(locator[0][1] for locator in locators)
        aftY = min(locator[0][1] for locator in locators)
        posHprs = []
        for x in range(numHolders):
            side = 1 if x % 2 == 0 else -1
            y = (foreY, aftY)[(x // 2) % 2]
            posHprs.append(((side * sideX, y, -10), (-90 * side, 0, 0)))

        return posHprs

    def createHolderTentacles(self):
        ship = self.getShip()
        posHprs = self.getHolderPosHprs(ship.getShipClass(), self.NumHolderTentacles)
        for x in range(self.NumHolderTentacles):
            holder = self.createPart(HolderTentacleAI, AvatarTypes.HolderTentacle)
            if x < len(posHprs):
                pos, hpr = posHprs[x]
                holder.setPos(*pos)
                holder.setHpr(*hpr)

            self.generatePart(holder)
            if hasattr(holder, 'sendCurrentPosition'):
                holder.sendCurrentPosition()

            self.holderTentacles.append(holder)

    def createGrabberTentacles(self):
        ship = self.getShip()
        for locatorId in range(self.getNumGrabberLocators(ship.getShipClass())):
            grabber = self.createPart(GrabberTentacleAI, AvatarTypes.GrabberTentacle)
            grabber.setLocatorId(locatorId)
            grabber.setEmerged(0)
            self.generatePart(grabber)
            self.grabberTentacles[locatorId] = grabber

    def getLivingGrabbers(self):
        return [grabber for grabber in self.grabberTentacles.values() if not grabber.isDead()]

    def getGrabbedAvatarIds(self):
        return [grabber.getGrabbedAvatar() for grabber in self.grabberTentacles.values() if grabber.getGrabbedAvatar()]

    def getGrabbedMasts(self):
        return [grabber.getGrabbedMast() for grabber in self.grabberTentacles.values() if grabber.getGrabbedMast()]

    def getGrabbableAvatars(self):
        ship = self.getShip()
        if not ship:
            return []

        grabbedAvatarIds = self.getGrabbedAvatarIds()
        avatars = []
        for avatarId in ship.getCrew():
            if avatarId in grabbedAvatarIds:
                continue

            avatar = self.air.doId2do.get(avatarId)
            if not avatar or avatar.getHp()[0] <= 0:
                continue

            avatars.append(avatar)

        return avatars

    def getGrabbableMasts(self):
        ship = self.getShip()
        if not ship:
            return []

        # masts are sent one based, zero means we are not holding a mast.
        grabbedMasts = self.getGrabbedMasts()
        return [x + 1 for x in range(len(ship.masts)) if x + 1 not in grabbedMasts]

    def partDied(self, part):
        if self.state not in ('Attack',):
            return

        if part is self.body:
            self.request('Defeated')
            return

        part.emerge(0)
        if isinstance(part, GrabberTentacleAI):
            part.releaseAll()
            if not self.getLivingGrabbers():
                self.request('Defeated')

    def handleShipSinking(self, ship):
        if self.state == 'Attack':
            self.request('SinkShip')

    def isShipSinking(self, ship):
        getState = getattr(ship, 'getCurrentGameState', None)
        return getState is not None and getState() in ('Sinking', 'Sunk')

    def handleShipDeleted(self):
        self.shipId = 0
        self.requestDelete()

    def getAttackTaskName(self):
        return self.taskName('attack')

    def startAttack(self):
        self.stopAttack()
        taskMgr.doMethodLater(self.AttackDelay, self.__attack, self.getAttackTaskName())

    def stopAttack(self):
        taskMgr.remove(self.getAttackTaskName())

    def __attack(self, task):
        ship = self.getShip()
        if not ship or ship.getHp() <= 0:
            if ship and self.isShipSinking(ship):
                self.request('SinkShip')
            else:
                self.request('Retreat')

            return Task.done

        # a freshly deployed ship is protected by its spawn dome:
        if ship.hasSpawnBuff():
            return Task.again

        numMastsHeld = 0
        for grabber in self.getLivingGrabbers():
            if grabber.getGrabbedMast():
                numMastsHeld += 1
                continue

            if grabber.getGrabbedAvatar():
                continue

            if random.random() < self.GrabAvatarChance:
                avatars = self.getGrabbableAvatars()
                if avatars:
                    grabber.grabAvatar(random.choice(avatars).doId)
                    continue

            if random.random() < self.GrabMastChance:
                masts = self.getGrabbableMasts()
                if masts:
                    grabber.grabMast(random.choice(masts))

        if numMastsHeld:
            damage = int(EnemyGlobals.getMonsterDmg(self.level, self.ShipDamageScale)) * numMastsHeld
            ship.b_setHp(max(0, ship.getHp() - damage))

        return Task.again

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterAttack(self):
        for holder in self.holderTentacles:
            holder.emerge(1)

        for grabber in self.grabberTentacles.values():
            grabber.emerge(1)

        self.startAttack()

    def exitAttack(self):
        self.stopAttack()

    def enterSinkShip(self):
        # the ship is lost, let go of the crew so they can go down with
        # her, the client hides the far side's tentacles and raises the
        # doom tentacle itself (Kraken.hideSideTentacles/spawnDoomTentacle)...
        for grabber in self.grabberTentacles.values():
            grabber.releaseAvatar()

        taskMgr.doMethodLater(self.SinkShipTimeout, self.__shipSunk, self.taskName('sinkShip'))

    def exitSinkShip(self):
        taskMgr.remove(self.taskName('sinkShip'))

    def __shipSunk(self, task):
        self.requestDelete()
        return Task.done

    def enterDefeated(self):
        self.rewardCrew()
        self.demand('Retreat')

    def exitDefeated(self):
        pass

    def rewardCrew(self):
        ship = self.getShip()
        if not ship:
            return

        for avatarId in ship.getCrew():
            avatar = self.air.doId2do.get(avatarId)
            if not avatar:
                continue

            inventory = avatar.getInventory()
            if not inventory:
                continue

            inventory.addGoldInPocket(EnemyGlobals.getGoldDrop(None, self.level, self.GoldScale))

    def enterRetreat(self):
        for grabber in self.grabberTentacles.values():
            grabber.releaseAll()
            grabber.emerge(0)

        for holder in self.holderTentacles:
            holder.emerge(0)

        taskMgr.doMethodLater(self.SubmergeDelay, self.__submerged, self.taskName('submerge'))

    def exitRetreat(self):
        taskMgr.remove(self.taskName('submerge'))

    def __submerged(self, task):
        self.requestDelete()
        return Task.done


def getKrakenForShip(air, shipId):
    for obj in list(air.doId2do.values()):
        if isinstance(obj, KrakenAI) and obj.getShipId() == shipId:
            return obj

    return None


def spawnKraken(air, ship):
    if not KrakenAI.getNumGrabberLocators(ship.getShipClass()):
        return None

    kraken = KrakenAI(air)
    kraken.setShipId(ship.doId)
    ship.generateChildWithRequired(kraken, PiratesGlobals.ShipZoneSilhouette)
    return kraken


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def kraken():
    """
    Summons the kraken to attack the invoker's ship, or sends it
    back to the deep if it is already attacking.
    """

    invoker = spellbook.getInvoker()
    air = spellbook.getManager().air
    ship = air.doId2do.get(invoker.getShipId())
    if not ship:
        return 'You must be aboard a ship to summon the kraken!'

    existing = getKrakenForShip(air, ship.doId)
    if existing:
        if existing.state == 'Attack':
            existing.request('Retreat')

        return 'The kraken returns to the deep.'

    if not spawnKraken(air, ship):
        return 'The kraken cannot attack this ship.'

    return 'The kraken has been summoned!'
