from pirates.npc import NavySailor
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pirates.battle import DistributedBattleNPC, WeaponGlobals
from pirates.leveleditor import NPCList
from pirates.pirate import AvatarTypes, DistributedPirateBase, HumanDNA
from pirates.piratesbase import PiratesGlobals, PLocalizer

class DistributedNPCNavySailor(DistributedBattleNPC.DistributedBattleNPC, NavySailor.NavySailor):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCNavySailor')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        NavySailor.NavySailor.__init__(self)

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
        if not self.loaded:
            if self.style:
                NavySailor.NavySailor.generateHuman(self, self.style.gender, base.cr.human)
        yieldThread('navy done')

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        self.setInteractOptions(isTarget=False, allowInteract=False)

    def disable(self):
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        self.stopBlink()

    def delete(self):
        DistributedBattleNPC.DistributedBattleNPC.delete(self)
        NavySailor.NavySailor.delete(self)

    def getNameText(self):
        return NavySailor.NavySailor.getNameText(self)

    def isBattleable(self):
        return 1

    def setDNAId(self, dnaId):
        if dnaId and NPCList.NPC_LIST.has_key(dnaId):
            dnaDict = NPCList.NPC_LIST[dnaId]
            customDNA = HumanDNA.HumanDNA()
            customDNA.loadFromNPCDict(dnaDict)
            self.setDNAString(customDNA)
        else:
            self.setDNAString(None)
            self.setDefaultDNA()
            if self.avatarType.isA(AvatarTypes.TradingCo):
                self.style.makeNPCIndiaNavySailor()
            else:
                self.style.makeNPCNavySailor()

    def play(self, *args, **kwArgs):
        NavySailor.NavySailor.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        NavySailor.NavySailor.loop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        NavySailor.NavySailor.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        NavySailor.NavySailor.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        NavySailor.NavySailor.stop(self, *args, **kwArgs)
