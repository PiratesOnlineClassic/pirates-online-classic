from panda3d.core import Datagram
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *

import traceback
import os
class MagicWordManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("MagicWordManagerAI")

    def processMagicWord(self, word, invokerId=None, targetId=None):
        remote = invokerId != None
        invoker = None
        access = CATEGORY_SYSTEM_ADMIN
        if not remote:
            invoker = self.air.doId2do.get(invokerId)
            access = invoker.getAdminAccess()

        if access <= MINIMUM_MAGICWORD_ACCESS:
            self.air.writeServerEvent(
                'suspicious',
                invokerId,
                'Attempted to issue magic word: %s' %
                word)
            return 'access denied'

        if not remote:
            if not invoker:
                return 'missing invoker'

        target = None
        if not remote:
            target = self.air.doId2do.get(targetId)
            if not target:
                return 'missing target'

        response = spellbook.process(self, invoker, target, word)

        if not remote:
            self.air.writeServerEvent(
                'magic-word', 
                invokerId=invokerId, 
                invokerName=invoker.getName(), 
                invokerAccess=invoker.getAdminAccess(), 
                targetId=targetId,
                targetName=target.getName(), 
                targetAccess=target.getAdminAccess(), 
                command=word, 
                remote=remote,
                response=response)
        else:
            self.air.writeServerEvent(
                'magic-word', 
                remote=remote ,
                command=word, 
                response=response)     

        return response

    def sendMagicWord(self, word, targetId):
        invokerId = self.air.getAvatarIdFromSender()
        try:
            response = self.processMagicWord(word, invokerId, targetId)
        except Exception as e:
            response = 'An internal error has occured'
            self.notify.warning('An Internal error has occured: %s' % str(e))
            print(traceback.format_exc())
        
        if not response:
            response = 'Invalid magic word. Use ~docs for a cheatsheet'
        
        self.sendUpdateToAvatarId(invokerId, 'sendMagicWordResponse', [response])

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def docs():
    """
    Generates helpful documentation regarding available server commands in a CSV file
    """

    if not os.path.exists('docs'):
        os.mkdir('docs')

    import csv
    rows = [['Name', 'Documentation', 'Types', 'Access']]
    for magicwordKey in spellbook.words:
        magicword = spellbook.words[magicwordKey]
        access = magicword.access if magicword.access else '0'
        doc = magicword.doc.strip() if magicword.doc else 'N\A'
        rows.append([magicword.name, doc, magicword.types, access])

    with open('docs/serverdocs.csv', 'w') as docsFile:
        writer = csv.writer(docsFile, delimiter=',', lineterminator='\n')
        writer.writerows(rows)

    return 'Command documentation generated'