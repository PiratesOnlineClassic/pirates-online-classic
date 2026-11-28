import hmac

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from otp.distributed.PotentialAvatar import PotentialAvatar
from pirates.pirate.HumanDNA import HumanDNA
from pirates.piratesbase import MembershipGlobals
from pirates.piratesgui import PiratesGuiGlobals
from requests import get


class ClientServicesManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('ClientServicesManager')
    AvatarSlots = MembershipGlobals.AvatarSlots

    # The name states of the avatar list, see ClientServicesManagerUD:
    NameStateClosed = 0
    NameStateOpen = 1
    NameStatePending = 2
    NameStateApproved = 3
    NameStateRejected = 4

    # ...and the wish states the AvatarChooser knows them by:
    NameState2WishState = {
        NameStateOpen: 'OPEN',
        NameStatePending: 'PENDING',
        NameStateApproved: 'APPROVED',
        NameStateRejected: 'DENIED'}

    def performLogin(self, doneEvent):
        self.doneEvent = doneEvent
        token = self.cr.playToken or 'dev'

        key = 'cd09ed406383f3d3ebb62b9ce23d41dd'
        digest_maker = hmac.new(key.encode('utf-8'), digestmod='md5')
        digest_maker.update(token.encode('utf-8'))
        clientKey = digest_maker.hexdigest()

        address = ''#get('https://api.ipify.org/').text

        self.sendUpdate('login', [token, address, clientKey])

    def acceptLogin(self, access, maxAvatars, maxSlots):
        # the account's membership and pirate slots, the DISL token used to
        # carry these (see LoginScreen.handleLoginResponseMsg3)...
        self.cr.setIsPaid(access)
        self.cr.accountDetailRecord.piratesAccess = access
        self.cr.accountDetailRecord.maxAvatars = maxAvatars
        self.cr.accountDetailRecord.maxAvatarSlots = maxSlots
        messenger.send(self.doneEvent, [{'mode': 'success'}])

        # TODO?
        #base.funnel.start_session()
        #base.funnel.submit_events()

    def requestAvatars(self):
        self.sendUpdate('requestAvatars')

    def setAvatars(self, avatars):
        avatarList = {}

        # the slots a Freebooter may not fill are "Unlimited Access Only",
        # each pirate takes the place of its own slot below...
        record = self.cr.accountDetailRecord
        positions = [avatar[3] for avatar in avatars]
        data = MembershipGlobals.getAvatarSlotStates(positions, record.maxAvatars,
            record.maxAvatarSlots or self.AvatarSlots)

        for avNum, avName, avDNA, avPosition, nameState, wishName, defaultShard, lastLogout in avatars:
            nameOpen = int(nameState == self.NameStateOpen)
            names = [avName, '', '', '']
            if nameState == self.NameStatePending:
                names[1] = avName
            elif nameState == self.NameStateApproved:
                names[2] = wishName
            elif nameState == self.NameStateRejected:
                names[3] = avName

            dna = HumanDNA()
            dna.makeFromNetString(avDNA)
            dna.setName(avName)

            # The AvatarChooser shows each pirate in its own slot of the account:
            if avPosition >= len(data):
                self.notify.warning('Avatar %d is in invalid slot %d!' % (avNum, avPosition))
                continue

            data[avPosition] = PotentialAvatar(avNum, names, dna, avPosition, nameOpen,
                wishState=self.NameState2WishState.get(nameState, 'CLOSED'), wishName=wishName,
                defaultShard=defaultShard, lastLogout=lastLogout)

        avatarList[1] = data
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
        self._nameTypedCallback = callback
        self.sendUpdate('setNameTyped', [avId, name])

    def setNameTypedResp(self, avId, status):
        callback = getattr(self, '_nameTypedCallback', None)
        self._nameTypedCallback = None
        if callback:
            callback(avId, status)

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

    def sendPopulateAvatar(self, avId, dna, usePattern, p1, p2, p3, p4):
        self.sendUpdate('populateAvatar', [avId, dna.makeNetString(), usePattern, p1, p2, p3, p4])

    def populateAvatarResp(self, success):
        messenger.send('avatarPopulated', [success])
