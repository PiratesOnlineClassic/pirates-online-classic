# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.DistributedCreature
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from pirates.battle.DistributedBattleNPC import DistributedBattleNPC
from pirates.creature.Alligator import Alligator
from pirates.creature.Bat import Bat
from pirates.creature.Chicken import Chicken
from pirates.creature.Crab import Crab
from pirates.creature.Dog import Dog
from pirates.creature.FlyTrap import FlyTrap
from pirates.creature.Monkey import Monkey
from pirates.creature.Pig import Pig
from pirates.creature.Rooster import Rooster
from pirates.creature.Scorpion import Scorpion
from pirates.creature.Seagull import Seagull
from pirates.creature.Stump import Stump
from pirates.creature.Wasp import Wasp
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PLocalizer

CreatureTypes = {AvatarTypes.Crab: Crab, AvatarTypes.RockCrab: Crab, AvatarTypes.GiantCrab: Crab, AvatarTypes.Chicken: Chicken, AvatarTypes.Rooster: Rooster, AvatarTypes.Pig: Pig, AvatarTypes.Dog: Dog, AvatarTypes.Seagull: Seagull, AvatarTypes.Stump: Stump, AvatarTypes.FlyTrap: FlyTrap, AvatarTypes.Scorpion: Scorpion, AvatarTypes.DreadScorpion: Scorpion, AvatarTypes.Alligator: Alligator, AvatarTypes.BigGator: Alligator, AvatarTypes.HugeGator: Alligator, AvatarTypes.Bat: Bat, AvatarTypes.VampireBat: Bat, AvatarTypes.Wasp: Wasp, AvatarTypes.AngryWasp: Wasp, AvatarTypes.Monkey: Monkey}

class DistributedCreature(DistributedBattleNPC):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCreature')

    def __init__(self, cr):
        DistributedBattleNPC.__init__(self, cr)
        self.creature = None
        return

    def generate(self):
        DistributedBattleNPC.generate(self)
        self.customInteractOptions()

    def announceGenerate(self):
        DistributedBattleNPC.announceGenerate(self)
        self.addActive()

    def delete(self):
        if self.creature:
            self.creature.detachNode()
            self.creature.delete()
            self.creature = None
        DistributedBattleNPC.delete(self)
        return

    def setupCreature(self, avatarType):
        if not self.creature:
            self.creature = CreatureTypes[avatarType.getNonBossType()]()
            self.creature.setAvatarType(avatarType)
            self.creature.reparentTo(self.getGeomNode())
            self.motionFSM.setAnimInfo(self.getAnimInfo('LandRoam'))
            self.nametag3d.setName('empty_use_self_dot_creature_dot_nametag3d_instead')
            self.creature.nametag3d.reparentTo(self.nametag3d)

    def loop(self, *args, **kw):
        return self.creature and self.creature.loop(*args, **kw)

    def play(self, *args, **kw):
        return self.creature and self.creature.play(*args, **kw)

    def pingpong(self, *args, **kw):
        return self.creature and self.creature.pingpong(*args, **kw)

    def pose(self, *args, **kw):
        return self.creature and self.creature.pose(*args, **kw)

    def stop(self, *args, **kw):
        return self.creature and self.creature.stop(*args, **kw)

    def setPlayRate(self, *args, **kw):
        return self.creature and self.creature.setPlayRate(*args, **kw)

    def getPlayRate(self, *args, **kw):
        return self.creature and self.creature.getPlayRate(*args, **kw)

    def getDuration(self, *args, **kw):
        return self.creature and self.creature.getDuration(*args, **kw)

    def actorInterval(self, *args, **kw):
        return self.creature and self.creature.actorInterval(*args, **kw)

    def getAnimControl(self, *args, **kw):
        return self.creature and self.creature.getAnimControl(*args, **kw)

    def getOuchSfx(self):
        return self.creature and self.creature.sfx.get('pain')

    def getSfx(self, *args, **kw):
        return self.creature and self.creature.getSfx(*args, **kw)

    @report(types=['module', 'args'], dConfigParam='want-nametag-report')
    def initializeNametag3d(self):
        return self.creature and self.creature.initializeNametag3d()

    @report(types=['module', 'args'], dConfigParam='want-nametag-report')
    def getNameText(self):
        return self.creature and self.creature.getNameText()

    @report(types=['module', 'args'], dConfigParam='want-nametag-report')
    def setName(self, name):
        DistributedBattleNPC.setName(self, name)
        self.refreshStatusTray()
        self.creature.nametag.setDisplayName('        ')
        nameText = self.getNameText()
        if nameText:
            if self.isNpc:
                self.accept('weaponChange', self.setMonsterNameTag)
                self.setMonsterNameTag()
                from pirates.battle import EnemyGlobals
                color2 = EnemyGlobals.getNametagColor(self.avatarType)
                if self.isBoss():
                    color2 = (0.95, 0.1, 0.1, 1)
                nameText['fg'] = color2

    @report(types=['module', 'args'], dConfigParam='want-nametag-report')
    def setMonsterNameTag(self):
        from pirates.piratesbase import PLocalizer
        if self.level:
            color = self.cr.battleMgr.getExperienceColor(base.localAvatar, self)
            name = '%s  %s\x01smallCaps\x01%s%s\x02\x02' % (self.name, color, PLocalizer.Lv, self.level)
        else:
            name = self.name
        self.getNameText()['text'] = name

    @report(types=['module', 'args'], dConfigParam='want-nametag-report')
    def addActive(self):
        if self.creature:
            self.creature.addActive()
            self.creature.nametag.setName(' ')

    def removeActive(self):
        if self.creature:
            self.creature.removeActive()

    def customInteractOptions(self):
        self.setInteractOptions(isTarget=False, allowInteract=False)

    @report(types=['module', 'args'], dConfigParam='want-nametag-report')
    def setAvatarType(self, avatarType):
        DistributedBattleNPC.setAvatarType(self, avatarType)
        self.setupCreature(avatarType)

    def getEnterDeathTrack(self):
        return Sequence(Func(self.setAllowInteract, False), self.creature.getEnterDeathTrack())

    def getExitDeathTrack(self):
        return Sequence(self.creature.getExitDeathTrack())

    def setLevel(self, level):
        DistributedBattleNPC.setLevel(self, level)
        self.creature.setLevel(level)

    def getAnimInfo(self, *args, **kw):
        return self.creature and self.creature.getAnimInfo(*args, **kw)

    def freezeShadow(self, *args, **kw):
        self.creature.shadowPlacer.off()
        self.freezeTask = None
        return

    def setHeight(self, height):
        self.height = height
        self.creature.adjustNametag3d(self.scale)
        if self.collTube:
            self.collTube.setPointB(0, 0, height)
            if self.collNodePath:
                self.collNodePath.forceRecomputeBounds()
        if self.battleTube:
            self.battleTube.setPointB(0, 0, max(5.0, height))
# okay decompiling .\pirates\creature\DistributedCreature.pyc
