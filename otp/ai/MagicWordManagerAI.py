from panda3d.core import Datagram
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *


class MagicWordManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("MagicWordManagerAI")

    def sendMagicWord(self, word, targetId):
        invokerId = self.air.getAvatarIdFromSender()
        invoker = self.air.doId2do.get(invokerId)

        if invoker.getAdminAccess() <= MINIMUM_MAGICWORD_ACCESS:
            self.air.writeServerEvent(
                'suspicious',
                invokerId,
                'Attempted to issue magic word: %s' %
                word)
            return

        if not invoker:
            self.sendUpdateToAvatarId(
                invokerId,
                'sendMagicWordResponse',
                ['missing invoker'])
            return

        target = self.air.doId2do.get(targetId)
        if not target:
            self.sendUpdateToAvatarId(
                invokerId,
                'sendMagicWordResponse',
                ['missing target'])
            return

        response = spellbook.process(self, invoker, target, word)
        if response:
            self.sendUpdateToAvatarId(
                invokerId, 'sendMagicWordResponse', [response])

        self.air.writeServerEvent('magic-word', invokerId=invokerId, invokerName=invoker.getName(), invokerAccess=invoker.getAdminAccess(), targetId=targetId,
                                  targetName=target.getName(), targetAccess=target.getAdminAccess(), command=word, response=response)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def docs():
    """
    Generates helpful documentation regarding available server commands in a CSV file
    """

    import csv
    rows = [['Name', 'Documentation', 'Types', 'Access']]
    for magicwordKey in spellbook.words:
        magicword = spellbook.words[magicwordKey]
        access = magicword.access if magicword.access else '0'
        rows.append([magicword.name, magicword.doc, magicword.types, access])

    with open('serverdocs.csv', 'w') as docsFile:
        writer = csv.writer(docsFile, delimiter=',', lineterminator='\n')
        writer.writerows(rows)

    return 'Command documentation generated'