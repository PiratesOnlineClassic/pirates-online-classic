from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship import ShipGlobals
from pirates.ship import ShipBalance
from pirates.battle import EnemyGlobals


class NPCShipAI(DistributedShipAI):
    """
    AI-controlled NPC ship with advanced combat behaviors.
    
    Extends DistributedShipAI with damage response hooks that trigger
    the GameFSMShipAI combat behaviors.
    
    Uses POTCO-authentic damage modifiers from:
    - ShipBalance: NPCDamageIn/Out, ArmorAbsorb/Bounce
    - WeaponGlobals: Level-based damage scaling
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('NPCShipAI')

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)
        self._isNpc = True  # Flag for WeaponGlobals damage calculations

    @property
    def isNpc(self):
        """Property for WeaponGlobals level damage calculations."""
        return True

    def generate(self):
        self.air.shipManager.addShip(self)
        DistributedShipAI.generate(self)

    def delete(self):
        self.air.shipManager.removeShip(self)
        DistributedShipAI.delete(self)

    def getLevel(self):
        """
        Get ship combat level for damage calculations.
        Delegates to GameFSM if available, otherwise uses ShipGlobals.
        """
        if hasattr(self, 'gameFSM') and self.gameFSM:
            return self.gameFSM._getShipLevel()
        try:
            return ShipGlobals.getShipLevel(self.shipClass)
        except:
            return 10

    def getDamageInputModifier(self):
        """Get damage input modifier (how much damage this NPC takes)."""
        return ShipBalance.NPCDamageIn.getValue()

    def getDamageOutputModifier(self):
        """Get damage output modifier (how much damage this NPC deals)."""
        return ShipBalance.NPCDamageOut.getValue()

    def getArmorModifier(self):
        """
        Get NPC armor modifier.
        NPC ships have reduced armor effectiveness (50%).
        """
        return ShipBalance.NPCArmorModifier.getValue()

    def takeDamage(self, damage, attackerDoId=0, applyModifiers=True):
        """
        Called when this ship takes damage.
        Applies NPC damage modifiers and notifies the AI FSM.
        
        Args:
            damage: Base damage amount
            attackerDoId: DoId of attacking ship (for threat tracking)
            applyModifiers: Whether to apply NPC damage input modifier
        """
        # Apply NPC damage input modifier if requested
        if applyModifiers:
            damage = damage * self.getDamageInputModifier()
        
        # Apply armor absorption (with NPC modifier)
        armorAbsorb = ShipBalance.ArmorAbsorb.getValue()
        npcArmorMod = self.getArmorModifier()
        effectiveArmor = armorAbsorb * npcArmorMod
        
        # Some damage is absorbed by armor
        damage = damage * (1.0 - effectiveArmor)
        
        # Apply the damage
        damage = int(damage)
        newHp = max(0, self.hp - damage)
        self.b_setHp(newHp)
        
        # Notify the AI FSM about the attack
        if hasattr(self, 'gameFSM') and self.gameFSM:
            self.gameFSM.onDamageReceived(attackerDoId, damage)
        
        # Check for sinking
        if newHp <= 0:
            self.b_setGameState('Sinking', 0)
        
        return newHp

    def handleCannonHit(self, attackerDoId, damage, hitPos):
        """
        Called when this ship is hit by a cannon.
        Applies armor bounce chance before taking damage.
        """
        # Check for armor bounce (20% chance to negate hit)
        armorBounce = ShipBalance.ArmorBounce.getValue()
        import random
        if random.random() < armorBounce:
            # Shot bounced off armor
            return
        
        self.takeDamage(damage, attackerDoId)

    def handleBroadsideHit(self, attackerDoId, damage):
        """
        Called when this ship is hit by a broadside.
        Broadsides cannot bounce off armor.
        """
        self.takeDamage(damage, attackerDoId)

    def calculateDamageToTarget(self, baseDamage, target, distance=0):
        """
        Calculate damage this NPC deals to a target.
        Applies NPC output modifier, level scaling, and distance falloff.
        
        Args:
            baseDamage: Base damage amount
            target: Target ship
            distance: Distance to target (for falloff)
            
        Returns:
            Final calculated damage
        """
        damage = baseDamage
        
        # Apply NPC damage output modifier (1.8x)
        damage = damage * self.getDamageOutputModifier()
        
        # Apply level-based modifier
        if hasattr(self, 'gameFSM') and self.gameFSM:
            levelMod = self.gameFSM._getLevelBasedDamageModifier(target)
            damage = damage * levelMod
        
        # Apply distance falloff
        if distance > 0 and hasattr(self, 'gameFSM') and self.gameFSM:
            falloffMod = self.gameFSM._calculateDamageFalloff(distance)
            damage = damage * falloffMod
        
        return int(damage)
