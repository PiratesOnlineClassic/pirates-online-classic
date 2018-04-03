# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.WeaponBaseBase
import math
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TeamUtils
import WeaponGlobals

class WeaponBaseBase:
    __module__ = __name__
    areaCollisionsCreated = 0
    areaCollSphere = None
    areaCollTube = None
    areaCollCone = None
    areaCollTrav = None
    areaCollQueue = None
    areaCollHandler = None

    @classmethod
    def createCollisions(self):
        if self.areaCollisionsCreated:
            return
        self.areaCollTrav = CollisionTraverser('WeaponBase.collTrav')
        collSphere = CollisionSphere(0, 0, 0, 1)
        node = CollisionNode('areaTargetCollSphere')
        node.addSolid(collSphere)
        node.setFromCollideMask(PiratesGlobals.BattleAimBitmask)
        node.setIntoCollideMask(BitMask32.allOff())
        self.areaCollSphere = NodePath(node)
        self.areaCollSphere.setName('WeaponBase.areaCollSphere')
        r = 3
        z = 0
        node = CollisionNode('areaTargetCollTube')
        for i in range(12):
            collSphere = CollisionSphere(0, r + i * r * 1.5, z, r)
            node.addSolid(collSphere)

        node.setFromCollideMask(PiratesGlobals.BattleAimBitmask)
        node.setIntoCollideMask(BitMask32.allOff())
        self.areaCollTube = NodePath(node)
        self.areaCollTube.setName('WeaponBase.areaCollTube')
        self.areaCollTube.setScale(1 / 50.0)
        self.areaCollTube.flattenStrong()
        numSpheres = 7
        node = CollisionNode('areaTargetCollCone')
        angle = 35.0
        angleFactor = math.tan(math.radians(angle * 0.5))
        for i in range(numSpheres):
            n = i + 1
            y = (n * n + 1) * 0.5
            z = 0
            r = angleFactor * y
            collSphere = CollisionSphere(0, y, z, r)
            node.addSolid(collSphere)

        node.setFromCollideMask(PiratesGlobals.BattleAimBitmask)
        node.setIntoCollideMask(BitMask32.allOff())
        self.areaCollCone = NodePath(node)
        self.areaCollCone.setName('WeaponBase.areaCollCone')
        finalSphere = node.getSolid(numSpheres - 1)
        totalLength = finalSphere.getCenter()[1] + finalSphere.getRadius()
        self.areaCollCone.setScale(1.0 / totalLength)
        self.areaCollCone.flattenStrong()
        self.areaCollQueue = CollisionHandlerQueue()
        self.areaCollHandler = CollisionHandlerEvent()
        self.areaCollTrav.addCollider(self.areaCollSphere, self.areaCollQueue)
        self.areaCollisionsCreated = 1

    def __init__(self, avatar, repository):
        self.repository = repository
        self.avatar = avatar
        if not hasattr(self.avatar, 'aimTubeNodePaths'):
            self.avatar.aimTubeNodePaths = []

    def delete(self):
        self.repository = None
        self.avatar = None
        return

    def runSphereAreaCollisions(self, skillId, ammoSkillId, target, pos):
        self.createCollisions()
        self.areaCollSphere.reparentTo(self.getRender())
        self.areaCollSphere.setPos(target, pos)
        radius = self.repository.battleMgr.getModifiedAttackAreaRadius(self.avatar, skillId, ammoSkillId)
        self.areaCollSphere.setScale(radius)
        self.areaCollTrav.addCollider(self.areaCollSphere, self.areaCollQueue)
        self.areaCollTrav.traverse(self.getRender())
        self.areaCollTrav.removeCollider(self.areaCollSphere)
        self.areaCollQueue.sortEntries()
        self.areaCollSphere.detachNode()

    def runTubeAreaCollisions(self, skillId, ammoSkillId, target, pos):
        self.createCollisions()
        self.areaCollTube.reparentTo(self.getRender())
        self.areaCollTube.setPosHpr(self, 0, 0, 0, 0, 0, 0)
        range = self.repository.battleMgr.getModifiedAttackRange(self.avatar, skillId, ammoSkillId)
        self.areaCollTube.setScale(range)
        self.areaCollTrav.addCollider(self.areaCollTube, self.areaCollQueue)
        self.areaCollTrav.traverse(self.getRender())
        self.areaCollTrav.removeCollider(self.areaCollTube)
        self.areaCollQueue.sortEntries()
        self.areaCollTube.detachNode()

    def getConeOriginNode(self):
        return self

    def runConeAreaCollisions(self, skillId, ammoSkillId, target, pos):
        self.createCollisions()
        self.areaCollCone.reparentTo(self.getRender())
        self.areaCollCone.setPosHpr(self.getConeOriginNode(), 0, 0, 0, 0, 0, 0)
        range = self.repository.battleMgr.getModifiedAttackRange(self.avatar, skillId, ammoSkillId)
        self.areaCollCone.setScale(range)
        self.areaCollTrav.addCollider(self.areaCollCone, self.areaCollQueue)
        self.areaCollTrav.traverse(self.getRender())
        self.areaCollTrav.removeCollider(self.areaCollCone)
        self.areaCollQueue.sortEntries()
        self.areaCollCone.detachNode()

    def getAreaList(self, skillId, ammoSkillId, target, pos, attackerId):
        targets = []
        areaShape = WeaponGlobals.getAttackAreaShape(skillId, ammoSkillId)
        if areaShape == WeaponGlobals.AREA_SPHERE:
            self.runSphereAreaCollisions(skillId, ammoSkillId, target, pos)
        else:
            if areaShape == WeaponGlobals.AREA_TUBE:
                self.runTubeAreaCollisions(skillId, ammoSkillId, target, pos)
            else:
                if areaShape == WeaponGlobals.AREA_CONE:
                    self.runConeAreaCollisions(skillId, ammoSkillId, target, pos)
                else:
                    if areaShape == WeaponGlobals.AREA_OFF:
                        return targets
        numEntries = self.areaCollQueue.getNumEntries()
        if numEntries == 0:
            return targets
        if numEntries > WeaponGlobals.MAX_AREA_TARGETS:
            numEntries = WeaponGlobals.MAX_AREA_TARGETS
        avTeam = self.avatar.getTeam()
        for i in range(numEntries):
            entry = self.areaCollQueue.getEntry(i)
            potentialTargetColl = entry.getIntoNodePath()
            if potentialTargetColl in self.avatar.aimTubeNodePaths:
                potentialTarget = self.avatar
            else:
                potentialTarget = self.repository.targetMgr.getObjectFromNodepath(potentialTargetColl)
            if potentialTarget:
                potentialTargetId = potentialTarget.getDoId()
                if potentialTargetId == target.getDoId():
                    continue
                if potentialTargetId in targets:
                    continue
                if not TeamUtils.damageAllowed(potentialTarget, self.avatar):
                    if attackerId and potentialTargetId == attackerId:
                        if not WeaponGlobals.isAttackAreaSelfDamaging(skillId, ammoSkillId):
                            continue
                    else:
                        continue
                if potentialTarget.gameFSM.state == 'Death':
                    continue
                if not self.repository.battleMgr.obeysPirateCode(self.avatar, potentialTarget):
                    continue
                targets.append(potentialTargetId)
            else:
                continue

        print 'getting area list of %s' % targets
        return targets
# okay decompiling .\pirates\battle\WeaponBaseBase.pyc
