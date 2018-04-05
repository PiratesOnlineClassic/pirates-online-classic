from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PLocalizer

class DistributedPlayerPirateAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerPirateAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.dnaString = ''
        self.emoteId = 0

    def setDNAString(self, dnaString):
        self.dnaString = dnaString

    def d_setDNAString(self, dnaString):
        self.sendUpdate('setDNAString', [dnaString])

    def b_setDNAString(self, dnaString):
        self.setDNAString(dnaString)
        self.d_setDNAString(dnaString)

    def getDNAString(self):
        return self.dnaString

    def hasEmote(self, emoteId):
        emote = PLocalizer.emotes.get(emoteId)
        if not emote:
            emote = PLocalizer.nonMenuEmoteAnimations.get(emoteId)

        if not emote:
            emote = PLocalizer.receiveWeaponEmotes.get(emoteId)

        return emote is not None

    def setEmote(self, emoteId):
        if not self.hasEmote(emoteId):
            self.notify.debug('Cannot set emote for %d, invalid emoteId specified!' % (
                self.doId))

            return

        self.emoteId = emoteId

        # we must send play emote twice because the field is marked broadcast,
        # which means everyone in the same interest will need to hear about the message;
        # we must first send a direct update to our client object, then broadcast the message...
        self.sendUpdateToAvatarId(self.doId, 'playEmote', [emoteId])
        self.sendUpdate('playEmote', [emoteId])

    def getEmoteId(self):
        return self.emoteId

    def d_relayTeleportLoc(self, shardId, zoneId, teleportMgrDoId):
        self.sendUpdateToAvatarId(self.doId, 'relayTeleportLoc', [shardId, zoneId, teleportMgrDoId])

    def d_forceTeleportStart(self, instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone):
        self.sendUpdateToAvatarId(self.doId, 'forceTeleportStart', [instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone])
