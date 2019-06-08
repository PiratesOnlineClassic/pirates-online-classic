import random
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.fsm import FSM
from direct.task import Task
from direct.showbase.PythonUtil import lerp, report, getShortestRotation
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.reputation import ReputationGlobals
from pirates.interact import InteractiveBase
from pirates.effects.Twister import Twister
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui.RewardPanel import RewardPanel
from PlayerPirateGameFSM import PlayerPirateGameFSM

from libotp import *

class LocalPirateGameFSM(PlayerPirateGameFSM):
    notify = directNotify.newCategory('LocalPirateGameFSM')

    def __init__(self, av):
        PlayerPirateGameFSM.__init__(self, av, 'LocalPirateGameFSM')
        self.enterBattleEvent = 'enemyTargeted'
        self.battleMusicNames = ('combat_a', 'combat_b', 'combat_c')
        self.battleMusicName = None
        self.setDefaultGameState()
        self.teleportTrack = None
        self.teleportEffect = None
        self.doorWalkTrack = None
        self.kickTrack = None
        self.enterTunnelSequence = None
        self.lockFSM = False
        self.camIval = None

    def cleanup(self):
        PlayerPirateGameFSM.cleanup(self)
        if self.teleportTrack:
            self.teleportTrack.pause()
            self.teleportTrack = None

        if self.teleportEffect:
            self.teleportEffect.cleanUpEffect()
            self.teleportEffect = None

        if self.doorWalkTrack:
            self.doorWalkTrack.pause()
            self.doorWalkTrack = None

        if self.kickTrack:
            self.kickTrack.pause()
            self.kickTrack = None

        if self.deathTrack:
            self.deathTrack.pause()
            self.deathTrack = None

        if self.camIval:
            self.camIval.pause()
            self.camIval = None

    def setDefaultGameState(self, state = 'LandRoam'):
        self.defaultState = state

    def defaultFilter(self, request, args):
        if self.lockFSM:
            if request in ('LandRoam', 'NPCInteract'):
                return None

        if request == 'Battle':
            noBattleStates = ('Death', 'ShipBoarding', 'Ensnared', 'Thrown', 'Knockdown', 'ThrownInJail', 'Unconcious', 'ParlorGame', 'PVPWait', 'EnterTunnel')
            if self.defaultState not in ('Battle',):
                noBattleStates += ('WaterRoam',)

            if self.state in noBattleStates:
                return None

            if self.state in ('Cannon', 'NPCInteract', 'Digging', 'Searching', 'ShipPilot', 'DinghyInteract', 'ShipRepair'):
                messenger.send(InteractiveBase.END_INTERACT_EVENT)
                return ('Battle',) + args

            if self.state in 'Dialog':
                return ('Battle',) + args

        if self.state == 'Death':
            if request not in ('Off', 'ThrownInJail', 'Unconcious', 'TeleportIn', 'LandRoam', 'PVPWait'):
                return None

        elif self.state == 'TeleportOut':
            if request in ('NPCInteract', 'DinghyInteract', 'DoorInteract'):
                return None

        return PlayerPirateGameFSM.defaultFilter(self, request, args)

    def enterOff(self, extraArgs = []):
        self.av.cameraFSM.request('Off')
        PlayerPirateGameFSM.enterOff(self, extraArgs)

    @report(types=['deltaStamp'], dConfigParam='want-teleport-report')
    def enterLandRoam(self, extraArgs = []):
        self.accept('localAvatarEnterWater', self.handleLocalAvatarEnterWater)
        base.cr.interactionMgr.start()
        self.av.speedIndex = PiratesGlobals.SPEED_NORMAL_INDEX
        self.av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[self.av.speedIndex])
        self.av.guiMgr.request('Interface')
        self.av.controlManager.use('walk', self.av)
        self.av.controlManager.get('walk').lifter.setGravity(32.174 * 2.0)
        self.av.controlManager.collisionsOn()
        self.av.setLifterDelayFrames(3)
        self.av.cameraFSM.request('FPS')
        self.accept(WeaponGlobals.LocalAvatarUseItem, self.av.composeRequestTargetedSkill)
        if self.av.ship:
            self.av.setSurfaceIndex(PiratesGlobals.SURFACE_WOOD)
        else:
            self.av.setSurfaceIndex(PiratesGlobals.SURFACE_DEFAULT)
        PlayerPirateGameFSM.enterLandRoam(self)
        self.av.enableMouseWeaponDraw()
        self.av.updatePlayerSpeed()
        self.av.delayAFK()

    def exitLandRoam(self):
        self.ignore('localAvatarEnterWater')
        base.cr.interactionMgr.stop()
        self.ignore(WeaponGlobals.LocalAvatarUseItem)
        PlayerPirateGameFSM.exitLandRoam(self)
        self.av.disableMouseWeaponDraw()

    def enterWaterRoam(self, extraArgs = []):
        self.accept('localAvatarExitWater', self.handleLocalAvatarExitWater)
        if self.av.setWeaponIval and self.av.setWeaponIval.isPlaying():
            self.av.setWeaponIval.finish()

        self.av.speedIndex = PiratesGlobals.SPEED_NORMAL_INDEX
        self.av.guiMgr.request('Interface')
        self.av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[self.av.speedIndex])
        self.av.controlManager.use('walk', self.av)
        self.av.controlManager.get('walk').lifter.setGravity(0.0)
        self.av.controlManager.get('walk').lifter.setVelocity(0.0)
        self.av.controlManager.disableAvatarJump()
        self.av.startBobSwimTask()
        base.cr.interactionMgr.start()
        self.av.cameraFSM.request('FPS')
        self.accept(WeaponGlobals.LocalAvatarUseItem, self.av.composeRequestTargetedSkill)
        self.av.setSurfaceIndex(PiratesGlobals.SURFACE_WATER)
        self.av.b_setTeleportFlag(PiratesGlobals.TFInWater, self.av.confirmSwimmingTeleport)
        PlayerPirateGameFSM.enterWaterRoam(self)
        self.av.updatePlayerSpeed()
        self.av.delayAFK()

    def exitWaterRoam(self):
        self.ignore('localAvatarExitWater')
        self.av.controlManager.get('walk').lifter.setGravity(32.174 * 2.0)
        self.av.controlManager.enableAvatarJump()
        self.av.stopBobSwimTask()
        base.cr.interactionMgr.stop()
        self.ignore(WeaponGlobals.LocalAvatarUseItem)
        self.av.b_clearTeleportFlag(PiratesGlobals.TFInWater)
        PlayerPirateGameFSM.exitWaterRoam(self)

    def enterUnconcious(self, extraArgs = []):
        PlayerPirateGameFSM.enterUnconcious(self)
        self.av.controlManager.collisionsOff()
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('Control')
        base.transitions.letterboxOn()
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.lock()
        self.av.stopAutoRun()
        camera.setPos(self.av, 0.5, -14, 6)
        camera.wrtReparentTo(self.av.getParent())
        camera.lookAt(self.av.headNode)
        task = taskMgr.add(self.trackNode, 'cameraPlayerTracking')
        task.lookAtNode = self.av.headNode
        task.lookAtOffset = Point3(0)

    def exitUnconcious(self):
        PlayerPirateGameFSM.exitUnconcious(self)
        self.av.controlManager.collisionsOn()
        base.transitions.letterboxOff()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        taskMgr.remove('cameraPlayerTracking')

    def enterSpawn(self, extraArgs = []):
        PlayerPirateGameFSM.enterSpawn(self)
        self.av.setScale(1, 1, 1)
        self.spawnIval = Sequence(Func(base.transitions.fadeOut, 0), Func(self.av.guiMgr.request, 'Interface'), Func(self.av.cameraFSM.request, 'Control'), Func(base.transitions.fadeIn, 2), Func(self.av.b_setGameState, self.defaultState))
        self.spawnIval.start()

    def exitSpawn(self):
        PlayerPirateGameFSM.exitSpawn(self)
        self.spawnIval.pause()
        del self.spawnIval

    def enterBattle(self, extraArgs = []):
        if base.cr.activeWorld == None:
            return None

        self.accept('localAvatarEnterWater', self.handleLocalAvatarEnterWater)
        self.av.speedIndex = PiratesGlobals.SPEED_BATTLE_INDEX
        self.av.guiMgr.request('Interface')
        self.av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[self.av.speedIndex])
        self.av.controlManager.use('walk', self.av)
        if self.av.ship:
            self.battleMusicName = 'he_is_a_pirate'
        else:
            self.battleMusicName = random.choice(self.battleMusicNames)
        base.musicMgr.request(self.battleMusicName, priority = 1, looping = 1, volume = 0.6)
        base.cr.targetMgr.startFollowAim()
        base.cr.interactionMgr.start()
        self.av.hideName()
        self.av.cameraFSM.request('FPS')
        self.av.cameraFSM.fpsCamera.avFaceCamera()
        self.accept(WeaponGlobals.LocalAvatarUseTargetedSkill, self.av.composeRequestTargetedSkill)
        self.accept(WeaponGlobals.LocalAvatarUseProjectileSkill, self.av.composeRequestProjectileSkill)
        self.accept(WeaponGlobals.LocalAvatarUseItem, self.av.composeRequestTargetedSkill)
        self.accept('requestGearExit', self.av.requestExitBattle)
        self.accept(InteractiveBase.END_INTERACT_EVENT, self.av.requestExitBattle)
        self.av.guiMgr.combatTray.showSkills()
        PlayerPirateGameFSM.enterBattle(self)
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)
        NametagGlobals.setMasterNametagsActive(0)
        self.av.updatePlayerSpeed()

    def exitBattle(self):
        self.ignore('localAvatarEnterWater')
        base.musicMgr.requestFadeOut(self.battleMusicName)
        self.av.guiMgr.combatTray.clearQueues()
        if base.cr.targetMgr:
            base.cr.targetMgr.stopFollowAim()

        base.cr.interactionMgr.stop()
        self.av.sendRequestRemoveStickyTargets(self.av.stickyTargets)
        self.av.setStickyTargets([])
        self.av.showName()
        self.av.l_setCurrentWeapon(self.av.currentWeaponId, 0)
        self.av.d_requestCurrentWeapon(self.av.currentWeaponId, 0)
        self.av.setAimMod(0)
        self.av.stopLookAtTarget()
        self.ignore(WeaponGlobals.LocalAvatarUseTargetedSkill)
        self.ignore(WeaponGlobals.LocalAvatarUseProjectileSkill)
        self.ignore(WeaponGlobals.LocalAvatarUseItem)
        self.ignore('requestGearExit')
        self.ignore(InteractiveBase.END_INTERACT_EVENT)
        self.av.guiMgr.combatTray.hideSkills()
        self.av.guiMgr.combatTray.disableTray()
        PlayerPirateGameFSM.exitBattle(self)
        self.ignore('wheel_up')
        self.ignore('wheel_down')
        NametagGlobals.setMasterNametagsActive(1)

    def enterLandTreasureRoam(self, extraArgs = []):
        self.accept('localAvatarEnterWater', self.handleLocalAvatarEnterWater)
        self.av.speedIndex = PiratesGlobals.SPEED_CARRY_INDEX
        self.av.guiMgr.request('Interface')
        self.av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[self.av.speedIndex])
        self.av.controlManager.use('walk', self.av)
        base.cr.interactionMgr.start()
        messenger.send('carryingTreasure')
        PlayerPirateGameFSM.enterLandTreasureRoam(self)
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)
        self.av.updatePlayerSpeed()

    def exitLandTreasureRoam(self):
        self.ignore('localAvatarEnterWater')
        base.cr.interactionMgr.stop()
        messenger.send('notCarryingTreasure')
        PlayerPirateGameFSM.exitLandTreasureRoam(self)
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def enterWaterTreasureRoam(self, extraArgs = []):
        self.accept('localAvatarExitWater', self.handleLocalAvatarExitWater)
        self.av.speedIndex = PiratesGlobals.SPEED_CARRY_INDEX
        self.av.guiMgr.request('Interface')
        self.av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[self.av.speedIndex])
        self.av.controlManager.use('walk', self.av)
        self.av.controlManager.get('walk').lifter.setGravity(0.0)
        self.av.controlManager.get('walk').lifter.setVelocity(0.0)
        self.av.controlManager.disableAvatarJump()
        self.av.startBobSwimTask()
        base.cr.interactionMgr.start()
        self.av.cameraFSM.request('FPS')
        self.av.b_setTeleportFlag(PiratesGlobals.TFInWater, self.av.confirmSwimmingTeleport)
        PlayerPirateGameFSM.enterWaterTreasureRoam(self)
        self.av.updatePlayerSpeed()

    def exitWaterTreasureRoam(self):
        self.ignore('localAvatarExitWater')
        self.av.stopBobSwimTask()
        self.av.guiMgr.request('Interface')
        self.av.controlManager.get('walk').lifter.setGravity(32.174 * 2.0)
        self.av.controlManager.enableAvatarJump()
        base.cr.interactionMgr.stop()
        self.av.b_clearTeleportFlag(PiratesGlobals.TFInWater)
        PlayerPirateGameFSM.exitWaterTreasureRoam(self)

    def enterTeleportOut(self, extraArgs = []):
        self.notify.debug('enterTeleportOut() for avId: %d' % self.av.getDoId())
        self.av.motionFSM.request('MoveLock')
        self.av.controlManager.get('walk').lifter.setGravity(0.0)
        self.av.guiMgr.request('Cutscene')
        self.av.cameraFSM.request('FPS')
        base.cr.interactionMgr.stop(endCurrent = True)
        base.cr.interactionMgr.lock()
        self.av.nametag3d.hide()
        self.av.stopAutoRun()
        timeOffset = 0.0
        if len(extraArgs) >= 1:
            timeOffset = extraArgs[0]

        if len(extraArgs) >= 2:
            doneEvent = extraArgs[1]
        else:
            doneEvent = ''
        if len(extraArgs) >= 3:
            doEffect = extraArgs[2]
        else:
            doEffect = True
        if doEffect:
            if not self.teleportEffect:
                teleportAnimPlayRate = 1.5
                teleportAnimLength = self.av.getDuration('teleport') / teleportAnimPlayRate
                twisterFadeLength = 1.0
                totalLength = teleportAnimLength + twisterFadeLength
                avFadeOutLength = 2.0
                avFlyTime = 1.5
                avFlyHeight = 7
                screenFadeLength = 0.5

                def setRelZ(t):
                    self.av.getGeomNode().setZ(lerp(0, avFlyHeight, t))

                def attemptRemoveFromShip():
                    ship = self.av.getShip()
                    if ship and ship.isGenerated():
                        self.av.removeFromShip(ship)

                    if __dev__ and ship and not ship.isGenerated():
                        import pdb
                        pdb.set_trace()

                teleportTrack = Sequence()
                teleportPar = Parallel()
                self.teleportEffect = Twister.getEffect()
                if self.teleportEffect:
                    teleportTrack.append(Func(self.teleportEffect.reparentTo, self.av.getEffectParent()))
                    teleportPar.append(self.teleportEffect.getParticleInterval(totalLength))

                def playTeleportAnim():
                    self.av.play('teleport', blendOutT = 0.0)
                    self.av.setPlayRate(teleportAnimPlayRate, 'teleport')

                teleportPar.append(Func(playTeleportAnim))
                teleportPar.append(Sequence(Wait(teleportAnimLength - avFadeOutLength), Func(self.av.setTransparency, 1, 1001), LerpFunc(self.av.setColorScale, duration = avFadeOutLength, toData = Vec4(1, 1, 1, 0), fromData = Vec4(1, 1, 1, 1))))
                teleportPar.append(Sequence(Wait(avFlyTime), LerpFunc(setRelZ, duration = teleportAnimLength - avFlyTime)))
                teleportPar.append(Sequence(Wait(totalLength - screenFadeLength), Func(base.transitions.fadeOut), Wait(0.5), Func(base.cr.loadingScreen.show, waitForLocation = True)))
                teleportTrack.append(teleportPar)
                teleportTrack.append(Func(attemptRemoveFromShip))
                teleportTrack.append(Func(self.av.controlManager.collisionsOff))
                self.teleportTrack = teleportTrack

            self.teleportTrack.setDoneEvent(doneEvent)
            self.teleportTrack.start(timeOffset)
        elif doneEvent:
            messenger.send(doneEvent)

    def exitTeleportOut(self):
        self.notify.debug('exitTeleportOut() for avId: %d' % self.av.getDoId())
        self.ignore(base.cr.getAllInterestsCompleteEvent())
        self.teleportTrack.finish()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        self.av.motionFSM.on()
        self.av.getGeomNode().setZ(0)
        self.av.clearColorScale()
        self.av.clearTransparency()
        self.av.nametag3d.show()
        if base.cr.tutorial:
            if self.av.style.getTutorial():
                base.transitions.noFade()

        else:
            base.transitions.noFade()

    def enterTeleportIn(self, extraArgs = []):
        self.notify.debug('enterTeleportIn() for avId: %d' % self.av.getDoId())
        self.av.guiMgr.request('Cutscene')
        self.av.motionFSM.request('MoveLock')
        base.transitions.fadeIn(finishIval = Func(self.av.b_setGameState, 'LandRoam'))
        self.av.stopAutoRun()

    def exitTeleportIn(self):
        self.notify.debug('exitTeleportIn() for avId: %d' % self.av.getDoId())
        self.av.motionFSM.on()
        base.cr.loadingScreen.hide()

    def enterShipPilot(self, extraArgs = []):
        ship = extraArgs[1]
        s = MiniLogSentry(ship.miniLog, 'enterShipPilot')
        self.av.guiMgr.request('Interface')
        self.av.guiMgr.hideSeaChest()
        self.av.guiMgr.combatTray.initCombatTray(InventoryType.SailingRep)
        self.av.stopAutoRun()
        self.accept(WeaponGlobals.LocalAvatarUseTargetedSkill, self.av.composeRequestTargetedSkill)
        self.accept(WeaponGlobals.LocalAvatarUseProjectileSkill, self.av.composeRequestProjectileSkill)
        self.accept(WeaponGlobals.LocalAvatarUseItem, self.av.composeRequestTargetedSkill)
        self.accept(WeaponGlobals.LocalAvatarUseShipSkill, self.av.composeRequestShipSkill)
        self._usingRepairKit = False
        if localAvatar.getSiegeTeam():
            self.accept(self.av.cr.distributedDistrict.siegeManager.getUseRepairKitEvent(), self._handleUseRepairKit)
            self._handleUseRepairKit(self.av.cr.distributedDistrict.siegeManager.getUseRepairKit())

        if localAvatar.getParentObj() is not ship or __dev__:
            if ship.miniLog:
                ship.miniLog.appendLine("localAvatar's parent: (%s)" % (localAvatar.getParentObj(),))

            logBlock(3, ship.miniLog)

        ship.resetMiniLog()
        ship.placeAvatarAtWheel(self.av)
        PlayerPirateGameFSM.enterShipPilot(self, [ship])

    def _handleUseRepairKit(self, useRepairKit):
        if useRepairKit and not self._usingRepairKit:
            localAvatar.guiMgr.combatTray.enableShipRepair()
        elif not useRepairKit and self._usingRepairKit:
            localAvatar.guiMgr.combatTray.disableShipRepair()

        self._usingRepairKit = useRepairKit

    def exitShipPilot(self):
        self._handleUseRepairKit(False)
        self.av.guiMgr.combatTray.disableTray()
        self.ignore(WeaponGlobals.LocalAvatarUseShipSkill)
        self.ignore(WeaponGlobals.LocalAvatarUseItem)
        self.ignore(WeaponGlobals.LocalAvatarUseTargetedSkill)
        self.ignore(WeaponGlobals.LocalAvatarUseProjectileSkill)
        PlayerPirateGameFSM.exitShipPilot(self)

    def enterDigging(self, extraArgs = []):
        PlayerPirateGameFSM.enterDigging(self)
        base.musicMgr.request('searching', looping = 0, priority = 1)
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('FPS')
        base.transitions.letterboxOn()
        self.av.stopAutoRun()
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)

    def exitDigging(self):
        PlayerPirateGameFSM.exitDigging(self)
        base.musicMgr.requestFadeOut('searching')
        base.transitions.letterboxOff()
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def enterSearching(self, extraArgs = []):
        PlayerPirateGameFSM.enterSearching(self)
        base.musicMgr.request('searching', looping = 0, priority = 1)
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('FPS')
        base.transitions.letterboxOn()
        self.av.stopAutoRun()
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)

    def exitSearching(self):
        PlayerPirateGameFSM.exitSearching(self)
        base.musicMgr.requestFadeOut('searching')
        base.transitions.letterboxOff()
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def enterStealing(self, extraArgs = []):
        PlayerPirateGameFSM.enterStealing(self)
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('FPS')
        base.transitions.letterboxOn()
        self.av.stopAutoRun()
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)

    def exitStealing(self):
        PlayerPirateGameFSM.exitStealing(self)
        base.transitions.letterboxOff()
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def enterWeaponReceive(self, extraArgs = []):
        self.notify.debug('enterWeaponReceive %s' % localAvatar.doId)
        PlayerPirateGameFSM.enterWeaponReceive(self)
        PlayerPirateGameFSM.enterEmote(self)
        self.rewardPanel = None
        self.startWeaponReceive()

    def startWeaponReceive(self):
        base.transitions.letterboxOn()
        self.av.guiMgr.request('Interface', [True, False])
        self.av.guiMgr.toggleGuiForNpcInteraction(0)
        self.av.stopAutoRun()
        print 'startWeaponReceive'
        dummy = localAvatar.attachNewNode('dummy')
        dummy.setPos(localAvatar.headNode.getX(localAvatar), localAvatar.headNode.getY(localAvatar) + 10, localAvatar.headNode.getZ(localAvatar) + 3)
        dummy.wrtReparentTo(render)
        dummy.lookAt(localAvatar, localAvatar.headNode.getX(localAvatar), localAvatar.headNode.getY(localAvatar), localAvatar.headNode.getZ(localAvatar) * 0.95)
        camPos = dummy.getPos()
        camHpr = dummy.getHpr()
        dummy.detachNode()
        camera.wrtReparentTo(render)
        camH = camera.getH() % 360
        h = camHpr[0] % 360
        if camH > h:
            h += 360

        if h - camH > 180:
            h -= 360

        camHpr.setX(h)
        camera.setH(camH)
        if self.camIval:
            self.camIval.pause()

        t = 1.5
        duration = 0.0
        if self.av.playRewardAnimation:
            emote = self.av.getEmote(self.av.playRewardAnimation)
            if emote:
                duration = self.av.getDuration(emote[0])

        def createRewardPanel(state):
            emote = state.av.getEmote(state.av.playRewardAnimation)
            if emote and emote[1]:
                state.rewardPanel = RewardPanel(aspect2d, type = state.av.playRewardAnimation, doneCallback = self.handleExitWeaponReceive)

        self.camIval = Sequence(camera.posHprInterval(t, pos = camPos, hpr = camHpr, blendType = 'easeOut'), Func(self.av.playEmote, self.av.playRewardAnimation), Wait(duration), Func(createRewardPanel, self))
        self.av.cameraFSM.request('Control')
        self.camIval.start()

    def exitWeaponReceive(self):
        PlayerPirateGameFSM.exitWeaponReceive(self)
        PlayerPirateGameFSM.exitEmote(self)
        self.endWeaponReceive()
        if self.av:
            if self.av.playRewardAnimation is not None:
                self.av.playRewardAnimation = None


        if self.rewardPanel:
            self.rewardPanel.cleanup()
            self.rewardPanel = None
        else:
            self.rewardPanel = RewardPanel(aspect2d, doneCallback = self.handleExitWeaponReceive)

    def endWeaponReceive(self):
        self.av.guiMgr.subtitler.clearText()
        base.transitions.letterboxOff()
        self.av.guiMgr.toggleGuiForNpcInteraction(1)
        if self.camIval:
            self.camIval.pause()
            self.camIval = None

    def handleExitWeaponReceive(self):
        if self.getCurrentOrNextState() == 'LandRoam':
            if self.rewardPanel:
                self.rewardPanel.cleanup()
                self.rewardPanel = None

        if self.av:
            self.av.b_setGameState('LandRoam')

    def enterNPCInteract(self, extraArgs = []):
        if len(extraArgs) != 3:
            self.notify.error('Unexpected number of extraArgs!')
            return

        (timeElapsed, npc, hasMenu) = extraArgs
        self.notify.debug('enterNPCInteract %s' % npc.doId)
        PlayerPirateGameFSM.enterNPCInteract(self)
        self.startNPCInteract(npc, hasMenu)

    def startNPCInteract(self, npc, hasMenu = True):
        base.transitions.letterboxOn()
        self.av.guiMgr.request('Interface', [True, False])
        self.av.guiMgr.toggleGuiForNpcInteraction(0)
        self.av.stopAutoRun()
        npc.playInteraction(hasMenu = hasMenu)
        print 'startNPCInteract'
        if npc.interactCamPosHpr:
            camPos = npc.interactCamPosHpr[0]
            camHpr = npc.interactCamPosHpr[1]
        else:
            dummy = npc.attachNewNode('dummy')
            dummy.setPos(npc.headNode.getX(npc), npc.headNode.getY(npc) + 4.5, npc.headNode.getZ(npc) + 1)
            dummy.wrtReparentTo(render)
            dummy.lookAt(npc, npc.headNode.getX(npc), npc.headNode.getY(npc), npc.headNode.getZ(npc) * 0.95)
            if hasMenu:
                dummy.setH(dummy, 15)

            camPos = dummy.getPos()
            camHpr = dummy.getHpr()
            dummy.detachNode()
        camera.wrtReparentTo(render)
        camH = camera.getH() % 360
        h = camHpr[0] % 360
        if camH > h:
            h += 360

        if h - camH > 180:
            h -= 360

        camHpr.setX(h)
        camera.setH(camH)
        if self.camIval:
            self.camIval.pause()

        t = 1.5
        self.camIval = Parallel(camera.posHprInterval(t, pos = camPos, hpr = camHpr, blendType = 'easeOut'), Sequence(Func(self.av.setTransparency, 1), self.av.colorScaleInterval(t / 2, VBase4(1, 1, 1, 0)), Func(self.av.hide)))
        self.av.cameraFSM.request('Control')
        self.camIval.start()

    def exitNPCInteract(self):
        PlayerPirateGameFSM.exitNPCInteract(self)
        self.endNPCInteract()

    def endNPCInteract(self):
        self.av.guiMgr.subtitler.clearText()
        base.transitions.letterboxOff()
        self.av.guiMgr.toggleGuiForNpcInteraction(1)
        if self.camIval:
            self.camIval.pause()
            self.camIval = None

        self.av.setColorScale(1, 1, 1, 1)
        self.av.setTransparency(0)
        self.av.show()

    def enterDinghyInteract(self, extraArgs = []):
        if len(extraArgs) != 2:
            self.notify.warning('Unexpected number of extraArgs!')
            return

        (timestamp, dinghy) = extraArgs
        self.notify.debug('enterDinghyInteract')
        PlayerPirateGameFSM.enterDinghyInteract(self)
        base.transitions.letterboxOn()
        self.av.guiMgr.request('Interface')
        self.av.guiMgr.toggleGuiForNpcInteraction(0)
        self.av.stopAutoRun()
        self.av.cameraFSM.request('Control')

    def exitDinghyInteract(self):
        PlayerPirateGameFSM.exitDinghyInteract(self)
        base.transitions.letterboxOff()
        self.av.guiMgr.toggleGuiForNpcInteraction(1)
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.start()

    def enterDoorInteract(self, extraArgs = []):
        self.av.guiMgr.request('Cutscene')
        self.av.motionFSM.off()
        self.av.controlManager.collisionsOn()
        base.transitions.letterboxOn()
        self.av.stopAutoRun()

    def exitDoorInteract(self):
        self.av.motionFSM.on()
        if self.doorWalkTrack:
            self.doorWalkTrack.pause()
            self.doorWalkTrack = None

        base.transitions.letterboxOff()

    def enterCutscene(self, extraArgs = []):
        self.av.guiMgr.request('Cutscene')
        self.av.cameraFSM.request('Control')
        self.av.guiMgr._hideCursor()
        print 'enterCutscene'
        self.av.motionFSM.off()
        if base.camLens.getAspectRatio() < 1.77:
            base.transitions.letterboxOn()

        self.av.stopAutoRun()
        self.av.hideQuestArrow()

    def exitCutscene(self):
        self.av.motionFSM.on()
        base.transitions.letterboxOff()
        if not self.av.guiMgr.ignoreAllKeys:
            self.av.guiMgr.showTrays()

        self.av.guiMgr._showCursor()
        self.av.showQuestArrow()

    def enterDialog(self, extraArgs = []):
        self.av.stopAutoRun()
        if self.av.currentDialogMovie is None or not self.av.currentDialogMovie.enableCameraLock:
            self.av.cameraFSM.request('Control')

        self.av.motionFSM.off()

    def exitDialog(self):
        pass

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def enterShipBoarding(self, extraArgs = []):
        self.av.guiMgr.request('Cutscene')
        self.av.motionFSM.request('MoveLock')
        self.av.controlManager.collisionsOff()
        self.av.cameraFSM.request('FPS')
        base.transitions.letterboxOn()
        PlayerPirateGameFSM.enterShipBoarding(self, extraArgs)
        self.av.stopAutoRun()

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def exitShipBoarding(self):
        PlayerPirateGameFSM.exitShipBoarding(self)
        self.av.controlManager.collisionsOn()
        base.transitions.letterboxOff()

    def enterCannon(self, extraArgs = []):
        self.notify.debug('enterCannon for avId: %d' % self.av.getDoId())
        PlayerPirateGameFSM.enterCannon(self)
        base.cr.interactionMgr.stop()
        self.av.guiMgr.request('Interface')
        self.av.guiMgr.combatTray.hideSkills()
        self.av.guiMgr.combatTray.disableTray()
        NametagGlobals.setMasterNametagsActive(0)
        self.av.stopAutoRun()

    def exitCannon(self):
        self.notify.debug('exitCannon for avId: %d' % self.av.getDoId())
        PlayerPirateGameFSM.exitCannon(self)
        base.cr.interactionMgr.start()
        NametagGlobals.setMasterNametagsActive(1)

    def enterEnsnared(self, extraArgs = []):
        PlayerPirateGameFSM.enterEnsnared(self)
        self.av.guiMgr.request('Cutscene')
        self.av.controlManager.collisionsOff()
        self.av.cameraFSM.request('Control')
        base.transitions.letterboxOn()
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.lock()
        self.av.stopAutoRun()
        camera.setPos(self.av, 0.5, -14, 6)
        camera.wrtReparentTo(self.av.getParent())
        camera.lookAt(self.av.headNode)
        task = taskMgr.add(self.trackNode, 'cameraPlayerTracking')
        task.lookAtNode = self.av.headNode
        task.lookAtOffset = Point3(0)

    def filterEnsnared(self, request, args = []):
        if request == 'Ensnared':
            return

        return self.defaultFilter(request, args)

    def exitEnsnared(self):
        PlayerPirateGameFSM.exitEnsnared(self)
        self.av.controlManager.collisionsOn()
        base.transitions.letterboxOff()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        taskMgr.remove('cameraPlayerTracking')

    def enterThrown(self, extraArgs = []):
        PlayerPirateGameFSM.enterThrown(self)
        self.av.stopAutoRun()

    def exitThrown(self):
        PlayerPirateGameFSM.exitThrown(self)

    def enterKnockdown(self, extraArgs = []):
        PlayerPirateGameFSM.enterKnockdown(self)
        self.av.guiMgr.request('Interface')
        if self.av.controlManager.currentControls:
            self.av.controlManager.collisionsOff()

        self.av.cameraFSM.request('Control')
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.lock()
        task = taskMgr.add(self.trackNode, 'cameraPlayerTracking')
        task.lookAtNode = self.av.headNode
        task.lookAtOffset = Point3(0)

    def exitKnockdown(self):
        PlayerPirateGameFSM.exitKnockdown(self)
        if self.av.controlManager.currentControls:
            self.av.controlManager.collisionsOn()

        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        taskMgr.remove('cameraPlayerTracking')

    @report(types=['frameCount', 'args'], dConfigParam='want-jail-report')
    def enterDeath(self, extraArgs = []):
        base.musicMgr.request('death', priority = 1, looping = 0)
        self.av.guiMgr.request('Cutscene')
        timeOffset = 0.0
        if len(extraArgs) >= 1:
            timeOffset = extraArgs[0]

        if self.av.motionFSM:
            self.av.motionFSM.off()

        self.av.deleteBattleCollisions()
        if self.av.guiMgr.targetStatusTray.doId == self.av.doId:
            self.av.guiMgr.targetStatusTray.fadeOut()

        self.av.cameraFSM.request('Control')
        base.transitions.letterboxOn()
        curInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if curInteractive:
            curInteractive.requestExit()

        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.lock()
        self.av.stopAutoRun()
        camera.setPos(self.av, 0.5, -14, 6)
        camera.wrtReparentTo(self.av.getParent())
        camera.lookAt(self.av.headNode)
        task = taskMgr.add(self.trackNode, 'cameraPlayerTracking')
        task.lookAtNode = self.av.headNode
        task.lookAtOffset = Point3(0)
        if self.deathTrack:
            self.deathTrack.finish()
            self.deathTrack = None

        self.deathTrack = Sequence(self.av.getEnterDeathTrack(), Wait(2))
        if self.av.getSiegeTeam():
            self.deathTrack.append(Func(self.av.b_setGameState, 'LandRoam'))
        else:
            self.deathTrack.append(Func(base.transitions.fadeOut, 1))
            self.deathTrack.append(Func(base.cr.activeWorld.localAvEnterDeath, self.av))
        self.deathTrack.start(timeOffset)
        self.av.refreshStatusTray()

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def exitDeath(self):
        if self.deathTrack:
            self.deathTrack.finish()
            self.deathTrack = None

        self.av.controlManager.collisionsOn()
        base.transitions.letterboxOff()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        base.transitions.fadeIn(0)
        taskMgr.remove('cameraPlayerTracking')
        if base.cr.activeWorld:
            self.deathTrack = Sequence(self.av.getExitDeathTrack(), Func(base.cr.activeWorld.localAvExitDeath, self.av))
            self.deathTrack.start()

        base.musicMgr.requestFadeOut('death')
        self.av.refreshStatusTray()

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def enterThrownInJail(self, extraArgs = []):
        self.av.stopAutoRun()
        if self.jailTrack:
            self.jailTrack.finish()

        self.av.guiMgr.request('Cutscene')
        self.av.cameraFSM.request('FPS')
        self.av.motionFSM.off()
        self.av.collisionsOn()
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.lock()
        base.transitions.letterboxOn()
        base.cr.loadingScreen.show()
        self.av.hide()

        @report(types=['frameCount'], dConfigParam='want-jail-report')
        def receivedSpawnPt():
            spawnInfo = self.av.cr.activeWorld.spawnInfo
            parent = self.av.getParentObj()
            if not isinstance(parent, NodePath):
                logBlock(4, 'Player(%s) in jail, but parentObj is %s' % (self.av.doId, parent))
                return

            self.av.setPosHpr(self.av.getParentObj(), *spawnInfo[0])

            def reqDefState():
                if not self.isInTransition():
                    self.av.b_setGameState(self.defaultState)

            self.jailTrack = Sequence(Func(self.av.hide), Wait(3), Func(base.transitions.fadeIn, 1.25), Wait(0.25), Func(base.cr.loadingScreen.hide), Wait(1.75), Func(self.av.show), self.av.actorInterval('jail_dropinto', blendOutT = 0), self.av.actorInterval('jail_standup', blendInT = 0), Func(reqDefState))
            self.jailTrack.start()

        self.spawnPtEvent = self.av.cr.activeWorld.uniqueName('spawnInfoReceived')
        self.acceptOnce(self.spawnPtEvent, receivedSpawnPt)
        self.acceptOnce('localAvatar-setLocation', self.av.getParentObj().handleAvatarSetLocation)

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def exitThrownInJail(self):
        self.ignore(self.spawnPtEvent)
        self.ignore('localAvatar-setLocation')
        if self.jailTrack:
            self.jailTrack.finish()

        self.av.show()
        self.av.motionFSM.on()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        base.transitions.letterboxOff()
        self.av.displayMoraleMessage()

    def enterDoorKicking(self, extraArgs = []):
        self.av.guiMgr.request('Cutscene')
        self.av.cameraFSM.request('FPS')
        self.av.motionFSM.off()
        base.transitions.letterboxOn()
        kickT = self.av.getDuration('kick_door_loop')
        self.kickSfx = base.loadSfx('phase_4/audio/sfx_kick_door_loop.mp3')
        self.kickTrack = Sequence(Func(messenger.send, self.av.kickEvents[0]), Func(base.playSfx, self.kickSfx, node = self.av), Wait(kickT), Func(messenger.send, self.av.kickEvents[1]))
        self.kickTrack.loop()
        self.av.loop('kick_door_loop')
        self.av.stopAutoRun()
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)

    def exitDoorKicking(self):
        self.kickTrack.pause()
        self.kickTrack = None
        loader.unloadSfx(self.kickSfx)
        del self.kickSfx
        self.av.motionFSM.on()
        base.transitions.letterboxOff()
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def handleLocalAvatarEnterWater(self):
        world = base.cr.getActiveWorld()
        if world:
            world.handleLocalAvatarEnterWater()

    def handleLocalAvatarExitWater(self):
        world = base.cr.getActiveWorld()
        if world:
            world.handleLocalAvatarExitWater()

    def enterEmote(self, extraArgs = []):
        self.accept('localAvatarExitEmote', self.handleLocalAvatarExitEmote)
        PlayerPirateGameFSM.enterEmote(self)

    def exitEmote(self, extraArgs = []):
        self.ignore('localAvatarExitEmote')
        PlayerPirateGameFSM.exitEmote(self)

    def handleLocalAvatarExitEmote(self):
        if self.av:
            self.av.b_setGameState('LandRoam')

    def enterParlorGame(self, extraArgs = []):
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('Control')
        self.av.hideName()
        self.av.b_setTeleportFlag(PiratesGlobals.TFParlorGame)
        PlayerPirateGameFSM.enterParlorGame(self)
        self.av.stopAutoRun()

    def exitParlorGame(self):
        self.av.showName()
        self.av.b_clearTeleportFlag(PiratesGlobals.TFParlorGame)
        PlayerPirateGameFSM.exitParlorGame(self)

    def enterMakeAPirate(self, extraArgs = []):
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('Off')
        self.av.motionFSM.off()
        self.av.stopAutoRun()

    def exitMakeAPirate(self):
        pass

    def enterEnterTunnel(self, extraArgs = []):
        self.startLocalSequence()
        self.av.cameraFSM.request('Control')
        distance = 40
        speed = PiratesGlobals.PirateSpeeds[self.av.speedIndex][0]
        duration = distance / speed
        self.av.startPosHprBroadcast()
        moveSequence = Sequence(Parallel(self.moveForwardInterval(distance), Sequence(Wait(duration - 0.8), Func(base.transitions.fadeOut, 0.75), Wait(0.75))), Func(base.cr.loadingScreen.show, waitForLocation = True), Func(messenger.send, 'EnterTunnelFinished'))
        cameraY = camera.getY()
        if cameraY < 13:
            cameraY = 13

        if self.enterTunnelSequence:
            self.enterTunnelSequence.finish()
            self.enterTunnelSequence = None

        self.enterTunnelSequence = Parallel(self.lookMoveCameraSequence(duration / 2.0, Point3(0, -abs(cameraY), self.av.getHeight()), lookAtNode = self.av, lookAtOffset = Point3(0, 0, self.av.getHeight()), blendType = 'easeIn'), moveSequence)
        self.enterTunnelSequence.start()

    def exitEnterTunnel(self):
        if self.enterTunnelSequence:
            self.enterTunnelSequence.finish()
            self.enterTunnelSequence = None

        self.av.stopPosHprBroadcast()

    def moveForwardInterval(self, distance, *args, **kw):
        dummy = NodePath('dummy')
        dummy.reparentTo(render)
        dummy.setPos(self.av, 0, 0, 0)
        dummy.setHpr(self.av, 0, 0, 0)
        speed = PiratesGlobals.PirateSpeeds[self.av.speedIndex][0]
        duration = distance / speed

        def gravityMoveForward(t, parent):
            self.av.setY(parent, t)
            self.av.controlManager.controls['walk'].placeOnFloor()

        return Sequence(Func(self.av.loop, 'run'), LerpFunc(gravityMoveForward, fromData = 0, toData = distance, extraArgs = [
            dummy], duration = duration), Func(dummy.removeNode))

    def enterLeaveTunnel(self, extraArgs = []):
        self.startLocalSequence()
        distance = 30
        speed = PiratesGlobals.PirateSpeeds[self.av.speedIndex][0]
        duration = distance / speed
        self.av.setY(self.av, -5)
        self.av.cameraFSM.fpsCamera.setHpr(0, 0, 0)
        self.av.cameraFSM.request('FPS')
        cameraFinalPos = camera.getPos(self.av)
        cameraFinalHpr = camera.getHpr(self.av)
        self.av.cameraFSM.request('Control')
        camera.reparentTo(self.av)
        camera.setPos(0, -13, self.av.getHeight() / 2)
        camera.lookAt(self.av.headNode)
        self.av.startPosHprBroadcast()
        leaveSequence = Sequence(Func(base.cr.loadingScreen.hide), Parallel(self.moveForwardInterval(distance, blendType = 'easeOut'), Func(base.transitions.fadeIn, 0.75), Sequence(Wait(duration / 2.0), self.rotateMoveCameraSequence(duration / 2.0, cameraFinalPos, hpr = cameraFinalHpr))), Func(messenger.send, 'LeaveTunnelFinished'))
        leaveSequence.start()

    def exitLeaveTunnel(self):
        self.av.stopPosHprBroadcast()
        self.av.cameraFSM.fpsCamera.setHpr(0, 0, 0)
        self.endLocalSequence()

    def enterPVPWait(self, extraArgs = []):
        self.av.motionFSM.request('MoveLock')

    def exitPVPWait(self):
        self.av.motionFSM.on()

    def enterShipRepair(self, extraArgs = []):
        PlayerPirateGameFSM.enterShipRepair(self, extraArgs)
        self.av.stopAutoRun()

    def filterShipRepair(self, request, args = []):
        if request in ('Emote',):
            return None
        else:
            return self.defaultFilter(request, args)

    def exitShipRepair(self):
        PlayerPirateGameFSM.exitShipRepair(self)

    def enterTentacleTargeted(self, extraArgs = []):
        PlayerPirateGameFSM.enterTentacleTargeted(self, extraArgs)
        tentacle = extraArgs[1]
        self.startLocalSequence()
        self.av.stopPosHprBroadcast()
        self.av.cameraFSM.request('Control')
        camParent = self.av.getShip().getModelRoot()
        camera.wrtReparentTo(camParent)
        pos = camParent.getRelativePoint(tentacle.creature, Point3(120, 120, 0) * 0.6)
        pos.setZ(80 * 0.6)
        self.camIval = self.lookMoveCameraSequence(2, pos)

    def exitTentacleTargeted(self):
        self.camIval.finish()
        base.transitions.letterboxOff()
        if not self.av.guiMgr.ignoreAllKeys:
            self.av.guiMgr.showTrays()

        self.av.guiMgr._showCursor()
        self.av.cameraFSM.request('FPS')
        PlayerPirateGameFSM.exitTentacleTargeted(self)

    def enterTentacleGrabbed(self, extraArgs = []):
        PlayerPirateGameFSM.enterTentacleGrabbed(self, extraArgs)

    def filterTentacleGrabbed(self, request, args = []):
        if request in ('TentacleGrabbed', 'Emote'):
            return None
        else:
            return self.defaultFilter(request, args)

    def exitTentacleGrabbed(self):
        self.av.startCompassEffect()
        PlayerPirateGameFSM.exitTentacleGrabbed(self)

    def startLocalSequence(self):
        self.av.guiMgr._hideCursor()
        self.av.motionFSM.off()
        self.av.stopAutoRun()
        self.av.guiMgr.request('Cutscene')
        base.transitions.letterboxOn()

    def endLocalSequence(self):
        base.transitions.letterboxOff()
        if not self.av.guiMgr.ignoreAllKeys:
            self.av.guiMgr.showTrays()

        self.av.guiMgr._showCursor()
        self.av.motionFSM.on()

    def rotateMoveCameraSequence(self, duration, pos, hpr, blendType = 'easeInOut'):
        (start, end) = getShortestRotation(camera.getH(), hpr[0])
        camera.setH(start)
        hpr.setX(end)
        return LerpPosHprInterval(camera, duration, pos, hpr, blendType = blendType)

    def lookMoveCameraSequence(self, duration, pos, wrtNode = None, lookAtNode = None, lookAtOffset = Point3(0), blendType = 'easeInOut'):

        def addTask(taskName):
            task = taskMgr.add(self.trackNode, taskName)
            task.lookAtNode = lookAtNode or self.av
            task.lookAtOffset = lookAtOffset

        return Sequence(Func(addTask, 'cameraPlayerTracking'), LerpPosInterval(camera, duration, pos, blendType = blendType, other = wrtNode), Func(taskMgr.remove, 'cameraPlayerTracking'))

    def trackNode(self, task):
        camera.lookAt(task.lookAtNode, task.lookAtOffset)
        return task.cont
