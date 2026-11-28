from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship import ShipGlobals
from pirates.ship import ShipBalance


class BlackPearlShipAI(DistributedShipAI):
    """
    The Black Pearl ship AI - Captain Jack Sparrow's legendary vessel.

    This is a special ship used in the Black Pearl treasure map instance.
    It functions as a player-controlled ship but with special behaviors
    for the quest instance.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('BlackPearlShipAI')

    # the Pearl belongs to the treasure map instance, it stays put once sunk
    # until the instance is cleaned up and isn't put away when it's crew leave:
    PutAwayWhenEmpty = False

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)

        # Black Pearl specific settings
        self.shipClass = ShipGlobals.BLACK_PEARL
        self.baseTeam = ShipGlobals.PLAYER_TEAM
        self.npcShip = 1
        self.isBoardable = 1
        self.isExitable = 1
        self.isFlagship = 1

        # Quest-related state
        self.questInstance = None
        self.npcsOnDeck = []
        self.allNpcsKilled = False

    def generate(self):
        DistributedShipAI.generate(self)
        self.notify.info('BlackPearlShipAI generated with doId %d' % self.doId)

    def announceGenerate(self):
        DistributedShipAI.announceGenerate(self)

    def delete(self):
        self.questInstance = None
        self.npcsOnDeck = []
        DistributedShipAI.delete(self)

    def setQuestInstance(self, instance):
        """Set the quest instance this ship belongs to"""
        self.questInstance = instance

    def getQuestInstance(self):
        return self.questInstance

    def isCrewedByPlayers(self):
        # the Pearl is an NPC ship to the client, but it's the players who sail her:
        return True

    # =========================================================================
    # NPC Management (enemies on the ship deck)
    # =========================================================================

    def addNPCOnDeck(self, npcDoId):
        """Add an NPC to the list of enemies on deck"""
        if npcDoId not in self.npcsOnDeck:
            self.npcsOnDeck.append(npcDoId)
            self.notify.debug('Added NPC %d to deck, total: %d' % (npcDoId, len(self.npcsOnDeck)))

    def removeNPCOnDeck(self, npcDoId):
        """Remove an NPC from the deck (killed)"""
        if npcDoId in self.npcsOnDeck:
            self.npcsOnDeck.remove(npcDoId)
            self.notify.debug('Removed NPC %d from deck, remaining: %d' % (npcDoId, len(self.npcsOnDeck)))

            # Check if all NPCs are killed
            self._checkAllNpcsKilled()

    def _checkAllNpcsKilled(self):
        """Check if all NPCs on deck have been killed"""
        if len(self.npcsOnDeck) == 0 and not self.allNpcsKilled:
            self.allNpcsKilled = True
            self.notify.info('All NPCs on Black Pearl killed!')

            # Notify the quest instance
            if self.questInstance:
                self.questInstance.handleNPCsKilledOnPearl()

    def canTakeWheel(self, avatar):
        # the Navy guards have to be cleared from the deck before the wheel
        # can be taken (see TreasureMapBlackPearl.disablePearlInteractions):
        return not self.npcsOnDeck

    # =========================================================================
    # Damage Handling
    # =========================================================================

    def takeDamage(self, damage, attackerId=0, applyModifiers=True):
        """Handle damage to the Black Pearl"""
        if self.hasSpawnBuff() or not self.isSailable():
            return self.hp

        self.notify.debug('Black Pearl taking %d damage from %d' % (damage, attackerId))

        if applyModifiers:
            damage *= ShipBalance.NPCDamageIn.getValue()
        effectiveArmor = (ShipBalance.ArmorAbsorb.getValue() *
                          ShipBalance.NPCArmorModifier.getValue())
        damage = int(damage * (1.0 - effectiveArmor))

        if isinstance(self.air.doId2do.get(attackerId), DistributedShipAI):
            self.recordAttacker(attackerId, damage)

        # the Pearl going down is handled by handleHpDepleted:
        self.b_setHp(max(0, self.hp - damage))

        if self.hp > 0 and getattr(self, 'gameFSM', None):
            self.gameFSM.onDamageReceived(attackerId, damage)

        return self.hp

    def handleHpDepleted(self):
        DistributedShipAI.handleHpDepleted(self)
        self._handleDestroyed()

    def _handleDestroyed(self):
        """Black Pearl has been destroyed"""
        self.notify.info('The Black Pearl has been destroyed!')

        # Notify the quest instance
        if self.questInstance:
            self.questInstance.handleBlackPearlDestroyed()

    def handleShipSunk(self):
        # the sunken Pearl is left where it went down, the treasure map
        # instance deletes it once the players have left (see TreasureMapBlackPearlAI.delete)...
        self.b_setGameState('Sunk', 0)

    def requestClientAggro(self):
        # the Pearl is sailed by the players, the enemy ships come for the Pearl
        # (see TreasureMapBlackPearlAI), not the other way around:
        pass

    # =========================================================================
    # Player Boarding
    # =========================================================================

    def handleChildArrive(self, childObj, zoneId):
        """Handle a player or NPC arriving on the ship"""
        DistributedShipAI.handleChildArrive(self, childObj, zoneId)

        # If it's a player, track them
        from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI
        if isinstance(childObj, DistributedPlayerPirateAI):
            self.notify.info('Player %d boarded the Black Pearl' % childObj.doId)

    def handleChildLeave(self, childObj, zoneId):
        """Handle a player or NPC leaving the ship"""
        DistributedShipAI.handleChildLeave(self, childObj, zoneId)

        from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI
        if isinstance(childObj, DistributedPlayerPirateAI):
            self.notify.info('Player %d left the Black Pearl' % childObj.doId)
