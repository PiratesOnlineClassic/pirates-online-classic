# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.tutorial.DistributedPiratesTutorial
import random
import time

from . import ShipWreck
from direct.actor import Actor
from direct.distributed import DistributedObject
from direct.fsm import FSM
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import DelayedCall
from direct.task import Task
from pandac.PandaModules import *
from pirates.battle.Cannon import Cannon, distFireSfxNames
from pirates.cutscene import CutsceneData
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.CeilingDebris import CeilingDebris
from pirates.effects.CeilingDust import CeilingDust
from pirates.effects.DarkWaterFog import DarkWaterFog
from pirates.effects.ProjectileEffect import ProjectileEffect
from pirates.leveleditor import NPCList
from pirates.makeapirate import MakeAPirate
from pirates.npc import Skeleton
from pirates.pirate import HumanDNA, Pirate
from pirates.piratesbase import (PiratesGlobals, PLocalizer, TimeOfDayManager,
                                 TODGlobals, UserFunnel)
from pirates.quest import QuestParser
from pirates.tutorial import TutorialGlobals
from pirates.uberdog import DistributedInventoryBase
from pirates.uberdog.UberDogGlobals import InventoryType

CannonDistance = 200
CannonballHitEvent = 'tutorialCannonballHit'

def _playHitEffect(pos, hitObject, skillId, task=None):
    attackerId = 0
    objType = None
    ProjectileEffect(base.cr, attackerId, hitObject, objType, pos, skillId, InventoryType.GrenadeExplosion)
    shakeCamera = False
    if localAvatar.ship:
        shakeCamera = False
    if localAvatar.style.tutorial >= PiratesGlobals.TUT_MADE_PIRATE:
        if localAvatar.gameFSM.lockFSM:
            shakeCamera = False
    if shakeCamera:
        cameraShaker = CameraShaker()
        cameraShaker.reparentTo(render)
        cameraShaker.shakeSpeed = 0.04
        cameraShaker.shakePower = 1.0
        cameraShaker.numShakes = 3
        cameraShaker.scalePower = 1
        cameraShaker.play(400.0)
    messenger.send(CannonballHitEvent)
    return


class TutorialInteriorEffects:
    __module__ = __name__

    def __init__(self, startFire=False, cannonDelay=None):
        self._target = render.attachNewNode('target')
        self._target.setPos(0, CannonDistance, 0)
        self._skillId = 12906
        self._ammoSkillId = self._skillId
        self._startFire = startFire
        self._cannonDelay = cannonDelay
        self._seachest = None
        return

    def destroy(self):
        self.stop()
        self._target.removeNode()
        del self._target

    def start(self):
        self._shootTaskString = 'TutorialInteriorCannonShoot'
        self._hitTaskString = 'TutorialInteriorCannonHit'
        if self._cannonDelay is None:
            self._shootTask()
        else:
            taskMgr.doMethodLater(self._cannonDelay, self._shootTask, uniqueName(self._shootTaskString))
        self._fireSound = None
        if self._startFire:
            self._startFireSound()
        CameraShaker.setTutorialInteriorScale(0.2)
        return

    def stop(self):
        CameraShaker.clearTutorialInteriorScale()
        taskMgr.removeTasksMatching('*%s*' % self._shootTaskString)
        taskMgr.removeTasksMatching('*%s*' % self._hitTaskString)
        if hasattr(self, '_shootTaskName'):
            del self._shootTaskName
        if hasattr(self, '_fireSound') and self._fireSound is not None:
            self._fireSound.pause()
            del self._fireSound
        return

    def _shootTask(self, task=None):
        targetPos = self._target.getPos()
        flightTime = 4.0
        self.currSnd = base.loader.loadSfx('audio/%s' % distFireSfxNames[random.randint(0, len(distFireSfxNames) - 1)])
        self.currSnd.play()
        taskMgr.doMethodLater(flightTime, Functor(self._handleCannonballHit, targetPos), uniqueName(self._hitTaskString))
        taskMgr.doMethodLater(1.0 + random.random() * 15.0, self._shootTask, uniqueName(self._shootTaskString))

    def _handleCannonballHit(self, targetPos, task=None):
        _playHitEffect(targetPos, self._target, self._skillId)
        self._startFireSound()

    def _startFireSound(self):
        if self._fireSound is None:
            self._fireSound = SoundInterval(base.loader.loadSfx('audio/bonfire.wav'), node=self._target, volume=0.2)
            self._fireSound.loop(stagger=True)
        return


class PhantomCannon(Cannon):
    __module__ = __name__

    def __init__(self, cr, parent, distance, height, targetNps, island):
        Cannon.__init__(self, cr)
        self.loadModel(None)
        self._started = False
        self._targetNps = targetNps
        self._skillId = 12906
        self._ammoSkillId = self._skillId
        self._pivotNode = parent.attachNewNode('phantomCannonPivot')
        self._island = island
        self.reparentTo(self._pivotNode)
        self._pivotNode.reparentTo(parent)
        self.setPos(0, distance, height)
        self.stash()
        return

    def destroy(self):
        self.stop()
        del self._island
        del self._targetNps
        self.unloadModel()
        self.delete()
        self._pivotNode.removeNode()
        del self._pivotNode

    def start(self):
        self._shootTaskString = 'PhantomCannonShoot'
        self._hitTaskString = 'PhantomCannonHit'
        self._shootTask(0, None)
        self._started = True
        return

    def isStarted(self):
        return self._started

    def stop(self):
        self._started = False
        taskMgr.removeTasksMatching('*%s*' % self._shootTaskString)
        taskMgr.removeTasksMatching('*%s*' % self._hitTaskString)
        if hasattr(self, '_shootTaskName'):
            del self._shootTaskName

    def _shootTask(self, time, task):
        maxDistance = time * 12.0
        self._pivotNode.setH(self._pivotNode.getH() + random.random() * maxDistance)
        target = random.choice(self._targetNps)
        targetPos = target.getPos(render)
        flightTime = 5.0
        self.playAttack(self._skillId, self._ammoSkillId, 'PhantomCannonballHit', targetPos=targetPos, flightTime=flightTime, preciseHit=True)
        taskMgr.doMethodLater(flightTime, Functor(_playHitEffect, targetPos, self._island, self._skillId), uniqueName(self._hitTaskString))
        delay = 1.0 + random.random() * 15.0
        taskMgr.doMethodLater(delay, Functor(self._shootTask, delay), uniqueName(self._shootTaskString))


class DistributedPiratesTutorial(DistributedObject.DistributedObject, FSM.FSM):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedPiratesTutorial')
    PRELOADED_CUTSCENES = []

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedPiratesTutorial')
        self.active = 1
        self.JackSparrowPos = Point3(0, 0, 0)
        self.JackSparrowHpr = Point3(200, 0, 0)
        self.NPCDoIds = []
        self.ShipDoIds = []
        self.pendingJackRequest = None
        self.pendingNavyBoatRequest = None
        self.pendingDanRequest = None
        self.pendingStumpyRequest = None
        self.pendingIslandRequest = None
        self.tutorialInstance = None
        self.BoatStumpyDoId = None
        self.island = None
        self.shipWreck = None
        self.loggingCannonDone = False
        self.shipWreckHitCount = 0
        self.shipWreckState = 0
        self.debugTutorial = base.config.GetBool('debug-tutorial', 0)
        self.noJailLight = base.config.GetBool('no-jail-light', 0)
        localAvatar.guiMgr.ignoreAllKeys = True
        localAvatar.guiMgr.hideTrays()
        self._leftJail = 0
        self.map = 0
        base.cr.tutorialObject = self
        return

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.notify.debug('generate')

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        if localAvatar.style.getTutorial() == 0:
            self.map = MakeAPirate.MakeAPirate([base.localAvatar], 'makeAPirateComplete')
            self.map.load()
        self.acceptOnce('localAvTeleportFinished', self.getStarted)
        messenger.send('localAvTeleportFinishedRequest')
        base.setOverrideShipVisibility(True)
        self.acceptOnce('localPirateDisabled', self.localPlayerLeft)

    def localPlayerLeft(self):
        self.cleanup()

    def getStarted(self, task=None):
        if self.state == 'Off':
            self.request('Act0Tutorial')

    def cleanup(self):
        if self.pendingJackRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingJackRequest)
            self.pendingJackRequest = None
        if self.pendingNavyBoatRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingNavyBoatRequest)
            self.pendingNavyBoatRequest = None
        if self.pendingDanRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingDanRequest)
            self.pendingDanRequest = None
        if self.pendingStumpyRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStumpyRequest)
            self.pendingStumpyRequest = None
        if self.pendingIslandRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingIslandRequest)
            self.pendingIslandRequest = None
        taskMgr.remove(self.taskName('handleAct0Tutorial'))
        self._stopFog()
        self._stopInteriorCannonballHitEffects()
        self._stopTutorialInteriorEffects()
        if hasattr(self, '_phantomCannon'):
            self._phantomCannon.destroy()
            del self._phantomCannon
        for pcs in self.PRELOADED_CUTSCENES:
            for currCutscene in pcs:
                base.cr.cleanupPreloadedCutscene(currCutscene)

        self.PRELOADED_CUTSCENES = []
        if self.island is not None:
            self.island.stopCustomEffects()
            self.island = None
        localAvatar.clearTutorialHandlerZone()
        self.ignoreAll()
        return

    def disable(self):
        self.cleanup()
        DistributedObject.DistributedObject.disable(self)

    def setInstance(self, instance):
        self.tutorialInstance = instance
        if localAvatar.style.getTutorial() == 0:
            self.preloadCutscene(CutsceneData.PRELOADED_CUTSCENE_STAGE1)

    def preloadCutscene(self, pcs):
        self.PRELOADED_CUTSCENES.append(pcs)
        for currCutscene in pcs:
            base.cr.preloadCutscene(currCutscene)

    def inventoryFailed(self):
        if localAvatar:
            localAvatar.b_setLocation(0, 0)
        if self.map:
            self.map.exit()
            self.map.unload()
            self.map = 0
        base.cr.gameFSM.request('closeShard', ['waitForAvatarList'])

    def enterAct0Tutorial(self):
        self.notify.debug('starting tutorial')
        QuestParser.init()
        if self.noJailLight:
            render.setLightOff()
        self.JackDoId = None
        self.DanDoId = None
        self.StumpyDoId = None
        self.IslandDoId = None

        def stumpyHere(stumpyId):
            self.StumpyDoId = stumpyId

        def stumpyBoatHere(stumpyBoatId):
            self.BoatStumpyDoId = stumpyBoatId
            self.pendingStumpyBoatRequest = base.cr.relatedObjectMgr.requestObjects([self.BoatStumpyDoId], eachCallback=self.doStumpyBoatIntro)

        def navyBoatHere(navyBoatId):
            self.BoatNavyDoId = navyBoatId
            self.pendingNavyBoatRequest = base.cr.relatedObjectMgr.requestObjects([self.BoatNavyDoId], eachCallback=self.setupNavyBoat)

        def danHere(danId):
            self.DanDoId = danId
            self.pendingDanRequest = base.cr.relatedObjectMgr.requestObjects([self.DanDoId], eachCallback=self.doDanIntro)

        def nellHere(nellId):
            self.NellDoId = nellId
            self.pendingNellRequest = base.cr.relatedObjectMgr.requestObjects([self.NellDoId], eachCallback=self.doNellIntro)

        def islandHere(islandId):
            self.IslandDoId = islandId
            self.pendingIslandRequest = base.cr.relatedObjectMgr.requestObjects([self.IslandDoId], eachCallback=self.handleIslandGenerate)

        self.cr.uidMgr.addUidCallback(TutorialGlobals.STUMPY_UID, stumpyHere)
        self.cr.uidMgr.addUidCallback(TutorialGlobals.NELL_UID, nellHere, onlyOnce=False)
        self.cr.uidMgr.addUidCallback(TutorialGlobals.DAN_UID, danHere, onlyOnce=False)
        self.cr.uidMgr.addUidCallback(TutorialGlobals.STUMPY_BOAT_UID, stumpyBoatHere, onlyOnce=False)
        self.cr.uidMgr.addUidCallback(TutorialGlobals.NAVY_BOAT_UID, navyBoatHere)
        self.cr.uidMgr.addUidCallback(TutorialGlobals.RAMBLESHACK_ISLE_UID, islandHere)
        self.accept('doneJackIntro', self.doneJackIntro)
        self.accept('doorToExteriorFadeIn', self.handleGoOutside)
        self.accept('doorToInteriorFadeIn', self.handleGoInside)
        self.acceptOnce('beginSeachest', self.beginSeachest)
        if localAvatar.style.getTutorial() > 0:
            self.ignore('doneJackIntro')
            localAvatar.openJailDoor()
            localAvatar.style.setName(localAvatar.getName())
            localAvatar.guiMgr.showTrays()
            base.transitions.fadeIn()
        self.sendUpdate('clientEnterAct0Tutorial')
        return

    def _startTutorialInteriorEffects(self, startFire, cannonDelay=None):
        self._jie = TutorialInteriorEffects(startFire, cannonDelay)
        self._jie.start()
        isJail = not startFire
        self.accept(CannonballHitEvent, Functor(self._handleInteriorCannonballHit, isJail))

    def _stopTutorialInteriorEffects(self):
        self.ignore(CannonballHitEvent)
        if hasattr(self, '_jie'):
            self._jie.stop()
            self._jie.destroy()
            del self._jie

    def handleIslandGenerate(self, island):
        self.island = island

    def handleWalkedOutToIsland(self):
        if not self._leftJail:
            self._leftJail = 1
            base.cr.centralLogger.writeClientEvent('LEAVING_JAIL')
            UserFunnel.logSubmit(0, 'LEAVING_JAIL')
            UserFunnel.logSubmit(1, 'LEAVING_JAIL')
            if base.downloadWatcher:
                base.downloadWatcher.setStatusBarLocation(1)
            self.preloadCutscene(CutsceneData.PRELOADED_CUTSCENE_STAGE2)
            self.preloadCutscene(CutsceneData.PRELOADED_CUTSCENE_STAGE3)
            self._stopTutorialInteriorEffects()
            self.island.setZoneLevel(0)
            self._targetNps = self.island.findAllMatches('**/TorchFire') 
            self._phantomCannon = PhantomCannon(self.cr, self.island, CannonDistance, 50, self._targetNps, self.island)
            self._phantomCannon.start()

    def generateShipWreck(self, island):
        objNP = island.find('**/=uid=%s' % TutorialGlobals.SHIP_WRECK_UID)
        self.shipWreck = ShipWreck.ShipWreck(objNP, TutorialGlobals.SHIP_WRECK_UID)
        self.shipWreck.tutorial = self
        self.shipWreck.makeTargetableCollision(island.doId)
        island.shipWreck = self.shipWreck

    def removeShipWreck(self):
        self.shipWreck.delete()
        self.shipWreck.removeNode()

    def doStumpyBoatIntro(self, object):
        stumpyBoat = base.cr.doId2do[self.BoatStumpyDoId]

        def setupTalkToDan(talkToDan):
            if talkToDan == False:
                self.notify.debug('stumpyBoat: talkToDan is False')
                self.accept(stumpyBoat.proximityCollisionEnterEvent, self.triggerBoBeckCut)
                self.acceptOnce('enableBoatBoarding', self.enableBoatBoarding)
                self.notify.debug('stumpyBoat:waiting for stumpy %s' % self.StumpyDoId)
                self.pendingStumpyRequest = base.cr.relatedObjectMgr.requestObjects([self.StumpyDoId], eachCallback=self.doStumpyIntro)
            else:
                self.notify.debug('stumpyBoat:talkToDan is True')

        self.playerNeedsToTalkToDan(setupTalkToDan)
        stumpyBoat.hideName()

    def triggerBoBeckCut(self, collEntry):
        self.notify.debug('triggerBoBeckCut')
        stumpyBoat = base.cr.doId2do[self.BoatStumpyDoId]
        self.ignore(stumpyBoat.proximityCollisionEnterEvent)
        self.sendUpdate('autoVisit', [self.BoatStumpyDoId])
        base.avatarPhysicsMgr.removePhysicalNode(stumpyBoat.actorNode)

    def exitAct0Tutorial(self):
        pass

    def doneJackIntro(self):
        self.notify.debug('Done Introducing Jack Sparrow')
        localAvatar.unstash()
        self.request('Act1MakeAPirate')

    def enterAct1MakeAPirate(self):
        base.disableMouse()
        localAvatar.gameFSM.request('MakeAPirate')
        localAvatar.gameFSM.lockFSM = True
        localAvatar.guiMgr.hideTrays()
        localAvatar.guiMgr.optionsButton.show()
        localAvatar.guiMgr.optionsButton.setX(-0.1)
        localAvatar.guiMgr.optionsButton.resetHelpWatcher()
        localAvatar.guiMgr.optionsButton.helpBox.setPos(0.1, 0, 0.05)
        self.avHpr = VBase3(180, 0, 0)
        ga = localAvatar.getParentObj()
        for light in ga.dynamicLights:
            light.turnOff()

        self.jail = ga.find('**/*navy_jail_interior*')
        self.jail.setLightOff()
        self.map.enter()
        self.accept('makeAPirateComplete', self.handleMakeAPirate)
        UserFunnel.logSubmit(1, 'CREATE_PIRATE_LOADS')
        UserFunnel.logSubmit(0, 'CREATE_PIRATE_LOADS')
        base.cr.centralLogger.writeClientEvent('CREATE_PIRATE_LOADS')

    def handleMakeAPirate(self):
        self.notify.debug('done make-a-pirate')
        done = self.map.getDoneStatus()
        if done == 'cancel':
            localAvatar.b_setLocation(0, 0)
            self.map.exit()
            self.map.unload()
            self.map = 0
            base.cr.gameFSM.request('closeShard', ['waitForAvatarList'])
        else:
            if done == 'created':
                dna = self.map.pirate.style
                localAvatar.setDNA(dna)
                localAvatar.generateHuman(dna.gender, base.cr.human)
                localAvatar.motionFSM.off()
                localAvatar.motionFSM.on()
                self.acceptOnce('avatarPopulated', self.avatarPopulated)
                if self.map.nameGui.customName:
                    localAvatar.setWishName()
                    base.cr.avatarManager.sendRequestPopulateAvatar(localAvatar.doId, localAvatar.style, 0, 0, 0, 0, 0)
                else:
                    name = self.map.nameGui.getNumericName()
                    base.cr.avatarManager.sendRequestPopulateAvatar(localAvatar.doId, localAvatar.style, 1, name[0], name[1], name[2], name[3])
                self.map.exit()
                self.map.unload()
                self.map = 0
            else:
                self.notify.error('Invalid doneStatus from MakeAPirate: ' + str(done))
        localAvatar.gameFSM.lockFSM = False
        ga = localAvatar.getParentObj()
        if ga is not None:
            for light in ga.dynamicLights:
                light.turnOn()
                self.jail.setLight(light.lightNodePath)

        return

    def avatarPopulated(self):
        self.request('EscapeFromLA')
        localAvatar.b_setGameState('LandRoam')
        self.sendUpdate('makeAPirateComplete')

    def makeAPirateCompleteResp(self):
        base.transitions.fadeIn(1.0)

    def handleGoOutside(self):
        self._stopTutorialInteriorEffects()
        if hasattr(self, '_phantomCannon'):
            self._phantomCannon.start()
        self.ignore(CannonballHitEvent)
        base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_DEFAULT)
        if base.cr.timeOfDayManager.cycleType == TODGlobals.TOD_REGULAR_CYCLE:
            base.cr.timeOfDayManager.request(base.cr.timeOfDayManager.getStateName(PiratesGlobals.TOD_NIGHT), 0)
        base.cr.timeOfDayManager.pause()
        self._startFog()
        self.handleWalkedOutToIsland()

    def handleGoInside(self):
        self._phantomCannon.stop()
        if hasattr(self, '_fireSound') and self._fireSound is not None:
            self._fireSound.pause()
        self._stopFog()
        isJail = False
        self.accept(CannonballHitEvent, Functor(self._handleInteriorCannonballHit, isJail))
        self._startTutorialInteriorEffects(True, random.random() * 3.0)
        return

    def _handleInteriorCannonballHit(self, isJail):
        if isJail:
            offset = 0
        else:
            offset = 3
        self._dustEffect = CeilingDust.getEffect()
        if self._dustEffect:
            self._dustEffect.reparentTo(base.localAvatar)
            self._dustEffect.setPos(0, 0, 12 + offset)
            self._dustEffect.play()
        self._debrisEffect = CeilingDebris.getEffect()
        if self._debrisEffect:
            self._debrisEffect.reparentTo(base.localAvatar)
            self._debrisEffect.setPos(0, 0, 22 + offset)
            self._debrisEffect.play()

    def _stopInteriorCannonballHitEffects(self):
        if hasattr(self, '_dustEffect'):
            self._dustEffect.finish()
            del self._dustEffect
        if hasattr(self, '_debrisEffect'):
            self._debrisEffect.finish()
            del self._debrisEffect

    def _startFog(self):
        self._fog = DarkWaterFog()
        self._fog.reparentTo(localAvatar)
        self._fog.startLoop()
        self._moveFogDownEvent = 'moveFogDown'
        taskMgr.add(self._fogPositionTask, self._moveFogDownEvent, priority=49)

    def _stopFog(self):
        if hasattr(self, '_fog'):
            taskMgr.remove(self._moveFogDownEvent)
            del self._moveFogDownEvent
            self._fog.stopLoop()
            self._fog.destroy()
            del self._fog

    def _tuneFog(self, alpha):
        if hasattr(self, '_fog'):
            self._fog.tuneFog(alpha)

    def _fogPositionTask(self, task):
        self._fog.setZ(render, 0)
        return task.cont

    def exitAct1MakeAPirate(self):
        base.enableMouse()
        base.localAvatar.setHpr(self.avHpr)
        localAvatar.b_setTutorial(PiratesGlobals.TUT_MADE_PIRATE)

    def enterEscapeFromLA(self):
        UserFunnel.logSubmit(1, 'CUTSCENE_ONE_END')
        UserFunnel.logSubmit(0, 'CUTSCENE_ONE_END')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_ONE_END')
        self.acceptOnce('startTutorialCannons', Functor(self._startTutorialInteriorEffects, False))

    def exitEscapeFromLA(self):
        pass

    def doDanIntro(self, object):
        self.notify.debug('doDanIntro')
        self.NPCDan = object
        if localAvatar.style.getTutorial() > PiratesGlobals.TUT_MADE_PIRATE:
            if not self.debugTutorial:
                self.NPCDan.stash()
                self.NPCDan.setInteractOptions(allowInteract=False)
            return
        dnaDict = NPCList.NPC_LIST[TutorialGlobals.DAN_UID]
        customDNA = HumanDNA.HumanDNA()
        customDNA.loadFromNPCDict(dnaDict)
        self.NPCDan.setDNA(customDNA)
        self.NPCDan.generateHuman('m', base.cr.human)
        self.NPCDan.hideName()
        self.NPCDan.setPurgeInteractGui(1)
        self.NPCDan.disableBodyCollisions()
        self.NPCDan.loop('tut_1_1_5_a_idle_dan')
        self.NPCDan.setInteractOptions(allowInteract=False)
        self.NPCDan.tutorialCharacter = 1

        def setupTalkToDan(talkToDan):
            if talkToDan:
                self.doneDanIntro(None)
            else:
                self.NPCDan.setAllowInteract(False)
            return

        self.playerNeedsToTalkToDan(setupTalkToDan)

    def doNellIntro(self, object):
        self.notify.debug('doNellIntro')
        self.NPCNell = object
        if localAvatar.style.getTutorial() > 1:
            if not self.debugTutorial:
                self.NPCNell.stash()
                self.NPCNell.setInteractOptions(allowInteract=False)
            return
        dnaDict = NPCList.NPC_LIST[TutorialGlobals.NELL_UID]
        customDNA = HumanDNA.HumanDNA()
        customDNA.loadFromNPCDict(dnaDict)
        self.NPCNell.setDNA(customDNA)
        self.NPCNell.generateHuman('f', base.cr.human)
        self.NPCNell.hideName()
        self.NPCNell.setPurgeInteractGui(1)
        self.NPCNell.loop('tut_1_1_5_a_idle_dan')
        self.NPCNell.setInteractOptions(allowInteract=False)
        self.accept('playNellAnimationDan_a', self.playNellAnimationDan_a)
        UserFunnel.logSubmit(1, 'CUTSCENE_TWO_START')
        UserFunnel.logSubmit(0, 'CUTSCENE_TWO_START')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_TWO_START')

    def loopNellAnimationDan_a_idle(self):
        self.notify.debug('startNellAnimationDan_a_idle')
        self.NPCNell.loop('tut_1_1_5_a_idle_dan')

    def playNellAnimationDan_a(self):
        self.notify.debug('startNellAnimationDan_a')
        self.NPCNell.play('tut_1_1_5_a_dan')
        self.accept('loopNellAnimationDan_a_idle', self.loopNellAnimationDan_a_idle)
        self.accept('playNellAnimationDan_b', self.playNellAnimationDan_b)

    def playNellAnimationDan_b(self):
        self.notify.debug('startNellAnimationDan_b')
        self.NPCNell.play('tut_1_1_5_b_dan')
        self.accept('assignStumpyQuest', self.assignStumpyQuest)

    def setupNavyBoat(self, object):
        object.hideName()

    def playerNeedsToTalkToDan(self, callback):
        if localAvatar.style.getTutorial() >= 2:
            callback(False)
            return

        def talkToDanCallback(inventory):
            if not inventory:
                callback(False)
            talkToDan = False
            for currQuest in inventory.getQuestList():
                if currQuest.questId == TutorialGlobals.SECOND_QUEST:
                    talkToDan = True
                    break

            callback(talkToDan)

        DistributedInventoryBase.DistributedInventoryBase.getInventory(localAvatar.inventoryId, talkToDanCallback)

    def doneDanIntro(self, collEntry):
        self.notify.debug('Done Introducing Doggerel Dan')
        self.NPCDan.setAllowInteract(False)
        self.request('Act2FindDan')

    def enterAct2FindDan(self):
        self.notify.debug('found Dan')
        self.sendUpdate('autoVisit', [self.NPCDan.getDoId()])
        self.accept('assignStumpyQuest', self.assignStumpyQuest)

    def exitAct2FindDan(self):
        pass

    def beginSeachest(self):
        self.notify.debug('beginSeachest')
        localAvatar.gameFSM.lockFSM = False
        localAvatar.b_setGameState('Dialog')
        localAvatar.gameFSM.lockFSM = True
        localAvatar.guiMgr.request('Interface', [False, True])
        localAvatar.guiMgr.optionsButton.setX(-0.22)
        localAvatar.guiMgr.optionsButton.helpBox.setPos(0, 0, 0)
        localAvatar.guiMgr.optionsButton.resetHelpWatcher()
        localAvatar.guiMgr.chestTray.show()
        localAvatar.cameraFSM.request('Control')
        stage = localAvatar.getParent().getParent()
        base.camera.reparentTo(stage)
        base.camera.setPos(9.561, 26.215, 5.255)
        base.camera.setHpr(-2.999, 5.293, 2.296)
        self.NPCDan.setHpr(-180, 0, 0)
        localAvatar.setPos(stage, 9.561, 26.215, 1.0)
        self._seachest = localAvatar.tutObject
        localAvatar.tutObject = None
        t = Parallel(Sequence(LerpPosInterval(self._seachest, 10, VBase3(15, -10, 3.0)), Func(self._seachest.removeNode)), Sequence(LerpScaleInterval(self._seachest, 1, VBase3(0.1, 0.1, 0.1))))
        t.start()
        return

    def assignStumpyQuest(self):
        self.notify.debug('assignStumpyQuest')
        self.accept('removeDanAndNell', self.removeDanAndNell)

    def removeDanAndNell(self):
        UserFunnel.logSubmit(1, 'CUTSCENE_TWO_END')
        UserFunnel.logSubmit(0, 'CUTSCENE_TWO_END')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_TWO_END')
        self.notify.debug('removeDanAndNell')
        localAvatar.setTutorial(PiratesGlobals.TUT_GOT_SEACHEST)
        localAvatar.gameFSM.lockFSM = False
        localAvatar.b_setGameState('LandRoam')
        localAvatar.guiMgr.chestTray.show()

    def stageStumpyPositionOnBoat(self):
        self.NPCStumpy.motionFSM.request('Off')
        self.NPCStumpy.setPos(0, -1.2, 9)
        self.NPCStumpy.setHpr(180, 0, 0)
        self.NPCStumpy.loop('wheel_idle')
        localAvatar.ship.wheel[0].geom_High.setScale(0.96)

    def enableBoatBoarding(self):
        self.notify.debug('enableBoatBoarding')
        if self.BoatStumpyDoId:
            stumpyBoat = base.cr.doId2do[self.BoatStumpyDoId]
            self.island.stopCustomEffects()
            localAvatar.placeOnShip(stumpyBoat)
            localAvatar.setH(-90)
            self.stageStumpyPositionOnBoat()
            self.acceptOnce('usedCannon', self.startShipMovement)
            list(stumpyBoat.cannons.values())[0][1].setIgnoreProximity(False)
            dialogue = base.loader.loadSfx('audio/beck_cs12_4_4c_tell_to_shoot.mp3')
            localAvatar.guiMgr.subtitler.showText(PLocalizer.QuestScriptTutorialStumpy_1, sfx=dialogue, timeout=dialogue.length() + 1.0)
            localAvatar.guiMgr.subtitler.clearTextOverride = True

    def doStumpyIntro(self, object):
        self.notify.debug('doStumpyIntro')
        self.NPCStumpy = object
        dnaDict = NPCList.NPC_LIST['1153439632.21darren']
        customDNA = HumanDNA.HumanDNA()
        customDNA.loadFromNPCDict(dnaDict)
        self.NPCStumpy.setDNA(customDNA)
        self.NPCStumpy.generateHuman('m', base.cr.human)
        self.NPCStumpy.setInteractOptions(allowInteract=False)
        self.NPCStumpy.setIgnoreProximity(True)
        self.NPCStumpy.disableBodyCollisions()
        self.NPCStumpy.setZ(9)
        self.notify.debug('collision event for Stumpy %s' % self.NPCStumpy.proximityCollisionEvent)
        if self.BoatStumpyDoId:
            stumpyBoat = base.cr.doId2do[self.BoatStumpyDoId]
            self.acceptOnce(stumpyBoat.uniqueName('localAvBoardedShip'), self.doneStumpyIntro)

    def doneStumpyIntro(self, task=None):
        self.notify.debug('Done Introducing Stumpy McGee')
        localAvatar.gameFSM.lockFSM = False
        localAvatar.b_setGameState('LandRoam')
        localAvatar.gameFSM.lockFSM = True
        self.sendUpdate('boardedTutorialShip')
        self.acceptOnce('showCannonExitPanel', self.showCannonExitPanel)
        self.accept('targetPracticeDone', self.targetPracticeDone)
        UserFunnel.logSubmit(1, 'CUTSCENE_THREE_START')
        UserFunnel.logSubmit(0, 'CUTSCENE_THREE_START')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_THREE_START')
        if self.BoatStumpyDoId:
            stumpyBoat = base.cr.doId2do[self.BoatStumpyDoId]
            stumpyBoat.ignoreFloors()
            self.ignore(stumpyBoat.uniqueName('localAvBoardedShip'))

    def startShipMovement(self):
        self.island.stopCustomEffects()
        self._phantomCannon.stop()
        self.generateShipWreck(self.island)
        self.sendUpdate('startSailingStumpy')
        UserFunnel.logSubmit(1, 'CUTSCENE_THREE_END')
        UserFunnel.logSubmit(0, 'CUTSCENE_THREE_END')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_THREE_END')

    def targetPracticeDone(self):
        pass

    def cannonHitWreck(self, shipWreck):
        self.notify.debug('cannonHitTarget')
        self.shipWreckHitCount += 1
        if self.shipWreckHitCount > 2 and self.shipWreckState == 0:
            self.shipWreckState = 1
            print('ship wreck hit count %s' % self.shipWreckHitCount)
            localAvatar.cannon.fireCannonPanel.setWreckButtonText(self.shipWreckHitCount)
            localAvatar.gameFSM.lockFSM = False
            self.showCannonExitPanel()
            dialogue = base.loader.loadSfx('audio/beck_cs12_5_5a_tell_praise.mp3')
            localAvatar.guiMgr.subtitler.showText(PLocalizer.QuestScriptTutorialStumpy_6, sfx=dialogue, timeout=dialogue.length() + 1.0)
        else:
            if self.shipWreckHitCount > 5 and self.shipWreckState == 1:
                self.shipWreckState = 2
                self.cannonDoneShooting()
            else:
                if self.shipWreckState == 0:
                    print('ship wreck hit count %s' % self.shipWreckHitCount)
                    localAvatar.cannon.fireCannonPanel.setWreckButtonText(self.shipWreckHitCount)

    def showCannonExitPanel(self):
        self.notify.debug('showCannonExitPanel')
        localAvatar.cannon.showExitCannonPanel()
        localAvatar.cannon.setIgnoreProximity(True)
        self.acceptOnce('exitedCannon', self.cannonDoneShooting)

    def cannonDoneShooting(self):
        if not self.loggingCannonDone:
            UserFunnel.logSubmit(1, 'ACCESS_CANNON')
            UserFunnel.logSubmit(0, 'ACCESS_CANNON')
            base.cr.centralLogger.writeClientEvent('ACCESS_CANNON')
            self.loggingCannonDone = True
        self.sendUpdate('targetPracticeDone')
        self.request('Act2TargetSunk')

    def enterAct2TargetSunk(self):
        self.notify.debug('Sunk the target')
        self.accept('introduceJR', self.introduceJR)

    def exitAct2TargetSunk(self):
        pass

    def introduceJR(self):
        if localAvatar.cannon:
            localAvatar.cannon.handleEndInteractKey()
        if localAvatar.ship and localAvatar.ship.gameFSM:
            localAvatar.ship.gameFSM.stopCurrentMusic()
        localAvatar.setPos(0, 0, 0)
        localAvatar.nametag3d.hide()
        self.notify.debug('introduceJR')
        self.request('Act3IntroduceJR')
        self.removeShipWreck()
        self.island.stopCustomEffects()
        self.island.stash()

    def enterAct3IntroduceJR(self):
        self.notify.debug('Here comes Jolly Roger')
        self.accept('JRAttackShip', self.JRAttackShip)
        UserFunnel.logSubmit(1, 'CUTSCENE_FOUR_START')
        UserFunnel.logSubmit(0, 'CUTSCENE_FOUR_START')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_FOUR_START')

    def exitAct3IntroduceJR(self):
        pass

    def JRAttackShip(self):
        self.notify.debug('JR Attacking Ship')
        self.accept('JRDestroyShip', self.JRDestroyShip)

    def JRDestroyShip(self):
        self.notify.debug('JR Destroying Ship')
        self.request('Act4BackToMain')
        UserFunnel.logSubmit(1, 'CUTSCENE_FOUR_END')
        UserFunnel.logSubmit(0, 'CUTSCENE_FOUR_END')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_FOUR_END')

    def enterAct4BackToMain(self):
        taskMgr.doMethodLater(0.0001, self.goBackToMain, self.taskName('goBackToMain'))

    def exitAct4BackToMain(self):
        pass

    def goBackToMain(self, task):
        self.request('Act4DoneTutorial')
        return Task.done

    def enterAct4DoneTutorial(self):
        base.transitions.fadeOut(1.0)
        base.cr.tutorial = 0
        base.cr.tutorialObject = None
        base.cr.loadingScreen.showHint('1150922126.8dzlu')
        base.cr.loadingScreen.showTarget('1150922126.8dzlu')
        base.cr.loadingScreen.show()
        localAvatar.setupAutoShipBoarding()
        localAvatar.removeFromShip(localAvatar.ship)
        localAvatar.guiMgr.ignoreAllKeys = False
        localAvatar.guiMgr.showTrays()
        if base.launcher.getPhaseComplete(4):
            self.teleportToPR()
        else:
            base.downloadWatcher.foreground()
            self.accept('phaseComplete-4', self.teleportToPR)
        return

    def teleportToPR(self):
        if base.downloadWatcher:
            base.downloadWatcher.background()
        if config.GetBool('want-welcome-worlds', 0):
            base.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_WELCOME, 'welcomeWorld', doneCallback=self.handleBackToMain)
        else:
            base.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld', doneCallback=self.handleBackToMain)

    def exitAct4DoneTutorial(self):
        pass

    def handleBackToMain(self, object):
        base.setOverrideShipVisibility(False)
        if base.downloadWatcher:
            base.downloadWatcher.setStatusBarLocation(2)
        messenger.send('stopTutorial')
        localAvatar.show()
        UserFunnel.logSubmit(1, 'STARTGAME_DOCK')
        UserFunnel.logSubmit(0, 'STARTGAME_DOCK')
        base.cr.centralLogger.writeClientEvent('STARTGAME_DOCK')
# okay decompiling .\pirates\tutorial\DistributedPiratesTutorial.pyc
