from direct.directtools.DirectSelection import *
from direct.distributed import DistributedObject
from direct.task import Task
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TeamUtils
from pirates.battle import WeaponGlobals
from pirates.battle import Sword
from pirates.battle import Wand
from pirates.battle import Doll
from pirates.battle import Grenade
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.pirate import AvatarTypes
from . import TargetManagerBase

class TargetManager(DistributedObject.DistributedObject, TargetManagerBase.TargetManagerBase):
    notify = directNotify.newCategory('TargetManager')
    neverDisable = 1
    WeaponsWithoutReticles = (0, InventoryType.CutlassWeaponL1, InventoryType.CutlassWeaponL2, InventoryType.CutlassWeaponL3, InventoryType.CutlassWeaponL4, InventoryType.CutlassWeaponL5, InventoryType.CutlassWeaponL6, InventoryType.DollWeaponL1, InventoryType.DollWeaponL2, InventoryType.DollWeaponL3, InventoryType.DollWeaponL4, InventoryType.DollWeaponL5, InventoryType.DollWeaponL6, InventoryType.GrenadeWeaponL1, InventoryType.GrenadeWeaponL2, InventoryType.GrenadeWeaponL3, InventoryType.GrenadeWeaponL4, InventoryType.GrenadeWeaponL5, InventoryType.GrenadeWeaponL6, InventoryType.MeleeWeaponL1, InventoryType.MeleeWeaponL2, InventoryType.MeleeWeaponL3, InventoryType.MeleeWeaponL4, InventoryType.MeleeWeaponL5, InventoryType.MeleeWeaponL6)
    WeaponBaseRange = {
        InventoryType.CutlassRep: 6,
        InventoryType.PistolRep: 70,
        InventoryType.DaggerRep: 50,
        InventoryType.GrenadeRep: 20,
        InventoryType.WandRep: 0,
        InventoryType.DollRep: 6}
    RETICLE_POS = Vec3(0, 0, 0.15)
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        TargetManagerBase.TargetManagerBase.__init__(self)
        self.iRay = SelectionRay(base.cam)
        self.setTargetNodePath(render)
        self.wantAimAssist = True
        self.distanceChecker = NodePath('distanceChecker')
        aimRay = CollisionSegment(0.0, 0.0, 0.0, 0.0, WeaponGlobals.MaxAimDistance, 0.0)
        aimRayNode = CollisionNode('TargetManager.aimRayNode')
        aimRayNode.addSolid(aimRay)
        bitmask = PiratesGlobals.BattleAimBitmask | PiratesGlobals.BattleAimOccludeBitmask
        aimRayNode.setFromCollideMask(bitmask)
        aimRayNode.setIntoCollideMask(BitMask32.allOff())
        self.aimRayNodePath = NodePath(aimRayNode)
        self.aimRayNodePath.reparentTo(camera)
        self.aimQueue = CollisionHandlerQueue()
        self.aimTrav = CollisionTraverser('TargetManager.aimTrav')
        self.aimTrav.addCollider(self.aimRayNodePath, self.aimQueue)
        self.reticleScale = 0.18
        self.reticleAlpha = 0.5
        self.reticle = loader.loadModel('models/effects/selectionCursor')
        self.reticle.setScale(self.reticleScale)
        self.reticle.setColorScale(1, 1, 1, self.reticleAlpha)
        self.cr.targetMgr = self
        messenger.send('targetMgrCreated')

    def delete(self):
        if self.cr.targetMgr == self:
            self.cr.targetMgr = None
        
        self.stopFollowMouse()
        self.stopFollowAim()
        self.aimRayNodePath.removeNode()
        self.reticle.removeNode()
        self.distanceChecker.removeNode()
        self.distanceChecker = None
        self.aimQueue = None
        self.aimTrav = None
        self.iRay = None
        DistributedObject.DistributedObject.delete(self)
        TargetManagerBase.TargetManagerBase.delete(self)

    def removeTarget(self, nodePathId):
        if not localAvatar.isDisabled():
            target = self.objectDict.get(nodePathId)
            if target:
                if localAvatar.currentMouseOver == target:
                    localAvatar.currentMouseOver = None
                
                if localAvatar.currentAimOver == target:
                    localAvatar.currentAimOver = None
                    self.reticle.setColorScale(1, 1, 1, self.reticleAlpha)
                    messenger.send(target.uniqueName('aimOver'), [0])
                    target.hideHpMeter(delay = 1.0)
                    target.hideEnemyTargetInfo()
                
                if localAvatar.currentSelection == target:
                    localAvatar.currentSelection = None
        
        TargetManagerBase.TargetManagerBase.removeTarget(self, nodePathId)

    def takeAim(self, av, skillId=None, ammoSkillId=None):
        if not self.aimTrav:
            return
        self.aimTrav.traverse(render)
        numEntries = self.aimQueue.getNumEntries()
        if numEntries == 0:
            return None
        self.aimQueue.sortEntries()
        avTeam = av.getTeam()
        currentWeaponId, isWeaponDrawn = av.getCurrentWeapon()
        friendlyWeapon = WeaponGlobals.isFriendlyFireWeapon(currentWeaponId)
        if skillId:
            friendlySkill = WeaponGlobals.isFriendlyFire(skillId, ammoSkillId)
        for i in range(numEntries):
            entry = self.aimQueue.getEntry(i)
            targetColl = entry.getIntoNodePath()
            if targetColl.node().getIntoCollideMask() == PiratesGlobals.BattleAimOccludeBitmask:
                break
            target = self.getObjectFromNodepath(targetColl)
            if target:
                targetTeam = target.getTeam()
                if target.gameFSM.state == 'Death':
                    continue
                if target.getY(av) < 0:
                    continue
                if not TeamUtils.damageAllowed(target, localAvatar):
                    if not friendlyWeapon:
                        continue
                    if skillId and not friendlySkill:
                        continue
                if not self.cr.battleMgr.obeysPirateCode(av, target):
                    localAvatar.guiMgr.showPirateCode()
                    continue
                return target
            else:
                continue

        return None

    def getAimHitPos(self, av):
        if not self.aimTrav:
            return
        self.aimTrav.traverse(render)
        numEntries = self.aimQueue.getNumEntries()
        if numEntries == 0:
            return None
        self.aimQueue.sortEntries()
        avTeam = av.getTeam()
        for i in range(numEntries):
            entry = self.aimQueue.getEntry(i)
            targetColl = entry.getIntoNodePath()
            if targetColl.node().getIntoCollideMask().hasBitsInCommon(PiratesGlobals.BattleAimOccludeBitmask):
                break
            target = self.getObjectFromNodepath(targetColl)
            if target:
                targetTeam = target.getTeam()
                if not TeamUtils.damageAllowed(target, localAvatar):
                    continue
                elif target.gameFSM.state == 'Death':
                    continue
                elif target.getY(av) < 0:
                    continue
                pos = entry.getSurfacePoint(target)
                return pos
            else:
                continue

        return None

    def setTargetNodePath(self, nodePath):
        self.targetNodePath = nodePath
    
    def isTargetableObject(self, nodePath):
        return nodePath.hasNetTag('targetableObject')

    def findTargetableObject(self, nodePath):
        np = nodePath.findNetTag('targetableObject')
        if np.isEmpty():
            return None
        else:
            return self.objectDict.get(np.get_key(), None)
    
    def pickObject(self):
        entry = self.iRay.pickBitMask(bitMask = PiratesGlobals.BattleAimBitmask, targetNodePath = self.targetNodePath, skipFlags = SKIP_CAMERA)
        while entry:
            nodePath = entry.getIntoNodePath()
            obj = self.getObjectFromNodepath(nodePath)
            if obj:
                return obj
            
            entry = self.iRay.findNextCollisionEntry(skipFlags = SKIP_CAMERA)

        return None

    def startFollowMouse(self, av):
        taskMgr.add(self.mouseOverTargetTask, 'mouseOverTarget', extraArgs = [av])
    
    def mouseOverTargetTask(self, av):
        target = self.pickObject()
        oldTarget = av.currentMouseOver
        if target == oldTarget:
            return Task.cont
        
        if oldTarget != None:
            messenger.send(oldTarget.uniqueName('mouseOver'), [0])
            av.currentMouseOver = None
        
        if target != None:
            messenger.send(target.uniqueName('mouseOver'), [1])
            av.currentMouseOver = target
            return Task.cont
        elif target == None:
            av.currentMouseOver = None
        
        return Task.cont

    def stopFollowMouse(self):
        taskMgr.remove('mouseOverTarget')
        localAvatar.currentMouseOver = None
    
    def startFollowAim(self):
        self.reticle.setPos(self.RETICLE_POS)
        self.reticle.setScale(self.reticleScale)
        if localAvatar.currentWeaponId not in self.WeaponsWithoutReticles:
            self.reticle.reparentTo(aspect2d)
            self.reticle.setColorScale(1, 1, 1, self.reticleAlpha)
            self.reticle.show()
        
        base.localAvatar.currentAimOver = None
        self.aimRayNodePath.setPos(0, 0, 1)
        taskMgr.remove('aimOverTarget')
        taskMgr.add(self.aimOverTargetTask, 'aimOverTarget', priority = 41)

    def aimOverTargetTask(self, task):
        if base.localAvatar.hasStickyTargets():
            if isinstance(base.localAvatar.currentWeapon, Doll.Doll):
                target = base.localAvatar.currentTarget
                if target:
                    pt = self.getNearProjectionPoint(target)
                    (pt, distance) = self.getTargetScreenXY(target)
                    self.reticle.setPos(pt)
                    self.reticle.setScale(self.reticleScale / distance)
                else:
                    self.reticle.setPos(self.RETICLE_POS)
                    self.reticle.setScale(self.reticleScale)
            
            return Task.cont
        
        target = self.takeAim(base.localAvatar)
        dt = globalClock.getDt()
        dt = min(1.0, 8 * dt)
        if self.wantAimAssist and target:
            pt = self.getNearProjectionPoint(target)
            (pt, distance) = self.getTargetScreenXY(target)
            rPos = self.reticle.getPos()
            if not rPos.almostEqual(pt, 0.001):
                nPos = Vec3(rPos)
                nPos += (pt - rPos) * dt
                self.reticle.setPos(nPos)
            
            rScale = self.reticle.getScale()
            if not rScale.almostEqual(Vec3(self.reticleScale), 0.001):
                nScale = Vec3(rScale)
                f = self.reticleScale / distance
                nScale += (Vec3(f, f, f) - rScale) * dt
                nScale.setX(max(self.reticleScale / 1.25, nScale[0]))
                nScale.setY(max(self.reticleScale / 1.25, nScale[1]))
                nScale.setZ(max(self.reticleScale / 1.25, nScale[2]))
                self.reticle.setScale(nScale)
            
        else:
            rPos = self.reticle.getPos()
            if not rPos.almostEqual(self.RETICLE_POS, 0.001):
                nPos = Vec3(rPos)
                nPos += (self.RETICLE_POS - rPos) * dt
                self.reticle.setPos(nPos)
                self.reticle.setScale(self.reticleScale)
            
        if target:
            if TeamUtils.damageAllowed(target, localAvatar):
                self.reticle.setColorScale(1, 1, 1, self.reticleAlpha)
                if base.localAvatar.currentWeapon:
                    repId = WeaponGlobals.getRepId(base.localAvatar.currentWeaponId)
                    baseRange = self.WeaponBaseRange.get(repId)
                    calcRange = 0
                    blastRange = 0
                    ammoSkillId = localAvatar.guiMgr.combatTray.ammoSkillId
                    if repId == InventoryType.PistolRep:
                        if localAvatar.guiMgr.combatTray.isCharging:
                            calcRange = base.cr.battleMgr.getModifiedAttackRange(localAvatar, InventoryType.PistolTakeAim, ammoSkillId)
                        else:
                            calcRange = base.cr.battleMgr.getModifiedAttackRange(localAvatar, InventoryType.PistolShoot, ammoSkillId)
                    elif repId == InventoryType.DaggerRep:
                        calcRange = base.cr.battleMgr.getModifiedAttackRange(localAvatar, InventoryType.DaggerAsp, 0)
                    elif repId == InventoryType.WandRep:
                        if ammoSkillId:
                            calcRange = base.cr.battleMgr.getModifiedAttackRange(localAvatar, ammoSkillId, 0)
                        
                        blastRange = base.cr.battleMgr.getModifiedAttackRange(localAvatar, InventoryType.StaffBlast, 0)
                    
                    distance = base.localAvatar.getDistance(target)
                    if hasattr(target, 'battleTubeNodePaths'):
                        for tube in target.battleTubeNodePaths:
                            tubeLength = max(target.battleTubeRadius, target.battleTubeHeight)
                            if distance - tubeLength < distance:
                                distance -= tubeLength

                    range = max(baseRange, calcRange)
                    secondaryRange = max(baseRange, blastRange)
                    tolerance = 0
                    if distance <= secondaryRange + tolerance:
                        self.reticle.setColorScale(1, 0.7, 0, self.reticleAlpha)
                    
                    if distance <= range + tolerance:
                        self.reticle.setColorScale(1, 0, 0, self.reticleAlpha)

            else:
                self.reticle.setColorScale(0, 0, 1, self.reticleAlpha)
        else:
            self.reticle.setColorScale(1, 1, 1, self.reticleAlpha)
        oldTarget = base.localAvatar.currentAimOver
        if target == oldTarget:
            return Task.cont
        
        if oldTarget != None:
            messenger.send(oldTarget.uniqueName('aimOver'), [0])
            base.localAvatar.currentAimOver = None
            oldTarget.hideEnemyTargetInfo()
        
        if oldTarget != None and not target:
            oldTarget.hideHpMeter(delay = 8.0)
        
        if target:
            target.showHpMeter()
            if TeamUtils.damageAllowed(target, localAvatar):
                target.showEnemyTargetInfo()
                messenger.send('pistolAimedTarget')
            else:
                target.showFriendlyTargetInfo()
            messenger.send(target.uniqueName('aimOver'), [1])
            base.localAvatar.currentAimOver = target
        else:
            base.localAvatar.currentAimOver = None
        return Task.cont

    def stopFollowAim(self):
        self.reticle.detachNode()
        self.reticle.hide()
        taskMgr.remove('aimOverTarget')
        if localAvatar.currentAimOver:
            if TeamUtils.damageAllowed(localAvatar.currentAimOver, localAvatar):
                localAvatar.currentAimOver.hideEnemyTargetInfo()
            else:
                localAvatar.currentAimOver.hideFriendlyTargetInfo()
            localAvatar.currentAimOver.hideHpMeter(delay = 1.0)
        
        localAvatar.currentAimOver = None

    def getNearProjectionPoint(self, target):
        origin = target.getPos(camera)
        if origin[1] != 0.0:
            return origin * (base.camLens.getNear() / origin[1])
        else:
            return Point3(0, base.camLens.getNear(), 0)
    
    def getTargetScreenXY(self, target):
        tNodePath = target.attachNewNode('temp')
        distance = camera.getDistance(target)
        tNodePath.setPos(target, 0, 0, target.getHeight() * 0.66)
        nearVec = self.getNearProjectionPoint(tNodePath)
        nearVec *= base.camLens.getFocalLength() / base.camLens.getNear()
        render2dX = CLAMP(nearVec[0] / (base.camLens.getFilmSize()[0] / 2.0), -.9, 0.9)
        aspect2dX = render2dX * base.getAspectRatio()
        aspect2dZ = CLAMP(nearVec[2] / (base.camLens.getFilmSize()[1] / 2.0), -.8, 0.9)
        tNodePath.removeNode()
        return (Vec3(aspect2dX, 0, aspect2dZ), distance)

    def setWantAimAssist(self, val):
        self.wantAimAssist = True


