import string
import time

from otp.avatar import AvatarDNA
from otp.avatar.Avatar import Avatar
from panda3d.core import *
from direct.actor.DistributedActor import DistributedActor
from direct.distributed import DistributedNode
from direct.showbase import PythonUtil
from direct.task import Task
from otp.chat import ChatGarbler, ChatManager
from otp.otpbase import OTPGlobals, OTPLocalizer
from otp.speedchat import SCDecoders
from otp.nametag.Nametag import Nametag


class DistributedAvatar(DistributedActor, Avatar):
    HpTextGenerator = TextNode('HpTextGenerator')
    HpTextEnabled = 1
    ManagesNametagAmbientLightChanged = True

    def __init__(self, cr):
        try:
            self.DistributedAvatar_initialized
            return
        except BaseException:
            self.DistributedAvatar_initialized = 1

        Avatar.__init__(self)
        DistributedActor.__init__(self, cr)
        self.hpText = None
        self.hp = None
        self.maxHp = None

    def disable(self):
        self.reparentTo(hidden)
        self.removeActive()
        self.disableBodyCollisions()
        self.hideHpText()
        self.hp = None
        self.ignore('nameTagShowAvId')
        self.ignore('nameTagShowName')
        self.ignoreNametagAmbientLightChange()
        DistributedActor.disable(self)

    def delete(self):
        try:
            self.DistributedAvatar_deleted
        except BaseException:
            self.DistributedAvatar_deleted = 1
            Avatar.delete(self)
            DistributedActor.delete(self)

    def generate(self):
        self.acceptNametagAmbientLightChange()
        DistributedActor.generate(self)
        if not self.isLocal():
            self.addActive()
            self.considerUnderstandable()

        self.setParent(OTPGlobals.SPHidden)
        self.setTag('avatarDoId', str(self.doId))
        self.accept('nameTagShowAvId', self.__nameTagShowAvId)
        self.accept('nameTagShowName', self.__nameTagShowName)

    def announceGenerate(self):
        if not self.isLocal():
            self.initializeBodyCollisions('distAvatarCollNode-' +
                                          str(self.doId))

        DistributedActor.announceGenerate(self)

    def __setTags(self, extra=None):
        if hasattr(base, 'idTags'):
            if base.idTags:
                self.__nameTagShowAvId()
            else:
                self.__nameTagShowName()

    def do_setParent(self, parentToken):
        if not self.isDisabled():
            if parentToken == OTPGlobals.SPHidden:
                self.nametag2dDist &= ~Nametag.CName
            else:
                self.nametag2dDist |= Nametag.CName
            self.nametag.getNametag2d().setContents(
                self.nametag2dContents & self.nametag2dDist)
            DistributedActor.do_setParent(self, parentToken)
            self.__setTags()

    def toonUp(self, hpGained):
        if self.hp is None or hpGained < 0:
            return

        oldHp = self.hp
        if self.hp + hpGained <= 0:
            self.hp += hpGained
        else:
            self.hp = min(max(self.hp, 0) + hpGained, self.maxHp)

        hpGained = self.hp - max(oldHp, 0)
        if hpGained > 0:
            self.showHpText(hpGained)
            self.hpChange(quietly=0)

    def takeDamage(self, hpLost, bonus=0):
        if self.hp is None or hpLost < 0:
            return

        oldHp = self.hp
        self.hp = max(self.hp - hpLost, 0)
        hpLost = oldHp - self.hp
        if hpLost > 0:
            self.showHpText(-hpLost, bonus)
            self.hpChange(quietly=0)
            if self.hp <= 0 and oldHp > 0:
                self.died()

    def setHp(self, hitPoints):
        justRanOutOfHp = hitPoints is not None and self.hp is not None and self.hp - \
            hitPoints > 0 and hitPoints <= 0
        self.hp = hitPoints
        self.hpChange(quietly=1)
        if justRanOutOfHp:
            self.died()

    def hpChange(self, quietly=0):
        if hasattr(self, 'doId'):
            if self.hp is not None and self.maxHp is not None:
                messenger.send(
                    self.uniqueName('hpChange'), [self.hp, self.maxHp, quietly])

            if self.hp is not None and self.hp > 0:
                messenger.send(self.uniqueName('positiveHP'))

    def died(self):
        pass

    def getHp(self):
        return self.hp

    def setMaxHp(self, hitPoints):
        self.maxHp = hitPoints
        self.hpChange()

    def getMaxHp(self):
        return self.maxHp

    def getName(self):
        return Avatar.getName(self)

    def setName(self, name):
        try:
            self.node().setName('%s-%d' % (name, self.doId))
            self.gotName = 1
        except BaseException:
            pass

        return Avatar.setName(self, name)

    def showHpText(self, number, bonus=0, scale=1):
        if self.HpTextEnabled and not self.ghostMode:
            if number != 0:
                if self.hpText:
                    self.hideHpText()
                self.HpTextGenerator.setFont(OTPGlobals.getSignFont())
                if number < 0:
                    self.HpTextGenerator.setText(str(number))
                else:
                    self.HpTextGenerator.setText('+' + str(number))
                self.HpTextGenerator.clearShadow()
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                if bonus == 1:
                    r = 1.0
                    g = 1.0
                    b = 0
                    a = 1
                elif bonus == 2:
                    r = 1.0
                    g = 0.5
                    b = 0
                    a = 1
                elif number < 0:
                    r = 0.9
                    g = 0
                    b = 0
                    a = 1
                else:
                    r = 0
                    g = 0.9
                    b = 0
                    a = 1
                self.HpTextGenerator.setTextColor(r, g, b, a)
                self.hpTextNode = self.HpTextGenerator.generate()
                self.hpText = self.attachNewNode(self.hpTextNode)
                self.hpText.setScale(scale)
                self.hpText.setBillboardPointEye()
                self.hpText.setBin('fixed', 100)
                self.hpText.setPos(0, 0, self.height / 2)
                seq = Task.sequence(
                    self.hpText.lerpPos(
                        Point3(0, 0, self.height + 1.5),
                        1.0,
                        blendType='easeOut'), Task.pause(0.85),
                    self.hpText.lerpColor(
                        Vec4(r, g, b, a), Vec4(r, g, b, 0), 0.1),
                    Task.Task(self.hideHpTextTask))
                taskMgr.add(seq, self.uniqueName('hpText'))

    def showHpString(self, text, duration=0.85, scale=0.7):
        if self.HpTextEnabled and not self.ghostMode:
            if text != '':
                if self.hpText:
                    self.hideHpText()

                self.HpTextGenerator.setFont(OTPGlobals.getSignFont())
                self.HpTextGenerator.setText(text)
                self.HpTextGenerator.clearShadow()
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                r = a = 1.0
                g = b = 0.0
                self.HpTextGenerator.setTextColor(r, g, b, a)
                self.hpTextNode = self.HpTextGenerator.generate()
                self.hpText = self.attachNewNode(self.hpTextNode)
                self.hpText.setScale(scale)
                self.hpText.setBillboardAxis()
                self.hpText.setPos(0, 0, self.height / 2)
                seq = Task.sequence(
                    self.hpText.lerpPos(
                        Point3(0, 0, self.height + 1.5),
                        1.0,
                        blendType='easeOut'), Task.pause(duration),
                    self.hpText.lerpColor(
                        Vec4(r, g, b, a), Vec4(r, g, b, 0), 0.1),
                    Task.Task(self.hideHpTextTask))

                taskMgr.add(seq, self.uniqueName('hpText'))

    def hideHpTextTask(self, task):
        self.hideHpText()
        return Task.done

    def hideHpText(self):
        if self.hpText:
            taskMgr.remove(self.uniqueName('hpText'))
            self.hpText.removeNode()
            self.hpText = None

    def getStareAtNodeAndOffset(self):
        return (self, Point3(0, 0, self.height))

    def __nameTagShowAvId(self, extra=None):
        self.setDisplayName('%s\n%s' % (self.getName(), self.doId))

    def __nameTagShowName(self, extra=None):
        self.setDisplayName(self.getName())

    def askAvOnShard(self, avId):
        if base.cr.doId2do.get(avId):
            messenger.send('AvOnShard%s' % avId, [True])
        else:
            self.sendUpdate('checkAvOnShard', [avId])

    def confirmAvOnShard(self, avId, onShard=True):
        messenger.send('AvOnShard%s' % avId, [onShard])
