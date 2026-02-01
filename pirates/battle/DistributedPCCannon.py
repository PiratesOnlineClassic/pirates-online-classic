import math
import random
import copy
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.showbase.DirectObject import *
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.task import Task
from direct.showutil import Rope
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase
from pirates.battle import CannonGUI
from pirates.uberdog import UberDogGlobals
from pirates.ship import ShipGlobals
from pirates.effects.CannonExplosion import CannonExplosion
from pirates.effects.DirtClod import DirtClod
from pirates.effects.DustCloud import DustCloud
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.RockShower import RockShower
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.DustRing import DustRing
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.ExplosionCloud import ExplosionCloud
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.FireTrail import FireTrail
from pirates.effects.Fire import Fire
from pirates.effects.GreenBlood import GreenBlood
from pirates.effects.HitFlashA import HitFlashA
from pirates.effects.ShipDebris import ShipDebris
from pirates.effects.WoodShards import WoodShards
from pirates.piratesbase import Freebooter
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from . import DistributedWeapon
from . import WeaponGlobals
from . import CannonGlobals
from . import Cannon

class DistributedPCCannon(DistributedWeapon.DistributedWeapon):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPCCannon')

    def __init__(self, cr):
        DistributedWeapon.DistributedWeapon.__init__(self, cr)
        self.ship = None
        self.tutorial = 0
        self.prop = None
        self.baseVel = Vec3(0)
        self.mouseX = 0
        self.mouseY = 0
        self.setPos(0, 0, 0)
        self.moveCannon = 0
        self.av = None
        self.ball = None
        self.ship = None
        self.shipId = None
        self.tubeNP = None
        self.cgui = None
        self.numShots = 0
        self.grapplingHook = None
        self.cannonDressingNode = NodePath(ModelNode('dressingNode'))
        self.collisionLists = {}
        self.listening = False
        self.skillId = InventoryType.CannonShoot
        self.reloadTime = 0
        self.rechargeTime = 0
        self.volley = WeaponGlobals.getAttackVolley(self.skillId, self.getAmmoSkillId())
        self.modeFSM = ClassicFSM.ClassicFSM('modeFSM', [
            State.State('off', self.enterOff, self.exitOff),
            State.State('fireCannon', self.enterFireCannon, self.exitFireCannon),
            State.State('tutorialCutscene', self.enterTutorialCutscene, self.exitTutorialCutscene)], 'off', 'off')
        self.modeFSM.enterInitialState()
        self.aimAITrack = None
        self.headingNode = NodePath('dummy')
        OTPRender.renderReflection(False, self, 'p_cannon', None)
        self.emptySound = base.loader.loadSfx('audio/outofammo.mp3')
        self.fireSubframeCall = None
        self.__invRequest = None

    def generate(self):
        DistributedWeapon.DistributedWeapon.generate(self)
        if self.tutorial:
            tutorialMode = 'useCannon'
            proximityText = (None,)
        else:
            tutorialMode = None
            proximityText = (PLocalizer.InteractCannon,)
        self.setInteractOptions(tutorialMode = tutorialMode, proximityText = proximityText, diskRadius = 12.0, sphereScale = 8.0, endInteract = 0)

    def announceGenerate(self):
        self.loadModel()
        DistributedWeapon.DistributedWeapon.announceGenerate(self)

    def disable(self):
        self.ignoreAll()
        del self.emptySound
        taskMgr.remove(self.getTrailTaskName())
        if self.aimAITrack:
            self.aimAITrack.pause()
            self.aimAITrack = None

        self.av = None
        self.prop.av = None
        if self.prop:
            self.prop = None

        if self.grapplingHook:
            self.grapplingHook.removeNode()
            self.grapplingHook = None

        DistributedWeapon.DistributedWeapon.disable(self)

    def delete(self):
        self.modeFSM.request('off')
        del self.modeFSM
        DistributedWeapon.DistributedWeapon.delete(self)

    def getConeOriginNode(self):
        return self.prop.pivot

    def showUseInfo(self):
        if self.disk:
            self.disk.hide()

    def loadModel(self):
        self.prop = Cannon.Cannon(self.cr)
        self.prop.cannonPost = self.prop
        self.prop.shipId = self.shipId
        self.prop.doId = self.doId
        self.prop.reparentTo(self)
        self.prop.loadModel(None)
        self.prop.initializeCollisions()

    def requestInteraction(self, avId, interactType = 0):
        base.localAvatar.motionFSM.off()
        DistributedWeapon.DistributedWeapon.requestInteraction(self, avId, interactType)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterTutorialCutscene(self):
        pass

    def exitTutorialCutscene(self):
        pass

    def setVolley(self, volley):
        self.volley = volley
        if self.cgui:
            self.cgui.setVolley(volley)

    def enterFireCannon(self):
        localAvatar.guiMgr.combatTray.setLinkedCannon(self)
        self.accept('mouse1', self.fireCannon)
        self.accept('control', self.fireCannon)
        self.accept('wheel_up', self.changeAmmo, extraArgs = [
            1])
        self.accept('wheel_down', self.changeAmmo, extraArgs = [
            -1])
        self.accept(InteractiveBase.END_INTERACT_EVENT, self.handleEndInteractKey)
        localAvatar.cameraFSM.request('Cannon', self.prop)
        self.cgui = CannonGUI.CannonGUI(self)
        self.cgui.setAmmoId(self.getAmmoSkillId())
        self.setVolley(0)

        def gotInventory(inv):
            ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(self.getAmmoSkillId())
            maxShots = inv.getStackLimit(ammoInvId)
            self.numShots = inv.getStackQuantity(ammoInvId)
            if WeaponGlobals.isInfiniteAmmo(self.getAmmoSkillId()):
                self.cgui.setAmmoLeft(-1, -1)
            else:
                self.cgui.setAmmoLeft(self.numShots, maxShots)
            self.startReload()
            base.localAvatar.guiMgr.combatTray.initCombatTray(InventoryType.CannonRep)
            base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTray(rep = InventoryType.CannonRep, weaponMode = WeaponGlobals.CANNON)
            self.updateCannonDressing()

        if self.__invRequest:
            DistributedInventoryBase.cancelGetInventory(self.__invRequest)

        self.__invRequest = DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), gotInventory)

    def exitFireCannon(self):
        self.ignore('mouse1')
        self.ignore('control')
        self.ignore('wheel_up')
        self.ignore('wheel_down')
        self.ignore(InteractiveBase.END_INTERACT_EVENT)
        self.cgui.destroy()
        self.cgui = None
        localAvatar.guiMgr.combatTray.hideSkills()
        localAvatar.guiMgr.combatTray.disableTray()
        if self.fireSubframeCall:
            self.fireSubframeCall.cleanup()
            self.fireSubframeCall = None

        self.cannonDressingNode.detachNode()
        base.localAvatar.guiMgr.combatTray.skillTray.hideSkillTray()
        base.localAvatar.guiMgr.combatTray.initCombatTray(localAvatar.currentWeaponId)

    def requestExit(self):
        DistributedWeapon.DistributedWeapon.requestExit(self)
        self.stopWeapon(self.av)

    def selectAmmo(self, atype):
        dif = atype - self.getAmmoSkillId()
        self.changeAmmo(dif)

    def setAmmoSkillId(self, ammoSkillId):
        localAvatar.setCannonAmmoSkillId(ammoSkillId)

    def getAmmoSkillId(self):
        return localAvatar.getCannonAmmoSkillId()

    def changeAmmo(self, amt = 1):
        keepChanging = True
        ammoSkillId = self.getAmmoSkillId()
        while keepChanging:
            ammoSkillId += amt
            if ammoSkillId > InventoryType.CannonGrappleHook:
                ammoSkillId = InventoryType.CannonRoundShot

            if ammoSkillId < InventoryType.begin_WeaponSkillCannon + 1:
                ammoSkillId = InventoryType.CannonGrappleHook

            inv = base.localAvatar.getInventory()
            if inv.getStackQuantity(ammoSkillId) >= 2:
                keepChanging = False

            if WeaponGlobals.isInfiniteAmmo(ammoSkillId):
                keepChanging = False

            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                if not WeaponGlobals.canFreeUse(ammoSkillId):
                    keepChanging = True

        self.setAmmoSkillId(ammoSkillId)
        del ammoSkillId
        if WeaponGlobals.isInfiniteAmmo(self.getAmmoSkillId()):
            self.cgui.setAmmoLeft(-1, -1)
        else:
            ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(self.getAmmoSkillId())
            self.numShots = inv.getStackQuantity(ammoInvId)
            maxShots = inv.getStackLimit(ammoInvId)
            self.cgui.setAmmoLeft(self.numShots, maxShots)
        self.cgui.setAmmoId(self.getAmmoSkillId())
        self.updateCannonDressing()
        self.hideCannonDressing()
        self.setVolley(0)
        self.startReload()

    def updateReloadBar(self):
        if not self.av:
            return

        timeSpentReloading = 0.0
        recharge = self.av.skillDiary.getTimeSpentRecharging(self.skillId)
        if recharge:
            timeSpentReloading = recharge

        self.startReload(elapsedTime = timeSpentReloading)

    def updateCannonDressing(self):
        if self.getAmmoSkillId() != InventoryType.CannonGrappleHook:
            self.cannonDressingNode.detachNode()
            if self.grapplingHook:
                self.grapplingHook.removeNode()
                self.grapplingHook = None
        else:
            if self.ship:
                self.cannonDressingNode.reparentTo(self.ship.avCannonPivot)
            else:
                self.cannonDressingNode.reparentTo(self.prop.pivot)
            if not self.grapplingHook:
                self.grapplingHook = loader.loadModel('models/ammunition/GrapplingHook')

            if self.grapplingHook:
                self.grapplingHook.setPos(0.3, -3.0, -1.0)
                self.grapplingHook.reparentTo(self.cannonDressingNode)

    def showCannonDressing(self):
        self.cannonDressingNode.show()

    def hideCannonDressing(self):
        self.cannonDressingNode.hide()

    def setMovie(self, mode, avId):

        def doMovie(av):
            if mode == WeaponGlobals.WEAPON_MOVIE_START:
                self.startWeapon(av)
            elif mode == WeaponGlobals.WEAPON_MOVIE_STOP:
                self.stopWeapon(av)
            elif mode == WeaponGlobals.WEAPON_MOVIE_CLEAR:
                pass

        if self.pendingDoMovie:
            base.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
            self.pendingDoMovie = None

        self.pendingDoMovie = base.cr.relatedObjectMgr.requestObjects([
            avId], eachCallback = doMovie, timeout = 60)

    def startWeapon(self, av):
        if av == base.localAvatar:
            if base.localAvatar.cannon:
                return

            base.localAvatar.b_setGameState('Cannon')
            self.acceptInteraction()
            self.setLocalAvatarUsingWeapon(1)
            base.localAvatar.cannon = self
            if self.ship:
                self.ship.hideMasts()
                self.ship.stopSmoke()
                self.ship.listenForFloorEvents(0)

            localAvatar.guiMgr.request('MouseLook')
            self.modeFSM.request('fireCannon')
            base.localAvatar.collisionsOn()

        self.prop.hNode.setHpr(0, 0, 0)
        self.prop.pivot.setHpr(0, 0, 0)
        self.prop.currentHpr = (0, 0, 0)
        av.stopSmooth()
        av.setPos(self.prop, 0, -2.5, 0)
        av.setHpr(self.prop, 0, 0, 0)
        av.play('kneel_fromidle', toFrame = 16)
        self.av = av
        self.prop.av = av

    def stopWeapon(self, av):
        if av != base.localAvatar:
            return

        if base.localAvatar.cannon != self:
            return

        if not base.localAvatar.cannon:
            return

        self.setLocalAvatarUsingWeapon(0)
        base.localAvatar.cannon = None
        self.modeFSM.request('off')
        if av.gameFSM.state == 'Cannon':
            av.b_setGameState(av.gameFSM.defaultState)

        av.startSmooth()
        self.av = None
        self.prop.av = None
        self.prop.hNode.setHpr(0, 0, 0)
        self.prop.pivot.setHpr(0, 0, 0)
        self.prop.currentHpr = (0, 0, 0)

    def fireCannon(self):
        rechargingTime = base.localAvatar.skillDiary.getTimeRemaining(self.skillId)
        if rechargingTime > 0:
            return

        if self.fireSubframeCall:
            self.fireSubframeCall.cleanup()

        self.fireSubframeCall = SubframeCall(self._doFireCannon, 10, self.uniqueName('fireCannon'))

    def _doFireCannon(self):
        if self.volley > 0:
            h = self.prop.hNode.getH(render)
            p = self.prop.pivot.getP(render)
            r = 0
            pos = self.prop.cannonExitPoint.getPos(render)
            posHpr = [
                pos[0],
                pos[1],
                pos[2],
                h,
                p,
                r]
            charge = 0.0
            timestamp = globalClockDelta.getFrameNetworkTime(bits = 32)
            self.sendRequestProjectileSkill(self.skillId, self.getAmmoSkillId(), posHpr, charge, timestamp)
            self.prop.playAttack(self.skillId, self.getAmmoSkillId(), self.projectileHitEvent, buffs = localAvatar.getSkillEffects())
            self.setVolley(self.volley - 1)
            if not WeaponGlobals.isInfiniteAmmo(self.getAmmoSkillId()) and not base.config.GetBool('infinite-ammo', 0):
                inv = base.localAvatar.getInventory()
                ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(self.getAmmoSkillId())
                maxShots = inv.getStackLimit(ammoInvId)
                self.numShots -= 1
                self.cgui.setAmmoLeft(self.numShots, maxShots)

            self.hideCannonDressing()
            base.localAvatar.skillDiary.startRecharging(self.skillId, 0)
            self.startReload()
        else:
            base.playSfx(self.emptySound)
        for i in range(len(localAvatar.guiMgr.combatTray.skillTray.traySkillMap)):
            if localAvatar.guiMgr.combatTray.skillTray.traySkillMap[i] == self.getAmmoSkillId():
                button = localAvatar.guiMgr.combatTray.skillTray.tray[i + 1]
                if button.skillStatus is True:
                    button.updateQuantity(self.numShots)

    def useProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, charge):
        (x, y, z, h, p, r) = posHpr
        if not self.localAvatarUsingWeapon:
            self.prop.hNode.setH(render, h)
            self.prop.pivot.setP(render, p)
            buffs = []
            if self.av:
                buffs = self.av.skillEffects

            self.prop.playAttack(skillId, ammoSkillId, self.projectileHitEvent, buffs = buffs)

    def doAIAttack(self, x, y, z, tzone, skillId, ammoSkillId, timestamp):
        if not (self.cr.activeWorld and self.cr.activeWorld.worldGrid):
            return

        buffs = []
        if self.av:
            buffs = self.av.getSkillEffects()

        zonePos = self.cr.activeWorld.worldGrid.getZoneCellOrigin(tzone)
        targetPos = Point3(zonePos[0] + x, zonePos[1] + y, zonePos[2] + z)
        self.prop.hNode.lookAt(render, targetPos)
        p = self.prop.hNode.getP()
        self.prop.pivot.setP(p)
        self.prop.hNode.setP(0)
        self.prop.playAttack(skillId, ammoSkillId, self.projectileHitEvent, targetPos, buffs = buffs, timestamp = timestamp)
        if __dev__ and base.config.GetBool('show-ai-cannon-targets', 0):
            self.tracker.setPos(render, targetPos)

    def getTrailTaskName(self):
        return self.uniqueName('cannonTrail')

    def destroy(self):
        self.ignoreAll()
        self.removeNode()

    def startReload(self, elapsedTime = 0):
        self.stopReload()
        if self.numShots == 0 and not WeaponGlobals.isInfiniteAmmo(self.getAmmoSkillId()):
            return

        self.rechargeTime = self.cr.battleMgr.getModifiedReloadTime(self.av, self.skillId, self.getAmmoSkillId())
        self.cgui.startReload(self.rechargeTime, self.volley, elapsedTime = elapsedTime, doneCallback = self.finishReload)

    def stopReload(self):
        self.cgui.stopReload()

    def finishReload(self):
        newVolley = WeaponGlobals.getAttackVolley(self.skillId, self.getAmmoSkillId())
        if newVolley > self.numShots and not WeaponGlobals.isInfiniteAmmo(self.getAmmoSkillId()):
            newVolley = self.numShots

        self.setVolley(newVolley)
        self.showCannonDressing()

    def setUserId(self, avId):
        DistributedWeapon.DistributedWeapon.setUserId(self, avId)
        self.checkInUse()

    def checkInUse(self):
        if self.userId and self.userId != localAvatar.doId:
            self.setAllowInteract(0)
        else:
            self.setAllowInteract(1)

    def setAllowInteract(self, allow, forceOff = False):
        DistributedWeapon.DistributedWeapon.setAllowInteract(self, allow)
        if not allow and forceOff:
            self.requestExit()

    def completeCannonCheck(self):
        for colList in list(self.collisionLists.values()):
            colList.sort()
            ammo = colList[0][1].getFromNodePath().getPythonTag('ammo')
            if not ammo or ammo.destroyed:
                continue

            for entryData in colList:
                DistributedWeapon.DistributedWeapon.projectileHitObject(self, entryData[1])
                if ammo.destroyed:
                    break

        self.collisionLists = {}
        self.listening = False

    def projectileHitObject(self, entry):
        shot = int(entry.getFromNodePath().getNetTag('shotNum'))
        if not self.collisionLists.get(shot):
            self.collisionLists[shot] = []

        spoint = entry.getSurfacePoint(entry.getIntoNodePath())
        y = entry.getSurfacePoint(entry.getIntoNodePath())[1]
        self.collisionLists[shot].append((y, entry))
        if not self.listening:
            self.listening = True
            self.acceptOnce('event-loop-done', self.completeCannonCheck)
