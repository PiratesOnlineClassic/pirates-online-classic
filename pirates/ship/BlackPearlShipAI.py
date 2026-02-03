from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship import ShipGlobals


class BlackPearlShipAI(DistributedShipAI):
    """
    The Black Pearl ship AI - Captain Jack Sparrow's legendary vessel.
    
    This is a special ship used in the Black Pearl treasure map instance.
    It functions as a player-controlled ship but with special behaviors
    for the quest instance.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('BlackPearlShipAI')

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

    # =========================================================================
    # Damage Handling
    # =========================================================================

    def takeDamage(self, damage, attackerId=0):
        """Handle damage to the Black Pearl"""
        self.notify.debug('Black Pearl taking %d damage from %d' % (damage, attackerId))

        newHp = max(0, self.hp - damage)
        self.b_setHp(newHp)

        # Check if destroyed
        if newHp <= 0:
            self._handleDestroyed()

    def _handleDestroyed(self):
        """Black Pearl has been destroyed"""
        self.notify.warning('The Black Pearl has been destroyed!')

        # Notify the quest instance
        if self.questInstance:
            self.questInstance.handleBlackPearlDestroyed()

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
