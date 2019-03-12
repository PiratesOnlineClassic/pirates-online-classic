from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from otp.uberdog.RejectCode import RejectCode
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.battle.DistributedBattleNPC import DistributedBattleNPC

class TradeInviterButton(DirectButton):
    
    def __init__(self, text, command):
        DirectButton.__init__(self, relief = DGG.RAISED, borderWidth = PiratesGuiGlobals.BorderWidthSmall, pos = (0, 0, 0), text = text, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0.04, 0.025), frameSize = (0, 0.08, 0, 0.08), frameColor = PiratesGuiGlobals.ButtonColor2, command = command)
        self.initialiseoptions(TradeInviterButton)



class TradeInviter(GuiPanel.GuiPanel):
    notify = DirectNotifyGlobal.directNotify.newCategory('TradeInviter')
    
    def __init__(self, avId, avName):
        GuiPanel.GuiPanel.__init__(self, 'Invite Trade', 0.5, 0.5)
        self.initialiseoptions(TradeInviter)
        self.avId = avId
        self.avName = avName
        self.avDisableName = 'disable-%s' % self.avId
        self.fsm = ClassicFSM.ClassicFSM('TradeInviter', [
            State.State('off', self.enterOff, self.exitOff),
            State.State('getNewTrade', self.enterGetNewTrade, self.exitGetNewTrade),
            State.State('begin', self.enterBegin, self.exitBegin),
            State.State('notYet', self.enterNotYet, self.exitNotYet),
            State.State('checkAvailability', self.enterCheckAvailability, self.exitCheckAvailability),
            State.State('notAvailable', self.enterNotAvailable, self.exitNotAvailable),
            State.State('notAcceptingTrades', self.enterNotAcceptingTrades, self.exitNotAcceptingTrades),
            State.State('wentAway', self.enterWentAway, self.exitWentAway),
            State.State('alreadyTrading', self.enterAlreadyTrading, self.exitAlreadyTrading),
            State.State('alreadyInvited', self.enterAlreadyInvited, self.exitAlreadyInvited),
            State.State('askingNPC', self.enterAskingNPC, self.exitAskingNPC),
            State.State('endTrade', self.enterEndTrade, self.exitEndTrade),
            State.State('tradeNoMore', self.enterTradeNoMore, self.exitTradeNoMore),
            State.State('self', self.enterSelf, self.exitSelf),
            State.State('ignored', self.enterIgnored, self.exitIgnored),
            State.State('asking', self.enterAsking, self.exitAsking),
            State.State('yes', self.enterYes, self.exitYes),
            State.State('no', self.enterNo, self.exitNo),
            State.State('maybe', self.enterMaybe, self.exitMaybe),
            State.State('down', self.enterDown, self.exitDown),
            State.State('cancel', self.enterCancel, self.exitCancel)], 'off', 'off')
        self.message = DirectLabel(parent = self, relief = None, text = '', text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.35), textMayChange = 1)
        self.context = None
        self.bOk = TradeInviterButton(text = PLocalizer.TradeInviterOK, command = self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.2, 0, 0.05)
        self.bOk.hide()
        self.bCancel = TradeInviterButton(text = PLocalizer.TradeInviterCancel, command = self.__handleCancel)
        self.bCancel.reparentTo(self)
        self.bCancel.setPos(0.2, 0, 0.05)
        self.bCancel.hide()
        self.bStop = TradeInviterButton(text = PLocalizer.TradeInviterStopTrading, command = self.__handleStop)
        self.bStop.reparentTo(self)
        self.bStop.setPos(0.2, 0, 0.15)
        self.bStop.hide()
        self.bYes = TradeInviterButton(text = PLocalizer.TradeInviterYes, command = self.__handleYes)
        self.bYes.reparentTo(self)
        self.bYes.setPos(0.1, 0, 0.05)
        self.bYes.hide()
        self.bNo = TradeInviterButton(text = PLocalizer.TradeInviterNo, command = self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.bNo.hide()
        self.fsm.enterInitialState()
        if self.avId == None:
            self.fsm.request('getNewTrade')
        else:
            self.fsm.request('begin')

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.fsm.request('cancel')
        del self.fsm
        GuiPanel.GuiPanel.destroy(self)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterGetNewTrade(self):
        self.message['text'] = PLocalizer.TradeInviterClickToon
        self.bCancel.show()
        self.accept('clickedNametag', self.__handleClickedNametag)

    def exitGetNewTrade(self):
        self.bCancel.hide()
        self.ignore('clickedNametag')

    def __handleClickedNametag(self, avatar):
        self.avId = avatar.doId
        self.avName = avatar.getName()
        self.avDisableName = avatar.uniqueName('disable')
        self.fsm.request('begin')

    def enterBegin(self):
        myId = base.localAvatar.doId
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        if self.avId == myId:
            self.fsm.request('self')
        else:
            self.fsm.request('notYet')

    def exitBegin(self):
        self.ignore(self.avDisableName)

    def enterNotYet(self):
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        self.message['text'] = PLocalizer.TradeInviterNotYet % self.avName
        self.bYes.show()
        self.bNo.show()

    def exitNotYet(self):
        self.ignore(self.avDisableName)
        self.bYes.hide()
        self.bNo.hide()

    def enterCheckAvailability(self):
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        avatar = base.cr.doId2do.get(self.avId)
        if not avatar:
            self.fsm.request('wentAway')
            return None
        
        if isinstance(avatar, DistributedBattleNPC):
            self.fsm.request('askingNPC')
            return None
        
        base.cr.tradeManager.sendRequestCreateTrade(self.avId)
        self.message['text'] = PLocalizer.TradeInviterCheckAvailability % self.avName
        self.accept(PiratesGlobals.TradeIncomingEvent, self.__tradeCreated)
        self.accept(PiratesGlobals.TradeRejectInviteEvent, self.__tradeRejectInvite)
        self.bCancel.show()

    def __tradeCreated(self, trade):
        self.destroy()

    def exitCheckAvailability(self):
        self.ignore(self.avDisableName)
        self.ignore(PiratesGlobals.TradeRejectInviteEvent)
        self.ignore(PiratesGlobals.TradeIncomingEvent)
        self.bCancel.hide()
    
    def enterNotAvailable(self):
        self.message['text'] = PLocalizer.TradeInviterNotAvailable % self.avName
        self.context = None
        self.bOk.show()
    
    def exitNotAvailable(self):
        self.bOk.hide()

    def enterNotAcceptingTrades(self):
        self.message['text'] = PLocalizer.TradeInviterTradeSaidNoNewTrades % self.avName
        self.context = None
        self.bOk.show()
    
    def exitNotAcceptingTrades(self):
        self.bOk.hide()
    
    def enterWentAway(self):
        self.message['text'] = PLocalizer.TradeInviterWentAway % self.avName
        if self.context != None:
            self.context = None
        
        self.bOk.show()
    
    def exitWentAway(self):
        self.bOk.hide()

    def enterAlreadyTrading(self):
        self.message['text'] = PLocalizer.TradeInviterAlready % self.avName
        self['text_pos'] = (0.0, 0.2)
        self.context = None
        self.bStop.show()
        self.bCancel.show()
    
    def exitAlreadyTrading(self):
        self.message['text'] = ''
        self['text_pos'] = (0.0, 0.13)
        self.bStop.hide()
        self.bCancel.hide()
    
    def enterAlreadyInvited(self):
        self.message['text'] = PLocalizer.TradeInviterAlreadyInvited % self.avName
        self['text_pos'] = (0.0, 0.2)
        self.context = None
        self.bStop.show()
        self.bCancel.show()
    
    def exitAlreadyInvited(self):
        self.message['text'] = ''
        self['text_pos'] = (0.0, 0.13)
        self.bStop.hide()
        self.bCancel.hide()

    def enterAskingNPC(self):
        self.message['text'] = PLocalizer.TradeInviterAskingNPC % self.avName
        taskMgr.doMethodLater(2.0, self.npcReplies, 'npcTrade')
        self.bCancel.show()

    def exitAskingNPC(self):
        taskMgr.remove('npcTrade')
        self.bCancel.hide()

    def npcReplies(self, task):
        self.fsm.request('no')
        return Task.done
    
    def enterEndTrade(self):
        self.message['text'] = PLocalizer.TradeInviterEndTrade % self.avName
        self.context = None
        self.bYes.show()
        self.bNo.show()

    def exitEndTrade(self):
        self.bYes.hide()
        self.bNo.hide()
    
    def enterTradeNoMore(self):
        self.message['text'] = PLocalizer.TradeInviterTradeNoMore % self.avName
        self.bOk.show()
        if not base.cr.doId2do.has_key(self.avId):
            messenger.send(self.avDisableName)
    
    def exitTradeNoMore(self):
        self.bOk.hide()
    
    def enterSelf(self):
        self.message['text'] = PLocalizer.TradeInviterSelf
        self.context = None
        self.bOk.show()

    def exitSelf(self):
        self.bOk.hide()
    
    def enterIgnored(self):
        self.message['text'] = PLocalizer.TradeInviterIgnored % self.avName
        self.context = None
        self.bOk.show()
    
    def exitIgnored(self):
        self.bOk.hide()

    def enterAsking(self):
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        self.message['text'] = PLocalizer.TradeInviterAsking % self.avName
        self.accept('tradeResponse', self.__tradeResponse)
        self.bCancel.show()

    def exitAsking(self):
        self.ignore(self.avDisableName)
        self.ignore('tradeResponse')
        self.bCancel.hide()

    def enterYes(self):
        self.message['text'] = PLocalizer.TradeInviterTradeSaidYes % self.avName
        self.context = None
        self.bOk.show()
    
    def exitYes(self):
        self.bOk.hide()

    def enterNo(self):
        self.message['text'] = PLocalizer.TradeInviterTradeSaidNo % self.avName
        self.context = None
        self.bOk.show()
    
    def exitNo(self):
        self.bOk.hide()

    def enterMaybe(self):
        self.message['text'] = PLocalizer.TradeInviterMaybe % self.avName
        self.context = None
        self.bOk.show()

    def exitMaybe(self):
        self.bOk.hide()

    def enterDown(self):
        self.message['text'] = PLocalizer.TradeInviterDown
        self.context = None
        self.bOk.show()

    def exitDown(self):
        self.bOk.hide()

    def enterCancel(self):
        if self.context != None:
            self.context = None
        
        self.fsm.request('off')

    def exitCancel(self):
        pass

    def __handleOk(self):
        self.destroy()
    
    def __handleCancel(self):
        self.destroy()
    
    def __handleStop(self):
        self.fsm.request('endFriendship')
    
    def __handleYes(self):
        if self.fsm.getCurrentState().getName() == 'notYet':
            self.fsm.request('checkAvailability')
        elif self.fsm.getCurrentState().getName() == 'endTrade':
            self.fsm.request('tradeNoMore')
        else:
            self.destroy()
    
    def __handleNo(self):
        self.destroy()

    def __handleList(self):
        messenger.send('openTradesList')

    def __tradeConsidering(self, yesNoAlready, context):
        if yesNoAlready == 1:
            self.context = context
            self.fsm.request('asking')
        elif yesNoAlready == 0:
            self.fsm.request('notAvailable')
        elif yesNoAlready == 2:
            self.fsm.request('alreadyTrading')
        elif yesNoAlready == 3:
            self.fsm.request('self')
        elif yesNoAlready == 4:
            self.fsm.request('ignored')
        elif yesNoAlready == 6:
            self.fsm.request('notAcceptingTrades')
        elif yesNoAlready == 10:
            self.fsm.request('no')
        else:
            self.notify.warning('Got unexpected response to tradeConsidering: %s' % yesNoAlready)
            self.fsm.request('maybe')

    def __tradeRejectInvite(self, avId, reason):
        if reason == RejectCode.NO_TRADES_LIST:
            pass

        if reason == RejectCode.TRADES_LIST_NOT_HANDY:
            pass

        if reason == RejectCode.INVITEE_NOT_ONLINE:
            self.fsm.request('notAvailable')
        elif reason == RejectCode.ALREADY_INVITED:
            self.fsm.request('alreadyInvited')
        elif reason == RejectCode.ALREADY_YOUR_TRADE:
            self.fsm.request('alreadyTrading')
        else:
            self.notify.warning('tradeRejectInvite: %s unknown reason: %s.' % (avId, reason))

    def __tradeResponse(self, yesNoMaybe, context):
        if self.context != context:
            self.notify.warning('Unexpected change of context from %s to %s.' % (self.context, context))
            self.context = context
        
        if yesNoMaybe == 1:
            self.fsm.request('yes')
        elif yesNoMaybe == 0:
            self.fsm.request('no')
        else:
            self.notify.warning('Got unexpected response to tradeResponse: %s' % yesNoMaybe)
            self.fsm.request('maybe')

    def __handleDisableAvatar(self):
        self.fsm.request('wentAway')


