from direct.distributed.DistributedObject import DistributedObject
from pirates.band import BandConstance
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import PLocalizer
from pirates.pirate.PAvatarHandle import PAvatarHandle
from otp.speedchat import SCDecoders
from pirates.speedchat import PSCDecoders
from pirates.piratesbase import PiratesGlobals

class DistributedBandMember(DistributedObject, PAvatarHandle):
    notify = directNotify.newCategory('BandMember')
    allBandmembers = {}
    band_map = {}

    @classmethod
    def areSameCrew(cls, doId1, doId2):
        bm1 = cls.getBandMember(doId1)
        bm2 = cls.getBandMember(doId2)
        return bm1 and bm2 and bm1.bandId == bm2.bandId

    @classmethod
    def getBandMember(cls, doId):
        return cls.allBandmembers.get(doId)

    @classmethod
    def getBandSet(cls, doId):
        bm = cls.getBandMember(doId)
        if bm:
            return cls.band_map.get(bm.bandId, set())
        else:
            return set()

    @classmethod
    def getBandSetLocalAvatar(cls):
        return cls.getBandSet(localAvatar.doId)

    @classmethod
    def getLeaderNameLocalAvatar(cls):
        b_set = cls.getBandSetLocalAvatar()
        print('----------------------------')
        for b in b_set:
            print('----------------------------%s-%s' % (b.isManager, b.name))
            if b.isManager:
                return b.name
        
        print('---------------------------- Return None')
        return None

    @classmethod
    def IsAvatarHeadOfBand(cls, doId):
        br = cls.getBandMember(doId)
        if br:
            return br.isManager
        else:
            return 0

    @classmethod
    def IsLocalAvatarHeadOfBand(cls):
        return cls.IsAvatarHeadOfBand(localAvatar.doId)

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.avatarId = 0
        self.name = ''
        self.maxHp = 0
        self.hp = 0
        self.bandId = None
        self.isManager = 0
        self.shipInfo = [0, '', 0, []]
        self.whiteListEnabled = base.config.GetBool('whitelist-chat-enabled', 1)
    
    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        messenger.send(BandConstance.BandMembershipChange, [self, 0])
    
    def disable(self):
        if self.bandId:
            self.band_map[self.bandId].remove(self)
            if len(self.band_map[self.bandId]) <= 0:
                del self.band_map[self.bandId]

        if self.avatarId != 0:
            del self.allBandmembers[self.avatarId]
        
        messenger.send(BandConstance.BandMembershipChange, [self, 1])
        DistributedObject.disable(self)

    def delete(self):
        self.avatarId = None
        DistributedObject.delete(self)
    
    def setAvatarId(self, avatarId):
        if self.avatarId != 0:
            del self.allBandmembers[avatarId]
        
        self.avatarId = avatarId
        self.allBandmembers[avatarId] = self

    def setName(self, name):
        self.name = name
        if self.isGenerated():
            messenger.send(BandConstance.BandMembershipChange, [self, 0])
    
    def setHp(self, hp):
        self.hp = hp
        if self.isGenerated():
            messenger.send(BandConstance.BandMemberHpChange, [self, self.hp, self.maxHp])
    
    def setMaxHp(self, maxHp):
        self.maxHp = maxHp
        if self.isGenerated():
            messenger.send(BandConstance.BandMemberHpChange, [self, self.hp, self.maxHp])

    def setBandId(self, manager, id):
        if self.bandId:
            self.band_map[self.bandId].remove(self)
            if len(self.band_map[self.bandId]) <= 0:
                del self.band_map[self.bandId]

        self.bandId = (manager, id)
        if self.bandId:
            self.band_map.setdefault(self.bandId, set()).add(self)

    def getBandId(self):
        return self.bandId

    def setIsManager(self, flag):
        self.isManager = flag
        if self.isGenerated():
            messenger.send(BandConstance.BandMembershipChange, [self, 0])
    
    def setShipInfo(self, shipId, shipName, shipClass, mastInfo):
        self.shipInfo = [
            shipId,
            shipName,
            shipClass,
            mastInfo]
        if self.isGenerated:
            messenger.send(BandConstance.BandMemberShipChange, [self, shipId])
    
    def getShipInfo(self):
        return self.shipInfo
    
    def setShipHasSpace(self, hasSpace):
        self.shipHasSpace = hasSpace
        if self.isGenerated:
            messenger.send(BandConstance.BandMemberShipChange, [self, self.shipInfo[0]])
    
    def getShipHasSpace(self):
        return self.shipInfo[0] and (self.shipHasSpace or localAvatar.getInventory() and self.shipInfo[0] in localAvatar.getInventory().getShipDoIdList())
    
    def setChat(self, message, chatFlags, DISLid):
        if not self.cr.avatarFriendsManager.checkIgnored(self.avatarId):
            displayMess = '%s %s %s' % (self.name, PLocalizer.CrewPrefix, message)
            base.chatAssistant.receivePartyMessage(displayMess)

    def setWLChat(self, message, chatFlags, DISLid):
        if not self.whiteListEnabled:
            return
        
        if not self.cr.avatarFriendsManager.checkIgnored(self.avatarId):
            displayMess = '%s %s %s' % (self.name, PLocalizer.CrewPrefix, message)
            base.chatAssistant.receivePartyMessage(displayMess)
    
    def setSpeedChat(self, senderId, msgIndex):
        if not self.cr.avatarFriendsManager.checkIgnored(self.avatarId):
            displayMess = '%s %s %s' % (self.name, PLocalizer.CrewPrefix, SCDecoders.decodeSCStaticTextMsg(msgIndex))
            base.chatAssistant.receivePartyMessage(displayMess)
    
    def setSCQuestChat(self, senderId, questInt, msgType, taskNum):
        if not self.cr.avatarFriendsManager.checkIgnored(self.avatarId):
            displayMess = '%s %s %s' % (self.name, PLocalizer.CrewPrefix, PSCDecoders.decodeSCQuestMsgInt(questInt, msgType, taskNum))
            base.chatAssistant.receivePartyMessage(displayMess)

    def getName(self):
        return self.name

    def setMessage(self, fromAvatarId, message):
        if self.avatarId != fromAvatarId:
            print(message)

    def setShipDeployMessage(self, fromAvatarId, shipName, locationName):
        if self.avatarId != localAvatar.doId:
            message = PLocalizer.OtherShipIsBeingDeployed % (self.name, shipName, locationName)
            localAvatar.guiMgr.messageStack.addTextMessage(message)

    def isOnline(self):
        return True

    def isUnderstandable(self):
        return True

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def sendTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        self.d_teleportQuery(localAvatar.doId, localGuildId, localShardId)

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def d_teleportQuery(self, localAvId, localGuildId, localShardId):
        self.sendUpdate('teleportQuery', [localAvId, localGuildId, localShardId])

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        self.d_teleportResponse(available, shardId, instanceDoId, areaDoId, sendToId)

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def d_teleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId):
        self.sendUpdate('teleportResponse', [localAvatar.doId, available, shardId, instanceDoId, areaDoId])

