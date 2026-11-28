import math
import random

from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship import ShipGlobals
from pirates.ship import ShipBalance
from pirates.ship import FlagshipGlobals
from pirates.battle import EnemyGlobals
from pirates.battle import LootGlobals
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class NPCShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NPCShipAI')

    # NPC ships are crewed by NPCs, players only ever board them to fight the crew:
    PutAwayWhenEmpty = False

    # flagships that are crippled wait to be grappled and boarded before sinking:
    CrippledTimeout = FlagshipGlobals.FLAGSHIP_CRIPPLED_TIMEOUT
    GrapplePullTime = FlagshipGlobals.FLAGSHIP_GRAPPLE_PULL_TIME
    GrappleMovePeriod = PiratesGlobals.AI_MOVEMENT_PERIOD
    BoardingOffset = 110.0
    DefeatedSinkDelay = 10.0
    DeckCrewPositions = [
        (-15, 30, 8), (15, 30, 8), (-20, 0, 8), (20, 0, 8), (0, 5, 8),
        (-15, -25, 8), (15, -25, 8), (0, -40, 12), (-10, 50, 8), (10, -10, 8)]

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)

        self.deckCrew = []
        self.objectData = {}
        self.grappleArriveTime = 0.0

    @property
    def isNpc(self):
        return True

    def generate(self):
        self.air.shipManager.addShip(self)
        DistributedShipAI.generate(self)

    def delete(self):
        self.__stopBoardingTasks()
        self.deleteDeckCrew()
        self.air.shipManager.removeShip(self)
        DistributedShipAI.delete(self)

    def getLevel(self):
        if hasattr(self, 'gameFSM'):
            return self.gameFSM._getShipLevel()

        return ShipGlobals.getShipLevel(self.shipClass)

    def getDamageInputModifier(self):
        return ShipBalance.NPCDamageIn.getValue()

    def getDamageOutputModifier(self):
        return ShipBalance.NPCDamageOut.getValue()

    def getArmorModifier(self):
        return ShipBalance.NPCArmorModifier.getValue()

    def takeDamage(self, damage, attackerDoId=0, applyModifiers=True):
        if self.hasSpawnBuff() or not self.isSailable():
            return self.hp

        if applyModifiers:
            damage = damage * self.getDamageInputModifier()

        # some of the damage is absorbed by the ship's armor:
        damage = int(damage * (1.0 - ShipBalance.ArmorAbsorb.getValue() * self.getArmorModifier()))

        attackerShip = self.air.doId2do.get(attackerDoId)
        if isinstance(attackerShip, DistributedShipAI):
            self.recordAttacker(attackerDoId, damage)

        # sinking is handled by setHp once the ship's hp reaches zero.
        oldHp = self.hp
        self.b_setHp(max(0, self.hp - damage))

        # the crew that sank this ship receive credit towards their quests
        if self.hp <= 0 < oldHp:
            self.air.questMgr.shipSunk(self, [attackerDoId])
            self.plunderShip(attackerShip)

        if self.hp > 0:
            self.gameFSM.onDamageReceived(attackerDoId, damage)

        return self.hp

    def plunderShip(self, attackerShip):
        # the ship that sank us plunders our cargo, the containers are
        # loaded into it's hold until they are sold at port...
        if not isinstance(attackerShip, DistributedShipAI) or attackerShip.getNPCship():
            return []

        cargo = list(attackerShip.getCargo())
        space = attackerShip.getMaxCargo() - len(cargo)
        if space <= 0:
            return []

        loot = LootGlobals.getShipLoot(bool(self.isFlagship),
            self.getTreasureSenseRank(attackerShip))[:space]

        attackerShip.b_setCargo(cargo + loot)
        attackerShip.d_notifyReceivedLoot(loot)
        return loot

    def getTreasureSenseRank(self, attackerShip):
        # the captain's Treasure Sense skill improves the quality of the
        # loot plundered, skill stacks hold the skill's rank plus one...
        owner = self.air.doId2do.get(attackerShip.getOwnerId())
        inventory = owner.getInventory() if owner and hasattr(owner, 'getInventory') else None
        if not inventory:
            return 0

        return max(inventory.getStackQuantity(InventoryType.SailTreasureSense) - 1, 0)

    # Flagship grappling and boarding:

    def canBeBoarded(self):
        return bool(self.isFlagship and self.isBoardable)

    def getBoardingShip(self):
        return self.air.doId2do.get(self.boardableShipId)

    def handleHpDepleted(self):
        attackerShip = self.air.doId2do.get(self.lastAttackerShipId)
        if not self.canBeBoarded() or not isinstance(attackerShip, DistributedShipAI) or attackerShip.getNPCship():
            DistributedShipAI.handleHpDepleted(self)
            return

        self.crippleShip(attackerShip)

    def crippleShip(self, attackerShip):
        # the flagship has been crippled, the attacking crew now have a limited
        # amount of time to grapple the flagship in and board it before it sinks...
        self.b_setBoardableShipId(attackerShip.doId)
        attackerShip.b_setBoardableShipId(self.doId)
        attackerShip.b_setLandedGrapples([])

        self.b_setSinkTimer(int(self.CrippledTimeout))
        self.b_setGameState('WaitingForGrapple', 0)

        self.accept(attackerShip.getDeleteEvent(), self.handleBoardingFailed)
        taskMgr.doMethodLater(self.CrippledTimeout, self.__crippledTimeout,
            self.uniqueName('crippled-timeout'))

    def __crippledTimeout(self, task):
        if self.getCurrentGameState() in ('WaitingForGrapple', 'GrappleLerping', 'InPosition'):
            self.handleBoardingFailed()

        return Task.done

    def handleGrappleHit(self, avatar, targetIndex):
        if self.getCurrentGameState() not in ('WaitingForGrapple', 'GrappleLerping'):
            return

        attackerShip = self.getBoardingShip()
        if not attackerShip or avatar.getCrewShipId() != attackerShip.doId:
            self.notify.debug('Avatar %d cannot grapple flagship %d, '
                'avatar is not crew of the boarding ship!' % (avatar.doId, self.doId))

            return

        landedGrapples = list(attackerShip.getLandedGrapples())
        landedGrapples.append([self.doId, targetIndex])
        attackerShip.b_setLandedGrapples(landedGrapples)

        # every grapple that lands pulls the flagship in faster:
        self.grappleArriveTime = globalClock.getFrameTime() + self.GrapplePullTime / len(landedGrapples)
        if self.getCurrentGameState() == 'WaitingForGrapple':
            self.b_setGameState('GrappleLerping', 0)
            taskMgr.doMethodLater(self.GrappleMovePeriod, self.__grappleLerpTask,
                self.uniqueName('grapple-lerp'))

    def getBoardingPosHpr(self, attackerShip):
        # the flagship is pulled alongside the boarding ship, on whichever side it was already on:
        side = 1.0 if self.getX(attackerShip) >= 0 else -1.0
        pos = self.getParentObj().getRelativePoint(attackerShip, (side * self.BoardingOffset, 0, 0))
        return pos, attackerShip.getH()

    def __grappleLerpTask(self, task):
        attackerShip = self.getBoardingShip()
        if not attackerShip:
            return Task.done

        state = self.getCurrentGameState()
        if state not in ('GrappleLerping', 'InPosition', 'Boarded', 'Defeated'):
            return Task.done

        pos, h = self.getBoardingPosHpr(attackerShip)
        if state == 'GrappleLerping':
            timeLeft = self.grappleArriveTime - globalClock.getFrameTime()
            if timeLeft > self.GrappleMovePeriod:
                t = self.GrappleMovePeriod / timeLeft
                pos = self.getPos() + (pos - self.getPos()) * t
                h = self.getH() + self.gameFSM._normalizeAngle(h - self.getH()) * t
            else:
                self.handleInBoardingPosition(attackerShip)

        # once in position the flagship stays lashed alongside the boarding ship:
        self.setPosHpr(pos[0], pos[1], 0, h, 0, 0)
        return Task.again

    def handleInBoardingPosition(self, attackerShip):
        attackerShip.b_setIsInBoardingPosition(1)
        attackerShip.b_setGameState('InBoardingPosition', 0)
        self.b_setIsInBoardingPosition(1)
        self.b_setGameState('InPosition', 0)

    def requestBoardingStart(self, attackerShip):
        if self.getCurrentGameState() != 'InPosition':
            return False

        if attackerShip.doId != self.boardableShipId:
            return False

        self.b_setGameState('Boarded', 0)
        self.spawnDeckCrew()

        # each of the boarding ship's crew will swing over to the flagship:
        attackerShip.d_setBoardingSuccess(self.doId)
        return True

    def getDeckCrewClass(self, avatarType):
        if avatarType.isA(AvatarTypes.Undead):
            from pirates.npc.DistributedNPCSkeletonAI import DistributedNPCSkeletonAI
            return DistributedNPCSkeletonAI

        from pirates.npc.DistributedNPCNavySailorAI import DistributedNPCNavySailorAI
        return DistributedNPCNavySailorAI

    def spawnDeckCrew(self):
        minLevel, maxLevel = FlagshipGlobals.getFlagshipEnemyLevels(self.shipClass)
        crewSize = min(FlagshipGlobals.getFlagshipCrewSize(self.shipClass), len(self.DeckCrewPositions))
        for x, y, z in self.DeckCrewPositions[:crewSize]:
            avatarType = FlagshipGlobals.pickCrewMember(self.shipClass, self.getBaseTeam())
            if not avatarType:
                continue

            level = random.randint(minLevel, maxLevel)
            npc = self.getDeckCrewClass(avatarType)(self.air)
            npc.setAvatarType(avatarType)
            npc.setTeam(self.getBaseTeam())
            npc.setCollisionMode(PiratesGlobals.COLL_MODE_FLOORS_CL)
            npc.setLevel(level)
            hp, mojo = EnemyGlobals.getEnemyStats(avatarType, level)
            npc.setMaxHp(hp)
            npc.setHp(hp)
            npc.setMaxMojo(mojo)
            npc.setMojo(mojo)
            npc.setName(avatarType.getName())
            npc.setSpawnPos((x, y, z))
            npc.setInitZ(z)
            npc.setAnimSet('default')
            npc.setStartState('Idle')
            npc.setSpawnNode(self)

            self.generateChildWithRequired(npc, PiratesGlobals.ShipZoneOnDeck)
            npc.setPos(self, x, y, z)
            npc.d_setInitZ(z)
            npc.d_setSpawnIn()
            npc.b_setGameState('Idle')
            self.deckCrew.append(npc)

    def processDeath(self):
        # called by our deck crew's game fsm when one of them dies, the
        # hp of the npc is set after it's death state has been entered...
        taskMgr.doMethodLater(0, self.__checkDeckCrew, self.uniqueName('check-deck-crew'))

    def __checkDeckCrew(self, task):
        for npc in list(self.deckCrew):
            hp = npc.getHp()
            if isinstance(hp, (list, tuple)):
                hp = hp[0]

            if hp <= 0 or npc.isDeleted():
                self.deckCrew.remove(npc)

        if not self.deckCrew and self.getCurrentGameState() == 'Boarded':
            self.handleCrewDefeated()

        return Task.done

    def deleteDeckCrew(self):
        for npc in self.deckCrew:
            if not npc.isDeleted():
                npc.requestDelete()

        self.deckCrew = []

    def handleCrewDefeated(self):
        self.b_setGameState('Defeated', 0)

        # send the boarders back over to their own ship before the flagship goes down:
        attackerShip = self.getBoardingShip()
        if attackerShip:
            for avatarId in list(self.crew):
                attackerShip.d_setMovie(ShipGlobals.SHIP_MOVIE_BOARD, avatarId, self.doId, 0)

        taskMgr.doMethodLater(self.DefeatedSinkDelay, self.__defeatedSink,
            self.uniqueName('defeated-sink'))

    def __defeatedSink(self, task):
        self.releaseBoardingShip()
        DistributedShipAI.handleHpDepleted(self)
        return Task.done

    def handleBoardingFailed(self, *args):
        if self.getCurrentGameState() in self.gameFSM.SinkingStates:
            return

        self.releaseBoardingShip()
        DistributedShipAI.handleHpDepleted(self)

    def releaseBoardingShip(self):
        attackerShip = self.getBoardingShip()
        if attackerShip:
            self.ignore(attackerShip.getDeleteEvent())
            attackerShip.b_setLandedGrapples([])
            attackerShip.b_setIsInBoardingPosition(0)
            attackerShip.b_setBoardableShipId(0)
            if attackerShip.getCurrentGameState() == 'InBoardingPosition':
                attackerShip.b_setGameState('Adrift', 0)

        self.__stopBoardingTasks()
        self.deleteDeckCrew()
        self.b_setIsInBoardingPosition(0)
        self.b_setBoardableShipId(0)

    def __stopBoardingTasks(self):
        taskMgr.remove(self.uniqueName('crippled-timeout'))
        taskMgr.remove(self.uniqueName('grapple-lerp'))
        taskMgr.remove(self.uniqueName('check-deck-crew'))
        taskMgr.remove(self.uniqueName('defeated-sink'))
