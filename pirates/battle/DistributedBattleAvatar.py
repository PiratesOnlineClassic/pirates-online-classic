import math
import random

from direct.actor import Actor
from direct.controls import BattleWalker
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed import DistributedSmoothNode
from direct.distributed.ClockDelta import *
from direct.fsm import FSM
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.showbase.PythonUtil import clampScalar, lerp, report
from direct.showutil import Rope
from direct.task import Task
from otp.otpbase import OTPGlobals, OTPRender
from panda3d.core import *
from pirates.battle import BattleRandom, EnemyGlobals, Pistol, WeaponGlobals
from pirates.battle.Teamable import Teamable
from pirates.battle.WeaponBase import WeaponBase
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.effects import PolyTrail, TextEffect
from pirates.effects.AttuneEffect import AttuneEffect
from pirates.effects.AttuneSmoke import AttuneSmoke
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.CannonExplosion import CannonExplosion
from pirates.effects.CannonSplash import CannonSplash
from pirates.effects.DirtClod import DirtClod
from pirates.effects.DustCloud import DustCloud
from pirates.effects.DustRing import DustRing
from pirates.effects.ExplosionCloud import ExplosionCloud
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.Fire import Fire
from pirates.effects.FireTrail import FireTrail
from pirates.effects.Flame import Flame
from pirates.effects.GraveShackles import GraveShackles
from pirates.effects.GreenBlood import GreenBlood
from pirates.effects.GroundDirt import GroundDirt
from pirates.effects.HitFlashA import HitFlashA
from pirates.effects.JRSpawnEffect import JRSpawnEffect
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.effects.PoisonEffect import PoisonEffect
from pirates.effects.RockShower import RockShower
from pirates.effects.ShipDebris import ShipDebris
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.effects.SlowEffect import SlowEffect
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.SmokeWisps import SmokeWisps
from pirates.effects.SpectralSmoke import SpectralSmoke
from pirates.effects.StunEffect import StunEffect
from pirates.effects.VoodooAura import VoodooAura
from pirates.effects.WoodShards import WoodShards
from pirates.movement import MotionFSM
from pirates.pirate import AvatarTypes, Human
from pirates.piratesbase import (Freebooter, PiratesGlobals, PLocalizer,
                                 TeamUtils)
from pirates.piratesgui.CrewBuffDisplay import CrewBuffDisplay
from pirates.reputation import ReputationGlobals
from pirates.reputation.DistributedReputationAvatar import \
    DistributedReputationAvatar
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedBattleAvatar(DistributedReputationAvatar, WeaponBase, Teamable):
    DiskUseColor = (1, 0, 0, 1)
    DiskWaitingColor = (1, 0, 0, 1)
    notify = directNotify.newCategory('DistributedBattleAvatar')
    PlayersInvulnerable = base.config.GetBool('players-invulnerable', False)
    ShowUnderstandable = base.config.GetBool('show-understandable', False)

    def __init__(self, cr):
        DistributedReputationAvatar.__init__(self, cr)
        WeaponBase.__init__(self)
        Teamable.__init__(self)
        self.level = 0
        self.money = 0
        self.bossIcon = None
        self.bankMoney = 0
        self.maxMoney = 0
        self.maxBankMoney = 0
        self.weight = None
        self.battleIval = None
        self.skillIval = None
        self.setWeaponIval = None
        self.skillEffects = {}
        self.durationTask = None
        self.ensnaredTargetId = 0
        self.attuneEffect = None
        self.shacklesEffect = None
        self.smokeWispEffect = None
        self.gunSmokeEffect = None
        self.poisonEffect = None
        self.slowEffect = None
        self.slowEffect2 = None
        self.stunEffect = None
        self.stunEffect2 = None
        self.compassFX = None
        self.fireEffect = None
        self.voodooAttuneEffect = None
        self.voodooSmokeEffect = None
        self.voodooAttuneSound = None
        self.chatIcon = None
        self.crewBuffDisplay = None
        self.battleTubeNodePaths = []
        self.aimTubeNodePaths = []
        self.height = 5.0
        self.battleTubeRadius = 2.0
        self.battleTubeHeight = 2.0
        self.battleCollisionBitmask = PiratesGlobals.WallBitmask | PiratesGlobals.TargetBitmask | PiratesGlobals.RadarAvatarBitmask
        self.battleTube = None
        self.consumable = None
        self.enemyId = None
        self.currentWeaponId = 0
        self.isWeaponDrawn = 0
        self.currentAmmo = 0
        self.currentTarget = None
        self.hp = 0
        self.maxHp = 0
        self.power = 0
        self.maxPower = 0
        self.luck = 0
        self.maxLuck = 0
        self.mojo = 0
        self.maxMojo = 0
        self.swiftness = 0
        self.maxSwiftness = 0
        self.powerMod = 0
        self.luckMod = 0
        self.mojoMod = 0
        self.swiftnessMod = 0.0
        self.stunMod = 0.0
        self.hasteMod = 0.0
        self.combo = 0
        self.comboDamage = 0
        self.lastComboTime = 0
        self.blinded = 0
        self.currentAttack = []
        self.ship = 0
        self.pendingSetShip = None
        self.cannon = None
        self.setNpc(0)
        self.nametagScale = 1.0
        self.setNametagScale(self.nametagScale)
        self.hpTextNodes = []
        self.hpTextIvals = []
        self.textEffects = []
        self.ouchAnim = None
        self.curAttackAnim = None
        self.rope = None
        self.ropeEndNode = None
        self.ropeActor = None
        self.ambientSfx = None
        self.ambientFx = 0
        self.bobbing = False
        self.aimMod = 0
        self.floorNorm = Vec3(0, 0, 1)
        self.tracksTerrain = None
        self.gNodeFwdPt = None

    def generate(self):
        DistributedReputationAvatar.generate(self)
        WeaponBase.generate(self)
        self.lookAroundTaskName = self.taskName('lookAround')
        self.createGameFSM()
        self.motionFSM = MotionFSM.MotionFSM(self)
        self.battleRandom = BattleRandom.BattleRandom(self.doId)
        self.accept('trackBackstab-%d' % self.doId, self.newBackstab)

    def announceGenerate(self):
        yieldThread('battle av start')
        DistributedReputationAvatar.announceGenerate(self)
        yieldThread('rep av gen')
        WeaponBase.announceGenerate(self)
        yieldThread('wb/start battle gen')
        self.initializeBattleCollisions()
        yieldThread('batttle collisions')
        if not self.isLocal() and self.canMove:
            self.showDebugName()
            self.startSmooth()

        yieldThread('smoothing')
        self.setCurrentWeapon(self.currentWeaponId, self.isWeaponDrawn)
        yieldThread('current weapon')
        self.setHeight(self.height)
        yieldThread('set Height')
        if self.ambientSfx:
            self.ambientFx = SoundInterval(self.ambientSfx, node=self)
            self.ambientFx.loop()
            yieldThread('sound')

    def disable(self):
        self.ignoreAll()
        self.detachNode()
        self.stopSmooth()
        taskMgr.remove(self.taskName('usingSkill'))
        taskMgr.removeTasksMatching(self.taskName('playMotionAnim*'))
        taskMgr.remove(self.taskName('playHitSoundTask'))
        taskMgr.remove(self.taskName('playOuchTask'))
        taskMgr.remove(self.taskName('playBonusOuchTask'))
        taskMgr.remove(self.taskName('showMissTask'))
        taskMgr.remove(self.taskName('endBlind'))
        taskMgr.remove(self.taskName('printExp'))
        taskMgr.remove(self.taskName('playMpDamage'))
        if not self.isLocal():
            self.deleteBattleCollisions()
        if hasattr(self, 'stopLookAroundTask'):
            self.stopLookAroundTask()
        self.stopBobSwimTask()
        self.ship = 0
        if self.pendingSetShip:
            self.cr.relatedObjectMgr.abortRequest(self.pendingSetShip)
            self.pendingSetShip = None
        if self.fireEffect:
            self.fireEffect.stopLoop()
            self.fireEffect = None
        if self.shacklesEffect:
            self.shacklesEffect.stopLoop()
            self.shacklesEffect = None
        if self.poisonEffect:
            self.poisonEffect.stopLoop()
            self.poisonEffect = None
        if self.voodooAttuneEffect:
            self.voodooAttuneEffect.stopLoop()
            self.voodooAttuneEffect = None
        if self.voodooSmokeEffect:
            self.voodooSmokeEffect.stopLoop()
            self.voodooSmokeEffect = None
        if self.slowEffect:
            self.slowEffect.stopLoop()
            self.slowEffect = None
        if self.slowEffect2:
            self.slowEffect2.stopLoop()
            self.slowEffect2 = None
        if self.smokeWispEffect:
            self.smokeWispEffect.stopLoop()
            self.smokeWispEffect = None
        if self.stunEffect:
            self.stunEffect.stopLoop()
            self.stunEffect = None
        if self.stunEffect2:
            self.stunEffect2.stopLoop()
            self.stunEffect2 = None
        if self.crewBuffDisplay:
            self.crewBuffDisplay.stop()
            self.crewBuffDisplay.destroy()
            self.crewBuffDisplay = None
        if self.isLocal():
            self.guiMgr.hideDirtPanel()
            self.guiMgr.hideSmokePanel()
        if self.ouchAnim:
            self.ouchAnim.finish()
            self.ouchAnim = None
        if self.curAttackAnim:
            self.curAttackAnim.pause()
            self.curAttackAnim = None
        self.stopCompassEffect()
        taskMgr.remove(self.taskName('sendSwitchMsgTask'))
        taskMgr.remove(self.taskName('pullOutWeaponTask'))
        for ival in self.hpTextIvals:
            if ival:
                ival.pause()

        self.hpTextIvals = []
        for hpText in self.hpTextNodes:
            if hpText:
                hpText.removeNode()

        self.hpTextNodes = []
        for currTextEffect in self.textEffects:
            if currTextEffect:
                currTextEffect.finish()

        self.textEffects = []
        self.hideHpMeter(0.0)
        self.gameFSM.cleanup()
        self.gameFSM = None
        self.motionFSM.cleanup()
        del self.motionFSM
        if self.setWeaponIval:
            self.setWeaponIval.pause()
            self.setWeaponIval = None
        if self.currentWeapon:
            self.currentWeapon.delete()
            self.currentWeapon = None
        self.currentWeaponId = 0
        self.isWeaponDrawn = 0
        self.currentTarget = None
        DistributedReputationAvatar.disable(self)
        WeaponBase.disable(self)
        if self.ambientFx:
            self.ambientFx.pause()
        self.ambientFx = None
        del self.battleRandom

    def delete(self):
        self.ropeActor = None
        if self.ropeEndNode:
            self.ropeEndNode.removeNode()
            self.ropeEndNode = None
        self.rope = None
        taskMgr.remove(self.getSwimTaskName())
        DistributedReputationAvatar.delete(self)
        WeaponBase.delete(self)

    def startSmooth(self):
        if not self.isLocal():
            broadcastPeriod = 2.0
            self.smoother.setMaxPositionAge(broadcastPeriod * 1.25 * 10)
            self.smoother.setExpectedBroadcastPeriod(PiratesGlobals.AI_MOVEMENT_PERIOD)
            self.smoother.setAcceptClockSkew(False)
            self.smoother.setDefaultToStandingStill(False)
            self.smoother.setDelay(OTPGlobals.NetworkLatency * 1.5)
            self.setSmoothWrtReparents(True)
        DistributedReputationAvatar.startSmooth(self)

    def setAvatarType(self, avatarType):
        self.avatarType = avatarType
        self.height = EnemyGlobals.getHeight(avatarType)
        self.battleTubeHeight = max(10.0, self.height)
        self.battleTubeRadius = EnemyGlobals.getBattleTubeRadius(avatarType)

    def smoothPosition(self):
        DistributedSmoothNode.DistributedSmoothNode.smoothPosition(self)
        if self.gameFSM.state == 'WaterRoam':
            if self.cr.wantSeapatch:
                world = self.cr.getActiveWorld()
                if world:
                    water = world.getWater()
                else:
                    water = None
                if water:
                    zWater, normal = water.calcHeightAndNormal(node=self)
                    self.setZ(render, zWater)
                    geom = self.getGeomNode()
                    geom.setP(render, normal[1] * 90 - 7)
        self.updateMyAnimState(self.smoother.getSmoothForwardVelocity(), self.smoother.getSmoothRotationalVelocity(), self.smoother.getSmoothLateralVelocity())

    def updateMyAnimState(self, forwardVel, rotationVel, lateralVel):
        self.motionFSM.motionAnimFSM.updateAnimState(forwardVel, rotationVel, lateralVel)

    def setNpc(self, isNpc):
        self.isNpc = isNpc

    def setTeam(self, team):
        if self.cr.activeWorld:
            handled, returnVal = self.cr.activeWorld.setAvTeam(self, team)
            if handled:
                team = returnVal
        Teamable.setTeam(self, team)

    def setAmbush(self, ambush):
        self.ambushEnemy = ambush

    def getTeam(self):
        handled = False
        if self.cr.activeWorld:
            handled, returnVal = self.cr.activeWorld.getAvTeam(self)
            if handled:
                return returnVal
        return Teamable.getTeam(self)

    def setShipId(self, shipId):
        if self.pendingSetShip:
            self.cr.relatedObjectMgr.abortRequest(self.pendingSetShip)
            self.pendingSetShip = None
        if shipId:
            self.pendingSetShip = self.cr.relatedObjectMgr.requestObjects([shipId], eachCallback=self._setShip)
        else:
            self._setShip(0)
            if self.crewBuffDisplay and self.isLocal():
                self.crewBuffDisplay.stop()
                self.crewBuffDisplay.destroy()

    def getShipId(self):
        return self.ship and self.ship.doId or 0

    def _setShip(self, ship):
        self.ship = ship

    def getShip(self):
        return self.ship

    def setName(self, name):
        DistributedReputationAvatar.setName(self, name)
        self.refreshStatusTray()
        self.nametag.setDisplayName('        ')
        nameText = self.getNameText()
        if nameText:
            if self.isNpc:
                if not self.avatarType.isA(AvatarTypes.Townfolk):
                    self.accept('weaponChange', self.setMonsterNameTag)
                    self.setMonsterNameTag()
                else:
                    nameText['text'] = self.name
                color2 = EnemyGlobals.getNametagColor(self.avatarType)
                if self.isBoss() and not self.bossIcon:
                    color2 = (0.95, 0.1, 0.1, 1)
                    self.bossIcon = loader.loadModel('models/gui/flag_boss')
                    self.bossIcon.reparentTo(nameText)
                    self.bossIcon.setScale(3.5)
                    self.bossIcon.flattenLight()
                    self.bossIcon.setBillboardPointEye()
                    self.bossIcon.setPos(-0.75, 0, 2.6)
                nameText['fg'] = color2

    def getNameText(self):
        pass

    def setMonsterNameTag(self):
        if self.level:
            color = self.cr.battleMgr.getExperienceColor(base.localAvatar, self)
            name = '%s  %s\x01smallCaps\x01%s%s\x02\x02' % (self.name, color, PLocalizer.Lv, self.level)
        else:
            name = self.name
        self.getNameText()['text'] = name

    def considerUnderstandable(self):
        DistributedReputationAvatar.considerUnderstandable(self)
        if self.ShowUnderstandable and not self.isNpc and self.iconNodePath and self.isUnderstandable() and not self.chatIcon and base.localAvatar.getDoId() != self.getDoId():
            self.chatIcon = loader.loadModel('models/textureCards/flagIcons')
            self.chatIcon.setScale(2.5, 1.5, 1.5)
            self.chatIcon.setPos(5, 0, -1.0)
            self.chatIcon.reparentTo(self.iconNodePath)

    def refreshStatusTray(self):
        statusTray = localAvatar.guiMgr.targetStatusTray
        if localAvatar.currentTarget == self or statusTray.doId == self.doId:
            statusTray.updateHp(self.hp, self.maxHp, self.doId)
            statusTray.updateVoodoo(self.mojo, self.maxMojo, self.doId)
            statusTray.updateStatusEffects(self.skillEffects)
            statusTray.updateSkill(self.currentAttack, self.doId)
            sticky = localAvatar.currentTarget == self and localAvatar.hasStickyTargets()
            statusTray.updateSticky(sticky)
            if self.hp > 0:
                statusTray.show()
            else:
                self.hideHpMeter(1.0)

    def showProximityInfo(self):
        if not hasattr(base, 'tutorial'):
            DistributedReputationAvatar.showProximityInfo(self)

    def initializeBattleCollisions(self):
        if self.battleTubeNodePaths:
            return
        self.battleTubeEvent = self.uniqueName('battleAvatarTube')
        self.battleTube = CollisionTube(0, 0, 0, 0, 0, self.battleTubeHeight, self.battleTubeRadius)
        self.battleTube.setTangible(1)
        battleTubeNode = CollisionNode(self.battleTubeEvent)
        battleTubeNode.addSolid(self.battleTube)
        battleTubeNode.setIntoCollideMask(self.battleCollisionBitmask)
        battleTubeNodePath = self.attachNewNode(battleTubeNode)
        battleTubeNodePath.setTag('objType', str(PiratesGlobals.COLL_AV))
        battleTubeNodePath.setTag('avId', str(self.doId))
        self.battleTubeNodePaths.append(battleTubeNodePath)
        if self.isBattleable():
            self.aimTubeEvent = self.uniqueName('aimTube')
            aimTube = CollisionTube(0, 0, -max(10, self.battleTubeHeight), 0, 0, max(10, self.battleTubeHeight), self.battleTubeRadius * 1.5)
            aimTube.setTangible(0)
            aimTubeNode = CollisionNode(self.aimTubeEvent)
            aimTubeNode.addSolid(aimTube)
            aimTubeNode.setIntoCollideMask(PiratesGlobals.BattleAimBitmask)
            aimTubeNodePath = self.attachNewNode(aimTubeNode)
            aimTubeNodePath.setTag('objType', str(PiratesGlobals.COLL_AV))
            aimTubeNodePath.setTag('avId', str(self.doId))
            self.cr.targetMgr.addTarget(aimTubeNodePath.get_key(), self)
            self.aimTubeNodePaths.append(aimTubeNodePath)

    def deleteBattleCollisions(self):
        if not self.battleTubeNodePaths:
            return

        if self.battleTube:
            self.battleTube = None

        for np in self.battleTubeNodePaths:
            np.removeNode()

        self.battleTubeNodePaths = []
        if self.isBattleable():
            for np in self.aimTubeNodePaths:
                if hasattr(self.cr, 'targetMgr') and self.cr.targetMgr:
                    self.cr.targetMgr.removeTarget(np.get_key())

                np.removeNode()

            self.aimTubeNodePaths = []

    def stashBattleCollisions(self):
        for tube in self.battleTubeNodePaths:
            tube.stash()

        for tube in self.aimTubeNodePaths:
            tube.stash()

    def unstashBattleCollisions(self):
        for tube in self.battleTubeNodePaths:
            tube.unstash()

        for tube in self.aimTubeNodePaths:
            tube.unstash()

    def createHitTrack(self, parent, explosionPoint=Point3(0)):
        explosion = loader.loadModel('models/sea/splash.bam')
        explosion.setScale(0.4)
        explosion.setColorScale(0, 1, 1, 1)
        explosion.setBillboardPointWorld()
        return Sequence(Func(explosion.reparentTo, parent), Func(explosion.setPos, explosionPoint),
            Wait(0.6), Func(explosion.detachNode))

    def isBattleable(self):
        return 1

    def canAggro(self):
        return True

    def requestInteraction(self, avId, interactType=0):
        if self.isLocal():
            self.notify.warning('We are hearing our own requestInteraction bounced back to us')
            return

        DistributedReputationAvatar.requestInteraction(self, avId, interactType)
        if not self.isBattleable():
            return

        if not self.canAggro():
            return

        skillEffects = self.getSkillEffects()
        if WeaponGlobals.C_SPAWN in skillEffects:
            return

        base.localAvatar.setCurrentTarget(self.doId)

    def requestExit(self):
        if self.isLocal():
            self.notify.warning('We are hearing our own requestExit bounced back to us')
            return

        DistributedReputationAvatar.requestExit(self)

    def setCurrentTarget(self, targetId):
        if self.currentTarget:
            if targetId == None:
                self.currentTarget.resetComboLevel()

        self.currentTarget = self.cr.doId2do.get(targetId)
        if hasattr(self, 'undead') and self.undead:
            self.skeleton.currentTarget = self.currentTarget

    def setLocalTarget(self, on):
        DistributedReputationAvatar.setLocalTarget(self, on)
        return
        if not self.isLocal():
            if on:
                self.battleTubeNodePath.stash()
            else:
                self.battleTubeNodePath.unstash()

    def getCurrentWeapon(self):
        return (
         self.currentWeaponId, self.isWeaponDrawn)

    def setCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        self.checkWeaponSwitch(currentWeaponId, isWeaponDrawn)
        weaponIds = base.localAvatar.equippedWeapons

    def checkWeaponSwitch(self, currentWeaponId, isWeaponDrawn):
        yieldThread('setCurrentWeapon begin')
        if isWeaponDrawn == self.isWeaponDrawn and currentWeaponId == self.currentWeaponId:
            return
        if isWeaponDrawn and not self.isWeaponDrawn:
            self.isWeaponDrawn = isWeaponDrawn
            self.currentWeaponId = currentWeaponId
            self.__initWeaponChange()
            self.__doDrawWeapon()
            self.__endWeaponChange()
        elif isWeaponDrawn and self.isWeaponDrawn and currentWeaponId != self.currentWeaponId:
            self.__initWeaponChange()
            self.__doPutAwayWeapon()
            self.isWeaponDrawn = isWeaponDrawn
            self.currentWeaponId = currentWeaponId
            self.__doDrawWeapon()
            self.__endWeaponChange()
        elif not isWeaponDrawn and self.isWeaponDrawn:
            self.isWeaponDrawn = isWeaponDrawn
            self.currentWeaponId = currentWeaponId
            self.__initWeaponChange()
            self.__doPutAwayWeapon()
            self.__endWeaponChange()
        else:
            self.currentWeaponId = currentWeaponId

    def __initWeaponChange(self):
        if self.isLocal():
            if hasattr(self.cr, 'targetMgr') and self.cr.targetMgr:
                self.cr.targetMgr.stopFollowAim()
        if self.setWeaponIval:
            self.setWeaponIval.finish()
            self.setWeaponIval = None
        self.setWeaponIval = Sequence()
        if self.isLocal():
            self.setWeaponIval.append(Func(messenger.send, 'drawStarted'))
        return

    def __endWeaponChange(self):
        if self.isLocal():
            self.setWeaponIval.append(Func(messenger.send, 'drawFinished'))
        self.setWeaponIval.start()
        if self.isNpc:
            if self.currentWeaponId:
                rep = WeaponGlobals.getRepId(self.currentWeaponId)
                if rep == InventoryType.DollRep:
                    if self.isWeaponDrawn:
                        self.showVoodooDollAttuned()
                    else:
                        self.showVoodooDollUnattuned()

    def __doPutAwayWeapon(self):
        if self.isLocal():
            taskMgr.remove('usageTask')
            localAvatar.guiMgr.combatTray.ignoreInput()
            localAvatar.guiMgr.combatTray.disableTray()
        if self.currentWeapon:
            ival = self.putAwayCurrentWeapon(blendInT=0.3, blendOutT=0)
            if ival:
                self.setWeaponIval.append(ival)
                self.setWeaponIval.append(Func(self.currentWeapon.delete))

    def __doDrawWeapon(self):
        weaponClass = WeaponGlobals.getWeaponClass(self.currentWeaponId)
        if weaponClass:
            self.currentWeapon = weaponClass(self.currentWeaponId)
            ammoSkillId = 0
            if self.currentWeaponId == InventoryType.GrenadeWeaponL1:
                if self.currentAmmo:
                    ammoSkillId = self.currentAmmo
            ival = self.pullOutCurrentWeapon(ammoSkillId=ammoSkillId, blendInT=0, blendOutT=0.3)
            if ival:
                self.setWeaponIval.append(ival)
            if self.isLocal():
                if hasattr(self.cr, 'targetMgr'):
                    self.setWeaponIval.append(Func(self.cr.targetMgr.startFollowAim))
                if self.currentWeaponId:
                    rep = WeaponGlobals.getRepId(self.currentWeaponId)
                    self.setWeaponIval.append(Func(localAvatar.guiMgr.combatTray.initCombatTray, rep))

    def showVoodooDollAttuned(self):
        if not self.isNpc:
            return
        if not self.attuneEffect:
            self.attuneEffect = VoodooAura.getEffect()
        if self.attuneEffect:
            self.attuneEffect.reparentTo(self.rightHandNode)
            self.attuneEffect.setPos(0, 0, 0)
            self.attuneEffect.particleDummy.reparentTo(self.rightHandNode)
            self.attuneEffect.setEffectColor(Vec4(0.2, 0.1, 0.5, 1))
            self.attuneEffect.startLoop()

    def showVoodooDollUnattuned(self):
        if not self.isNpc:
            return
        if self.attuneEffect:
            self.attuneEffect.stopLoop()
            self.attuneEffect = None
        return

    def isCurrentWeapon(self, weaponId):
        if self.currentWeaponId:
            return self.currentWeaponId == weaponId
        return 0

    def getCurrentAmmo(self):
        return self.currentAmmo

    def setCurrentAmmo(self, currentAmmo, init=0):
        if currentAmmo == self.currentAmmo and not init:
            return
        oldCurrentAmmo = self.currentAmmo
        self.currentAmmo = currentAmmo
        if hasattr(self, 'undead') and self.undead:
            self.skeleton.currentAmmo = self.currentAmmo
        if self.isNpc:
            self.currentAmmo = currentAmmo
            if hasattr(self, 'undead') and self.undead:
                self.skeleton.currentAmmo = self.currentAmmo
        if self.currentWeapon:
            if self.setWeaponIval:
                self.setWeaponIval.finish()
                self.setWeaponIval = None
            self.setWeaponIval = Sequence()
            ival = self.changeAmmunition()
            if ival:
                self.setWeaponIval.append(ival)
            self.setWeaponIval.start()
        return

    def pullOutCurrentWeapon(self, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        self.setWalkForWeapon()
        if hasattr(self, 'undead') and self.undead:
            drawIval = self.currentWeapon.getDrawIval(self.skeleton, ammoSkillId, blendInT, blendOutT)
        else:
            drawIval = self.currentWeapon.getDrawIval(self, ammoSkillId, blendInT, blendOutT)
        return drawIval

    def putAwayCurrentWeapon(self, blendInT=0.1, blendOutT=0.1):
        if hasattr(self, 'undead') and self.undead:
            returnIval = self.currentWeapon.getReturnIval(self.skeleton, blendInT, blendOutT)
        else:
            returnIval = self.currentWeapon.getReturnIval(self, blendInT, blendOutT)
        return returnIval

    def changeAmmunition(self):
        if hasattr(self, 'undead') and self.undead:
            returnIval = self.currentWeapon.getAmmoChangeIval(self.skeleton, 0, self.currentAmmo, 0, None)
        else:
            returnIval = self.currentWeapon.getAmmoChangeIval(self, 0, self.currentAmmo, 0, None)
        return returnIval

    def setWalkForWeapon(self):
        if self.currentWeapon:
            walkAnim, runAnim, reverseAnim, neutralAnim, strafeLeftAnim, strafeRightAnim, strafeDiagLeftAnim, strafeDiagRightAnim, strafeRevDiagLeftAnim, strafeRevDiagRightAnim, fallGroundAnim, fallWaterAnim, spinLeftAnim, spinRightAnim = self.currentWeapon.getWalkForWeapon(self)
            self.motionFSM.setAnimInfo(((neutralAnim, 1.0), (walkAnim, 1.5), (runAnim, 1.0), (reverseAnim, -1.5), (strafeLeftAnim, 1.0), (strafeRightAnim, 1.0), (strafeDiagLeftAnim, 1.0), (strafeDiagRightAnim, 1.0), (strafeRevDiagLeftAnim, 1.0), (strafeRevDiagRightAnim, 1.0), (fallGroundAnim, 1.0), (fallWaterAnim, -1.0), (spinLeftAnim, 1.0), (spinRightAnim, 1.0)))

    def getSkillQuantity(self, skillId):
        inv = self.getInventory()
        if inv:
            return inv.getStackQuantity(skillId)
        else:
            return 0

    def getAmmoQuantity(self, ammoInvId):
        inv = self.getInventory()
        if inv:
            return inv.getStackQuantity(ammoInvId)
        else:
            return 0

    def useTargetedSkill(self, skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, timestamp, pos, charge=0, localSignal=0):
        DistributedReputationAvatar.useTargetedSkill(self, skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, timestamp, pos, charge, localSignal)
        WeaponBase.useTargetedSkill(self, skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, timestamp, pos, charge)

    def useProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, charge):
        WeaponBase.useProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, charge)
        if not self.isLocal():
            self.playSkillMovie(skillId, ammoSkillId, WeaponGlobals.RESULT_DELAY, charge)

    def packMultiHitEffects(self, targetEffects, numHits):
        if numHits <= 1:
            return targetEffects
        divDamage = int(targetEffects[0] / numHits + 1)
        multiHitEffects = []
        multiHitEffects.append(list(targetEffects))
        multiHitEffects[0][0] = divDamage
        for i in range(numHits - 2):
            multiHitEffects.append([divDamage, 0, 0, 0, 0])

        multiHitEffects.append([targetEffects[0] - divDamage * (numHits - 1), 0, 0, 0, 0])
        return multiHitEffects

    def toonUp(self, hpGained):
        if self.hp == None or hpGained < 0:
            return
        if hpGained > 0:
            self.showHpText(hpGained)
            self.hpChange(quietly=0)
        return

    def takeDamage(self, hpLost, pos, bonus=0):
        if self.hp == None or hpLost < 0:
            return
        if hpLost > 0:
            self.showHpText(-hpLost, pos, bonus)
            self.hpChange(quietly=0)
        return

    def takeMpDamage(self, mpLost, pos, bonus=3):
        if self.mojo == None or mpLost < 0 or self.mojo <= 0:
            return
        self.refreshStatusTray()
        if mpLost > 0:
            self.showHpText(-mpLost, pos, bonus)
        return

    def playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, multihit=0, targetBonus=0):
        if self.isDisabled():
            return
        DistributedReputationAvatar.playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, multihit=multihit, targetBonus=targetBonus)
        targetHp, targetPower, targetEffect, targetMojo, targetSwiftness = targetEffects
        if self.PlayersInvulnerable and targetHp < 0 and not self.isNpc:
            pass
        else:
            if targetHp < 0:
                self.takeDamage(-targetHp, pos, bonus=targetBonus)
            else:
                if targetHp > 0:
                    self.toonUp(targetHp)
            if targetMojo < 0:
                taskMgr.doMethodLater(WeaponGlobals.MP_DAMAGE_DELAY, self.takeMpDamage, self.taskName('playMpDamage'), extraArgs=[-targetMojo, pos])
            messenger.send('pistolHitTarget')

    def playSkillMovie(self, skillId, ammoSkillId, skillResult, charge, targetId=0):
        self.cleanupOuchIval()
        skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
        if not skillInfo:
            return
        anim = skillInfo[WeaponGlobals.PLAYABLE_INDEX]
        if self.curAttackAnim:
            if self.curAttackAnim.isPlaying() and WeaponGlobals.getIsInstantSkill(skillId, ammoSkillId):
                return
            else:
                self.curAttackAnim.pause()
                self.curAttackAnim = None
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.currentAttack = [skillId, ammoSkillId, timestamp]
        self.refreshStatusTray()
        target = self.cr.doId2do.get(targetId)
        self.curAttackAnim = getattr(self.cr.combatAnims, anim)(self, skillId, ammoSkillId, charge, target)
        self.preprocessAttackAnim()
        if self.curAttackAnim != None:
            self.curAttackAnim.start()
        return

    def preprocessAttackAnim(self):
        pass

    def cleanupOuchIval(self):
        DistributedReputationAvatar.cleanupOuchIval(self)
        if self.ouchAnim != None:
            self.ouchAnim.finish()
            self.ouchAnim = None
        if self.avatarType.isA(AvatarTypes.Kraken):
            if self.gameFSM.emergeTrack != None:
                self.gameFSM.emergeTrack.pause()
                self.gameFSM.emergeTrack = None
            if self.gameFSM.submergeTrack != None:
                self.gameFSM.submergeTrack.pause()
                self.gameFSM.submergeTrack = None
            if self.gameFSM.deathTrack != None:
                self.gameFSM.deathTrack.pause()
                self.gameFSM.deathTrack = None
        return

    def getFadeInTrack(self):
        parent = self.getParentObj()
        if not parent:
            return
        dclassName = parent.dclass.getName()
        if dclassName == 'DistributedGAInterior':
            return
        if self.getNameText():
            fadeInIval = Sequence(Func(self.setTransparency, TransparencyAttrib.MAlpha), Func(self.setAlphaScale, 0.0), Func(self.getNameText().setAlphaScale, 0.0), Parallel(LerpFunctionInterval(self.setAlphaScale, 1.0, fromData=0.0, toData=1.0), LerpFunctionInterval(self.getNameText().setAlphaScale, 1.0, fromData=0.0, toData=1.0)), Func(self.clearTransparency), Func(self.clearColorScale), Func(self.getNameText().clearColorScale))
        else:
            fadeInIval = Sequence(Func(self.setTransparency, TransparencyAttrib.MAlpha), Func(self.setAlphaScale, 0.0), LerpFunctionInterval(self.setAlphaScale, 1.0, fromData=0.0, toData=1.0), Func(self.clearTransparency), Func(self.clearColorScale))
        return fadeInIval

    def getSpawnTrack(self):
        avatarTeam = self.getTeam()
        if avatarTeam == PiratesGlobals.UNDEAD_TEAM:
            if self.getAnimControl('intro'):
                duration = self.getDuration('intro')
                intro = self.actorInterval('intro')
            else:
                duration = 1.5
                scaleUp = LerpScaleInterval(self, 2.0, 1.0, startScale=0.1)
                fadeIn = LerpFunctionInterval(self.setAlphaScale, 2.0, fromData=0.0, toData=1.0)
                intro = Sequence(Func(self.setTransparency, 1), Parallel(scaleUp, fadeIn), Func(self.clearTransparency), Func(self.clearColorScale))

            def startSFX():
                sfx = self.getSfx('spawn')
                if sfx:
                    base.playSfx(sfx, node=self)

            def startVFX():
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    avatarScale = self.getEnemyScale()
                    spawnEffect = JRSpawnEffect.getEffect()
                    if spawnEffect:
                        spawnEffect.reparentTo(render)
                        spawnEffect.setPos(self.getPos(render))
                        spawnEffect.effectScale = avatarScale
                        spawnEffect.duration = duration / 1.5
                        spawnEffect.play()

            if hasattr(self, 'ambushEnemy'):
                spawnIval = Sequence(Func(startSFX), Func(startVFX), intro, Func(self.ambushIntroDone))
            else:
                spawnIval = Sequence(Func(startSFX), Func(startVFX), intro)
            return spawnIval
        else:
            if self.getAnimControl('intro'):
                intro = self.actorInterval('intro')
            else:
                fadeIn = LerpFunctionInterval(self.setAlphaScale, 2.0, fromData=0.0, toData=1.0)
                intro = Sequence(Func(self.setTransparency, 1), fadeIn, Func(self.clearTransparency), Func(self.clearColorScale))
            return intro

    def ambushIntroDone(self):
        self.sendUpdate('ambushIntroDone')

    def b_setGameState(self, gameState, localArgs=[]):
        timestamp = globalClockDelta.getFrameNetworkTime()
        state = self.getGameState()
        self.setGameState(gameState, timestamp, localArgs)
        if state != self.getGameState():
            self.d_setGameState(gameState, timestamp)

    def d_setGameState(self, gameState, timestamp):
        self.sendUpdate('setGameState', [gameState, timestamp])

    def setGameState(self, gameState, timestamp=None, localArgs=[]):
        self.notify.debug('setGameState: %s state: %s' % (self.doId, gameState))
        if timestamp is None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        if self.gameFSM:
            if self.gameFSM.getCurrentOrNextState() != gameState:
                self.gameFSM.request(gameState, [ts] + localArgs)
        return

    def getGameState(self):
        return self.gameFSM.getCurrentOrNextState()

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def b_setAirborneState(self, airborneState):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.setAirborneStateLocal(airborneState, timestamp)
        self.d_setAirborneState(airborneState, timestamp)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def d_setAirborneState(self, airborneState, timestamp):
        self.sendUpdate('setAirborneState', [airborneState, timestamp])

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def setAirborneStateLocal(self, airborneState, timestamp):
        self.motionFSM.motionAnimFSM.setAirborneState(airborneState)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def setAirborneState(self, airborneState, timestamp):
        wait = self.smoother.getDelay() - globalClockDelta.localElapsedTime(timestamp)

        def wrap():
            self.motionFSM.motionAnimFSM.setAirborneState(airborneState)
            self.motionFSM.motionAnimFSM.updateAnimState(self.smoother.getSmoothForwardVelocity(), self.smoother.getSmoothRotationalVelocity(),
                self.smoother.getSmoothLateralVelocity())

        taskMgr.doMethodLater(wait, wrap, self.taskName('playMotionAnim-%s-%d' % (airborneState, timestamp)), [])

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def b_playMotionAnim(self, anim):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.d_playMotionAnim(anim, timestamp)
        self.l_playMotionAnim(anim, timestamp)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def d_playMotionAnim(self, anim, timestamp):
        self.d_broadcastPosHpr()
        self.sendUpdate('playMotionAnim', [anim, timestamp])

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def l_playMotionAnim(self, anim, timestamp):
        self.motionFSM.motionAnimFSM.playMotionAnim(anim, local=True)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def playMotionAnim(self, anim, timestamp):
        wait = self.smoother.getDelay() - globalClockDelta.localElapsedTime(timestamp)
        taskMgr.doMethodLater(wait, self.motionFSM.motionAnimFSM.playMotionAnim, self.taskName('playMotionAnim-%s-%d' % \
            (anim, timestamp)), [anim, False])

    def b_setGroundState(self, groundState):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.setGroundStateLocal(groundState, timestamp)
        self.d_setGroundState(groundState, timestamp)

    def d_setGroundState(self, groundState, timestamp):
        self.sendUpdate('setGroundState', [groundState, timestamp])

    def setGroundStateLocal(self, groundState, timestamp):
        self.motionFSM.motionAnimFSM.setGroundState(groundState)

    def setGroundState(self, groundState, timestamp):
        wait = self.smoother.getDelay() - globalClockDelta.localElapsedTime(timestamp)
        if wait > 0:
            taskMgr.doMethodLater(wait, self.motionFSM.motionAnimFSM.setGroundState, self.taskName('playMotionAnim-%s-%d' % (groundState, timestamp)), [
             groundState])

    def getSwimTaskName(self):
        return self.taskName('swimBobTask')

    def startBobSwimTask(self):
        swimTaskName = self.getSwimTaskName()
        task = taskMgr.add(self.bobTask, swimTaskName, priority=35)
        task.zPosTime = PiratesGlobals.SWIM_WALK_TRANSITION_TIME
        task.zStart = self.getZ(render)
        self.bobbing = True

    def bobTask(self, task):
        world = self.cr.getActiveWorld()
        if world:
            water = world.getWater()
        else:
            water = None
        if self.cr.wantSeapatch and water:
            zWater, normal = water.calcHeightAndNormal(node=self)
        else:
            zWater = 0.0
            normal = Vec3(0, 0, 1)
        if self.bobbing:
            zWater = lerp(task.zStart, zWater, clampScalar(0.0, 1.0, task.time / task.zPosTime))
            if task.time >= task.zPosTime:
                self.bobbing = False
        self.setZ(render, zWater)
        geom = self.getGeomNode()
        geom.setP(render, normal[1] * 90)
        return task.cont

    def stopBobSwimTask(self):
        swimTaskName = self.getSwimTaskName()
        taskMgr.remove(swimTaskName)
        self.bobbing = False
        geom = self.getGeomNode()
        geom.setP(0)
        geom.setR(0)

    def getTotalHp(self):
        if self.hp is None:
            return 0
        return self.hp

    def hpChange(self, quietly=0):
        pass

    def setMaxHp(self, hp):
        DistributedReputationAvatar.setMaxHp(self, hp)
        self.refreshStatusTray()

    def setHp(self, hp, quietly=0):
        justRanOutOfHp = hp is not None and self.hp is not None and self.hp - hp > 0 and hp <= 0
        self.hp = hp
        self.refreshStatusTray()
        localAvatar.guiMgr.attuneSelection.update()
        self.hpChange(quietly=1)
        if justRanOutOfHp:
            self.died()
        return

    def getTotalLuck(self):
        return self.luck + self.luckMod

    def getLuck(self):
        return self.luck

    def setLuck(self, luck):
        self.luck = luck

    def setLuckMod(self, luck):
        self.luckMod = luck

    def getMaxLuck(self):
        return self.maxLuck

    def setMaxLuck(self, maxLuck):
        self.maxLuck = maxLuck

    def getTotalPower(self):
        return self.power + self.powerMod

    def getPower(self):
        return self.power

    def setPower(self, power):
        self.power = power

    def setPowerMod(self, power):
        self.notify.debug('setPowerMod %s' % power)
        self.powerMod = power

    def setMaxPower(self, maxPower):
        self.maxPower = maxPower

    def getTotalMojo(self):
        return self.mojo + self.mojoMod

    def setMojo(self, mojo):
        self.mojo = mojo
        self.refreshStatusTray()
        base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTrayStates()

    def setMojoMod(self, mojo):
        self.mojoMod = mojo
        self.refreshStatusTray()
        base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTrayStates()

    def setMaxMojo(self, maxMojo):
        self.maxMojo = maxMojo
        self.refreshStatusTray()

    def getMaxMojo(self):
        return self.maxMojo

    def getMojo(self):
        return self.mojo

    def getTotalSwiftness(self):
        return self.swiftness + self.swiftnessMod

    def setSwiftness(self, swiftness):
        self.swiftness = swiftness

    def setSwiftnessMod(self, swiftness):
        self.notify.debug('setSwiftnessMod %s' % swiftness)
        self.swiftnessMod = swiftness

    def setStunMod(self, stun):
        self.notify.debug('setStunMod %s' % stun)
        self.stunMod = stun

    def setHasteMod(self, haste):
        self.notify.debug('setHasteMod %s' % haste)
        self.hasteMod = haste

    def setAimMod(self, stun):
        self.notify.debug('setAimMod %s' % stun)
        self.aimMod = stun

    def setMaxSwiftness(self, maxSwiftness):
        self.maxSwiftness = maxSwiftness

    def getCombo(self):
        return (self.combo, self.isTeamCombo, self.comboDamage)

    def setCombo(self, combo, teamCombo, comboDamage, attackerId=0):
        DistributedReputationAvatar.setCombo(self, combo, teamCombo, comboDamage,
            attackerId=attackerId)

        if attackerId == base.localAvatar.getDoId():
            return

        self.combo = combo
        if teamCombo:
            self.isTeamCombo = teamCombo

        self.comboDamage = comboDamage
        if base.localAvatar.currentTarget == self:
            messenger.send('trackCombo', [self.combo, self.isTeamCombo, self.comboDamage])

    def resetComboLevel(self, args=None):
        DistributedReputationAvatar.resetComboLevel(self, args)
        self.isTeamCombo = 0
        self.setCombo(0, 0, 0)
        self.comboAttackers = {}

    def getSkills(self, weaponId):
        if self.getInventory() is None:
            self.notify.warning('Inventory not created yet!')
            return {}

        return self.getInventory().getSkills(weaponId)

    def setSkillEffects(self, buffs):
        for entry in buffs:
            buffKeyId = '%s-%s' % (entry[0], entry[3])
            if buffKeyId not in self.skillEffects.keys():
                self.skillEffects[buffKeyId] = (
                    entry[0],
                    entry[1],
                    entry[2],
                    entry[3])

                self.addStatusEffect(entry[0], entry[3], entry[1])

        killList = []
        for buffKeyId in self.skillEffects.keys():
            foundEntry = 0
            for entry in buffs:
                id = '%s-%s' % (entry[0], entry[3])
                if buffKeyId == id:
                    foundEntry = 1

            if not foundEntry:
                killList.append((buffKeyId, self.skillEffects[buffKeyId][0],
                    self.skillEffects[buffKeyId][3]))

        for buffKeyId, effectId, attackerId in killList:
            del self.skillEffects[buffKeyId]
            self.removeStatusEffect(effectId, attackerId)

        self.refreshStatusTray()

    def findAllBuffCopyKeys(self, effectId):
        buffCopies = []
        for buffKeyId in self.skillEffects.keys():
            if self.skillEffects[buffKeyId][0] == effectId:
                buffCopies.append(buffKeyId)

        return buffCopies

    def getSkillEffects(self):
        buffIds = []
        for buffKeyId in self.skillEffects.keys():
            buffId = self.skillEffects[buffKeyId][0]
            if buffId not in buffIds:
                buffIds.append(buffId)

        return buffIds

    def addStatusEffect(self, effectId, attackerId, duration):
        attacker = self.cr.doId2do.get(attackerId)
        if effectId == WeaponGlobals.C_BLIND:
            if self.isLocal():
                self.guiMgr.showSmokePanel()
        elif effectId == WeaponGlobals.C_DIRT:
            if self.isLocal():
                self.guiMgr.showDirtPanel()
        elif effectId == WeaponGlobals.C_POISON:
            LerpColorScaleInterval(self.getGeomNode(), 1.0, Vec4(0.7, 1, 0.6, 1), startColorScale=Vec4(1, 1, 1, 1)).start()
            if self.poisonEffect:
                return
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                avatarScale = self.getEnemyScale()
                self.poisonEffect = PoisonEffect.getEffect()
                if self.poisonEffect:
                    self.poisonEffect.reparentTo(self)
                    self.poisonEffect.setPos(0, 0.75, self.height - 1.5)
                    self.poisonEffect.effectScale = avatarScale
                    self.poisonEffect.startLoop()
        elif effectId == WeaponGlobals.C_ACID:
            self.smokeWispEffect = SmokeWisps.getEffect()
            if self.smokeWispEffect:
                self.smokeWispEffect.reparentTo(self)
                self.smokeWispEffect.setPos(0, 0, self.height)
                self.smokeWispEffect.startLoop()
        elif effectId == WeaponGlobals.C_WOUND:
            pass
        elif effectId == WeaponGlobals.C_TAUNT:
            self.getGeomNode().setColorScale(1.0, 0.4, 0.4, 1)
        elif effectId == WeaponGlobals.C_ON_FIRE:
            if self.fireEffect:
                return
            avatarScale = self.getEnemyScale()
            self.fireEffect = Flame.getEffect()
            if self.fireEffect:
                if hasattr(self, 'headNode') and self.headNode:
                    self.fireEffect.reparentTo(self.headNode)
                    self.fireEffect.setPos(self.headNode, -2, 0, 0)
                    self.fireEffect.setHpr(0, 0, 80)
                else:
                    self.fireEffect.reparentTo(self)
                    self.fireEffect.setPos(0, 0, self.height * 0.8)
                self.fireEffect.effectScale = 0.25 * avatarScale
                self.fireEffect.duration = 4.0
                self.fireEffect.play()
            self.smokeWispEffect = SmokeWisps.getEffect()
            if self.smokeWispEffect:
                self.smokeWispEffect.reparentTo(self)
                self.smokeWispEffect.setPos(0, 0, self.height)
                self.smokeWispEffect.startLoop()
        elif effectId == WeaponGlobals.C_SLOW:
            if self.slowEffect:
                return
            self.slowEffect = SlowEffect.getEffect()
            if self.slowEffect:
                self.slowEffect.duration = 1.75
                self.slowEffect.effectScale = 0.85
                if hasattr(self, 'headNode') and self.headNode:
                    self.slowEffect.reparentTo(self.headNode)
                    self.slowEffect.setHpr(0, 0, 90)
                    self.slowEffect.setPos(self.headNode, 1.5, 0, 0)
                else:
                    self.slowEffect.reparentTo(self)
                    self.slowEffect.setHpr(self, 0, 0, 0)
                    self.slowEffect.setPos(self, 0, 0, self.getHeight() + 1.5)
                self.slowEffect.startLoop()
            self.slowEffect2 = SlowEffect.getEffect()
            if self.slowEffect2:
                self.slowEffect2.duration = 1.75
                self.slowEffect2.effectScale = 0.75
                if hasattr(self, 'headNode') and self.headNode:
                    self.slowEffect2.reparentTo(self.headNode)
                    self.slowEffect2.setHpr(0, 120, 90)
                    self.slowEffect2.setPos(self.headNode, 1.75, 0, 0)
                else:
                    self.slowEffect2.reparentTo(self)
                    self.slowEffect2.setHpr(self, 120, 0, 0)
                    self.slowEffect2.setPos(self, 0, 0, self.getHeight() + 1.25)
                self.slowEffect2.startLoop()
        elif effectId == WeaponGlobals.C_STUN:
            if self.stunEffect:
                return
            self.stunEffect = StunEffect.getEffect()
            if self.stunEffect:
                self.stunEffect.duration = 1.0
                self.stunEffect.direction = 1
                self.stunEffect.effectScale = 0.65
                if hasattr(self, 'headNode') and self.headNode:
                    self.stunEffect.reparentTo(self.headNode)
                    self.stunEffect.setHpr(0, 0, 90)
                    self.stunEffect.setPos(self.headNode, 1, 0, 0)
                else:
                    self.stunEffect.reparentTo(self)
                    self.stunEffect.setHpr(self, 0, 0, 0)
                    self.stunEffect.setPos(self, 0, 0, self.getHeight() + 1)
                self.stunEffect.startLoop()
            self.stunEffect2 = StunEffect.getEffect()
            if self.stunEffect2:
                self.stunEffect2.duration = 1.0
                self.stunEffect2.direction = -1
                self.stunEffect2.effectScale = 0.5
                if hasattr(self, 'headNode') and self.headNode:
                    self.stunEffect2.reparentTo(self.headNode)
                    self.stunEffect2.setHpr(0, 120, 90)
                    self.stunEffect2.setPos(self.headNode, 1.25, 0, 0)
                else:
                    self.stunEffect2.reparentTo(self)
                    self.stunEffect2.setHpr(self, 120, 0, 0)
                    self.stunEffect2.setPos(self, 0, 0, self.getHeight() + 0.9)
                self.stunEffect2.startLoop()
        elif effectId == WeaponGlobals.C_HOLD:
            if self.shacklesEffect:
                return
            avatarScale = self.getEnemyScale()
            self.shacklesEffect = GraveShackles.getEffect()
            if self.shacklesEffect:
                self.shacklesEffect.reparentTo(self)
                self.shacklesEffect.setScale(avatarScale * 1.25)
                self.shacklesEffect.setPos(0, 0, 0)
                self.shacklesEffect.startLoop()
            self.voodooSmokeEffect = AttuneSmoke.getEffect()
            if self.voodooSmokeEffect:
                self.voodooSmokeEffect.reparentTo(self)
                self.voodooSmokeEffect.setPos(0, 0, 0.2)
                self.voodooSmokeEffect.startLoop()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = GroundDirt.getEffect()
                if effect:
                    effect.effectScale = avatarScale
                    effect.setScale(avatarScale)
                    effect.reparentTo(self)
                    effect.play()
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.reparentTo(self)
                cameraShakerEffect.setPos(0, 0, 0)
                cameraShakerEffect.shakeSpeed = 0.08
                cameraShakerEffect.shakePower = 1.5
                cameraShakerEffect.numShakes = 2
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(100.0)
        elif effectId == WeaponGlobals.C_ATTUNE:
            self.checkAttuneBuffEffect()
            if attacker and attacker.isLocal():
                attacker.addStickyTarget(self.doId)
        elif effectId == WeaponGlobals.C_VOODOO_STUN:
            self.showVoodooDollUnattuned()
            self.showEffectString(PLocalizer.AttackUnattune)
        elif effectId == WeaponGlobals.C_VOODOO_HEX_STUN:
            self.showVoodooDollUnattuned()
        elif effectId == WeaponGlobals.C_INTERRUPTED:
            self.showEffectString(PLocalizer.AttackInterrupt)
        elif effectId == WeaponGlobals.C_OPENFIRE and self.doId == localAvatar.doId:
            if self.crewBuffDisplay:
                self.crewBuffDisplay.stop()
                self.crewBuffDisplay.destroy()
            self.crewBuffDisplay = CrewBuffDisplay(skillIcon=loader.loadModel('models/textureCards/skillIcons').find('**/sail_openfire2'), duration=duration, buffName=PLocalizer.CrewBuffOpenFireString, buffDesc=PLocalizer.CrewBuffOpenFire % int((WeaponGlobals.OPEN_FIRE_BONUS - 1) * 100), parent=base.a2dBottomRight)
            self.crewBuffDisplay.reparentTo(base.a2dBottomRight, sort=-1000)
            self.crewBuffDisplay.play()
        elif effectId == WeaponGlobals.C_TAKECOVER and self.doId == localAvatar.doId:
            if self.crewBuffDisplay:
                self.crewBuffDisplay.stop()
                self.crewBuffDisplay.destroy()
            self.crewBuffDisplay = CrewBuffDisplay(skillIcon=loader.loadModel('models/textureCards/skillIcons').find('**/sail_take_cover'), duration=duration, buffName=PLocalizer.CrewBuffTakeCoverString, buffDesc=PLocalizer.CrewBuffTakeCover % int((1 - WeaponGlobals.TAKE_COVER_BONUS) * 100), parent=base.a2dBottomRight)
            self.crewBuffDisplay.reparentTo(base.a2dBottomRight, sort=-1000)
            self.crewBuffDisplay.play()

    def removeStatusEffect(self, effectId, attackerId):
        if effectId == WeaponGlobals.C_ATTUNE:
            self.checkAttuneBuffEffect()
        if self.findAllBuffCopyKeys(effectId):
            return
        if effectId == WeaponGlobals.C_BLIND:
            if self.isLocal():
                self.guiMgr.hideSmokePanel()
        elif effectId == WeaponGlobals.C_DIRT:
            if self.isLocal():
                self.guiMgr.hideDirtPanel()
        elif effectId == WeaponGlobals.C_POISON:
            LerpColorScaleInterval(self.getGeomNode(), 1.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(0.7, 1.0, 0.6, 1)).start()
            if self.poisonEffect:
                self.poisonEffect.stopLoop()
                self.poisonEffect = None
        elif effectId == WeaponGlobals.C_ACID:
            if self.smokeWispEffect:
                self.smokeWispEffect.stopLoop()
                self.smokeWispEffect = None
        elif effectId == WeaponGlobals.C_WOUND:
            pass
        elif effectId == WeaponGlobals.C_TAUNT:
            self.getGeomNode().setColorScale(1, 1, 1, 1)
        elif effectId == WeaponGlobals.C_ON_FIRE:
            if self.fireEffect:
                self.fireEffect.stopLoop()
                self.fireEffect = None
            if self.smokeWispEffect:
                self.smokeWispEffect.stopLoop()
                self.smokeWispEffect = None
        elif effectId == WeaponGlobals.C_SLOW:
            if self.slowEffect:
                self.slowEffect.stopLoop()
                self.slowEffect = None
            if self.slowEffect2:
                self.slowEffect2.stopLoop()
                self.slowEffect2 = None
        elif effectId == WeaponGlobals.C_STUN:
            if self.stunEffect:
                self.stunEffect.stopLoop()
                self.stunEffect = None
            if self.stunEffect2:
                self.stunEffect2.stopLoop()
                self.stunEffect2 = None
        elif effectId == WeaponGlobals.C_HOLD:
            effect = GroundDirt.getEffect()
            if effect:
                avatarScale = self.getEnemyScale()
                effect.effectScale = avatarScale / 1.5
                effect.setScale(avatarScale)
                effect.reparentTo(self)
                effect.play()
            if self.voodooSmokeEffect:
                self.voodooSmokeEffect.stopLoop()
                self.voodooSmokeEffect = None
            if self.shacklesEffect:
                self.shacklesEffect.stopLoop()
                self.shacklesEffect = None
        elif effectId == WeaponGlobals.C_VOODOO_STUN and self.currentTarget:
            if self.findAllBuffCopyKeys(WeaponGlobals.C_VOODOO_HEX_STUN):
                return
            self.showVoodooDollAttuned()
        elif effectId == WeaponGlobals.C_VOODOO_HEX_STUN and self.currentTarget:
            if self.findAllBuffCopyKeys(WeaponGlobals.C_VOODOO_STUN):
                return
            self.showVoodooDollAttuned()
        elif effectId == WeaponGlobals.C_OPENFIRE:
            if self.crewBuffDisplay:
                self.crewBuffDisplay.stop()
                self.crewBuffDisplay.destroy()
                self.crewBuffDisplay = None
        elif effectId == WeaponGlobals.C_TAKECOVER:
            if self.crewBuffDisplay:
                self.crewBuffDisplay.stop()
                self.crewBuffDisplay.destroy()
                self.crewBuffDisplay = None

    def checkAttuneBuffEffect(self):
        attuneBuffs = self.findAllBuffCopyKeys(WeaponGlobals.C_ATTUNE)
        if not attuneBuffs:
            if self.voodooAttuneEffect:
                self.voodooAttuneSound.stop()
                self.voodooAttuneSound = None
                self.voodooAttuneEffect.stopLoop()
                self.voodooAttuneEffect = None
            return
        if not self.voodooAttuneEffect:
            self.voodooAttuneEffect = AttuneEffect.getEffect()
            if self.voodooAttuneEffect:
                self.voodooAttuneEffect.reparentTo(self)
                self.voodooAttuneEffect.setPos(0, 0, self.getHeight())
                self.voodooAttuneEffect.startLoop()
        if self.voodooAttuneEffect:
            self.voodooAttuneSound = loader.loadSfx('audio/sfx_doll_attune_loop.wav')
            base.playSfx(self.voodooAttuneSound, looping=1, node=self, volume=0.25)
            buffColorType = None
            for buffKeyId in attuneBuffs:
                entry = self.skillEffects[buffKeyId]
                attackerId = entry[3]
                attacker = self.cr.doId2do.get(attackerId)
                if attacker:
                    if not TeamUtils.damageAllowed(attacker, self):
                        if buffColorType != 'hostile':
                            if buffColorType != 'localHostile' and (attackerId == localAvatar.doId or self.doId == localAvatar.doId):
                                buffColorType = 'localFriendly'
                            elif buffColorType != 'localFriendly':
                                buffColorType = 'friendly'
                    elif attackerId == localAvatar.doId or self.doId == localAvatar.doId:
                        buffColorType = 'localHostile'
                    elif buffColorType != 'localHostile' and buffColorType != 'localFriendly':
                        buffColorType = 'hostile'

            if buffColorType == 'localHostile':
                self.voodooAttuneEffect.setEffectColor(Vec4(0.2, 0.1, 0.5, 1))
            elif buffColorType == 'localFriendly':
                self.voodooAttuneEffect.setEffectColor(Vec4(0.2, 0.5, 0.1, 1))
            elif buffColorType == 'hostile':
                self.voodooAttuneEffect.setEffectColor(Vec4(0.0, 0.0, 0.0, 0.5))
            elif buffColorType == 'friendly':
                self.voodooAttuneEffect.setEffectColor(Vec4(0.0, 0.0, 0.0, 0.5))
        return

    def getPVPMoney(self):
        inv = self.getInventory()
        if inv:
            return inv.getStackQuantity(InventoryType.PVPCurrentInfamy)
        else:
            return 0

    def getMaxPVPMoney(self):
        inv = self.getInventory()
        if inv:
            return inv.getStackLimit(InventoryType.PVPCurrentInfamy)
        else:
            return 0

    def setMaxMoney(self, maxMoney):
        self.maxMoney = maxMoney

    def getMaxMoney(self):
        return self.maxMoney

    def setMoney(self, money):
        self.money = money

    def getMoney(self):
        return self.money

    def setMaxBankMoney(self, maxMoney):
        self.maxBankMoney = maxMoney

    def getMaxBankMoney(self):
        return self.maxBankMoney

    def setBankMoney(self, money):
        self.bankMoney = money

    def getBankMoney(self):
        return self.bankMoney

    def getTotalMoney(self):
        return self.getBankMoney() + self.getMoney()

    def updateReputation(self, category, value):
        DistributedReputationAvatar.updateReputation(self, category, value)

    def showHpText(self, number, pos=0, bonus=0, duration=2.0, scale=0.5, basicPenalty=0, crewBonus=0, doubleXPBonus=0, holidayBonus=0):
        if self.HpTextEnabled and not self.ghostMode and base.showGui:
            freebooter = not Freebooter.getPaidStatus(base.localAvatar.getDoId())
            distance = camera.getDistance(self)
            scale *= min(max(1.0, distance / 25.0), 20.0)
            startPos = (0, 0, 5.0)
            newEffect = None

            def cleanup():
                if newEffect in self.textEffects:
                    self.textEffects.remove(newEffect)

            mods = {}
            if basicPenalty > 0:
                mods[TextEffect.MOD_BASICPENALTY] = basicPenalty
            if crewBonus > 0:
                mods[TextEffect.MOD_CREWBONUS] = crewBonus
            if doubleXPBonus > 0:
                mods[TextEffect.MOD_2XPBONUS] = doubleXPBonus
            if holidayBonus > 0:
                mods[TextEffect.MOD_HOLIDAYBONUS] = holidayBonus
            newEffect = TextEffect.genTextEffect(self, self.HpTextGenerator, number, bonus, self.isNpc, cleanup, startPos, scale=scale, modifiers=mods)
            if newEffect:
                self.textEffects.append(newEffect)
        return

    def hideHpText(self, hpText=None):
        if hpText:
            index = self.hpTextNodes.index(hpText)
            self.hpTextIvals[index].finish()
            self.hpTextIvals[index] = None
            self.hpTextNodes[index].removeNode()
            self.hpTextNodes[index] = None
        return

    def showHpString(self, text, pos=0, duration=2.0, scale=0.5):
        if self.HpTextEnabled and not self.ghostMode and base.showGui:
            if text != '':
                self.HpTextGenerator.setFont(PiratesGlobals.getPirateOutlineFont())
                self.HpTextGenerator.setText(text)
                self.HpTextGenerator.clearShadow()
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                if self.isNpc:
                    r = 0.9
                    g = 0.1
                    b = 0.1
                    a = 1
                else:
                    r = 0.9
                    g = 0.3
                    b = 0.1
                    a = 1
                self.HpTextGenerator.setTextColor(r, g, b, a)
                hpTextNode = self.HpTextGenerator.generate()
                hpTextDummy = self.attachNewNode('hpTextDummy')
                hpText = hpTextDummy.attachNewNode(hpTextNode)
                distance = camera.getDistance(self)
                scale *= min(max(1.0, distance / 25.0), 20.0)
                hpText.setScale(scale)
                hpText.setBillboardPointEye(3.0)
                hpText.setBin('fixed', 100)
                hpText.setDepthWrite(0)
                hpText.setFogOff()
                hpText.setLightOff()
                if pos:
                    hpTextDummy.setPos(self, pos[0], pos[1], pos[2])
                else:
                    hpTextDummy.setPos(self, 0, 0, self.height * 0.666)
                hpTextDummy.setHpr(render, 0, 0, 0)
                numberMoveUp = hpText.posInterval(duration, Point3(0, 0, 8.0), startPos=Point3(0, 0, 2.0))
                fadeOut = hpText.colorScaleInterval(duration * 0.333, Vec4(r, g, b, 0), startColorScale=Vec4(r, g, b, a))
                track = Sequence(Parallel(numberMoveUp, Sequence(Wait(duration * 0.666), fadeOut)), Func(self.hideHpText, hpTextDummy))
                track.start()
                self.hpTextNodes.append(hpTextDummy)
                self.hpTextIvals.append(track)

    def newBackstab(self):
        self.showEffectString(PLocalizer.AttackBackstab, 0, 1.7, 0.46)

    def showEffectString(self, text, pos=0, duration=2.0, scale=0.5):
        if self.HpTextEnabled and not self.ghostMode and base.showGui:
            if text != '':
                self.HpTextGenerator.setFont(PiratesGlobals.getPirateOutlineFont())
                self.HpTextGenerator.setText(text)
                self.HpTextGenerator.clearShadow()
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                r = 0.99
                g = 0.84
                b = 0.01
                a = 1
                self.HpTextGenerator.setTextColor(r, g, b, a)
                hpTextNode = self.HpTextGenerator.generate()
                hpTextDummy = self.attachNewNode('hpTextDummy')
                hpText = hpTextDummy.attachNewNode(hpTextNode)
                distance = camera.getDistance(self)
                scale *= min(max(1.0, distance / 25.0), 20.0)
                hpText.setScale(scale)
                hpText.setBillboardPointEye(3.0)
                hpText.setBin('fixed', 100)
                hpText.setDepthWrite(0)
                hpText.setFogOff()
                hpText.setLightOff()
                if pos:
                    hpTextDummy.setPos(self, pos[0], pos[1], pos[2])
                else:
                    hpTextDummy.setPos(self, 0, 0, self.height * 0.8)
                hpTextDummy.setHpr(render, 0, 0, 0)
                numberScaleUp = hpText.scaleInterval(0.15, scale * 0.7, scale * 1.3)
                numberScaleDown = hpText.scaleInterval(0.15, scale * 1.3, scale)
                fadeOut = hpText.colorScaleInterval(duration * 0.162, Vec4(r, g, b, 0), startColorScale=Vec4(r, g, b, a))
                track = Sequence(numberScaleUp, Parallel(numberScaleDown, Sequence(Wait(duration * 0.333), fadeOut)), Func(self.hideHpText, hpTextDummy))
                track.start()
                self.hpTextNodes.append(hpTextDummy)
                self.hpTextIvals.append(track)

    def showHpMeter(self):
        DistributedReputationAvatar.showHpMeter(self)
        statusTray = localAvatar.guiMgr.targetStatusTray
        statusTray.updateName(self.getShortName(), self.level, self.doId)
        statusTray.updateHp(self.hp, self.maxHp, self.doId)
        statusTray.updateVoodoo(self.mojo, self.maxMojo, self.doId)
        statusTray.updateStatusEffects(self.skillEffects)
        statusTray.updateSkill(self.currentAttack, self.doId)
        statusTray.updateIcon(self.doId)
        sticky = localAvatar.currentTarget == self and localAvatar.hasStickyTargets()
        statusTray.updateSticky(sticky)
        statusTray.show()

    def hideHpMeter(self, delay=6.0):
        DistributedReputationAvatar.hideHpMeter(self, delay=delay)
        if base.localAvatar.guiMgr.targetStatusTray.doId == self.getDoId():
            if self.getTotalHp() <= 0:
                localAvatar.guiMgr.targetStatusTray.updateHp(0, self.maxHp)
            localAvatar.guiMgr.targetStatusTray.fadeOut(delay=delay)

    def getLandRoamIdleAnimInfo(self):
        return ('idle', 1.0)

    def setEnsnaredTargetId(self, avId):
        self.ensnaredTargetId = avId

    def getEnsnaredTargetId(self):
        return self.ensnaredTargetId

    def getRope(self, thickness=0.125):
        if not self.rope:
            rope = Rope.Rope()
            rope.ropeNode.setRenderMode(RopeNode.RMBillboard)
            rope.ropeNode.setUvMode(RopeNode.UVDistance)
            rope.ropeNode.setUvDirection(1)
            rope.ropeNode.setUvScale(0.5)
            ropeHigh = loader.loadModel('models/char/rope_high')
            ropeTex = ropeHigh.findTexture('rope_single_omit')
            if ropeTex != None:
                rope.setTexture(ropeTex)
            ropeHigh.removeNode()
            self.rope = rope
            ropeActor = Actor.Actor()
            ropeActor.loadModel('models/char/rope_high', 'modelRoot')
            ropeActor.loadAnims({'swing_aboard': 'models/char/rope_mtp_swing_aboard', 'board': 'models/char/rope_mtp_board'}, 'modelRoot')
            self.ropeActor = ropeActor
            self.ropeActor.setH(180)
            self.ropeEndNode = self.attachNewNode('ropeEndNode')
        self.rope.ropeNode.setThickness(thickness)
        return (
         self.rope, self.ropeActor, self.ropeEndNode)

    def startCompassEffect(self):
        if not self.isDisabled():
            self.stopCompassEffect()
            taskMgr.add(self.compassTask, self.uniqueName('compassTask'))

    def stopCompassEffect(self):
        taskMgr.remove(self.uniqueName('compassTask'))

    def compassTask(self, task):
        if not self.tracksTerrain:
            self.setR(render, 0)
        return Task.cont

    def setHeight(self, height):
        self.height = height
        self.adjustNametag3d()
        if self.collTube:
            self.collTube.setPointB(0, 0, height - self.getRadius())
            if self.collNodePath:
                self.collNodePath.forceRecomputeBounds()
        if self.battleTube:
            self.battleTube.setPointB(0, 0, max(10.0, height) - self.getRadius())
        for tube in self.aimTubeNodePaths:
            tube.node().modifySolid(0).setPointA(0, 0, -max(10.0, height))
            tube.node().modifySolid(0).setPointB(0, 0, max(10.0, height))

    def adjustNametag3d(self):
        defaultZ = 1
        scaleOffset = 0
        newZ = defaultZ
        if self.scale > 1:
            scaleOffset = self.scale - 1
            newZ = 5.4 * scaleOffset + defaultZ
        else:
            if 1 > self.scale:
                scaleOffset = 1 - self.scale
                newZ = 1 - scaleOffset * 5
        self.nametag3d.setPos(0, 0, newZ)

    def drainMojo(self, amt):
        self.sendUpdate('drainMojo', [amt])

    def isAirborne(self):
        return self.motionFSM.isAirborne()

    def printExpText(self, totalExp, colorSetting, basicPenalty, crewBonus, doubleXPBonus, holidayBonus):
        taskMgr.doMethodLater(0.5, self.showHpText, self.taskName('printExp'), [
         totalExp, 0, colorSetting, 5.0, 0.5, basicPenalty, crewBonus, doubleXPBonus, holidayBonus])

    def swapFloorCollideMask(self, oldMask, newMask):
        pass

    def setLevel(self, level):
        if level is None:
            if __dev__:
                import pdb
                pdb.set_trace()
            level = 0
        self.level = level
        return

    def getLevel(self):
        return self.level

    def motionFSMEnterState(self, anim):
        pass

    def motionFSMExitState(self, anim):
        pass

    def getAdjMaxHp(self):
        if self.isNpc:
            inv = 0
        else:
            inv = self.getInventory()
        if inv:
            if inv.getStackQuantity(InventoryType.Vitae_Level) > 0:
                return int(self.maxHp * 0.75)
            else:
                return self.maxHp
        else:
            return self.maxHp

    def getAdjMaxMojo(self):
        if self.isNpc:
            inv = 0
        else:
            inv = self.getInventory()
        if inv:
            if inv.getStackQuantity(InventoryType.Vitae_Level) > 0:
                return int(self.maxMojo * 0.75)
            else:
                return self.maxMojo
        else:
            return self.maxMojo

    def interrupted(self, effectId):
        pass

    def getSfx(self, name):
        return self.sfx.get(name)

    def getEnemyScale(self):
        return EnemyGlobals.getEnemyScale(self)

    def isBoss(self):
        return self.avatarType.isA(AvatarTypes.BossType)

    def getShortName(self):
        if self.isBoss():
            return self.getName()
        return self.avatarType.getShortName()

    def trackTerrain(self):
        if self.tracksTerrain == None:
            trackingCreatures = [
                AvatarTypes.Crab,
                AvatarTypes.RockCrab,
                AvatarTypes.GiantCrab,
                AvatarTypes.Pig,
                AvatarTypes.Dog,
                AvatarTypes.Scorpion,
                AvatarTypes.DreadScorpion,
                AvatarTypes.Alligator,
                AvatarTypes.BigGator,
                AvatarTypes.HugeGator
            ]
            if self.avatarType.getNonBossType() in trackingCreatures:
                self.tracksTerrain = True
            else:
                self.tracksTerrain = False
        if self.tracksTerrain:
            gNode = self.getGeomNode()
            if gNode and not gNode.isEmpty():
                if self.gNodeFwdPt == None:
                    self.gNodeFwdPt = gNode.getRelativePoint(self, Point3(0, 1, 0))
                parentObj = self.getParentObj()
                if parentObj:
                    gNode.headsUp(self.gNodeFwdPt, self.getRelativeVector(parentObj, self.floorNorm))
        return self.tracksTerrain

    def battleRandomSync(self):
        if hasattr(self, 'battleRandom'):
            self.battleRandom.resync()
