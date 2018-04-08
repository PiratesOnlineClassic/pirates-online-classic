import random
import re

import Townfolk
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from otp.nametag.NametagConstants import CFSpeech, CFThought, CFTimeout, CFPageButton, CFNoQuitButton, CFQuitButton
from pandac.PandaModules import *
from pirates.battle import (DistributedBattleAvatar, DistributedBattleNPC,
                            EnemyGlobals, WeaponGlobals)
from pirates.distributed import InteractGlobals
from pirates.economy import DistributedShopKeeper, EconomyGlobals
from pirates.interact import InteractiveBase
from pirates.leveleditor import CustomAnims, NPCList
from pirates.pirate import AvatarTypes, Biped, HumanDNA, TitleGlobals
from pirates.piratesbase import MusicManager, PiratesGlobals, PLocalizer
from pirates.piratesgui import (InteractGUI, NamePanelGui, PDialog,
                                PiratesGuiGlobals)
from pirates.piratesgui.NewTutorialPanel import NewTutorialPanel
from pirates.quest import QuestParser, QuestTaskDNA
from pirates.quest.QuestConstants import NPCIds
from pirates.uberdog.UberDogGlobals import *


class DistributedNPCTownfolk(DistributedBattleNPC.DistributedBattleNPC, DistributedShopKeeper.DistributedShopKeeper, Townfolk.Townfolk):
    __module__ = __name__
    DiskWaitingColor = (0, 0, 1, 0.5)
    DiskUseColor = None
    HelpTextIconTexture = None
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCTownfolk')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        DistributedShopKeeper.DistributedShopKeeper.__init__(self)
        Townfolk.Townfolk.__init__(self)
        self.interactSphereNodePath = None
        self.interactMode = 0
        self.interactCamPosHpr = 0
        self.purgeInteractGui = 0
        self.beginFight = 0
        self.respecWeapon = 0
        self.pendingDoMovie = None
        self.hideHpMeterFlag = 1
        self.confirmDialog = None
        self.amUsingObj = None
        self.interactAnim = None
        self.animIval = None
        self.interactGUI = None
        self.questMenuGUI = None
        self.respecMenuGUI = None
        self.shipNamePanel = None
        self.classNameText = None
        self.shopId = PiratesGlobals.PORT_ROYAL_DEFAULTS
        self.helpId = 0
        return

    def makeMyAnimDict(self, gender, animNames):
        self.makeAnimDict(gender, animNames)

    def generateMyself(self):
        Townfolk.Townfolk.generateHuman(self, self.style.gender, base.cr.human)

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
        yieldThread('battle gen')
        DistributedShopKeeper.DistributedShopKeeper.announceGenerate(self)
        yieldThread('shop gen')
        self.setName(self.name)
        self.setInteractOptions(proximityText=PLocalizer.InteractNamedTownfolk % self.name)
        localAvatar.checkForAutoTrigger(self.doId)
        yieldThread('auto trigger')
        if not self.canMove:
            self.motionFSM.off()
        self.updateNametagQuestIcon()
        self.accept('localAvatarQuestComplete', self.updateNametagQuestIcon)
        self.accept('localAvatarQuestUpdate', self.updateNametagQuestIcon)
        self.accept('localAvatarQuestItemUpdate', self.updateNametagQuestIcon)
        self.accept('inventoryAddDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS), self.updateNametagQuestIcon)
        self.accept('inventoryRemoveDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS), self.updateNametagQuestIcon)
        if self.getHelpId():
            if DistributedNPCTownfolk.HelpTextIconTexture is None:
                gui = loader.loadModel('models/gui/toplevel_gui')
                DistributedNPCTownfolk.HelpTextIconTexture = gui.find('**/generic_question*')
            self.nametagIcon = DistributedNPCTownfolk.HelpTextIconTexture.copyTo(self.nametag3d)
            self.nametagIcon.setScale(20)
            self.nametagIcon.setPos(0, 0, 3.5)
            self.nametagIcon.reparentTo(self.getNameText())
            self.nametagIcon.setDepthWrite(0)
            self.nametagIconGlow = loader.loadModel('models/effects/lanternGlow')
            self.nametagIconGlow.reparentTo(self.nametag.getNameIcon())
            self.nametagIconGlow.setScale(10.0)
            self.nametagIconGlow.setColorScaleOff()
            self.nametagIconGlow.setFogOff()
            self.nametagIconGlow.setLightOff()
            self.nametagIconGlow.setPos(0, -0.05, 3.2)
            self.nametagIconGlow.setDepthWrite(0)
            self.nametagIconGlow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            self.nametagIconGlow.setColor(0.85, 0.85, 0.85, 0.85)
        return

    def autoTriggerCheck(self, Task=None):
        localAvatar.checkForAutoTrigger(self.doId)
        if Task:
            return Task.done

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        DistributedShopKeeper.DistributedShopKeeper.generate(self)

    def setupAnimInfoState(self, state, info):
        if len(info) < len(self.FailsafeAnims):
            info += self.FailsafeAnims[len(info) - len(self.FailsafeAnims):]
        self.animInfo[state] = info

    def disable(self):
        self.stopInteract(localAvatar)
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        DistributedShopKeeper.DistributedShopKeeper.disable(self)
        self.stopBlink()
        if self.pendingDoMovie:
            base.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
            self.pendingDoMovie = None
        self.ignore('doneChatPage')
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if self.animIval:
            self.animIval.pause()
            self.animIval = None
        self.ignore('localAvatarQuestComplete')
        self.ignore('localAvatarQuestUpdate')
        self.ignore('localAvatarQuestItemUpdate')
        self.ignore('inventoryAddDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS))
        self.ignore('inventoryRemoveDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS))
        return

    def delete(self):
        DistributedBattleNPC.DistributedBattleNPC.delete(self)
        DistributedShopKeeper.DistributedShopKeeper.delete(self)
        self.ignoreAll()
        Townfolk.Townfolk.delete(self)

    def getNameText(self):
        return Townfolk.Townfolk.getNameText(self)

    def isBattleable(self):
        return 0

    def setDNAId(self, dnaId):
        if dnaId and NPCList.NPC_LIST.has_key(dnaId):
            dnaDict = NPCList.NPC_LIST[dnaId]
            customDNA = HumanDNA.HumanDNA()
            customDNA.loadFromNPCDict(dnaDict)
            self.setDNAString(customDNA)
        else:
            if dnaId and re.search('/', dnaId):
                self.loadCast(dnaId)
            else:
                self.setDNAString(None)
                self.setDefaultDNA()
                self.style.makeNPCTownfolk()
        return

    def requestInteraction(self, avId, interactType=0):
        if localAvatar.zombie and avId == localAvatar.doId:
            localAvatar.guiMgr.createWarning(PLocalizer.ZombieNoPeople, PiratesGuiGlobals.TextFG6)
            return
        DistributedBattleNPC.DistributedBattleNPC.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        self.cancelInteraction(base.localAvatar)
        DistributedBattleNPC.DistributedBattleNPC.rejectInteraction(self)

    def requestStopInteract(self):
        messenger.send('stop interact', [])
        self.requestExit()

    def startInteract(self, av):
        if av == base.localAvatar and not self.interactMode:
            self.interactMode = 1
            self.setNameVisible(0)
            self.hideHpMeterFlag = 1
            self.playedFirstDialog = False
            self.setChatAbsolute('', CFSpeech | CFTimeout)
            self.acceptInteraction()
            if self.avatarType.isA(AvatarTypes.Tailor) or self.avatarType.isA(AvatarTypes.Tattoo) or self.avatarType.isA(AvatarTypes.Jeweler) or self.avatarType.isA(AvatarTypes.Barber):
                localAvatar.setSoloInteraction(True)

    def stopInteract(self, av, dialogStr=''):
        if av == base.localAvatar and self.interactMode and not self.isDeleted():
            localAvatar.setSoloInteraction(False)
            self.cleanUpQuestDetails()
            self.cleanUpQuestMenu()
            if self.interactGUI:
                self.notify.warning('stopInteract: old interact GUI still around')
                self.interactGUI.destroy()
                self.interactGUI = None
            if self.respecMenuGUI:
                self.respecMenuGUI.destroy()
                self.respecMenuGUI = None
            self.finishShopping()
            self.playDialog(dialogStr=dialogStr)
            self.interactMode = 0
            self.setNameVisible(1)
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
            base.cr.interactionMgr.start()
            if self.amUsingObj:
                interactType = self.amUsingObj.interactType
            else:
                interactType = self.animSet
            self.endInteractMovie(interactType)
        return

    def playDialog(self, dialogStr=''):
        if dialogStr:
            self.playQuestString(dialogStr, timeout=True)
        else:
            if self.firstDialog == True and self.dialogFlag == 0:
                questStr = ''
                if self.getUniqueId() in PLocalizer.GreetingStrings:
                    questStr = PLocalizer.GreetingStrings[self.getUniqueId()].get('greeting')
                    if questStr is None or len(questStr) == 0:
                        questStr = InteractGlobals.getNPCGreeting(self.avatarType)
                else:
                    questStr = InteractGlobals.getNPCGreeting(self.avatarType)
                self.playQuestString(questStr, timeout=True)
            else:
                if self.dialogFlag == 0:
                    questStr = ''
                    if self.getUniqueId() in PLocalizer.GreetingStrings:
                        questStr = PLocalizer.GreetingStrings[self.getUniqueId()].get('goodbye')
                        if questStr is None or len(questStr) == 0:
                            questStr = InteractGlobals.getNPCGreeting(self.avatarType)
                    else:
                        questStr = InteractGlobals.getNPCGoodbye(self.avatarType)
                    self.playQuestString(questStr, timeout=True, useChatBubble=True)
                else:
                    if self.dialogFlag == 1:
                        questStr = InteractGlobals.getNPCDuring(self.avatarType)
                        self.playQuestString(questStr, timeout=True, useChatBubble=True)
                    else:
                        if self.dialogFlag == 2:
                            questStr = ''
                            if self.getHelpId():
                                helpStrings = PLocalizer.townfolkHelpText.get(self.getHelpId())
                                self.clearOffer()
                                if len(helpStrings):
                                    self.playQuestString(random.choice(helpStrings), timeout=False)
                            else:
                                if self.getUniqueId() in PLocalizer.GreetingStrings:
                                    questStr = PLocalizer.GreetingStrings[self.getUniqueId()].get('brushoff')
                                    if questStr is None or len(questStr) == 0:
                                        questStr = InteractGlobals.getNPCGreeting(self.avatarType)
                                else:
                                    questStr = InteractGlobals.getNPCBrushoff(self.avatarType)
                                    if not base.config.GetBool('want-privateering', True):
                                        if self.getUniqueId() in [NPCIds.PIERRE_LE_PORC, NPCIds.GARCIA_DE_AVARCIA]:
                                            questStr = random.choice(PLocalizer.ShipPVPLordBrushoff)
                                self.playQuestString(questStr, timeout=True, useChatBubble=True)
                        else:
                            self.notify.warning('Invalid dialogFlag: %d' % self.dialogFlag)
        self.newDialog = False
        self.dialogFlag = 0
        return

    def hasOpenGUI(self):
        if self.interactGUI or self.questMenuGUI or self.shipNamePanel:
            return True
        return False

    def offerOptions(self, dialogFlag):
        self.dialogFlag = dialogFlag
        if self.interactGUI:
            self.notify.warning('offerOptions: old interact GUI still around')
            self.interactGUI.destroy()
            self.interactGUI = None
        if hasattr(self, 'currentDialogMovie') or self.purgeInteractGui or self.playingQuestString == True:
            self.receiveOffer(self.InteractOffer)
            self.genericDialog = False
            return
        if not self.interactMode:
            return
        if self.avatarType.isA(AvatarTypes.Musician):
            self.acceptOnce('stoppedShopping', self.cancelInteraction, [base.localAvatar])
            self.startShopping(InteractGlobals.MUSICIAN)
            if localAvatar.getGameState() != 'NPCInteract':
                localAvatar.b_setGameState('NPCInteract', localArgs=[self, True])
            self.clearOffer()
            return
        optionIds, stateCodes, bribeType = self.computeOptions()
        anyActive = False
        for i in range(len(optionIds)):
            if optionIds[i] != InteractGlobals.CANCEL and stateCodes[i] != InteractGlobals.DISABLED:
                anyActive = True
                break

        if anyActive:
            self.interactGUI = InteractGUI.InteractGUI()
            title = self.getMenuTitle()
            self.interactGUI.setOptions(title, optionIds, stateCodes, self.selectOptionConfirm, bribeType)
        else:
            if self.dialogOpen == False:
                if self.firstDialog == True:
                    self.dialogFlag = 2
                if not self.getHelpId():
                    self.cancelInteraction(base.localAvatar)
                    return
        if localAvatar.getGameState() != 'NPCInteract':
            localAvatar.b_setGameState('NPCInteract', localArgs=[self, True])
        if self.dialogOpen == False:
            self.playDialog()
        else:
            self.newDialog = True
            self.dialogFlag = dialogFlag
        self.clearOffer()
        return

    def selectOptionConfirm(self, optionId):
        if optionId == InteractGlobals.BRIBE:
            self.confirmBribe()
        else:
            if optionId == InteractGlobals.HEAL_HP:
                self.confirmHealHp()
            else:
                if optionId == InteractGlobals.HEAL_MOJO:
                    self.confirmHealMojo()
                else:
                    if optionId == InteractGlobals.RESPEC:
                        self.showRespecMenu()
                    else:
                        self.b_selectOption(optionId)

    def setMovie(self, mode, avId):

        def doMovie(av):
            if mode == 'start':
                pass
            else:
                if mode == 'stop':
                    self.cancelInteraction(av)
                else:
                    if mode == 'clear':
                        pass
            self.pendingDoMovie = None
            return

        av = base.cr.doId2do.get(avId)
        if avId != 0 and not av:
            self.notify.warning('setMovie: avId: %s not found' % avId)
            if self.pendingDoMovie:
                base.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
                self.pendingDoMovie = None
            self.pendingDoMovie = base.cr.relatedObjectMgr.requestObjects([avId], eachCallback=doMovie, timeout=60)
        else:
            doMovie(av)
        return

    def getMenuTitle(self):
        return self.getName()

    def confirmHealHp(self):
        maxHp = localAvatar.getAdjMaxHp()
        hp = localAvatar.getHp()
        from pirates.economy import EconomyGlobals
        gold = EconomyGlobals.getAvatarHealHpCost(maxHp - hp)
        if self.confirmDialog:
            self.confirmDialog.destroy()
        self.confirmDialog = PDialog.PDialog(text=PLocalizer.HealHpConfirmDialog % {'gold': gold}, style=OTPDialog.YesNo, command=self.__handleHealHpConfirmation)

    def __handleHealHpConfirmation(self, value):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if value == 1:
            self.b_selectOption(InteractGlobals.HEAL_HP)
        return

    def confirmHealMojo(self):
        maxMojo = localAvatar.getMaxMojo()
        mojo = localAvatar.getMojo()
        gold = EconomyGlobals.getAvatarHealMojoCost(maxMojo - mojo)
        if self.confirmDialog:
            self.confirmDialog.destroy()
        self.confirmDialog = PDialog.PDialog(text=PLocalizer.HealMojoConfirmDialog % {'gold': gold}, style=OTPDialog.YesNo, command=self.__handleHealMojoConfirmation)

    def __handleHealMojoConfirmation(self, value):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if value == 1:
            self.b_selectOption(InteractGlobals.HEAL_MOJO)
        return

    def confirmBribe(self):
        gold = 0
        for quest in localAvatar.getInventory().getQuestList():
            if quest.isComplete():
                continue
            for task in quest.questDNA.getTasks():
                if isinstance(task, QuestTaskDNA.BribeNPCTaskDNA) and task.getNpcId() == self.getUniqueId() and task.getGold() > gold:
                    gold = task.getGold()

        if self.confirmDialog:
            self.confirmDialog.destroy()
        avGold = localAvatar.getMoney()
        if avGold >= gold:
            self.confirmDialog = PDialog.PDialog(text=PLocalizer.BribeConfirmDialog % {'name': self.getName(), 'gold': gold}, style=OTPDialog.YesNo, command=self.__handleBribeConfirmation)
        else:
            self.confirmDialog = PDialog.PDialog(text=PLocalizer.BribeNotEnoughGold % {'gold': gold}, style=OTPDialog.CancelOnly, command=self.__handleBribeConfirmation)
        gui = loader.loadModel('models/gui/toplevel_gui')
        goldCoin = gui.find('**/treasure_w_coin*')
        self.confirmDialog.goldLabel = DirectLabel(parent=self.confirmDialog, relief=0, text=PLocalizer.BribeConfirmYourGold % avGold, text_align=TextNode.ALeft, text_scale=0.035, text_pos=(0.0,
                                                                                                                                                                                              0.0), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, image=goldCoin, image_scale=0.22, image_pos=(-0.04, 0, 0.01), pos=(-0.08, 0, -0.12))

    def __handleBribeConfirmation(self, value):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if value == 1:
            self.b_selectOption(InteractGlobals.BRIBE)
        return

    def computeOptions(self):
        questButtonState = InteractGlobals.NORMAL
        shipButtonState = InteractGlobals.NORMAL
        sellShipButtonState = InteractGlobals.NORMAL
        repairButtonState = InteractGlobals.DISABLED
        healButtonState = InteractGlobals.DISABLED
        healMojoButtonState = InteractGlobals.DISABLED
        storeButtonState = InteractGlobals.DISABLED
        sailButtonState = InteractGlobals.DISABLED
        sailTMButtonState = InteractGlobals.DISABLED
        bribeButtonState = InteractGlobals.DISABLED
        respecButtonState = InteractGlobals.NORMAL
        if not self.anyWeaponsRespecable():
            respecButtonState = InteractGlobals.DISABLED
        bribeType = 0
        inv = localAvatar.getInventory()
        if inv is None:
            self.notify.warning('computeOptions: inventory not present')
        else:
            if len(inv.getQuestList()) >= inv.getStackLimit(InventoryType.OpenQuestSlot) or not self.hasQuestOffers():
                questButtonState = InteractGlobals.DISABLED
            for quest in inv.getQuestList():
                foundBribe = 0
                if quest.isComplete():
                    continue
                if quest.questDNA is None:
                    self.notify.error('quest %s: does not contain a dna; is it a rogue quest, given in error?' % quest.getQuestId())
                for task in quest.questDNA.getTasks():
                    if isinstance(task, QuestTaskDNA.BribeNPCTaskDNA) and task.getNpcId() == self.getUniqueId():
                        bribeButtonState = InteractGlobals.NORMAL
                        foundBribe = 1
                        bribeType = task.bribeType
                        break

                if foundBribe:
                    break

            if len(inv.getShipDoIdList()) >= inv.getCategoryLimit(InventoryCategory.SHIPS) or localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_SHIP:
                shipButtonState = InteractGlobals.DISABLED
            if len(inv.getShipDoIdList()) <= 0:
                sellShipButtonState = InteractGlobals.DISABLED
            for shipId in inv.getShipDoIdList():
                sailButtonState = InteractGlobals.NORMAL
                ship = base.cr.getOwnerView(shipId)
                if ship:
                    if ship.Hp < ship.maxHp:
                        repairButtonState = InteractGlobals.NORMAL

            if inv.getTreasureMapsList():
                if sailButtonState == InteractGlobals.NORMAL:
                    sailTMButtonState = InteractGlobals.NORMAL
        if base.localAvatar.hp < base.localAvatar.getAdjMaxHp():
            healButtonState = InteractGlobals.NORMAL
        if base.localAvatar.mojo < base.localAvatar.maxMojo:
            healMojoButtonState = InteractGlobals.NORMAL
        if self.shopInventory:
            storeButtonState = InteractGlobals.NORMAL
        print 'DEBUG - optionIds: %s' % InteractGlobals.getNPCInteractMenu(self.avatarType)[1]
        optionIds = InteractGlobals.getNPCInteractMenu(self.avatarType)[1]
        buttonStateDict = {InteractGlobals.QUEST: questButtonState, InteractGlobals.TALK: InteractGlobals.DISABLED, InteractGlobals.DUEL: InteractGlobals.DISABLED, InteractGlobals.STORE: storeButtonState, InteractGlobals.SHIPS: shipButtonState, InteractGlobals.SELL_SHIPS: sellShipButtonState, InteractGlobals.TRAIN: InteractGlobals.DISABLED, InteractGlobals.REPAIR: repairButtonState, InteractGlobals.UPGRADE: InteractGlobals.DISABLED, InteractGlobals.TRADE: InteractGlobals.DISABLED, InteractGlobals.HEAL_HP: healButtonState, InteractGlobals.HEAL_MOJO: healMojoButtonState, InteractGlobals.CANCEL: InteractGlobals.NORMAL, InteractGlobals.SAIL: sailButtonState, InteractGlobals.SAILTM: sailTMButtonState, InteractGlobals.BRIBE: bribeButtonState, InteractGlobals.ACCESSORIES_STORE: InteractGlobals.NORMAL, InteractGlobals.TATTOO_STORE: InteractGlobals.NORMAL, InteractGlobals.JEWELRY_STORE: InteractGlobals.NORMAL, InteractGlobals.BARBER_STORE: InteractGlobals.NORMAL, InteractGlobals.RESPEC: respecButtonState, InteractGlobals.MUSICIAN: InteractGlobals.NORMAL, InteractGlobals.PVP_REWARDS_TATTOO: InteractGlobals.NORMAL, InteractGlobals.PVP_REWARDS_EYE_PATCHES: InteractGlobals.DISABLED, InteractGlobals.PVP_REWARDS_HATS: InteractGlobals.DISABLED}
        stateCodes = []
        for i in range(len(optionIds)):
            state = buttonStateDict.get(optionIds[i])
            if not state:
                state = InteractGlobals.DISABLED
            stateCodes.append(state)

        return (
         optionIds, stateCodes, bribeType)
        return

    def d_selectOption(self, optionId):
        DistributedBattleNPC.DistributedBattleNPC.d_selectOption(self, optionId)

    def selectOption(self, optionId):
        if optionId in [InteractGlobals.STORE, InteractGlobals.TRAIN, InteractGlobals.SHIPS, InteractGlobals.UPGRADE, InteractGlobals.ACCESSORIES_STORE, InteractGlobals.TATTOO_STORE, InteractGlobals.JEWELRY_STORE, InteractGlobals.BARBER_STORE, InteractGlobals.PVP_REWARDS_TATTOO]:
            if self.interactGUI:
                self.interactGUI.hide()
            self.startShopping(optionId)
        else:
            if optionId == InteractGlobals.MUSICIAN:
                if self.interactGUI:
                    self.interactGUI.hide()
                self.startShopping(optionId)
            else:
                if optionId == InteractGlobals.REPAIR:
                    if self.interactGUI:
                        self.interactGUI.hide()
                    self.startRepair(optionId)
                else:
                    if optionId == InteractGlobals.SELL_SHIPS:
                        if self.interactGUI:
                            self.interactGUI.hide()
                        self.startSellShip(optionId)
                    else:
                        if optionId == InteractGlobals.OVERHAUL:
                            if self.interactGUI:
                                self.interactGUI.hide()
                            self.startOverhaul(optionId)
                        else:
                            if optionId == InteractGlobals.QUEST:
                                if self.interactGUI:
                                    self.interactGUI.hide()
                            else:
                                if optionId == InteractGlobals.BRIBE:
                                    if self.interactGUI:
                                        self.interactGUI.destroy()
                                        self.interactGUI = None
                                else:
                                    if optionId == InteractGlobals.CANCEL:
                                        if self.interactGUI:
                                            self.interactGUI.hide()
                                        self.cancelInteraction(base.localAvatar)
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-shipdeploy-report')
    def cancelInteraction(self, av, dialogStr=''):
        if av == localAvatar:
            self.requestStopInteract()
            self.stopInteract(av, dialogStr=dialogStr)
            self.firstDialog = True
            if av.playRewardAnimation:
                localAvatar.b_setGameState('WeaponReceive')

    def handleEndInteractKey(self):
        cutscenePlaying = False
        if base.cr.currentCutscene and not base.cr.currentCutscene.isEmpty():
            cutscenePlaying = True
        if not hasattr(self, 'currentDialogMovie') and not cutscenePlaying:
            if self.getHelpId():
                self.playingQuestString = False
                self.dialogOpen = False
            self.cancelInteraction(base.localAvatar)
        else:
            self.notify.warning('handleEndInteractKey failed')

    def finishShopping(self):
        DistributedShopKeeper.DistributedShopKeeper.finishShopping(self)
        if self.interactGUI:
            self.interactGUI.show()
        self.ignore('makeSale')

    def makeSaleResponse(self, result):
        DistributedShopKeeper.DistributedShopKeeper.makeSaleResponse(self, result)
        self.ignore('makeSale')

    def swordTutorialPt1(self):
        self.sendUpdate('swordTutorialPt1', [localAvatar.getDoId()])
        localAvatar.cameraFSM.request('FPS')

    def pistolTutorialPt1(self):
        self.sendUpdate('pistolTutorialPt1', [localAvatar.getDoId()])

    def setHp(self, hitPoints, quietly):
        DistributedBattleNPC.DistributedBattleNPC.setHp(self, hitPoints, quietly)

    def drawWeapon(self):
        print 'draw weapon'
        ival = self.pullOutCurrentWeapon()
        ival.start()

    def putAwayWeapon(self):
        self.beginFight = 0
        self.loop('idle')

    def drawSwordTutorial(self):
        self.drawSwordPanel = NewTutorialPanel(['drawSword'])
        taskMgr.doMethodLater(4.0, self.drawSwordPanel.activate, self.uniqueName('drawSwordPanelPause'), extraArgs=[])

    def attackSwordTutorial(self):
        if not self.beginFight:
            base.localAvatar.guiMgr.subtitler.confirmCallback()
            self.beginFight = 1
        taskMgr.remove(self.uniqueName('drawSwordPanelPause'))
        if hasattr(self, 'drawSwordPanel'):
            self.drawSwordPanel.hide()
        self.attackSwordPanel = NewTutorialPanel(['attackSword'])
        taskMgr.doMethodLater(4.0, self.attackSwordPanel.activate, self.uniqueName('attackSwordPanelPause'), extraArgs=[])

    def createHpMeter(self):
        pass

    def listenTime(self):
        self.accept('tooFast', self.tooFast)
        self.accept('tooSlow', self.tooSlow)

    def tooFast(self):
        pass

    def tooSlow(self):
        pass

    def ignoreTime(self):
        self.ignore('tooFast')
        self.ignore('tooSlow')

    def watchDistance(self):
        self.accept('tooFar', self.getCloser)

    def getCloser(self):
        pass

    def ignoreDistance(self):
        self.ignore('tooFar')

    def shipTutorialPt1(self):
        nameData = [
         PLocalizer.PirateShipPrefix.keys(), PLocalizer.PirateShipSuffix.keys()]
        self.shipNamePanel = NamePanelGui.NamePanelGui(PLocalizer.NamePanelTitle, nameData, showClose=False)
        self.shipNamePanel.setPos(-1, 0, 0)
        self.acceptOnce('nameChosen', self.handleShipNameChosen)

    def handleShipNameChosen(self, shipName):
        self.ignore('nameChosen')
        self.shipNamePanel.destroy()
        self.shipNamePanel = None
        avId = localAvatar.getDoId()
        self.sendUpdate('shipTutorialPt1', [avId, shipName])
        return

    def playDialogMovie(self, dialogId, doneCallback=None, oldLocalAvState=None):
        DistributedBattleNPC.DistributedBattleNPC.playDialogMovie(self, dialogId, doneCallback, oldLocalAvState)
        if self.interactGUI:
            self.interactGUI.destroy()
            self.interactGUI = None
        self.acceptOnce(InteractiveBase.END_INTERACT_EVENT, self.stopDialogMovieEvent)
        return

    def stopDialogMovieEvent(self):
        messenger.send('dialogFinish')

    def setPurgeInteractGui(self, val):
        self.purgeInteractGui = val

    def play(self, *args, **kwArgs):
        Townfolk.Townfolk.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        Townfolk.Townfolk.loop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        Townfolk.Townfolk.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        Townfolk.Townfolk.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        Townfolk.Townfolk.stop(self, *args, **kwArgs)

    def triggerInteractShow(self, interactObj):
        self.amUsingObj = self.cr.doId2do.get(interactObj)
        self.startInteract(base.localAvatar)

    def playInteraction(self, hasMenu=True):
        if self.amUsingObj:
            interactType = self.amUsingObj.interactType
        else:
            interactType = self.animSet
        self.playInteractMovie(interactType, hasMenu)

    def playInteractMovie(self, interactType='default', hasMenu=True):
        allAnims = CustomAnims.INTERACT_ANIMS.get(interactType)
        if allAnims == None:
            self.notify.warning('undefined interaction type %s, not found in CustomAnims.INTERACT_ANIMS' % self.interactType)
        else:
            availAnims = allAnims.get('interact')
            availAnimsInto = allAnims.get('interactInto')
            if self.animIval:
                self.animIval.pause()
                self.animIval = None
            chosenAnim = random.choice(availAnims)
            if not self.interactCamPosHpr:
                curAnim = self.getCurrentAnim()
                self.pose(chosenAnim, 1, blendT=0)
                if self.castDnaId and self.castDnaId in ['models/char/js_2000', 'models/char/td_2000', 'models/char/es_2000']:
                    np = self.attachNewNode('interactCamNode')
                    np.setPos(self.headNode.getX(self), self.headNode.getY(self) + 4.5, self.headNode.getZ(self) + 1)
                else:
                    np = self.headNode.attachNewNode('interactCamNode')
                    np.setPos(1, 0, -4.5)
                np.wrtReparentTo(render)
                np.lookAt(self, self.headNode.getX(self), self.headNode.getY(self), self.headNode.getZ(self) * 0.95)
                if hasMenu:
                    np.setH(np.getH() + 15)
                self.interactCamPosHpr = [
                 np.getPos(render), np.getHpr(render)]
                np.removeNode()
            if chosenAnim in self.getAnimNames():
                chosenAnimInto = None
                if availAnimsInto:
                    chosenAnimInto = random.choice(availAnimsInto)
                if chosenAnimInto in self.getAnimNames():
                    duration = self.getDuration(chosenAnimInto)
                    self.lockFSM = True
                    if duration is None:
                        duration = 1
                    if self.isMixingEnabled():
                        self.animIval = Sequence(Func(self.play, chosenAnimInto), Func(self.loop, chosenAnim))
                    else:
                        self.animIval = Sequence(Func(self.play, chosenAnimInto), Wait(duration), Func(self.loop, chosenAnim))
                    self.animIval.start()
                if self.animIval == None:
                    self.loop(chosenAnim)
                self.interactAnim = chosenAnim
        return

    def endInteractMovie(self, interactType='default'):
        if self.interactAnim:
            if self.animIval:
                self.animIval.finish()
                self.animIval = None
            allAnims = CustomAnims.INTERACT_ANIMS.get(interactType)
            if allAnims == None:
                self.notify.warning('undefined interaction type %s, not found in CustomAnims.INTERACT_ANIMS' % self.interactType)
            else:
                availAnims = allAnims.get('idles')
                availAnimsOutof = allAnims.get('interactOutof')
                chosenAnim = random.choice(availAnims)
                if chosenAnim in self.getAnimNames():
                    self.interactAnim = chosenAnim
                    chosenAnimOutof = None
                    if availAnimsOutof:
                        chosenAnimOutof = random.choice(availAnimsOutof)
                    if chosenAnimOutof in self.getAnimNames():
                        duration = self.getDuration(chosenAnimOutof)
                        if duration is None:
                            duration = 1
                        self.lockFSM = True
                        if self.isMixingEnabled():
                            self.animIval = Sequence(Func(self.play, chosenAnimOutof), Func(self.loop, self.interactAnim))
                        else:
                            self.animIval = Sequence(Func(self.play, chosenAnimOutof), Wait(duration), Func(self.loop, self.interactAnim))
                        self.animIval.start()
            if self.animIval == None:
                self.loop(self.interactAnim)
            self.interactAnim = None
        return

    def levelUpCutlass(self):
        self.sendUpdate('levelUpCutlass', [localAvatar.getDoId()])

    def initializeNametag3d(self):
        Biped.Biped.initializeNametag3d(self)
        if not self.classNameText:
            self.classNameText = OnscreenText(parent=self.iconNodePath, pos=(0, -1.0), fg=(1,
                                                                                           1,
                                                                                           1,
                                                                                           1), bg=(0,
                                                                                                   0,
                                                                                                   0,
                                                                                                   0), scale=0.8, mayChange=1, font=PiratesGlobals.getPirateBoldOutlineFont())
            self.classNameText.setTransparency(TransparencyAttrib.MDual, 2)
            self.classNameText.setColorScaleOff(100)
            self.classNameText.setLightOff()
            self.classNameText.setFogOff()

    def setName(self, name):
        DistributedBattleAvatar.DistributedBattleAvatar.setName(self, name)
        if self.classNameText:
            if self.avatarType.isA(AvatarTypes.Blacksmith):
                self.classNameText['text'] = PLocalizer.ShopBlacksmith
            elif self.avatarType.isA(AvatarTypes.Gunsmith):
                self.classNameText['text'] = PLocalizer.ShopGunsmith
            elif self.avatarType.isA(AvatarTypes.Shipwright):
                self.classNameText['text'] = PLocalizer.ShopShipwright
            elif self.avatarType.isA(AvatarTypes.Cannoneer):
                self.classNameText['text'] = PLocalizer.ShopCannoneer
            elif self.avatarType.isA(AvatarTypes.Gypsy):
                self.classNameText['text'] = PLocalizer.ShopGypsy
            elif self.avatarType.isA(AvatarTypes.MedicineMan):
                self.classNameText['text'] = PLocalizer.ShopMedicineMan
            elif self.avatarType.isA(AvatarTypes.Grenadier):
                self.classNameText['text'] = PLocalizer.ShopGrenadier
            elif self.avatarType.isA(AvatarTypes.Bartender):
                self.classNameText['text'] = PLocalizer.ShopBartender
            elif self.avatarType.isA(AvatarTypes.Merchant):
                self.classNameText['text'] = PLocalizer.ShopMerchant
            elif self.avatarType.isA(AvatarTypes.Tailor):
                self.classNameText['text'] = PLocalizer.ShopTailor
            elif self.avatarType.isA(AvatarTypes.Tattoo):
                self.classNameText['text'] = PLocalizer.ShopTattoo
            elif self.avatarType.isA(AvatarTypes.Jeweler):
                self.classNameText['text'] = PLocalizer.ShopJewelry
            elif self.avatarType.isA(AvatarTypes.Barber):
                self.classNameText['text'] = PLocalizer.ShopBarber
            elif self.avatarType.isA(AvatarTypes.Musician):
                self.classNameText['text'] = PLocalizer.ShopMusician
            elif self.avatarType.isA(AvatarTypes.Trainer):
                self.classNameText['text'] = PLocalizer.ShopTrainer
            elif self.avatarType.isA(AvatarTypes.PvPRewards):
                self.classNameText['text'] = PLocalizer.ShopPvP
            else:
                self.classNameText.hide()

    def setShopId(self, val):
        self.shopId = val

    def getShopId(self):
        return self.shopId

    def setHelpId(self, val):
        self.helpId = val

    def getHelpId(self):
        return self.helpId

    def showVoodooDollToAvatar(self):
        print 'triggering the interaction complete'

    def showRespecMenu(self):
        if self.interactGUI:
            self.interactGUI.hide()
        if self.respecMenuGUI:
            self.respecMenuGUI.destroy()
        optionIds = [
         InteractGlobals.RESPEC_CUTLASS, InteractGlobals.RESPEC_PISTOL, InteractGlobals.RESPEC_DAGGER, InteractGlobals.RESPEC_DOLL, InteractGlobals.RESPEC_GRENADE, InteractGlobals.RESPEC_STAFF, InteractGlobals.RESPEC_SAILING, InteractGlobals.RESPEC_CANNON, InteractGlobals.BACK]
        stateCodes = []
        for opt in optionIds:
            stateCodes.append(self.isRespecAvailable(opt))

        self.respecMenuGUI = InteractGUI.InteractGUI()
        title = self.getMenuTitle()
        self.respecMenuGUI.setOptions(title, optionIds, stateCodes, self.selectRespecOptionConfirm, 0)

    def isRespecAvailable(self, igOption):
        if igOption == InteractGlobals.CANCEL or igOption == InteractGlobals.BACK:
            return InteractGlobals.NORMAL
        else:
            basicSkills = InventoryType.StartingSkills
            begin = -1
            end = -1
            weaponRep = self.getIGToITMap()[igOption]
            if weaponRep == InventoryType.CutlassRep:
                begin = InventoryType.begin_WeaponSkillCutlass
                end = InventoryType.end_WeaponSkillCutlass
            else:
                if weaponRep == InventoryType.PistolRep:
                    begin = InventoryType.begin_WeaponSkillPistol
                    end = InventoryType.end_WeaponSkillPistol
                else:
                    if weaponRep == InventoryType.DaggerRep:
                        begin = InventoryType.begin_WeaponSkillDagger
                        end = InventoryType.end_WeaponSkillDagger
                    else:
                        if weaponRep == InventoryType.GrenadeRep:
                            begin = InventoryType.begin_WeaponSkillGrenade
                            end = InventoryType.end_WeaponSkillGrenade
                        else:
                            if weaponRep == InventoryType.DollRep:
                                begin = InventoryType.begin_WeaponSkillDoll
                                end = InventoryType.end_WeaponSkillDoll
                            else:
                                if weaponRep == InventoryType.WandRep:
                                    begin = InventoryType.begin_WeaponSkillWand
                                    end = InventoryType.end_WeaponSkillWand
                                else:
                                    if weaponRep == InventoryType.SailingRep:
                                        begin = InventoryType.begin_SkillSailing
                                        end = InventoryType.end_SkillSailing
                                    else:
                                        if weaponRep == InventoryType.CannonRep:
                                            begin = InventoryType.begin_WeaponSkillCannon
                                            end = InventoryType.end_WeaponSkillCannon
                                        else:
                                            return InteractGlobals.DISABLED
            for skillId in range(begin, end):
                if skillId in InventoryType.DontResetSkills:
                    continue
                skillPts = localAvatar.getInventory().getStackQuantity(skillId)
                if skillId in basicSkills:
                    if skillPts > 2:
                        return InteractGlobals.NORMAL
                elif skillPts > 1:
                    return InteractGlobals.NORMAL

            return InteractGlobals.DISABLED

    def anyWeaponsRespecable(self):
        list = [InteractGlobals.RESPEC_CUTLASS, InteractGlobals.RESPEC_PISTOL, InteractGlobals.RESPEC_DAGGER, InteractGlobals.RESPEC_DOLL, InteractGlobals.RESPEC_GRENADE, InteractGlobals.RESPEC_STAFF, InteractGlobals.RESPEC_SAILING, InteractGlobals.RESPEC_CANNON]
        for optionId in list:
            if self.isRespecAvailable(optionId) == InteractGlobals.NORMAL:
                return 1

        return 0

    def selectRespecOptionConfirm(self, optionId):
        if optionId == InteractGlobals.CANCEL or optionId == InteractGlobals.BACK:
            self.respecMenuGUI.destroy()
            self.respecMenuGUI = None
            self.interactGUI.show()
            return
        weaponRep = self.getIGToITMap()[optionId]
        self.respecWeapon = optionId
        if self.confirmDialog:
            self.confirmDialog.destroy()
        self.respecMenuGUI.hide()
        numRespecs = localAvatar.getInventory().getStackQuantity(getNumRespecType(weaponRep))
        goldCost = EconomyGlobals.getRespecCost(numRespecs)
        respecText = PLocalizer.RespecConfirmDialog % {'gold': str(goldCost), 'weapon': PLocalizer.InventoryTypeNames[weaponRep]}
        if numRespecs < 2:
            respecText += PLocalizer.RespecPriceIncreaseDialog
        self.confirmDialog = PDialog.PDialog(text=respecText, style=OTPDialog.YesNo, command=self.__handleRespecConfirmation)
        return

    def __handleRespecConfirmation(self, value):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if value == 1:
            if self.hasEnoughRespecMoney(self.respecWeapon):
                self.respecTransaction(self.respecWeapon)
                self.respecMenuGUI.destroy()
                self.respecMenuGUI = None
                self.offerOptions(self.dialogFlag)
            else:
                self.confirmDialog = PDialog.PDialog(text=PLocalizer.NotEnoughMoneyWarning, style=OTPDialog.Acknowledge, command=self.notEnoughMoney)
        else:
            self.respecMenuGUI.show()
        return

    def notEnoughMoney(self, value=0):
        self.respecMenuGUI.destroy()
        self.respecMenuGUI = None
        self.confirmDialog.destroy()
        self.confirmDialog = None
        self.offerOptions(self.dialogFlag)
        return

    def getIGToITMap(self):
        return {InteractGlobals.RESPEC_CUTLASS: InventoryType.CutlassRep, InteractGlobals.RESPEC_PISTOL: InventoryType.PistolRep, InteractGlobals.RESPEC_DAGGER: InventoryType.DaggerRep, InteractGlobals.RESPEC_DOLL: InventoryType.DollRep, InteractGlobals.RESPEC_GRENADE: InventoryType.GrenadeRep, InteractGlobals.RESPEC_STAFF: InventoryType.WandRep, InteractGlobals.RESPEC_SAILING: InventoryType.SailingRep, InteractGlobals.RESPEC_CANNON: InventoryType.CannonRep}

    def respecTransaction(self, weaponOpt):
        weaponRep = self.getIGToITMap()[weaponOpt]
        if self.hasEnoughRespecMoney(self.respecWeapon):
            localAvatar.guiMgr.skillPage.respec(weaponRep)
            self.b_selectOption(weaponOpt)

    def hasEnoughRespecMoney(self, weaponRep):
        curGold = localAvatar.getInventory().getGoldInPocket()
        numRespecs = localAvatar.getInventory().getStackQuantity(getNumRespecType(weaponRep))
        goldCost = EconomyGlobals.getRespecCost(numRespecs)
        if curGold >= goldCost:
            return 1
        else:
            return 0

    def getShipRank(self):
        inv = localAvatar.getInventory()
        if not inv:
            return 0
        return TitleGlobals.getRank(TitleGlobals.ShipPVPTitle, inv.getStackQuantity(InventoryType.PVPTotalInfamySea))

    def getLandRank(self):
        inv = localAvatar.getInventory()
        if not inv:
            return 0
        return TitleGlobals.getRank(TitleGlobals.LandPVPTitle, inv.getStackQuantity(InventoryType.PVPTotalInfamyLand))

    def playMusic(self, songId):
        songName = MusicManager.songItem2MusicLabel[songId]
        base.musicMgr.request(name=songName, priority=5, looping=False)
        base.localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.SongPlayingAnnouncement % PLocalizer.InventoryTypeNames[songId], seconds=10, priority=0, color=(0, 0, 0, 1))