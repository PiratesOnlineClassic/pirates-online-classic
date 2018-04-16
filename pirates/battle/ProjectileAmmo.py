from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from pandac.PandaModules import *
from pirates.effects.ProjectileEffect import ProjectileEffect
from pirates.piratesbase import PiratesGlobals


class ProjectileAmmo(DirectObject, NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory('ProjectileAmmo')

    def __init__(self, cr, ammoSkillId, event, weaponControlled=False):
        NodePath.__init__(self, 'projectileAmmo')
        self.cr = cr
        self.ammoSkillId = ammoSkillId
        self.projectileHitEvent = event
        self.ival = None
        model = self.loadModel()
        model.reparentTo(self)
        self.collHandler = None
        self.collNode = None
        self.destroyed = False
        self.weaponControlled = weaponControlled
        if not weaponControlled:
            self.accept(self.projectileHitEvent, self.projectileHitObject)
        self.setPythonTag('ammo', self)
        self.accept(base.cr.StopVisibilityEvent, self.destroy)
        return

    def removeNode(self):
        NodePath.removeNode(self)

    def destroy(self):
        if self.destroyed:
            return
        self.setPythonTag('ammo', 0)
        self.collHandler = None
        self.pauseIval(remove=True)
        self.ignore(self.projectileHitEvent)
        if base.cTrav:
            base.cTrav.removeCollider(self.getCollNode())
        self.removeNode()
        if self.collNode:
            self.collNode.detachNode()
        self.collNode = None
        self.cr = None
        self.destroyed = True
        return

    def setTag(self, key, value):
        NodePath.setTag(self, key, value)
        collNode = self.getCollNode()
        collNode.setTag(key, value)

    def setPythonTag(self, key, value):
        NodePath.setPythonTag(self, key, value)
        collNode = self.getCollNode()
        collNode.setPythonTag(key, value)

    def getModel(self):
        pass

    def getCollNode(self, team=None):
        if self.collNode == None:
            node = CollisionNode('projectileCollNode')
            node.setFromCollideMask(PiratesGlobals.TargetBitmask)
            node.setIntoCollideMask(BitMask32.allOff())
            self.collNode = NodePath(node)
            self.collHandler = CollisionHandlerEvent()
            self.collHandler.addInPattern(self.projectileHitEvent)
        return self.collNode

    def projectileHitObject(self, entry=None):
        if base.cr.wantSpecialEffects == 0:
            return
        if not entry.hasSurfacePoint() or not entry.hasInto():
            self.notify.warning('no surface point or into or from entry')
            return
        if not entry.getInto().isTangible():
            return
        fromNodePath = entry.getFromNodePath()
        sequence = int(fromNodePath.getNetTag('ammoSequence'))
        if int(self.getTag('ammoSequence')) != sequence:
            return
        hitObject = entry.getIntoNodePath()
        objType = hitObject.getNetTag('objType')
        if not objType:
            return
        objType = int(objType)
        if objType == PiratesGlobals.COLL_FORT:
            if fromNodePath.getNetTag('fortId') == hitObject.getNetTag('fortId'):
                return
        if fromNodePath.getNetTag('shipId') and fromNodePath.getNetTag('shipId') == hitObject.getNetTag('shipId'):
            return
        skillId = int(fromNodePath.getNetTag('skillId'))
        ammoSkillId = int(fromNodePath.getNetTag('ammoSkillId'))
        cannonPass = hitObject.getNetTag('cannonPass')
        pos = entry.getSurfacePoint(hitObject)
        normal = entry.getSurfaceNormal(hitObject)
        pos += normal * 2
        attackerId = 0
        attacker = None
        attackerStr = fromNodePath.getNetTag('attackerId')
        if attackerStr:
            attackerId = int(attackerStr)
        if cannonPass != '1':
            ProjectileEffect(self.cr, attackerId, hitObject, objType, pos, skillId, ammoSkillId, normal)
            self.destroy()
        return

    def setIval(self, ival, start=False, offset=0):
        if self.ival:
            self.ival.finish()
        self.ival = ival
        if start:
            self.startIval(offset)

    def getIval(self):
        return self.ival

    def startIval(self, offset=0):
        if self.ival:
            self.ival.start(offset)

    def finishIval(self, remove=False):
        if self.ival:
            self.ival.finish()
            if remove:
                self.ival = None
        return

    def pauseIval(self, remove=False):
        if self.ival:
            self.ival.pause()
            if remove:
                self.ival = None
        return
