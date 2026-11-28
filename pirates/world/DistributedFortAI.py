from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from direct.directnotify import DirectNotifyGlobal

from pirates.piratesbase import PiratesGlobals
from pirates.pirate import AvatarTypes


class DistributedFortAI(DistributedBattleAvatarAI):
    """
    AI-side implementation of a fort/barricade in the world.
    
    Forts are used in the Black Pearl quest as obstacles (drawbridges)
    that must be destroyed to proceed. They can take damage from
    ship cannons and other attacks.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFortAI')

    BaseProjectileDamage = 500

    def __init__(self, air):
        DistributedBattleAvatarAI.__init__(self, air)

        self.islandId = 0
        self.objKey = ''
        self.fortLevel = 1
        self.maxHp = 5000
        self.hp = 5000
        self.destroyed = False

        # Reference to the treasure map instance (if part of one)
        self.treasureMapInstance = None

        # Cannons that are mounted on this fort (DistributedFortCannonAI)
        self.cannons = []

        # forts are always manned by the navy, the client sets the same team
        # for the radar (see DistributedFort.setupRadarGui)
        self.setTeam(PiratesGlobals.NAVY_TEAM)

        # the client sizes every battle avatar from it's avatar type's enemy stats,
        # the default type (Anyone) has none and the client cannot generate the fort...
        self.setAvatarType(AvatarTypes.Navy)

    def generate(self):
        DistributedBattleAvatarAI.generate(self)

    def announceGenerate(self):
        DistributedBattleAvatarAI.announceGenerate(self)
        self.notify.debug('Fort %s generated with doId %d' % (self.objKey, self.doId))

    def delete(self):
        self.treasureMapInstance = None
        self.cannons = []
        DistributedBattleAvatarAI.delete(self)

    # =========================================================================
    # DC Fields
    # =========================================================================

    def setIslandId(self, islandId):
        self.islandId = islandId

    def d_setIslandId(self, islandId):
        self.sendUpdate('setIslandId', [islandId])

    def b_setIslandId(self, islandId):
        self.setIslandId(islandId)
        self.d_setIslandId(islandId)

    def getIslandId(self):
        return self.islandId

    def setObjKey(self, objKey):
        self.objKey = objKey

    def d_setObjKey(self, objKey):
        self.sendUpdate('setObjKey', [objKey])

    def b_setObjKey(self, objKey):
        self.setObjKey(objKey)
        self.d_setObjKey(objKey)

    def getObjKey(self):
        return self.objKey

    def setFortLevel(self, level):
        self.fortLevel = level

    def getFortLevel(self):
        return self.fortLevel

    def d_setDrawbridgesLerpR(self, r):
        self.sendUpdate('setDrawbridgesLerpR', [r])

    def d_hideDrawbridges(self):
        self.sendUpdate('hideDrawbridges', [])

    # =========================================================================
    # Cannons
    # =========================================================================

    def addCannon(self, cannon):
        if cannon in self.cannons:
            return

        self.cannons.append(cannon)
        if self.destroyed:
            cannon.destroyCannon(repair=False)

    def removeCannon(self, cannon):
        if cannon in self.cannons:
            self.cannons.remove(cannon)

    def getCannons(self):
        return self.cannons

    # =========================================================================
    # Damage Handling
    # =========================================================================

    def takeDamage(self, damage, attackerId=0):
        """Handle damage to the fort"""
        if self.destroyed:
            return

        self.notify.debug('Fort %s taking %d damage from %d' % (self.objKey, damage, attackerId))

        newHp = max(0, self.hp - damage)
        self.b_setHp(newHp, False)

        # Check if destroyed
        if newHp <= 0:
            self._handleDestroyed(attackerId)

    def _handleDestroyed(self, attackerId=0):
        """Fort has been destroyed"""
        if self.destroyed:
            return

        self.destroyed = True
        self.notify.info('Fort %s destroyed by %d' % (self.objKey, attackerId))

        # a destroyed fort can no longer man its cannons
        for cannon in list(self.cannons):
            cannon.destroyCannon(repair=False)

        # Notify the treasure map instance if we're part of one
        if self.treasureMapInstance:
            from pirates.treasuremap import TreasureMapBlackPearlGlobals
            for barricadeId, (uid1, uid2) in TreasureMapBlackPearlGlobals.FortPairsDict.items():
                if self.objKey in (uid1, uid2):
                    forts = self.treasureMapInstance.forts
                    if all(uid in forts and forts[uid].isDestroyed() for uid in (uid1, uid2)):
                        self.treasureMapInstance.handleBarricadeDestroyed(barricadeId)

    def setTreasureMapInstance(self, instance):
        """Set the treasure map instance this fort belongs to"""
        self.treasureMapInstance = instance

    # =========================================================================
    # Combat
    # =========================================================================

    def hitByProjectile(self, skillId, ammoSkillId):
        """Called when hit by a projectile (cannonball)"""
        if self.destroyed:
            return

        attackerId = self.air.getAvatarIdFromSender()
        self.takeDamage(self.getProjectileDamage(attackerId, skillId, ammoSkillId), attackerId)

    def getProjectileDamage(self, attackerId, skillId, ammoSkillId):
        # forts take hull damage from cannon ammo, just like a ship hull does
        attacker = self.air.doId2do.get(attackerId)
        damage = 0
        if attacker:
            damage = int(abs(self.air.battleMgr.getModifiedHullDamage(attacker, self, skillId, ammoSkillId)))

        return damage or self.BaseProjectileDamage

    def isDestroyed(self):
        return self.destroyed