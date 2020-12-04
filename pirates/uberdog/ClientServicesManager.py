import hmac

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from otp.distributed.PotentialAvatar import PotentialAvatar
from otp.otpbase import OTPGlobals
from pirates.pirate.HumanDNA import HumanDNA
from pirates.piratesgui import PiratesGuiGlobals
from requests import get


class ClientServicesManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('ClientServicesManager')

    def performLogin(self, doneEvent):
        self.doneEvent = doneEvent
        token = self.cr.playToken or 'dev'

        key = 'cd09ed406383f3d3ebb62b9ce23d41dd'
        digest_maker = hmac.new(key)
        digest_maker.update(token)
        clientKey = digest_maker.hexdigest()

        address = ''#get('https://api.ipify.org/').text

        self.sendUpdate('login', [token, address, clientKey])

    def acceptLogin(self):
        messenger.send(self.doneEvent, [{'mode': 'success'}])

        # TODO?
        #base.funnel.start_session()
        #base.funnel.submit_events()

    def requestAvatars(self):
        self.sendUpdate('requestAvatars')

    def setAvatars(self, avatars):
        avatarList = {}
        data = []

        for avNum, avName, avDNA, avPosition, nameState in avatars:
            nameOpen = int(nameState == 1)
            names = [avName, '', '', '']
            if nameState == 2:  # PENDING
                names[1] = avName
            elif nameState == 3:  # APPROVED
                names[2] = avName
            elif nameState == 4:  # REJECTED
                names[3] = avName

            dna = HumanDNA()
            dna.makeFromNetString(avDNA)

            data.append(PotentialAvatar(avNum, names, dna, avPosition, nameOpen))

        avatarList[1] = data + [OTPGlobals.AvatarSlotAvailable] * (4 - len(data))
        self.cr.handleAvatarsList(avatarList)

    def sendCreateAvatar(self, avDNA, _, index, name):
        self.sendUpdate('createAvatar', [avDNA.makeNetString(), index, name])

    def createAvatarResp(self, avId):
        messenger.send('createdNewAvatar', [avId])

    def sendDeleteAvatar(self, avId):
        self.sendUpdate('deleteAvatar', [avId])

    def acknowledgeDeleteAvatarResp(self, avid, status):
        if status == False:
            messenger.send('rejectRemoveAvatar', [0])
        if status == True:
            messenger.send('removeAvatarResponse', [avid, 0])

    def sendSetNameTyped(self, avId, name, callback):
        self._callback = callback
        self.sendUpdate('setNameTyped', [avId, name])

    def setNameTypedResp(self, avId, status):
        self._callback(avId, status)

    def sendSetNamePattern(self, avId, p1, f1, p2, f2, p3, f3, p4, f4, callback):
        self._callback = callback
        self.sendUpdate('setNamePattern', [avId, p1, f1, p2, f2, p3, f3, p4, f4])

    def setNamePatternResp(self, avId, status):
        self._callback(avId, status)

    def sendAcknowledgeAvatarName(self, avId, callback):
        self._callback = callback
        self.sendUpdate('acknowledgeAvatarName', [avId])

    def acknowledgeAvatarNameResp(self):
        self._callback()

    def sendChooseAvatar(self, avId):
        self.sendUpdate('chooseAvatar', [avId])
