from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import globalClockDelta
from pirates.battle import WeaponGlobals
from pirates.battle.EnemySkills import EnemySkills
from pirates.uberdog.UberDogGlobals import InventoryType

class ComboDiary:
    notify = directNotify.newCategory('ComboDiary')
    TIMESTAMP_INDEX = 0
    SKILLID_INDEX = 1
    DAMAGE_INDEX = 2
    TOLERANCE = 3.0
    COMBO_ORDER = {
        InventoryType.CutlassRep: [
            InventoryType.CutlassHack,
            InventoryType.CutlassSlash,
            InventoryType.CutlassCleave,
            InventoryType.CutlassFlourish,
            InventoryType.CutlassStab],
        InventoryType.DaggerRep: [
            InventoryType.DaggerCut,
            InventoryType.DaggerSwipe,
            InventoryType.DaggerGouge,
            InventoryType.DaggerEviscerate]}
    SPECIAL_SKILLS = {
        InventoryType.CutlassRep: [
            InventoryType.CutlassSweep,
            InventoryType.CutlassBrawl,
            InventoryType.CutlassBladestorm],
        InventoryType.DaggerRep: [
            InventoryType.DaggerAsp,
            InventoryType.DaggerAdder,
            InventoryType.DaggerSidewinder,
            InventoryType.DaggerViperNest]}
    EXCLUDED_SKILLS = (InventoryType.CannonShoot, InventoryType.CutlassTaunt, InventoryType.DaggerThrowDirt, InventoryType.DollAttune, EnemySkills.DOLL_UNATTUNE, InventoryType.DollHeal, InventoryType.DollCure, InventoryType.DollShackles, InventoryType.DollCurse)
    
    def __init__(self, av):
        self.owner = av
        self.timers = {}

    def cleanup(self):
        self.timers = {}
        self.owner = None
    
    def clear(self):
        self.timers = {}
    
    def recordAttack(self, avId, skillId, damage):
        if skillId in self.EXCLUDED_SKILLS:
            return 0
        
        timestamp = globalClock.getFrameTime()
        val = self.checkComboExpired(avId, skillId)
        if val:
            self.owner.resetComboLevel()
            self.clear()
        
        if not self.timers.get(avId):
            self.timers[avId] = []
        else:
            val = self.verifyCombo(avId, skillId, timestamp)
            if not val:
                return
            
        self.timers[avId].append((timestamp, skillId, damage))

    def getCombo(self):
        totalCombo = 0
        totalDamage = 0
        numAttackers = 0
        for avId in self.timers:
            numAttackers += 1
            for entry in self.timers[avId]:
                skillId = entry[self.SKILLID_INDEX]
                numHits = WeaponGlobals.getNumHits(skillId)
                totalCombo += numHits
                totalDamage += entry[self.DAMAGE_INDEX]

        return (totalCombo, totalDamage, numAttackers)

    def checkComboExpired(self, avId, skillId):
        barTime = 3.0
        curTime = globalClock.getFrameTime()
        for attackerId in self.timers:
            comboLength = len(self.timers[attackerId])
            lastEntry = self.timers[attackerId][comboLength - 1]
            lastSkillId = lastEntry[self.SKILLID_INDEX]
            timestamp = lastEntry[self.TIMESTAMP_INDEX]
            if (barTime + timestamp - curTime) + self.TOLERANCE > 0:
                if attackerId != avId:
                    return 0
                
                repId = WeaponGlobals.getSkillReputationCategoryId(skillId)
                if not repId:
                    return 0
                
                comboChain = self.COMBO_ORDER.get(repId)
                if comboChain:
                    if skillId in self.SPECIAL_SKILLS.get(repId):
                        if lastSkillId not in self.SPECIAL_SKILLS.get(repId):
                            return 0
                        
                    elif skillId in comboChain:
                        index = comboChain.index(skillId)
                        if index > 0:
                            requisiteAttack = comboChain[index - 1]
                            if lastSkillId == requisiteAttack:
                                return 0
                            
                        elif not comboLength:
                            return 0

        return 1

    def verifyCombo(self, avId, skillId, timestamp):
        if skillId in self.EXCLUDED_SKILLS:
            return 0
        
        combo = self.timers.get(avId)
        if not combo:
            return 0
        
        comboLength = len(combo)
        lastEntry = combo[comboLength - 1]
        lastSkillId = lastEntry[self.SKILLID_INDEX]
        lastTimestamp = lastEntry[self.TIMESTAMP_INDEX]
        repId = WeaponGlobals.getSkillReputationCategoryId(skillId)
        if not repId:
            return 0
        
        comboChain = self.COMBO_ORDER.get(repId)
        if not comboChain:
            return 0
        
        if skillId in comboChain:
            index = comboChain.index(skillId)
            requisiteAttack = comboChain[index - 1]
            if lastSkillId != requisiteAttack and lastSkillId not in self.SPECIAL_SKILLS.get(repId):
                return 0

        barTime = 3.0
        if barTime + lastTimestamp + self.TOLERANCE < timestamp:
            return 0
        
        return 1

    def __str__(self):
        s = 'ComboDiary\n'
        s += ' Avatar: Combos\n'
        for (avId, combos) in list(self.timers.items()):
            s += ' %s : \n' % avId
            for entry in combos:
                skillId = entry[self.SKILLID_INDEX]
                damage = entry[self.DAMAGE_INDEX]
                timestamp = entry[self.TIMESTAMP_INDEX]
                s += '    %s : %s damage, timestamp=%f (s)\n' % (skillId, damage, timestamp)

        return s


