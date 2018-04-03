# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.BattleNPCGameFSM
import BattleAvatarGameFSM
from direct.fsm import FSM
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from pandac.PandaModules import *
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PiratesGlobals, PLocalizer


class BattleNPCGameFSM(BattleAvatarGameFSM.BattleAvatarGameFSM):
    __module__ = __name__

    def __init__(self, av):
        BattleAvatarGameFSM.BattleAvatarGameFSM.__init__(self, av, 'BattleNPCFSM')

    def enterAttackChase(self, extraArgs=[]):
        self.av.motionFSM.on()

    def exitAttackChase(self):
        self.av.motionFSM.off()

    def enterFollow(self, extraArgs=[]):
        self.av.motionFSM.on()

    def exitFollow(self):
        self.av.motionFSM.off()

    def enterRetreat(self, extraArgs=[]):
        self.av.motionFSM.on()

    def exitRetreat(self):
        if self.av.motionFSM.state != 'Off':
            self.av.motionFSM.off()

    def enterInteract(self, extraArgs=[]):
        animState = 'LandRoam'
        self.av.motionFSM.setAnimInfo(self.av.getAnimInfo(animState))

    def exitInteract(self):
        pass

    def enterBattle(self, extraArgs=[]):
        BattleAvatarGameFSM.BattleAvatarGameFSM.enterBattle(self, extraArgs)

    def exitBattle(self):
        BattleAvatarGameFSM.BattleAvatarGameFSM.exitBattle(self)

    def enterPatrol(self, extraArgs=[]):
        self.demand('LandRoam')

    def enterPathFollow(self, extraArgs=[]):
        self.demand('LandRoam')

    def enterIdle(self, extraArgs=[]):
        self.demand('LandRoam')

    def enterDeath(self, extraArgs=[]):
        BattleAvatarGameFSM.BattleAvatarGameFSM.enterDeath(self)
        messenger.send(self.av.uniqueName(PiratesGlobals.AVATAR_DEATH_MSG))

    def enterBreakCombat(self, extraArgs=[]):
        self.av.showHpString(PLocalizer.Disengage, 0, 5, 0.5)

    def filterBreakCombat(self, request, args=[]):
        if request == 'advance':
            return 'LandRoam'
        if request == 'Battle':
            return
        return self.defaultFilter(request, args)

    def exitBreakCombat(self):
        pass

    def destroy(self):
        if hasattr(self, 'fadeOutIval'):
            self.fadeOutIval.pause()
            del self.fadeOutIval

    def enterFadeOut(self, args=[]):
        if self.av is None:
            return
        if self.av.motionFSM:
            self.av.motionFSM.off()
        self.av.stashBattleCollisions()
        parentGA = self.av.getParentObj()
        npcDoId = self.av.getDoId()
        if base.localAvatar.guiMgr.targetStatusTray.doId == npcDoId:
            base.localAvatar.guiMgr.targetStatusTray.hide()
        if hasattr(self, 'fadeOutIval'):
            self.fadeOutIval.pause()
            del self.fadeOutIval
        nameText = self.av.getNameText()
        if nameText is None:
            return
        self.fadeOutIval = Sequence(Func(self.av.setTransparency, TransparencyAttrib.MAlpha), Func(self.av.setAlphaScale, 1.0), Func(nameText.setAlphaScale, 1.0), Parallel(LerpFunctionInterval(self.av.setAlphaScale, 3.0, fromData=1.0, toData=0.0, blendType='easeInOut'), LerpFunctionInterval(nameText.setAlphaScale, 3.0, fromData=1.0, toData=0.0, blendType='easeInOut')), Func(self.av.hide), Func(nameText.hide), Func(parentGA.sendUpdate, 'requestNPCRemoval', [npcDoId]))
        self.fadeOutIval.start()
        return
# okay decompiling .\pirates\pirate\BattleNPCGameFSM.pyc
