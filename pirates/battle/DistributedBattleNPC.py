import copy
import random
import types

from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from otp.otpbase import OTPGlobals
from pirates.battle import (DistributedBattleAvatar, EnemyGlobals, EnemySkills, WeaponGlobals)
from pirates.leveleditor import CustomAnims
from pirates.pirate import AvatarTypes, BattleNPCGameFSM, Biped
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.reputation.DistributedReputationAvatar import DistributedReputationAvatar
from pirates.uberdog.UberDogGlobals import *

class DistributedBattleNPC(DistributedBattleAvatar.DistributedBattleAvatar):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleNPC')
    deferrable = True

    def __init__(self, cr):
        NodePath.__init__(self, 'BattleNPC')
        DistributedBattleAvatar.DistributedBattleAvatar.__init__(self, cr)
        self.headTrack = None
        self.setNpc(1)
        self.level = None
        self.cRay = None
        self.cRayNode = None
        self.cRayNodePath = None
        self.cRayBitMask = None
        self.lifter = None
        self.cTrav = None
        self.pusher = None
        self.floorChecksEnabled = False
        self.canCheckFloors = True
        self.cAggro = None
        self.cAggroNode = None
        self.cAggroNodePath = None
        self.handler = None
        self.pendingBoardVehicle = None
        self.spawnIvals = []
        self.headingNode = self.attachNewNode('headingNode')
        self.enableZPrint = False
        self.animProp = None
        self.freezeTask = None
        self.animSet = 'default'
        self.animSetSetup = False
        self.loaded = 0
        self.lastSmoothPosUpdateTime = 0

    def setupStyle(self):
        if self.style:
            if self.animSet != 'default':
                allAnims = copy.copy(CustomAnims.INTERACT_ANIMS.get(self.animSet))
                if allAnims:
                    if allAnims.has_key('props'):
                        del allAnims['props']
                    if self.startState != 'Idle':
                        allAnims['walk'] = [
                         'walk']
                        allAnims['walk_back_diagonal_left'] = ['walk_back_diagonal_left']
                        allAnims['walk_back_diagonal_right'] = ['walk_back_diagonal_right']
                        allAnims['run'] = ['run']
                        allAnims['run_diagonal_left'] = ['run_diagonal_left']
                        allAnims['run_diagonal_right'] = ['run_diagonal_right']
                    self.makeMyAnimDict(self.style.gender, allAnims)
                yieldThread('make Anims')
            self.generateMyself()
            yieldThread('finished Gen')

    def makeMyAnimDict(self, gender, animNames):
        pass

    def generateMyself(self):
        pass

    def setupAnimSet(self):
        if self.animSet != 'default' and self.animSetSetup == False:
            self.animSetSetup = True
            allAnims = CustomAnims.INTERACT_ANIMS.get(self.animSet)
            if allAnims == None:
                return
            allIdles = allAnims.get('idles')
            if type(allIdles) is dict:
                allAnims = allIdles.get(getSkillCategory(self.currentWeaponId))
                allIdles = allAnims.get('idles')
            allProps = allAnims.get('props')
            currChoice = random.choice(allIdles)
            animInfoCopy = copy.copy(Biped.Biped.animInfo)
            self.animInfo = animInfoCopy
            animStateNames = ['LandRoam', 'BayonetLandRoam']
            for currAnimState in animStateNames:
                oldAnimInfo = animInfoCopy.get(currAnimState)
                if oldAnimInfo == None:
                    continue
                newAnimInfo = ((currChoice, oldAnimInfo[0][1]),) + oldAnimInfo[1:]
                if self.motionFSM.motionAnimFSM.state == currAnimState:
                    self.motionFSM.setAnimInfo(newAnimInfo)
                self.animInfo[currAnimState] = newAnimInfo
                yieldThread('custom anim info')

            self.holdAnimProp(allProps)
            self.canCheckFloors = False
            yieldThread('hold anim prop')

    def announceGenerate(self):
        DistributedBattleAvatar.DistributedBattleAvatar.announceGenerate(self)
        if not self.loaded:
            self.setupStyle()
        self.setupAnimSet()
        self.setName(self.name)
        self.setPickable(0)
        if __dev__ and base.config.GetBool('show-aggro-radius', 0):
            if self.isBattleable():
                size = self.getAggroSphereSize()
                sphere = loader.loadModel('models/effects/explosion_sphere')
                sphere.reparentTo(self)
                sphere.setTransparency(1)
                sphere.setAlphaScale(0.3)
                sphere.setScale(render, size)
        if self.shadowPlacer:
            self.shadowPlacer.resetToOrigin()
            self.shadowPlacer.off()

    def freezeShadow(self):
        self.shadowPlacer.off()
        self.freezeTask = None

    def generate(self):
        DistributedBattleAvatar.DistributedBattleAvatar.generate(self)
        self.lastFloorCheckedXYZ = [0, 0, 0]

    def reparentTo(self, parent):
        DistributedBattleAvatar.DistributedBattleAvatar.reparentTo(self, parent)

    def wrtReparentTo(self, parent):
        DistributedBattleAvatar.DistributedBattleAvatar.wrtReparentTo(self, parent)

    def createGameFSM(self):
        self.gameFSM = BattleNPCGameFSM.BattleNPCGameFSM(self)

    def disable(self):
        if self.freezeTask:
            self.freezeTask.remove()
            self.freezeTask = None
        if self.pendingBoardVehicle:
            base.cr.relatedObjectMgr.abortRequest(self.pendingBoardVehicle)
            self.pendingBoardVehicle = None
        self.ignoreAll()
        self.stopLookAt()
        self.disableBodyCollisions()
        for currSpawnIval in self.spawnIvals:
            currSpawnIval.finish()

        self.spawnIvals = []
        DistributedBattleAvatar.DistributedBattleAvatar.disable(self)

    def delete(self):
        DistributedBattleAvatar.DistributedBattleAvatar.delete(self)

    def isDistributed(self):
        return 1

    def requestGameState(self, state, optParam=None):
        self.gameFSM.request(state, optParam)

    def setSpawnPosHpr(self, x, y, z, h, p, r):
        self.setPosHpr(self.getParentObj(), x, y, z, h, p, r)

    def lookAtTarget(self, task=None):
        if self.currentTarget:
            self.headsUp(self.currentTarget)
            return Task.cont
        return Task.done

    def getUpdateLookAtTaskName(self):
        return self.taskName('lookAtTarget')

    def startLookAt(self):
        taskMgr.add(self.lookAtTarget, self.getUpdateLookAtTaskName())

    def stopLookAt(self):
        taskMgr.remove(self.getUpdateLookAtTaskName())

    def setLevel(self, level):
        if self.level is not None:
            return
        self.level = level
        enemyScale = self.getEnemyScale()
        self.height *= enemyScale
        self.setAvatarScale(self.scale * enemyScale)

    def setState(self, stateName, timeStamp):
        self.request(stateName)

    def boardVehicle(self, vehicleDoId):
        if self.pendingBoardVehicle:
            base.cr.relatedObjectMgr.abortRequest(self.pendingBoardVehicle)
            self.pendingBoardVehicle = None
        self.pendingBoardVehicle = base.cr.relatedObjectMgr.requestObjects([vehicleDoId], eachCallback=self.boardExistingVehicle)

    def boardExistingVehicle(self, vehicle):
        self.reparentTo(vehicle.getModel())
        self.pendingBoardVehicle = None

    def initializeBodyCollisions(self, collIdStr):
        pass

    def updateCollisions(self):
        self.cTrav = base.localAvatar.cTrav
        if self.collisionMode & PiratesGlobals.COLL_MODE_FLOORS_CL:
            if self.cRay == None:
                self.cRay = CollisionRay(0.0, 0.0, 4000.0, 0.0, 0.0, -1.0)
                self.cRayNode = CollisionNode(self.taskName('cRay'))
                self.cRayNode.addSolid(self.cRay)
                self.cRayNode.setFromCollideMask(PiratesGlobals.FloorBitmask | PiratesGlobals.ShipFloorBitmask)
                self.cRayNode.setIntoCollideMask(BitMask32.allOff())
                self.cRayNode.setBounds(BoundingSphere())
                self.cRayNode.setFinal(1)
                self.cRayNodePath = self.attachNewNode(self.cRayNode)
                self.lifter = CollisionHandlerGravity()
                self.lifter.setGravity(32.174 * 4.0)
                self.lifter.setReach(self.getFloorRayReach())
                self.lifter.setMaxVelocity(64.0)
                self.lifter.setInPattern('enterFloor%fn')
                self.lifter.setAgainPattern('againFloor%fn')
                hitFloorEvent = self.taskName('enterFloorcRay')
                againFloorEvent = self.taskName('againFloorcRay')
                self.accept(hitFloorEvent, self._hitFloorCallback)
                self.accept(againFloorEvent, self._hitFloorCallback)
        aggroSphereSize = self.getInstantAggroSphereSize()
        if self.cAggro == None and self.isBattleable() and aggroSphereSize > 0:
            self.cAggro = CollisionSphere(0, 0, 0, aggroSphereSize)
            self.cAggro.setTangible(0)
            self.cAggroNode = CollisionNode(self.uniqueName('AggroSphere'))
            self.cAggroNode.setFromCollideMask(BitMask32.allOff())
            self.cAggroNode.setIntoCollideMask(PiratesGlobals.WallBitmask)
            self.cAggroNode.addSolid(self.cAggro)
            self.cAggroNodePath = self.attachNewNode(self.cAggroNode)
            if base.config.GetBool('show-aggro-radius', 0):
                self.cAggroNodePath.show()
            if base.config.GetBool('npcs-auto-target', 1):
                enterCollEvent = self.uniqueName('enter' + 'AggroSphere')
                self.accept(enterCollEvent, self._handleEnterAggroSphere)

    def disableFloorChecks(self):
        if self.floorChecksEnabled and self.lifter:
            self.floorChecksEnabled = False
            self.cTrav.removeCollider(self.cRayNodePath)
            self.lifter.removeCollider(self.cRayNodePath)

    def enableFloorChecks(self):
        if self.floorChecksEnabled == False and self.lifter:
            self.floorChecksEnabled = True
            self.lifter.addCollider(self.cRayNodePath, self)
            self.cTrav.addCollider(self.cRayNodePath, self.lifter)

    def performQuickFloorCheck(self):
        if self.cRayNodePath == None:
            self.notify.debug('aborting quick floor check for %s' % self.name)
            return
        self.notify.debug('performing quick floor check %s' % self.cRayNodePath)
        self.notify.debug('  myPos is %s' % self.getPos())
        cTrav = CollisionTraverser('quickFloorCheck')
        floorRay = CollisionHandlerFloor()
        floorRay.setOffset(OTPGlobals.FloorOffset)
        floorRay.setReach(self.getFloorRayReach())
        floorRay.addCollider(self.cRayNodePath, self)
        cTrav.addCollider(self.cRayNodePath, floorRay)
        cTrav.traverse(render)
        cTrav.removeCollider(self.cRayNodePath)
        floorRay.removeCollider(self.cRayNodePath)
        self.notify.debug('  quick floor check hasContact: %s' % floorRay.hasContact())
        self.notify.debug('  myPos NEW is %s' % self.getPos())
        self.lastFloorCheckedXYZ = [self.getX(), self.getY(), self.getZ()]

    def disableBodyCollisions(self):
        if self.cRayNodePath:
            self.cTrav.removeCollider(self.cRayNodePath)
            self.floorChecksEnabled = False
            self.cRayNodePath.removeNode()
            self.cRayNodePath = None
        if self.cRayNode:
            self.cRayNode = None
        if self.cRay:
            self.cRay = None
        if self.lifter:
            self.lifter = None
        if self.cAggroNodePath:
            self.cTrav.removeCollider(self.cAggroNodePath)
            self.cAggroNodePath.removeNode()
            self.cAggroNodePath = None
        if self.cAggroNode:
            self.cAggroNode = None
        if self.cAggro:
            self.cAggro = None
        if self.handler:
            self.handler = None

    def sendRequestClientAggro(self):
        self.sendUpdate('requestClientAggro', [])

    def _handleEnterAggroSphere(self, collEntry):
        if localAvatar.getSiegeTeam():
            return
        otherCollNode = collEntry.getFromNodePath()
        myCollNode = collEntry.getIntoNodePath()
        if not self.isBattleable():
            return
        skillEffects = self.getSkillEffects()
        if WeaponGlobals.C_SPAWN in skillEffects:
            return
        playerLevel = localAvatar.getLevel()
        if playerLevel <= EnemyGlobals.NEWBIE_AGGRO_LEVEL:
            return
        self.sendRequestClientAggro()

    def _hitFloorCallback(self, collEntry):
        self.floorNorm = collEntry.getInto().getNormal()
        self.disableFloorChecks()

    def canAggro(self):
        if self.aggroMode == EnemyGlobals.AGGRO_MODE_NEVER:
            return False
        return True

    def setupDebugCollisions(self):
        self.debugCSphere = CollisionSphere(0.0, 0.0, 0.0, 5)
        self.debugCSphere.setTangible(0)
        cSphereNode.addSolid(self.debugCSphere)
        self.debugCSphereNodePath = self.attachNewNode(cSphereNode)

    def cleanupDebugcollisions(self):
        if self.debugCSphereNodePath:
            self.debugCSphereNodePath.removeNode()
            del self.debugCSphereNodePath
            self.debugCSphereNodePath = None
        if self.debugCSphere:
            del self.debugCSphere
            self.debugCSphere = None

    def _handleEnterSphereTest(self, collEntry):
        otherCollNode = collEntry.getFromNodePath()
        myCollNode = collEntry.getIntoNodePath()
        print 'NPC colliding me %s other %s' % (str(myCollNode), str(otherCollNode))

    def _handleAgainSphereTest(self, collEntry):
        print 'NPC colliding'

    def _handleExitSphereTest(self, collEntry):
        print 'NPC colliding'

    def updateMyAnimState(self, forwardVel, rotationVel, lateralVel):
        pass

    def smoothPosition(self):
        cantMove = False
        if not self.canMove:
            cantMove = True
        parentObj = render
        if cantMove == False:
            self.headingNode.reparentTo(self)
            self.headingNode.setPos(0, 0, 0)
            self.headingNode.wrtReparentTo(parentObj)
            oldZ = self.getZ(parentObj)
            oldH = self.getH(parentObj)
        DistributedBattleAvatar.DistributedBattleAvatar.smoothPosition(self)
        if cantMove == False:
            newPos = self.getPos(parentObj)
            self.setZ(parentObj, oldZ)
            self.headingNode.setZ(oldZ)
            inAttack = self.curAttackAnim and self.curAttackAnim.isPlaying()
            if inAttack:
                self.setH(parentObj, oldH)
            if self.enableZPrint:
                print '%s:  new z is %s, old z is %s' % (self.doId, newPos[2], oldZ)
            headingNodePos = self.headingNode.getPos()
            xDiff = abs(newPos[0] - headingNodePos[0])
            yDiff = abs(newPos[1] - headingNodePos[1])
            diffChangeLimitF = 0.01
            diffChangeLimitH = 0.075
            if self.gameFSM.state == 'Battle':
                diffChangeLimitH = 2.0
            if xDiff > diffChangeLimitF or yDiff > diffChangeLimitF:
                self.enableFloorChecks()
                if xDiff > diffChangeLimitH or yDiff > diffChangeLimitH and not inAttack:
                    self.headsUp(self.headingNode)
                    self.setH(self.getH() + 180)
            animTime = globalClock.getFrameTime()
            deltaTime = animTime - self.lastSmoothPosUpdateTime
            distMoved = self.headingNode.getDistance(self)
            if deltaTime <= 0:
                speed = 0
            else:
                speed = distMoved / deltaTime
            self.lastSmoothPosUpdateTime = animTime
            slideScale = 0.0
            if base.config.GetBool('npc-sidestep', 0) and distMoved > 0.005:
                moveVec = self.headingNode.getPos() - self.getPos(parentObj)
                self.headingNode.reparentTo(self)
                self.headingNode.setPos(0, 1, 0)
                self.headingNode.wrtReparentTo(parentObj)
                headVec = self.headingNode.getPos() - self.getPos(parentObj)
                moveAngle = headVec.relativeAngleRad(moveVec)
                cosVal = math.sin(moveAngle)
                slideScale = cosVal
            self.headingNode.reparentTo(hidden)
            if inAttack:
                hChange = 0.0
            else:
                hChange = self.getH(parentObj) - oldH
                if hChange and hChange < 0.1 and hChange > -0.1:
                    hChange = 0.0
            self.motionFSM.motionAnimFSM.updateNPCAnimState(speed, hChange, slideScale)
        if self.canCheckFloors == True and self.floorChecksEnabled == False and (self.getX() != self.lastFloorCheckedXYZ[0] or self.getY() != self.lastFloorCheckedXYZ[1] or self.getZ() != self.lastFloorCheckedXYZ[2]):
            self.performQuickFloorCheck()
        self.trackTerrain()

    def setSpawnIn(self, timestamp):
        t = globalClockDelta.localElapsedTime(timestamp, bits=32)
        if t < 10:
            ival = self.getSpawnTrack()
            if ival:
                ival.start()
                self.spawnIvals.append(ival)
            else:
                ival = self.getFadeInTrack()
                if ival:
                    ival.start()
                    self.spawnIvals.append(ival)
        else:
            ival = self.getFadeInTrack()
            if ival:
                ival.start()
                self.spawnIvals.append(ival)

    def startLookAroundTask(self):
        pass

    def stopLookAroundTask(self):
        pass

    def b_setChat(self, chatString, chatFlags):
        messenger.send('wakeup')
        self.setChatAbsolute(chatString, chatFlags)
        self.d_setChat(chatString, chatFlags)

    def d_setChat(self, chatString, chatFlags):
        self.sendUpdate('setChat', [chatString, chatFlags])

    def setChat(self, chatString, chatFlags):
        chatFlags &= ~(CFQuicktalker | CFPageButton | CFQuitButton)
        if chatFlags & CFThought:
            chatFlags &= ~(CFSpeech | CFTimeout)
        else:
            chatFlags |= CFSpeech | CFTimeout
        self.setChatAbsolute(chatString, chatFlags)

    def getAggroRadius(self):
        if base.cr.activeWorld:
            return base.cr.activeWorld.getAggroRadius()
        return 0

    def getAggroSphereSize(self):
        if not self.canAggro():
            return 0
        playerLevel = base.localAvatar.getLevel()
        enemyLevel = self.getLevel()
        levelDiff = max(1, abs(playerLevel - enemyLevel) - EnemyGlobals.AGGRO_RADIUS_LEVEL_BUFFER)
        searchDist = self.getAggroRadius() / max(1.0, levelDiff / EnemyGlobals.AGGRO_RADIUS_FALLOFF_RATE)
        return max(searchDist, EnemyGlobals.MIN_SEARCH_RADIUS)

    def getInstantAggroSphereSize(self):
        return self.aggroRadius

    def swapFloorCollideMask(self, oldMask, newMask):
        if self.cRayNode:
            collideMask = self.cRayNode.getFromCollideMask()
            collideMask = collideMask & ~oldMask
            collideMask |= newMask
            self.cRayNode.setFromCollideMask(collideMask)

    def holdAnimProp(self, availProps):
        if self.isWeaponDrawn:
            return
        if availProps == None or len(availProps) == 0:
            return
        self.clearAnimProp()
        propPath = random.choice(availProps)
        propType = CustomAnims.PROP_TYPE_DYNAMIC
        if type(propPath) is types.ListType:
            propType = propPath[1]
            propPath = propPath[0]
        if propType == CustomAnims.PROP_TYPE_PERSIST:
            return
        if 'gator_high' in propPath:
            prop = None
        else:
            prop = loader.loadModel(propPath)
        if prop and not prop.isEmpty():
            if self.getName() == 'Captain Barbossa':
                handNode = self.leftHandNode
            else:
                handNode = self.rightHandNode
            if handNode == None:
                self.notify.warning('could not find hand to place prop %s in' % propPath)
                return
            motion_blur = prop.find('**/motion_blur')
            if not motion_blur.isEmpty():
                motion_blur.stash()
            prop.flattenStrong()
            prop.reparentTo(handNode)
            self.animProp = prop
            self.animPropType = propType
        else:
            self.notify.warning('could not load prop %s to be used with DistInteractiveProp' % propPath)
        
    def clearAnimProp(self):
        if self.animProp:
            self.animProp.removeNode()
            self.animProp = None

    def setAggroMode(self, val):
        DistributedBattleAvatar.DistributedBattleAvatar.setAggroMode(self, val)
        if self.aggroMode == EnemyGlobals.AGGRO_MODE_DEFAULT or self.aggroMode == EnemyGlobals.AGGRO_MODE_CUSTOM:
            if self.cAggroNodePath:
                if self.cAggroNodePath.isStashed():
                    self.cAggroNodePath.unstash()
        else:
            if self.cAggroNodePath:
                self.cAggroNodePath.stash()

    def motionFSMEnterState(self, state):
        if state == 'Idle':
            if self.animSet != 'default':
                allAnims = CustomAnims.INTERACT_ANIMS.get(self.animSet)
                if allAnims:
                    allProps = allAnims.get('props')
                    self.holdAnimProp(allProps)

    def motionFSMExitState(self, state):
        if state == 'Idle':
            self.clearAnimProp()

    def setAnimSet(self, animSet):
        self.animSet = animSet
        if self.isGenerated():
            self.setupAnimSet()

    def setCollisionMode(self, collisionMode):
        self.collisionMode = collisionMode
        self.updateCollisions()

    def setInitZ(self, z):
        self.initZ = z
        self.setZ(z)

    def playSkillMovie(self, skillId, ammoSkillId, skillResult, charge, targetId=0):
        if self.currentTarget:
            self.headsUp(self.currentTarget)
        if targetId == 0 and self.currentTarget:
            targetId = self.currentTarget.doId
        DistributedBattleAvatar.DistributedBattleAvatar.playSkillMovie(self, skillId, ammoSkillId, skillResult, charge, targetId)

    def preprocessAttackAnim(self):
        if self.currentAttack[0] >= InventoryType.begin_WeaponSkillGrenade and self.currentAttack[0] < InventoryType.end_WeaponSkillGrenade:
            skillInfo = WeaponGlobals.getSkillAnimInfo(EnemySkills.EnemySkills.GRENADE_RELOAD)
            if not skillInfo:
                return
            anim = skillInfo[WeaponGlobals.PLAYABLE_INDEX]
            reloadAnim = getattr(self.cr.combatAnims, anim)(self, EnemySkills.EnemySkills.GRENADE_RELOAD, 0, 0, None)
            self.curAttackAnim = Sequence(self.curAttackAnim, reloadAnim)

    def checkWeaponSwitch(self, currentWeaponId, isWeaponDrawn):
        if isWeaponDrawn == self.isWeaponDrawn and currentWeaponId == self.currentWeaponId:
            self.setWalkForWeapon()
        DistributedBattleAvatar.DistributedBattleAvatar.checkWeaponSwitch(self, currentWeaponId, isWeaponDrawn)

    def getFloorRayReach(self):
        if self.ship:
            return 1000.0
        return 8.0

    def setShipId(self, shipId):
        DistributedBattleAvatar.DistributedBattleAvatar.setShipId(self, shipId)
        if self.lifter:
            self.lifter.setReach(self.getFloorRayReach())
