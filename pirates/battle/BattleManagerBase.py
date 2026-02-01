from direct.directnotify import DirectNotifyGlobal
from pirates.battle import WeaponGlobals
from pirates.pirate import AvatarTypes
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import EnemyGlobals
from pirates.battle.EnemySkills import EnemySkills
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PiratesGlobals

class BattleManagerBase:
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleManager')
    PirateCodeWeapons = (InventoryType.PistolWeaponL1, InventoryType.PistolWeaponL2, InventoryType.PistolWeaponL3, InventoryType.PistolWeaponL4, InventoryType.PistolWeaponL5, InventoryType.PistolWeaponL6, InventoryType.MusketWeaponL1, InventoryType.MusketWeaponL2, InventoryType.MusketWeaponL3)
    SkillRechargeTimeConfig = config.GetFloat('skill-recharge-time', -1.0)
    
    def isPVP(self, attacker, target):
        if target and target.getTeam() == PiratesGlobals.PLAYER_TEAM and attacker and attacker.getTeam() == PiratesGlobals.PLAYER_TEAM:
            return True
        
        return False
    
    def obeysPirateCode(self, attacker, target):
        if not hasattr(target, 'avatarType'):
            return True
        
        if not target.isNpc and target.zombie:
            return True
        
        human = target.avatarType.isA(AvatarTypes.Navy) or target.avatarType.isA(AvatarTypes.Townfolk) or target.avatarType.isA(AvatarTypes.Pirate) or target.avatarType.isA(AvatarTypes.TradingCo)
        if human and attacker.currentWeaponId in self.PirateCodeWeapons:
            return False
        
        return True

    def willWeaponHit(self, attacker, target, skillId, ammoSkillId, charge):
        if not attacker.getWorld():
            return WeaponGlobals.RESULT_NOT_AVAILABLE
        
        inPVPMode = self.isPVP(attacker, target)
        chanceOfHit = WeaponGlobals.getAttackAccuracy(skillId, ammoSkillId)
        if target and not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId):
            if not inPVPMode:
                accuracyModifier = WeaponGlobals.getComparativeLevelAccuracyModifier(attacker, target)
                chanceOfHit = max(0.0, chanceOfHit + accuracyModifier)

        skillRange = self.getModifiedAttackRange(attacker, skillId, ammoSkillId)
        chanceOfParry = 0.0
        chanceOfDodge = 0.0
        chanceOfResist = 0.0
        skillEffects = attacker.getSkillEffects()
        for targetEffect in skillEffects:
            if targetEffect == WeaponGlobals.C_BLIND or targetEffect == WeaponGlobals.C_DIRT:
                chanceOfHit *= WeaponGlobals.BLIND_PERCENT

            elif targetEffect == WeaponGlobals.C_TAUNT:
                chanceOfHit *= WeaponGlobals.TAUNT_PERCENT
        
        attackType = WeaponGlobals.getAttackClass(skillId)
        if target and hasattr(target, 'isNpc') and not target.isNpc:
            defInv = target.getInventory()
            if defInv:
                if attackType == WeaponGlobals.AC_MISSILE:
                    chanceOfDodge = max(0, defInv.getStackQuantity(InventoryType.PistolDodge) - 1) * WeaponGlobals.getAttackDodge(InventoryType.PistolDodge)
                elif attackType == WeaponGlobals.AC_COMBAT:
                    chanceOfParry = max(0, defInv.getStackQuantity(InventoryType.CutlassParry) - 1) * WeaponGlobals.getAttackDodge(InventoryType.CutlassParry)
                elif attackType == WeaponGlobals.AC_MAGIC:
                    chanceOfResist = max(0, defInv.getStackQuantity(InventoryType.DollSpiritWard) - 1) * WeaponGlobals.getAttackDodge(InventoryType.DollSpiritWard)

        if not attacker.isNpc:
            attInv = attacker.getInventory()
            if attInv:
                if attackType == WeaponGlobals.AC_MAGIC:
                    pass
                elif attackType == WeaponGlobals.AC_MISSILE:
                    chanceOfHit += max(0, attInv.getStackQuantity(InventoryType.PistolSharpShooter) - 1) * WeaponGlobals.getAttackAccuracy(InventoryType.PistolSharpShooter)
                    chanceOfDodge -= max(0, attInv.getStackQuantity(InventoryType.PistolSharpShooter) - 1) * WeaponGlobals.getAttackAccuracy(InventoryType.PistolSharpShooter) / 2
                elif attackType == WeaponGlobals.AC_COMBAT:
                    pass

        randVal = attacker.battleRandom.getRandom('willWeaponHit:accuracy')
        hitRoll = chanceOfHit - randVal * 100
        randVal = attacker.battleRandom.getRandom('willWeaponHit:dodge')
        dodgeRoll = chanceOfDodge - randVal * 100
        randVal = attacker.battleRandom.getRandom('willWeaponHit:resist')
        resistRoll = chanceOfResist - randVal * 100
        randVal = attacker.battleRandom.getRandom('willWeaponHit:parry')
        parryRoll = chanceOfParry - randVal * 100
        if hitRoll < 0:
            return WeaponGlobals.RESULT_MISS
        
        if dodgeRoll >= 0:
            return WeaponGlobals.RESULT_DODGE
        
        if parryRoll >= 0:
            return WeaponGlobals.RESULT_PARRY
        
        if resistRoll >= 0:
            return WeaponGlobals.RESULT_RESIST
        
        return WeaponGlobals.RESULT_HIT
    
    def getModifiedSkillEffects(self, attacker, target, skillId, ammoSkillId, charge = 0, distance = 0.0):
        if not attacker.getWorld():
            return ([
                0,
                0,
                0,
                0,
                0], [
                0,
                0,
                0,
                0,
                0])
        
        (attackerEffects, targetEffects) = WeaponGlobals.getAttackEffects(skillId, ammoSkillId)
        inPVPMode = self.isPVP(attacker, target)
        tHealth = targetEffects[0]
        tMojo = targetEffects[3]
        aHealth = attackerEffects[0]
        aMojo = attackerEffects[3]
        randVal = attacker.battleRandom.getRandom('getModifiedSkillEffect %s %s' % (attacker, target))
        if attacker.isNpc:
            minValue = -1
        else:
            minValue = 0
        if tHealth <= 0:
            if attacker.isNpc:
                tHealth = -1 * attacker.getMonsterDmg() * WeaponGlobals.getNPCModifier(skillId)
            
            randomDamageMod = randVal / 2 + 0.5
            tHealth = min(tHealth * randomDamageMod, minValue)
        
        if tMojo < 0:
            randomDamageMod = randVal / 2 + 0.5
            tMojo = min(tMojo * randomDamageMod, minValue)
        
        if not attacker.isNpc and skillId != InventoryType.UseItem:
            if not inPVPMode or tHealth > 0:
                damageMod = WeaponGlobals.getLevelDamageModifier(attacker.getLevel())
                tHealth *= damageMod
                tMojo *= damageMod
                aHealth *= damageMod

        if skillId != InventoryType.UseItem:
            if hasattr(attacker, 'currentWeaponId'):
                (attackerBonus, targetBonus) = WeaponGlobals.getWeaponStats(attacker.currentWeaponId)
                if attackerBonus and targetBonus:
                    if aHealth > 0:
                        aHealth -= attackerBonus[0]
                    elif aHealth < 0:
                        aHealth += attackerBonus[0]
                    
                    if tHealth > 0:
                        tHealth -= targetBonus[0]
                    elif tHealth < 0:
                        tHealth += targetBonus[0]
                    
                    if tMojo > 0:
                        tMojo -= targetBonus[3]
                    elif tMojo < 0:
                        tMojo += targetBonus[3]

        if skillId != InventoryType.UseItem:
            scaleVal = 1
            if hasattr(attacker, 'currentWeaponId'):
                scaleVal = WeaponGlobals.getWeaponDamageScale(attacker.currentWeaponId)
            
            aHealth *= scaleVal
            tHealth *= scaleVal

        if attacker.isNpc:
            pass
        else:
            inv = attacker.getInventory()
            if inv and skillId != InventoryType.UseItem:
                amt = max(0, inv.getStackQuantity(skillId) - 2) * WeaponGlobals.LEVELUP_DAMAGE_MULTIPLIER
                amt += 1.0
                tHealth *= amt
                tMojo *= amt
                aHealth *= amt
                amt = max(0, inv.getStackQuantity(ammoSkillId) - 2) * WeaponGlobals.LEVELUP_DAMAGE_MULTIPLIER
                amt += 1.0
                tHealth *= amt
                tMojo *= amt
                aHealth *= amt
                if WeaponGlobals.isVoodooWeapon(attacker.currentWeaponId):
                    amt = max(0, inv.getStackQuantity(InventoryType.StaffSpiritLore) - 1) * WeaponGlobals.getAttackTargetHP(InventoryType.StaffSpiritLore)
                    amt += 1.0
                    tHealth *= amt
                    tMojo *= amt
                    aHealth *= amt

                if WeaponGlobals.isVoodooWeapon(attacker.currentWeaponId) and aMojo < 0:
                    amt = max(0, inv.getStackQuantity(InventoryType.StaffConservation) - 1) * WeaponGlobals.getAttackSelfMojo(InventoryType.StaffConservation)
                    aMojo = min(aMojo - aMojo * amt, 1)

                if WeaponGlobals.isBladedWeapon(attacker.currentWeaponId):
                    amt = max(0, inv.getStackQuantity(InventoryType.DaggerBladeInstinct) - 1) * WeaponGlobals.getAttackTargetHP(InventoryType.DaggerBladeInstinct)
                    amt += 1.0
                    tHealth *= amt
                    tMojo *= amt
                    aMojo *= amt

                if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_CANNON or WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_GRENADE:
                    amt = max(0, inv.getStackQuantity(InventoryType.CannonBarrage) - 1) * WeaponGlobals.getAttackTargetHP(InventoryType.CannonBarrage)
                    amt += 1.0
                    tHealth *= amt
                    tMojo *= amt
                    aHealth *= amt

        if skillId in InventoryType.BackstabSkills and charge:
            tHealth *= WeaponGlobals.BACKSTAB_BONUS

        if attacker:
            if hasattr(attacker, 'isNpc'):
                if attacker.isNpc:
                    pass
                else:
                    inv = attacker.getInventory()
                    if inv:
                        attackClass = WeaponGlobals.getAttackClass(skillId)
                        if attackClass == WeaponGlobals.AC_GRENADE or attackClass == WeaponGlobals.AC_CANNON:
                            amt = max(0, inv.getStackQuantity(InventoryType.GrenadeToughness) - 1) * WeaponGlobals.getAttackSelfHP(InventoryType.GrenadeToughness)
                            amt = 1.0 - amt
                            aHealth *= amt

        if target:
            if hasattr(target, 'isNpc'):
                if target.isNpc:
                    pass
                else:
                    inv = target.getInventory()
                    if inv:
                        attackClass = WeaponGlobals.getAttackClass(skillId)
                        if attackClass == WeaponGlobals.AC_GRENADE or attackClass == WeaponGlobals.AC_CANNON:
                            amt = max(0, inv.getStackQuantity(InventoryType.GrenadeToughness) - 1) * WeaponGlobals.getAttackSelfHP(InventoryType.GrenadeToughness)
                            amt = 1.0 - amt
                            tHealth *= amt

        if skillId == InventoryType.PistolTakeAim:
            if charge > 0:
                maxCharge = WeaponGlobals.getAttackMaxCharge(skillId, ammoSkillId)
                charge = min(charge, maxCharge)
                tHealth += tHealth * charge * 1.0
                aHealth += aHealth * charge * 1.0

        if hasattr(attacker, 'getSkillEffects') and skillId != InventoryType.UseItem:
            skillEffects = attacker.getSkillEffects()
            if WeaponGlobals.C_OPENFIRE in skillEffects:
                if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_CANNON:
                    tHealth *= WeaponGlobals.OPEN_FIRE_BONUS
                    aHealth *= WeaponGlobals.OPEN_FIRE_BONUS

            if WeaponGlobals.C_WEAKEN in skillEffects:
                if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_COMBAT:
                    tHealth = min(-1, tHealth - tHealth * WeaponGlobals.WEAKEN_PENALTY)
                    aHealth = min(-1, aHealth - aHealth * WeaponGlobals.WEAKEN_PENALTY)

        if target and skillId != InventoryType.UseItem:
            if hasattr(target, 'getSkillEffects'):
                skillEffects = target.getSkillEffects()
                if WeaponGlobals.C_CURSE in skillEffects:
                    if WeaponGlobals.getAttackClass(skillId) != WeaponGlobals.AC_MAGIC:
                        tHealth += int(tHealth * WeaponGlobals.CURSED_DAM_AMP)
                        aHealth += int(aHealth * WeaponGlobals.CURSED_DAM_AMP)

                if WeaponGlobals.C_TAKECOVER in skillEffects:
                    tHealth = 0
                    aHealth = 0

        buff = WeaponGlobals.getSkillEffectFlag(skillId)
        ammoBuff = WeaponGlobals.getSkillEffectFlag(ammoSkillId)
        if target and skillId != InventoryType.UseItem and not inPVPMode:
            if hasattr(target, 'avatarType'):
                avClass = EnemyGlobals.getMonsterClass(target.avatarType)
                if avClass == EnemyGlobals.MONSTER:
                    if buff == WeaponGlobals.C_UNDEAD_KILLER or ammoBuff == WeaponGlobals.C_UNDEAD_KILLER:
                        tHealth = min(-1, tHealth * WeaponGlobals.RESIST_DAMAGE_PENALTY)

                elif avClass == EnemyGlobals.SKELETON:
                    if buff == WeaponGlobals.C_MONSTER_KILLER or ammoBuff == WeaponGlobals.C_MONSTER_KILLER:
                        tHealth = min(-1, tHealth * WeaponGlobals.RESIST_DAMAGE_PENALTY)

                elif avClass == EnemyGlobals.HUMAN:
                    if buff == WeaponGlobals.C_MONSTER_KILLER or ammoBuff == WeaponGlobals.C_MONSTER_KILLER or buff == WeaponGlobals.C_UNDEAD_KILLER or ammoBuff == WeaponGlobals.C_UNDEAD_KILLER:
                        tHealth = min(-1, tHealth * WeaponGlobals.RESIST_DAMAGE_PENALTY)

        if buff == WeaponGlobals.C_LIFEDRAIN or ammoBuff == WeaponGlobals.C_LIFEDRAIN:
            aHealth += abs(tHealth)
        elif buff == WeaponGlobals.C_SOULTAP or ammoBuff == WeaponGlobals.C_SOULTAP:
            aHealth -= attacker.hp * 0.666
        
        if WeaponGlobals.getIsDollAttackSkill(skillId) and not attacker.isNpc:
            friendlyFire = WeaponGlobals.isFriendlyFire(skillId)
            if friendlyFire:
                numTargets = len(attacker.getFriendlyStickyTargets())
            else:
                numTargets = len(attacker.getHostileStickyTargets())
            if numTargets > 1:
                tHealth /= numTargets
                tMojo /= numTargets

        if target:
            if hasattr(target, 'isTeamCombo'):
                if target.isTeamCombo > 1:
                    comboLength = target.combo
                    bonus = WeaponGlobals.getComboBonus(comboLength)
                    if bonus:
                        tHealth -= bonus

        if attacker.isNpc:
            aHealth *= EnemyGlobals.ENEMY_DAMAGE_NERF
            tHealth *= EnemyGlobals.ENEMY_DAMAGE_NERF
            tMojo *= EnemyGlobals.ENEMY_DAMAGE_NERF
        
        if skillId != InventoryType.UseItem and target and not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId) and not inPVPMode:
            damageMod = WeaponGlobals.getComparativeLevelDamageModifier(attacker, target)
            numHits = WeaponGlobals.getNumHits(skillId, ammoSkillId)
            if numHits > 1:
                numHits += 1
            
            if tHealth <= 0:
                tHealth = min(-numHits, tHealth * damageMod)
            
            if aHealth <= 0:
                aHealth = min(0.0, aHealth * damageMod)

        if inPVPMode:
            scale = WeaponGlobals.getWeaponPvpDamageScale(attacker.currentWeaponId)
            tHealth *= scale
            tMojo *= scale
            aHealth *= scale
        
        targetEffects = [
            tHealth,
            targetEffects[1],
            targetEffects[2],
            tMojo,
            targetEffects[4]]
        attackerEffects = [
            aHealth,
            attackerEffects[1],
            attackerEffects[2],
            aMojo,
            attackerEffects[4]]
        if not target:
            for i in range(len(targetEffects)):
                targetEffects[i] = 0

        targetEffects[0] = max(-30000, int(targetEffects[0]))
        targetEffects[3] = max(-30000, int(targetEffects[3]))
        attackerEffects[0] = max(-30000, int(attackerEffects[0]))
        attackerEffects[3] = max(-30000, int(attackerEffects[3]))
        buff = WeaponGlobals.getSkillEffectFlag(ammoSkillId)
        if target and skillId == InventoryType.UseItem:
            if buff == WeaponGlobals.C_SHIPHEAL:
                if hasattr(target, 'b_setSpDelta'):
                    hpDelta = WeaponGlobals.getAttackHullHP(skillId, ammoSkillId)
                    target.b_setHpDelta(hpDelta)
                    spDelta = WeaponGlobals.getAttackSailHP(skillId, ammoSkillId)
                    target.b_setSpDelta(spDelta)

        return (attackerEffects, targetEffects)

    def getModifiedSkillEffectsSword(self, attacker, target, skillId, ammoSkillId, charge = 0, distance = 0.0):
        if not target or not attacker.getWorld():
            return ([
                0,
                0,
                0,
                0,
                0], [
                0,
                0,
                0,
                0,
                0])
        
        (attackerEffects, targetEffects) = WeaponGlobals.getAttackEffects(skillId, ammoSkillId)
        tDamage = targetEffects[0]
        inPVPMode = self.isPVP(attacker, target)
        randVal = attacker.battleRandom.getRandom('getModifiedSkillEffectSword %s' % tDamage)
        randomDamageMod = randVal / 2 + 0.5
        if attacker.isNpc:
            minValue = -1
        else:
            minValue = 0
        if attacker.isNpc:
            tDamage = -1 * attacker.getMonsterDmg() * WeaponGlobals.getNPCModifier(skillId)
        tDamage = min(tDamage * randomDamageMod, minValue)
        if not attacker.isNpc and not inPVPMode:
            damageMod = WeaponGlobals.getLevelDamageModifier(attacker.getLevel())
            tDamage *= damageMod
        if hasattr(attacker, 'currentWeaponId'):
            attackerBonus, targetBonus = WeaponGlobals.getWeaponStats(attacker.currentWeaponId)
            if tDamage != 0:
                tDamage += targetBonus[0]
        if hasattr(attacker, 'currentWeaponId'):
            tDamage *= WeaponGlobals.getWeaponDamageScale(attacker.currentWeaponId)
        if attacker.isNpc:
            pass
        else:
            inv = attacker.getInventory()
            if inv:
                tDamage *= max(0, inv.getStackQuantity(skillId) - 2) * WeaponGlobals.LEVELUP_DAMAGE_MULTIPLIER + 1
                tDamage *= max(0, inv.getStackQuantity(InventoryType.DaggerBladeInstinct) - 1) * WeaponGlobals.getAttackTargetHP(InventoryType.DaggerBladeInstinct) + 1
        if hasattr(attacker, 'getSkillEffects'):
            skillEffects = attacker.getSkillEffects()
            if WeaponGlobals.C_WEAKEN in skillEffects:
                tDamage = min(-1, tDamage - tDamage * WeaponGlobals.WEAKEN_PENALTY)
        if hasattr(target, 'getSkillEffects'):
            skillEffects = target.getSkillEffects()
            if WeaponGlobals.C_CURSE in skillEffects:
                tDamage += int(tDamage * WeaponGlobals.CURSED_DAM_AMP)
            if WeaponGlobals.C_TAKECOVER in skillEffects:
                tDamage = 0
        if hasattr(target, 'isTeamCombo'):
            if target.isTeamCombo > 1:
                comboLength = target.combo
                bonus = WeaponGlobals.getComboBonus(comboLength)
                if bonus:
                    tDamage -= bonus
        if skillId != InventoryType.UseItem and target and not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId):
            damageMod = WeaponGlobals.getComparativeLevelDamageModifier(attacker, target)
            if inPVPMode:
                damageMod = 1
            numHits = WeaponGlobals.getNumHits(skillId, ammoSkillId)
            if numHits > 1:
                numHits += 1
            if tDamage <= 0:
                tDamage = min(-numHits, tDamage * damageMod)
        if attacker.isNpc:
            tDamage *= EnemyGlobals.ENEMY_DAMAGE_NERF
        elif inPVPMode:
            scale = WeaponGlobals.getWeaponPvpDamageScale(attacker.currentWeaponId)
            tDamage *= scale
        
        return ([
            0,
            0,
            0,
            0,
            0], [
            int(tDamage),
            targetEffects[1],
            targetEffects[2],
            targetEffects[3],
            targetEffects[4]])

    def getModifiedShipEffects(self, skillId, ammoSkillId = 0, distance = 0.0):
        shipEffects = WeaponGlobals.getShipEffects(skillId, ammoSkillId)
        return shipEffects

    def addStats(self, attackerStats, targetStats, attackerBonusStats, targetBonusStats):
        for i in range(len(attackerStats)):
            if attackerStats[i] != 0:
                attackerStats[i] += attackerBonusStats[i]
        
        for i in range(len(targetStats)):
            if targetStats[i] != 0:
                targetStats[i] += targetBonusStats[i]
        
        return (attackerStats, targetStats)

    def damageModifier(self, level, attacker, damage):
        modifier = level * EnemyGlobals.CANNON_DAMAGE_MODIFIER_PER_LEVEL + EnemyGlobals.CANNON_BASE_DAMAGE_MODIFIER
        return int(damage * modifier)

    def getModifiedHullDamage(self, attacker, target, skillId, ammoSkillId):
        damage = WeaponGlobals.getAttackHullHP(skillId, ammoSkillId)
        if attacker:
            damage = self.damageModifier(attacker.getLevel(), attacker, damage)
        else:
            self.notify.warning('ship taking damage with no attacker')
        finalDamage = self.getModifiedShipDamage(attacker, target, skillId, ammoSkillId, damage)
        return finalDamage

    def getModifiedSailDamage(self, attacker, target, skillId, ammoSkillId):
        damage = WeaponGlobals.getAttackSailHP(skillId, ammoSkillId)
        if attacker:
            damage = self.damageModifier(attacker.getLevel(), attacker, damage)
        else:
            self.notify.warning('ship taking damage with no attacker')
        finalDamage = self.getModifiedShipDamage(attacker, target, skillId, ammoSkillId, damage)
        return finalDamage

    def getModifiedShipDamage(self, attacker, target, skillId, ammoSkillId, damage):
        if not attacker:
            return damage
        
        if hasattr(attacker, 'ship') and attacker.ship:
            damage *= attacker.ship.getDamageOutputModifier()
        elif hasattr(attacker, 'getDamageOutputModifier'):
            damage *= attacker.getDamageOutputModifier()
        
        if hasattr(target, 'ship') and target.ship:
            damage *= target.ship.getDamageInputModifier()
        elif hasattr(target, 'getDamageInputModifier'):
            damage *= target.getDamageInputModifier()
        
        if hasattr(attacker, 'isNpc') and not attacker.isNpc:
            inv = attacker.getInventory()
            if inv:
                if skillId != InventoryType.CannonShoot:
                    amt = max(0, inv.getStackQuantity(skillId) - 2) * WeaponGlobals.LEVELUP_DAMAGE_MULTIPLIER
                    amt += 1.0
                    damage *= amt
                
                amt = max(0, inv.getStackQuantity(ammoSkillId) - 2) * WeaponGlobals.LEVELUP_DAMAGE_MULTIPLIER
                amt += 1.0
                damage *= amt
                if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_CANNON or WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_GRENADE or skillId == EnemySkills.LEFT_BROADSIDE or skillId == EnemySkills.RIGHT_BROADSIDE:
                    amt = max(0, inv.getStackQuantity(InventoryType.CannonBarrage) - 1) * WeaponGlobals.getAttackTargetHP(InventoryType.CannonBarrage)
                    amt += 1.0
                    damage *= amt
                
                if skillId == EnemySkills.LEFT_BROADSIDE:
                    amt = max(0, inv.getStackQuantity(InventoryType.SailBroadsideLeft) - 2) * WeaponGlobals.getAttackTargetHP(InventoryType.SailBroadsideLeft)
                    amt += 1.0
                    damage *= amt
                
                if skillId == EnemySkills.RIGHT_BROADSIDE:
                    amt = max(0, inv.getStackQuantity(InventoryType.SailBroadsideRight) - 2) * WeaponGlobals.getAttackTargetHP(InventoryType.SailBroadsideRight)
                    amt += 1.0
                    damage *= amt

        if hasattr(attacker, 'getSkillEffects'):
            skillEffects = attacker.getSkillEffects()
            for buff in skillEffects:
                if buff == WeaponGlobals.C_OPENFIRE:
                    damage = damage * WeaponGlobals.OPEN_FIRE_BONUS

        if hasattr(target, 'getSkillEffects'):
            skillEffects = target.getSkillEffects()
            for buff in skillEffects:
                if buff == WeaponGlobals.C_TAKECOVER:
                    damage = damage * WeaponGlobals.TAKE_COVER_BONUS

        if hasattr(attacker, 'isNpc') and attacker.isNpc and ammoSkillId:
            scale = WeaponGlobals.getAmmoNPCDamageScale(ammoSkillId)
            damage *= scale
        
        if target:
            if hasattr(attacker, 'getNPCship') and attacker.getNPCship() or hasattr(target, 'getNPCship') and target.getNPCship():
                damageMod = max(EnemyGlobals.MAX_COMPARATIVE_SHIP_LEVEL_DAMAGE_MOD, WeaponGlobals.getComparativeShipLevelDamageModifier(attacker, target))
                if damage <= 0:
                    damage = min(-1, damage * damageMod)

        return int(damage)

    def getModifiedRechargeTime(self, av, skillId, ammoSkillId = 0):
        if config.GetBool('instant-skill-recharge', 0):
            return 0.0
        
        if self.SkillRechargeTimeConfig >= 0.0:
            return self.SkillRechargeTimeConfig
        
        if skillId == InventoryType.CannonShoot or skillId == EnemySkills.LEFT_BROADSIDE or skillId == EnemySkills.RIGHT_BROADSIDE:
            ammoSkillId = 0
        
        rechargeTime = WeaponGlobals.getAttackRechargeTime(skillId, ammoSkillId)
        if rechargeTime:
            if av:
                if not av.isNpc:
                    inv = av.getInventory()
                    if inv:
                        if WeaponGlobals.getIsShipSkill(skillId):
                            if hasattr(av.ship, 'getSkillEffects'):
                                skillEffects = av.ship.getSkillEffects()
                                for buff in skillEffects:
                                    if buff == WeaponGlobals.C_RECHARGE:
                                        if skillId != InventoryType.SailPowerRecharge:
                                            rechargeTime *= WeaponGlobals.POWER_RECHARGE_RATE_REDUCTION

                        if skillId == InventoryType.CannonShoot:
                            rechargeTime *= 1.0 - max(0, inv.getStackQuantity(InventoryType.CannonShoot) - 2) * WeaponGlobals.CANNON_SHOOT_RATE_REDUCTION
                        elif WeaponGlobals.getIsShipSkill(skillId):
                            if skillId == InventoryType.SailBroadsideLeft or skillId == InventoryType.SailBroadsideRight:
                                rechargeTime *= 1.0 - max(0, inv.getStackQuantity(InventoryType.SailTaskmaster) - 1) * WeaponGlobals.getAttackRechargeTime(InventoryType.SailTaskmaster)
                            
                        elif WeaponGlobals.isBladedWeapon(av.currentWeaponId):
                            rechargeTime *= 1.0 - max(0, inv.getStackQuantity(InventoryType.DaggerFinesse) - 1) * WeaponGlobals.getAttackRechargeTime(InventoryType.DaggerFinesse)

        return rechargeTime

    def getModifiedReloadTime(self, av, skillId, ammoSkillId = 0):
        if config.GetBool('instant-skill-recharge', 0):
            return 0.0
        
        rechargeTime = WeaponGlobals.getAttackRechargeTime(0, ammoSkillId)
        if rechargeTime:
            if av:
                if not av.isNpc:
                    inv = av.getInventory()
                    if inv:
                        if WeaponGlobals.getIsCannonSkill(skillId):
                            if hasattr(av.ship, 'getSkillEffects'):
                                skillEffects = av.ship.getSkillEffects()
                                for buff in skillEffects:
                                    if buff == WeaponGlobals.C_RECHARGE:
                                        rechargeTime *= WeaponGlobals.POWER_RECHARGE_RATE_REDUCTION

                        if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_CANNON:
                            amt = max(0, inv.getStackQuantity(InventoryType.CannonRapidReload) - 1) * WeaponGlobals.getAttackRechargeTime(InventoryType.CannonRapidReload)
                            amt = 1.0 - amt
                            rechargeTime *= amt

        return rechargeTime

    def getModifiedAttackRange(self, av, skillId, ammoSkillId = 0):
        range = WeaponGlobals.getAttackRange(skillId, ammoSkillId)
        if range:
            if av:
                if not av.isNpc:
                    inv = av.getInventory()
                    if inv:
                        attackType = WeaponGlobals.getAttackClass(skillId)
                        if attackType == WeaponGlobals.AC_MISSILE:
                            amt = max(0, inv.getStackQuantity(InventoryType.PistolEagleEye) - 1) * WeaponGlobals.getAttackRange(InventoryType.PistolEagleEye)
                            range += amt

        return range

    def getModifiedAttackAreaRadius(self, av, skillId, ammoSkillId = 0):
        aoeRadius = WeaponGlobals.getAttackAreaRadius(skillId, ammoSkillId)
        if aoeRadius:
            if av:
                if hasattr(av, 'isNpc') and not av.isNpc:
                    inv = av.getInventory()
                    if inv:
                        attackType = WeaponGlobals.getAttackClass(skillId)
                        if attackType == WeaponGlobals.AC_GRENADE or attackType == WeaponGlobals.AC_CANNON:
                            amt = max(0, inv.getStackQuantity(InventoryType.GrenadeDemolitions) - 1) * WeaponGlobals.getAttackAreaRadius(InventoryType.GrenadeDemolitions)
                            amt += 1.0
                            aoeRadius *= amt

        return aoeRadius

    def getModifiedAttackReputation(self, attacker, target, skillId, ammoSkillId):
        reputation = WeaponGlobals.getAttackReputation(skillId, ammoSkillId)
        if reputation:
            reputation *= WeaponGlobals.getWeaponExperienceScale(attacker.currentWeaponId)
        
        return reputation

    def getModifiedExperienceGrade(self, attacker, target, skillId = 0, ammoSkillId = 0, currentWeaponId = 0, repId = 0):
        attackerLevel = attacker.getLevel()
        targetLevel = target.getLevel()
        isBoss = target.isBoss()
        inv = attacker.getInventory()
        if not attackerLevel or not targetLevel or not inv:
            return 0
        
        weaponLevel = 0
        if not repId:
            if currentWeaponId:
                repId = WeaponGlobals.getRepId(currentWeaponId)
            elif skillId or ammoSkillId:
                repId = WeaponGlobals.getSkillReputationCategoryId(skillId)

        if repId:
            value = inv.getReputation(repId)
            (weaponLevel, leftoverValue) = ReputationGlobals.getLevelFromTotalReputation(repId, value)
        
        levelWeight = 0
        if weaponLevel:
            levelWeight = 2
        
        expLevel = (attackerLevel + weaponLevel * 2) / (1 + levelWeight)
        if isBoss:
            targetLevel *= 1.5
        
        if expLevel > targetLevel + EnemyGlobals.ENEMY_LEVEL_THRESHOLD:
            levelGrade = EnemyGlobals.GREY
        elif expLevel > targetLevel:
            levelGrade = EnemyGlobals.GREEN
        elif expLevel > targetLevel - EnemyGlobals.ENEMY_LEVEL_THRESHOLD:
            levelGrade = EnemyGlobals.YELLOW
        else:
            levelGrade = EnemyGlobals.RED
        return levelGrade

    def getExperienceColor(self, av, target):
        levelRank = self.getModifiedExperienceGrade(av, target, currentWeaponId = av.currentWeaponId)
        if levelRank >= EnemyGlobals.RED:
            color = '\x01red\x01'
        elif levelRank >= EnemyGlobals.YELLOW:
            color = '\x01yellow\x01'
        elif levelRank >= EnemyGlobals.GREEN:
            color = '\x01midgreen\x01'
        elif levelRank == EnemyGlobals.GREY:
            color = '\x01grey\x01'
        else:
            color = '\x01white\x01'
        return color


