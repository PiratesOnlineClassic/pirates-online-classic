from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
import json

class CentralLoggerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('CentralLoggerUD')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def sendMessage(self, category, message, targetDISLid, targetAvId):
        self.notify.debug('Received message from client')

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

    def reportException(self, sender, exception, isClient=False):
        self.notify.info('Received exception log request')

        exceptionLogger = config.GetString('exception-logger', 'event-logger')
        messageTitle = 'client-exception' if isClient else 'server-exception'
        messageBody = {
            'exception': exception,
            'devServer': self.air.isDevServer(),
            'serverVersion': config.GetString('server-version', 'pirates-dev')         
        }

        if self.notify.getDebug():
            # Print to console
            print((json.dumps(event)))

        if exceptionLogger == 'splunk':
            pass #TODO

        elif exceptionLogger == 'event-logger':

            # Log exception to event logger
            self.air.writeServerEvent(messageTitle, **messageBody)

        else:
            self.notify.warning('Unknown exception-logger: %s' % exceptionLogger)