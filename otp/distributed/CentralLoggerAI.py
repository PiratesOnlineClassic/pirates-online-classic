from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal


class CentralLoggerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('CentralLoggerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def sendMessage(self, category, message, targetDISLid, targetAvId):
        self.sendUpdate(
            'sendMessage', [
                category, message, targetDISLid, targetAvId])

    def logMessageLocally(self, category, message, targetDISLid, targetAvId):
        parts = message.split('|')
        msgType = parts[0]
        fields = {
            'targetDISLid': targetDISLid,
            'targetAvId': targetAvId
        }

        if msgType == 'GUEST_FEEDBACK':
            fields['feedbackCategory'] = parts[1]
            fields['feedbackMessage'] = parts[2]

        if self.notify.getDebug():
            event = {
                'category': category,
                'message': message,
                'type': msgType,
            }
            event.update(fields)

            data = json.dumps(event)
            print(data)

        self.air.writeServerEvent(
            category,
            messageType=msgType,
            message=message,
            **fields)
