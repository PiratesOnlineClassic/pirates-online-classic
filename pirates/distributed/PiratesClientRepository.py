import gc
import random
import types

from pirates.distributed import PlayGame
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed import DistributedSmoothNode, DoInterestManager
from direct.distributed.ClientRepositoryBase import ClientRepositoryBase
from direct.distributed.ClockDelta import *
from direct.distributed.InterestWatcher import InterestWatcher
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.fsm import ClassicFSM, State
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.EventGroup import EventGroup
from direct.showbase.PythonUtil import report
from direct.showbase.ShowBaseGlobal import *
from direct.task import Task
from otp.distributed import DistributedDistrict, OtpDoGlobals, PotentialShard
from otp.distributed.OTPClientRepository import OTPClientRepository
from otp.distributed.PotentialAvatar import PotentialAvatar
from otp.friends import FriendSecret
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from otp.uberdog.AccountDetailRecord import (AccountDetailRecord,
                                             SubDetailRecord)
from panda3d.core import *
from panda3d.direct import *
from pirates.ai import NewsManager
from pirates.band import DistributedBandMember
from pirates.battle import (BattleManager, CombatAnimations,
                            DistributedBattleNPC)
from pirates.coderedemption.CodeRedemption import CodeRedemption
from pirates.cutscene import Cutscene
from pirates.interact import InteractionManager
from pirates.login.AvatarChooser import AvatarChooser
from pirates.makeapirate import PCPickANamePattern
from pirates.makeapirate.MakeAPirate import MakeAPirate
from pirates.pirate import (AvatarTypes, DistributedPlayerPirate, Human,
                            HumanDNA, MasterHuman)
from pirates.pirate.LocalPirate import LocalPirate
from pirates.piratesbase import (LoadingScreen, PiratesGlobals, PLocalizer,
                                 UniqueIdManager)
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.DialMeter import DialMeter
from pirates.quest import QuestLadderDynMap
from pirates.quest.QuestLadderDependency import QuestLadderDependency
from pirates.reputation import ReputationGlobals
from pirates.ship import DistributedShip
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.world import WorldGlobals
from otp.distributed.OtpDoGlobals import *
from otp.nametag import NametagGlobals

want_fifothreads = base.config.GetBool('want-fifothreads', False)
if want_fifothreads:

    class ClientNetworkReader(PythonThread):

        def __init__(self, repository):
            PythonThread.__init__(self, self.run, None, 'ClientNetworkReader', 'ClientNetworkReader')
            self.repository = repository
            self.keeprunning = 1
            self.verbose = base.config.GetBool('network-thread-verbose', 0)

        def run(self):
            while self.keeprunning:
                Thread.forceYield()
                if self.keeprunning:
                    PStatClient.threadTick('ClientNetworkReader')
                    while self.repository.readerPollOnce() and self.keeprunning:
                        Thread.considerYield()
                        PStatClient.threadTick('ClientNetworkReader')

                    if self.verbose:
                        print 'traffic done'

        def PonderYield(self, comment=''):
            Thread.considerYield()

        def PleaseStop(self):
            self.keeprunning = 0


class PiratesClientRepository(OTPClientRepository):
    notify = directNotify.newCategory('PiratesClientRepository')
    SupportTutorial = 0
    GameGlobalsId = OTP_DO_ID_PIRATES
    StopVisibilityEvent = 'pirates-stop-visibility'

    def __init__(self, serverVersion, launcher=None):
        OTPClientRepository.__init__(self, serverVersion, launcher, playGame=PlayGame.PlayGame)
        self.createAvatarClass = DistributedPlayerPirate.DistributedPlayerPirate
        self.tradeManager = None
        self.pvpManager = None
        self.avatarManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_AVATAR_MANAGER, 'DistributedAvatarManager')
        self.chatManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_CHAT_MANAGER, 'DistributedChatManager')
        self.avatarFriendsManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_AVATAR_FRIENDS_MANAGER, 'PCAvatarFriendsManager')
        self.playerFriendsManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PLAYER_FRIENDS_MANAGER, 'PCPlayerFriendsManager')
        self.guildManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_GUILD_MANAGER, 'GuildManager')
        self.shipLoader = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_SHIP_MANAGER, 'DistributedShipLoader')
        self.matchMaker = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_MATCH_MAKER, 'DistributedMatchMaker')
        self.codeRedemption = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_CODE_REDEMPTION, 'CodeRedemption')
        self.settingsMgr = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_SETTINGS_MANAGER, 'PiratesSettingsMgr')
        self.csm = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        self.inventoryManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_INVENTORY_MANAGER, 'DistributedInventoryManager')
        self.wantSeapatch = base.config.GetBool('want-seapatch', True)
        self.wantSpecialEffects = base.config.GetBool('want-special-effects', True)
        self.wantMakeAPirate = base.config.GetBool('want-make-a-pirate', False)
        self.forceTutorial = base.config.GetBool('force-tutorial', False)
        self.skipTutorial = base.config.GetBool('skip-tutorial', False)
        self.tutorialObject = None
        self.avCreate = None
        self.currentCutscene = None
        self.activeWorld = None
        self.oldWorld = None
        self.teleportMgr = None
        self.targetMgr = None
        self.treasureMap = None
        self.distributedDistrict = None
        self.district = None
        self.friendManager = None
        self.battleMgr = BattleManager.BattleManager(self)
        self.combatAnims = CombatAnimations.CombatAnimations()
        self.interactionMgr = InteractionManager.InteractionManager()
        self.currCamParent = None
        self.uidMgr = UniqueIdManager.UniqueIdManager(self)
        self.accountDetailRecord = AccountDetailRecord()
        self.fakeMSP = None
        self.questDynMap = QuestLadderDynMap.QuestLadderDynMap()
        self.questDependency = QuestLadderDependency()
        self.human = [
            MasterHuman.MasterHuman(),
            MasterHuman.MasterHuman()]

        self.human[0].billboardNode.removeNode()
        self.human[1].billboardNode.removeNode()
        self.human[0].style = HumanDNA.HumanDNA('m')
        self.human[1].style = HumanDNA.HumanDNA('f')
        self.human[0].generateHuman('m')
        self.human[1].generateHuman('f')
        self.human[0].ignoreAll()
        self.human[1].ignoreAll()
        self.human[0].stopBlink()
        self.human[1].stopBlink()
        A = AvatarTypes
        del A
        self.preloadedCutscenes = {}

        if want_fifothreads:
            taskMgr.doYield = self.taskManagerDoYieldCall

        self.loadingScreen = LoadingScreen.LoadingScreen(self)
        self.defaultShard = 0

        self.interestHandles = []

    def gotoFirstScreen(self):
        self.startReaderPollTask()
        self.startHeartbeat()
        self.loginFSM.request('login')

    def getOldWorld(self):
        return self.oldWorld

    def getActiveWorld(self):
        return self.activeWorld

    def preloadCutscene(self, name):
        newCutscene = Cutscene.Cutscene(self, name)
        self.preloadedCutscenes[name] = newCutscene

    def getPreloadedCutsceneInfo(self, name):
        return self.preloadedCutscenes.get(name)

    def cleanupPreloadedCutscene(self, name):
        plCutscene = self.preloadedCutscenes.get(name)
        if plCutscene:
            if not plCutscene.isEmpty():
                plCutscene.destroy()
            del self.preloadedCutscenes[name]

    @report(types=['frameCount', 'args'], dConfigParam='want-connector-report')
    def setActiveWorld(self, world):
        if self.activeWorld != world:
            self.oldWorld = self.activeWorld
        self.activeWorld = world

    def getWaterHeight(self, node):
        if self.wantSeapatch and self.activeWorld:
            water = self.activeWorld.getWater()
            if water:
                return water.calcHeight(node=node)
        else:
            return 0.0

    def isOceanEnabled(self):
        if self.wantSeapatch and self.activeWorld:
            water = self.activeWorld.getWater()
            if water:
                return water.enabled

        return False

    def enterChooseAvatar(self, avList):
        self.sendSetAvatarIdMsg(0)
        self.handler = self.handleMessageType
        self.avChoiceDoneEvent = 'avatarChooserDone'
        self.avChoice = AvatarChooser(self.loginFSM, self.avChoiceDoneEvent)
        self.avChoice.load()
        self.avChoice.enter()
        self.accept(self.avChoiceDoneEvent, self.__handleAvatarChooserDone)

    def __handleAvatarChooserDone(self, doneStatus):
        done = doneStatus['mode']
        if done == 'exit':
            self.notify.info('handleAvatarChooserDone: shutting down')
            self.loginFSM.request('shutdown')
            return

        subId, slot = self.avChoice.getChoice()
        self.avChoice.exit()
        if done == 'chose':
            av = self.avList[subId][slot]
            if av.dna.getTutorial() < 3 and self.skipTutorial == 0:
                self.tutorial = 1
            else:
                self.tutorial = 0

            self.loginFSM.request('waitForSetAvatarResponse', [av])
        else:
            if done == 'create':
                self.loginFSM.request('createAvatar', [self.avList[subId],
                    slot, subId])

    def exitChooseAvatar(self):
        self.handler = None
        self.avChoice.exit()
        self.avChoice.unload()
        self.avChoice = None
        self.ignore(self.avChoiceDoneEvent)

    def enterCreateAvatar(self, avList, index, subId):
        if self.skipTutorial:
            self.tutorial = 0
            self.avCreate = MakeAPirate(avList, 'makeAPirateComplete', subId, index, self.isPaid())
            self.avCreate.load()
            self.avCreate.enter()
            self.accept('makeAPirateComplete', self.__handleMakeAPirate)
        else:
            self.tutorial = 1
            dna = HumanDNA.HumanDNA()
            newPotAv = PotentialAvatar(0, ['dbp', '', '', ''], dna, index, 0)
            self.csm.sendCreateAvatar(newPotAv.dna, '', newPotAv.position)
            self.accept('createdNewAvatar', self.handleAvatarCreated, [newPotAv])

    def handleAvatarCreated(self, newPotAv, avatarId, subId):
        newPotAv.id = avatarId
        self.loginFSM.request('waitForSetAvatarResponse', [newPotAv])

    def __handleMakeAPirate(self):
        done = self.avCreate.getDoneStatus()
        if done == 'cancel':
            self.avCreate.exit()
            self.loginFSM.request('chooseAvatar', [self.avList])
        elif done == 'created':
            self.handleAvatarCreated(self.avCreate.newPotAv, self.avCreate.avId, self.avCreate.subId)
        else:
            self.notify.error('Invalid doneStatus from MakeAPirate: ' + str(done))

    def exitCreateAvatar(self):
        if self.skipTutorial:
            self.ignore('makeAPirateComplete')
            self.ignore('nameShopPost')
            self.ignore('nameShopCreateAvatar')
            self.avCreate.exit()
            self.avCreate.unload()
            self.avCreate = None
            self.handler = None

        self.ignore('createdNewAvatar')

    def sendGetAvatarsMsg(self):
        self.accept('avatarListFailed', self.avatarListFailed)
        self.accept('avatarList', self.avatarList)
        self.avatarManager.sendRequestAvatarList()

    def avatarListFailed(self, reason):
        self.ignore('avatarListFailed')
        self.ignore('avatarList')
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.avatarListFailedBox = dialogClass(message=PLocalizer.CRAvatarListFailed, doneEvent='avatarListFailedAck', text_wordwrap=18, style=OTPDialog.Acknowledge)
        self.avatarListFailedBox.show()
        self.acceptOnce('avatarListFailedAck', self.__handleAvatarListFailedAck)

    def __handleAvatarListFailedAck(self):
        self.ignore('avatarListFailedAck')
        self.avatarListFailedBox.cleanup()
        self.loginFSM.request('shutdown')

    def avatarList(self, avatars):
        self.ignore('avatarListFailed')
        self.ignore('avatarList')
        self.avList = {}
        for subId, avData in avatars.items():
            data = []
            self.avList[subId] = data
            for av in avData:
                if av == OTPGlobals.AvatarSlotAvailable:
                    data.append(OTPGlobals.AvatarSlotAvailable)
                elif av == OTPGlobals.AvatarSlotUnavailable:
                    data.append(OTPGlobals.AvatarSlotUnavailable)
                elif av == OTPGlobals.AvatarPendingCreate:
                    data.append(OTPGlobals.AvatarPendingCreate)
                else:
                    avNames = [av['name'], av['wishName'], '', '']

                    aName = 0
                    pa = PotentialAvatar(av['id'], avNames, av['dna'], av['slot'], aName, av['creator'], av['shared'],
                        av['online'], wishState=av['wishState'], wishName=av['wishName'],
                        defaultShard=av['defaultShard'], lastLogout=av['lastLogout'])

                    data.append(pa)

        if self.loginFSM.getCurrentState().getName() == 'chooseAvatar':
            self.avChoice.updateAvatarList()
        else:
            self.loginFSM.request('chooseAvatar', [self.avList])

    def handleGetAvatarsRespMsg(self, di):
        pass

    def handleGetAvatarsResp2Msg(self, di):
        pass

    def handleAvatarResponseMsg(self, avatarId, di):
        self.cleanupWaitingForDatabase()
        dclass = self.dclassesByName['DistributedPlayerPirate']
        NametagGlobals.setMasterArrowsOn(0)
        self.loadingScreen.show(waitForLocation=True)
        localAvatar = LocalPirate(self)
        localAvatar.dclass = dclass
        if __dev__:
            __builtins__['lu'] = self.getDo

        localAvatar.doId = avatarId
        self.localAvatarDoId = avatarId
        self.doId2do[avatarId] = localAvatar
        self.doId2ownerView[avatarId] = localAvatar
        parentId = None
        zoneId = None
        localAvatar.generateInit()
        localAvatar.generate()
        dclass.receiveUpdateBroadcastRequiredOwner(localAvatar, di)
        localAvatar.announceGenerate()
        localAvatar.postGenerateMessage()
        locUID = localAvatar.getReturnLocation()
        if locUID:
            self.loadingScreen.showTarget(locUID)
            self.loadingScreen.showHint(locUID)
            base.richPresence.setLocation(locUID)
        else:
            locUID = '1150922126.8dzlu'
            localAvatar.setReturnLocation(locUID)
            self.loadingScreen.showTarget(jail=True)

        self.loginFSM.request('playingGame')

    def handleGenerateWithRequiredOtherOwner(self, di):
        if self.loginFSM.getCurrentState().getName() == 'waitForSetAvatarResponse':
            doId = di.getUint32()
            parentId = di.getUint32()
            zoneId = di.getUint32()
            classId = di.getUint16()
            self.handleAvatarResponseMsg(doId, di)
        else:
            OTPClientRepository.handleGenerateWithRequiredOtherOwner(self, di)

    def enterWaitForDeleteAvatarResponse(self, potentialAvatar):
        raise StandardError, 'This should be handled within AvatarChooser.py'

    def exitWaitForDeleteAvatarResponse(self):
        raise StandardError, 'This should be handled within AvatarChooser.py'

    def sendMsgToTravelAgent(self, fieldName, args):
        dcfile = self.getDcFile()
        dclass = dcfile.getClassByName('DistributedTravelAgent')
        dg = dclass.clientFormatUpdate(fieldName, OtpDoGlobals.OTP_DO_ID_PIRATES_TRAVEL_AGENT, args)
        self.send(dg)

    @report(types=['deltaStamp', 'module'], prefix='------', dConfigParam='want-teleport-report')
    def enterPlayingGame(self):
        OTPClientRepository.enterPlayingGame(self)
        if __dev__ and config.GetBool('want-dev-hotkeys', False):

            def toggleKraken():
                if base.localAvatar:
                    if base.localAvatar.ship:
                        messenger.send('magicWord', ['~kraken', base.localAvatar.getDoId(), base.localAvatar.zoneId])

            self.accept(PiratesGlobals.KrakenHotkey, toggleKraken)

        def logout():
            self._userLoggingOut = True
            self.gameFSM.request('closeShard', ['waitForAvatarList'])

        self._userLoggingOut = False
        self.accept(PiratesGlobals.LogoutHotkey, logout)
        if __dev__ and config.GetBool('want-dev-hotkeys', False):

            def deployShip():
                messenger.send('magicWord', ['~deployShip', base.localAvatar.getDoId(), base.localAvatar.zoneId])

            self.accept(PiratesGlobals.ShipHotkey, deployShip)

        if localAvatar.style.getTutorial() < PiratesGlobals.TUT_MET_JOLLY_ROGER and self.skipTutorial == 0:
            localAvatar.teleportToType = PiratesGlobals.INSTANCE_TUTORIAL
            localAvatar.teleportToName = WorldGlobals.PiratesTutorialSceneFileBase
            self.sendMsgToTravelAgent('requestInitLocUD', ['unused', 0])
        elif localAvatar.onWelcomeWorld and self.defaultShard != 0 and config.GetBool('want-welcome-worlds', 0):
            localAvatar.teleportToType = PiratesGlobals.INSTANCE_WELCOME
            localAvatar.teleportToName = 'Welcome World'
            self.sendMsgToTravelAgent('requestInitLocUD', ['unused', 0])
        else:
            desiredShard = self.defaultShard
            localAvatar.teleportToType = PiratesGlobals.INSTANCE_MAIN
            localAvatar.teleportToName = WorldGlobals.PiratesWorldSceneFileBase
            self.sendMsgToTravelAgent('requestInitLocUD', ['unused', desiredShard])

    def playingGameLocReceived(self, shardId, zoneId):
        self.gameFSM.request('waitOnEnterResponses', [shardId, zoneId,
            zoneId, -1])

    def exitPlayingGame(self):
        self.notify.info('exitPlayingGame')
        self.loadingScreen.destroy()
        ivalMgr.interrupt()
        self.notify.info('sending clientLogout')
        messenger.send('clientLogout')
        if config.GetBool('want-dev-hotkeys', False):
            self.ignore(PiratesGlobals.KrakenHotkey)
            self.ignore(PiratesGlobals.ShipHotkey)
            self.ignore(PiratesGlobals.LogoutHotkey)

        self.uidMgr.reset()
        if self.distributedDistrict:
            self.distributedDistrict.worldCreator.cleanupAllAreas()

        for doId, obj in self.doId2do.items():
            if not isinstance(obj, LocalPirate) and not isinstance(obj, DistributedDistrict.DistributedDistrict):
                if hasattr(self, 'disableObject'):
                    self.disableObject(doId)

        if hasattr(base, 'localAvatar'):
            camera.reparentTo(render)
            camera.setPos(0, 0, 0)
            camera.setHpr(0, 0, 0)

        base.transitions.noTransitions()
        if self._userLoggingOut:
            self.detectLeaks(okTasks=['physics-avatar', 'memory-monitor-task', 'multitexFlatten'], okEvents=[
                'destroy-ToontownLoadingScreenTitle',
                'destroy-ToontownLoadingScreenTip',
                'destroy-ToontownLoadingScreenWaitBar',
                'f12',
                'f7',
                'close_main_window',
                'open_main_window',
                PiratesGlobals.LogoutHotkey])

        OTPClientRepository.exitPlayingGame(self)

    def enterTutorialQuestion(self, hoodId, zoneId, avId):
        self.__requestTutorial(hoodId, zoneId, avId)

    def handleTutorialQuestion(self, msgType, di):
        if msgType == CLIENT_ENTER_OBJECT_REQUIRED:
            self.handleGenerateWithRequired(di)
        elif msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
            self.handleGenerateWithRequired(di, other=True)
        elif msgType == CLIENT_OBJECT_SET_FIELD:
            self.handleUpdateField(di)
        elif msgType == CLIENT_OBJECT_LEAVING:
            self.handleDisable(di)
        elif msgType == CLIENT_OBJECT_LEAVING_OWNER:
            self.handleDisable(di, ownerView=True)
        else:
            self.handleUnexpectedMsgType(msgType, di)

    def exitTutorialQuestion(self):
        self.handler = None
        self.handlerArgs = None
        self.ignore('startTutorial')
        taskMgr.remove('waitingForTutorial')

    def __requestTutorial(self, hoodId, zoneId, avId):
        self.acceptOnce('startTutorial', self.__handleStartTutorial, [
            avId])

        messenger.send('requestTutorial')

    def __handleStartTutorial(self, avId, zoneId):
        self.gameFSM.request('playGame', [Tutorial, zoneId, avId])

    @report(types=['deltaStamp', 'module'], prefix='------', dConfigParam='want-teleport-report')
    def enterWaitOnEnterResponses(self, shardId, hoodId, zoneId, avId):
        self.cleanGameExit = False
        self.handlerArgs = {
            'hoodId': hoodId,
            'zoneId': zoneId,
            'avId': avId}

        if shardId is not None:
            district = self.activeDistrictMap.get(shardId)
        else:
            district = None

        if not district:
            self.distributedDistrict = self.getStartingDistrict()
            if self.distributedDistrict is None:
                self.loginFSM.request('noShards')
                return
            shardId = self.distributedDistrict.doId
        else:
            self.distributedDistrict = district

        self.waitForDatabaseTimeout(requestName='WaitOnEnterResponses')
        self.handleSetShardComplete()

    @report(types=['deltaStamp', 'module'], prefix='------', dConfigParam='want-teleport-report')
    def handleSetShardComplete(self):
        self.cleanupWaitingForDatabase()
        hoodId = self.handlerArgs['hoodId']
        zoneId = self.handlerArgs['zoneId']
        avId = self.handlerArgs['avId']
        self.uberZoneInterest = self.addInterest(base.localAvatar.getDefaultShard(), OTPGlobals.UberZone,
            'uberZone', 'uberZoneInterestComplete')

        self.acceptOnce('uberZoneInterestComplete', self.uberZoneInterestComplete)
        self.waitForDatabaseTimeout(20, requestName='waitingForUberZone')

    def getFriendFlags(self, doId):
        return 0

    def isFriend(self, doId):
        return self.avatarFriendsManager.isFriend(doId) or self.playerFriendsManager.isFriend(doId)

    def isFriendOnline(self, doId):
        info = self.identifyFriend(doId)
        if info:
            return info.isOnline()
        return False

    def identifyFriend(self, doId):
        pfm = self.playerFriendsManager
        afm = self.avatarFriendsManager
        pId = pfm.findPlayerIdFromAvId(doId)
        if pfm.isFriend(pId) or afm.isFriend(doId):
            return pfm.getFriendInfo(pId) or afm.getFriendInfo(doId)

    def getAvatar(self, doId):
        if doId in self.doId2do:
            return self.doId2do[doId]

    def identifyAvatar(self, doId):
        pass#return self.crewMatchManager.getHandle(doId) # TODO

    def identifyPlayer(self, playerId):
        return self.playerFriendsManager.getFriendInfo(playerId)

    def setViewpoint(self, obj, useOobe=1):
        wasOobe = 0
        try:
            if base.oobeMode is 1:
                wasOobe = 1
                base.oobe()
        except:
            pass
        else:
            obj.setViewpoint()
            if useOobe == 1 or wasOobe == 1:
                base.oobe()

    def getCycleCamTaskName(self):
        return 'cycleCam' + str(id(self))

    def cycleCameraObjects(self, delay, objType, task):
        currParentFound = 0
        newObj = None
        currObj = None
        searches = 0
        while newObj is None and searches < 2:
            for currId in base.cr.doId2do:
                currObj = base.cr.doId2do.get(currId)
                if isinstance(currObj, objType):
                    if self.currCamParent is None:
                        newObj = currObj
                        break
                    elif self.currCamParent == currId:
                        currParentFound = 1
                        continue
                    elif currParentFound:
                        newObj = currObj
                        break

            searches = searches + 1

        if newObj is not None:
            self.currCamParent = newObj.getDoId()
            self.setViewpoint(newObj, 0)
            print 'reparenting camera to object %d' % self.currCamParent
        else:
            print 'problem finding a new camera parent, will try again'

        if task:
            task.delayTime = delay

        return Task.again

    def stopCycleCamera(self):
        taskMgr.remove(self.getCycleCamTaskName())

    def handleObjDelete(self, obj):
        if self.currCamParent == obj.getDoId():
            self.currCamParent = None

    def toggleAutoCamReparent(self, word):
        if taskMgr.hasTaskNamed(self.getCycleCamTaskName()):
            self.stopCycleCamera()
            return

        delay = 10
        args = word.split()
        if len(args) >= 2:
            delay = int(args[1])

        if word == '~ccNPC':
            objType = DistributedBattleNPC.DistributedBattleNPC
        else:
            objType = DistributedShip.DistributedShip

        taskMgr.doMethodLater(0.5, self.cycleCameraObjects, self.getCycleCamTaskName(),
            extraArgs=[delay, objType], appendTask=True)

    def performCamReparent(self, objDoId=None):
        selectedObj = localAvatar.currentTarget
        if objDoId:
            obj = base.cr.doId2do[objDoId]
            if obj and self.currCamParent is not obj:
                self.setViewpoint(obj)
                return

        if selectedObj and self.currCamParent is None:
            self.currCamParent = selectedObj.getDoId()
            self.setViewpoint(selectedObj)
        elif self.currCamParent is not None:
            if selectedObj is None or selectedObj.compareTo(camera.getParent()) is 0:
                camera.reparentTo(base.localAvatar)
                self.currCamParent = None
                try:
                    if base.oobeMode is 1:
                        base.oobe()
                except:
                    pass
            else:
                self.setViewpoint(selectedObj)

    def handleDelete(self, di):
        doId = di.getUint32()

        if doId in self.doId2ownerView:
            return

        self.deleteObject(doId)

    def deleteObject(self, doId, ownerView = False):
        if self.doId2do.has_key(doId):
            obj = self.doId2do[doId]
            del self.doId2do[doId]
            obj.deleteOrDelay()
            if obj.getDelayDeleteCount() <= 0:
                obj.detectLeaks()
        elif self.cache.contains(doId):
            self.cache.delete(doId)
        else:
            self.notify.warning('Asked to delete non-existent DistObj ' + str(doId))

    def enterCloseShard(self, loginState=None):
        self.loadingScreen.show()
        self._processVisStopIW = InterestWatcher(self, 'stopProcessViz')
        self.acceptOnce(self._processVisStopIW.getDoneEvent(), Functor(self._removeShardObjects,
            loginState))

        messenger.send(PiratesClientRepository.StopVisibilityEvent)
        self._processVisStopIW.stopCollect()
        OTPClientRepository.enterCloseShard(self, loginState)

    def _removeShardObjects(self, loginState):
        callback = self._deleteLocalAv
        self.cache.turnOff()
        localAvatar.clearInventoryInterest()
        if base.slowCloseShard:
            taskMgr.doMethodLater(base.slowCloseShardDelay * 0.5, Functor(self.removeShardInterest,
                callback), 'slowCloseShard')
        else:
            self.removeShardInterest(callback)

    def _deleteLocalAv(self):
        self.sendSetAvatarIdMsg(0)
        self._removeAllOV()
        self.disableDoId(localAvatar.doId)
        self.cache.turnOn()
        self.loginFSM.request(self._closeShardLoginState)

    def enterNoConnection(self):
        OTPClientRepository.enterNoConnection(self)
        if hasattr(base, 'localAvatar'):
            base.localAvatar.logDefaultShard()

    def _disableLocalAv(self, loginState):
        self._localAvDisableIW = InterestWatcher(self, 'disableLocalAv', mustCollect=True)
        self.acceptOnce(self._localAvDisableIW.getDoneEvent(), self._removeLocalAvFromStateServer)
        self.disableDoId(localAvatar.doId)
        self._localAvDisableIW.stopCollect()

    def isShardInterestOpen(self):
        return False

    def _removeCurrentShardInterest(self, callback):
        parentId2handles = {}
        for handle, state in self._interests.items():
            parentId2handles.setdefault(state.parentId, set())
            parentId2handles[state.parentId].add(handle)

        doId2parentId = {}
        for doId in parentId2handles.keys():
            obj = self.getDo(doId)
            if obj is not None:
                doId2parentId[doId] = obj.parentId

        parentId2childIds = {}
        for doId, parentId in doId2parentId.items():
            parentId2childIds.setdefault(parentId, set())
            parentId2childIds[parentId].add(doId)

        print 'parentId2handles: %s' % parentId2handles
        print 'parentId2childIds: %s' % parentId2childIds
        self.closeShardEGroup = EventGroup('closeShardInterest')
        self.acceptOnce(self.closeShardEGroup.getDoneEvent(), callback)
        for districtId in self.activeDistrictMap.keys():
            self._remInterests(districtId, parentId2childIds, parentId2handles)

    def _remInterests(self, parentId, parentId2childIds, parentId2handles):
        for childId in parentId2childIds.get(parentId, tuple()):
            self._remInterests(childId, parentId2childIds, parentId2handles)

        for handle in parentId2handles.get(parentId, tuple()):
            if not self._interests[handle].isPendingDelete():
                self.removeInterest(DoInterestManager.InterestHandle(handle),
                    self.closeShardEGroup.newEvent('handle-%s' % handle))

    def exitCloseShard(self):
        self.loadingScreen.hide()
        if hasattr(self, 'closeShardEGroup'):
            self.ignore(self.closeShardEGroup.getDoneEvent())
            del self.closeShardEGroup

        if hasattr(self, '_localAvDisableIW'):
            self.ignore(self._localAvDisableIW.getDoneEvent())
            self._localAvDisableIW.destroy()
            del self._localAvDisableIW

        if hasattr(self, '_processVisStopIW'):
            self.ignore(self._processVisStopIW.getDoneEvent())
            self._processVisStopIW.destroy()
            del self._processVisStopIW

        OTPClientRepository.exitCloseShard(self)

    def startReaderPollTask(self):
        print '########## startReaderPollTask Pirate'
        self.stopReaderPollTask()
        self.accept(CConnectionRepository.getOverflowEventName(), self.handleReaderOverflow)
        if want_fifothreads:
            self.ClientNetworkReader = ClientNetworkReader(self)
            self.ClientNetworkReader.start(TPLow, False)
        else:
            taskMgr.add(self.readerPollUntilEmpty, self.uniqueName('readerPollTask'), priority=self.taskPriority)

    def stopReaderPollTask(self):
        print '########## stopReaderPollTask Pirate'
        self.ignore(CConnectionRepository.getOverflowEventName())
        if want_fifothreads:
            if hasattr(self, 'ClientNetworkReader'):
                self.ClientNetworkReader.PleaseStop()
                del self.ClientNetworkReader
        else:
            taskMgr.remove(self.uniqueName('readerPollTask'))

    def taskManagerDoYieldCall(self, frameStartTime, nextScheuledTaksTime):
        Thread.forceYield()

    def yieldThread(self, comment=''):
        if want_fifothreads:
            Thread.considerYield()

    def handleSystemMessage(self, di):
        message = ClientRepositoryBase.handleSystemMessage(self, di)
        if hasattr(base, 'chatAssistant') and hasattr(base, 'localAvatar'):
            base.chatAssistant.receiveSystemMessage(message)
        else:
            if self.fakeMSP is None:
                from pirates.piratesgui.MessageStackPanel import MessageStackPanel
                self.fakeMSP = MessageStackPanel(parent=base.a2dBottomLeft, relief=None, pos=(1.75, 0, 1.3))
            self.fakeMSP.addTextMessage(message, seconds=20, priority=0, color=(0.5, 0, 0, 1), icon=('admin', ''))

            def cleanupFakeMSP(task):
                if self.fakeMSP is not None:
                    self.fakeMSP.destroy()
                    self.fakeMSP = None

            taskMgr.remove('cleanupFakeMSP')
            taskMgr.doMethodLater(25.0, cleanupFakeMSP, 'cleanupFakeMSP')

        if not self.systemMessageSfx:
            self.systemMessageSfx = base.loader.loadSfx('phase_3.5/audio/sfx/GUI_whisper_3.mp3')

        if self.systemMessageSfx:
            base.playSfx(self.systemMessageSfx)

    def setDistrict(self, district):
        self.district = district

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def addTaggedInterest(self, parentId, zone, interestTags, event=None):
        context = self.addInterest(parentId, zone, interestTags[0], event)
        if context:
            self.notify.debug('adding interest %d: %d %d' % (context.asInt(),
                parentId, zone))

            self.interestHandles.append([interestTags, context])
            return

        self.notify.warning('Tried to set interest when shard was closed')

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def clearTaggedInterest(self, event):
        if len(self.interestHandles) > 0:
            contextInfo = self.interestHandles[0]
            self.notify.debug('removing interest %d' % contextInfo[1])
            self.removeInterest(contextInfo[1], event)
            self.interestHandles.remove(contextInfo)

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def clearTaggedInterestNamed(self, callback, interestTags):
        toBeRemoved = []
        numInterests = 0
        for currContext in self.interestHandles:
            matchFound = False
            for currTag in interestTags:
                if currTag in currContext[0]:
                    matchFound = True
                    break

            if matchFound:
                context = currContext[1]
                self.notify.debug('removing interest %s' % context)
                self.removeInterest(context, callback)
                toBeRemoved.append(currContext)
                numInterests += 1

        for currToBeRemoved in toBeRemoved:
            self.interestHandles.remove(currToBeRemoved)

        if numInterests == 0 and callback:
            messenger.send(callback)

        return numInterests

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def replaceTaggedInterestTag(self, oldTag, newTag):
        for tags, handle in self.interestHandles:
            if oldTag in tags:
                tags.remove(oldTag)
                tags.append(newTag)
                base.cr.updateInterestDescription(handle, newTag)
