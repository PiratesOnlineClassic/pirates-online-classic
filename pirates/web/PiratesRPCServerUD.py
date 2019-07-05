from direct.directnotify.DirectNotifyGlobal import *

from pirates.web.PiratesRPCHandler import PiratesRPCHandler
from pirates.web import RPCGlobals

from SimpleXMLRPCServer import SimpleXMLRPCServer
import traceback

class PiratesRPCServerUD(SimpleXMLRPCServer):
    notify = directNotify.newCategory('PiratesRPCServerUD')
    notify.setInfo(True)

    def __init__(self, air, addr, **kwargs):
        logRequests = config.GetBool('rpc-log-requests', True)
        SimpleXMLRPCServer.__init__(
            self, addr, 
            logRequests=logRequests,
            requestHandler=PiratesRPCHandler,
            **kwargs)
        self.air = air

    def _dispatch(self, method, params):
        self.notify.debug('Received request. Method (%s) Params (%s)' % (method, params))
        try:
            return SimpleXMLRPCServer._dispatch(self, method, params)
        except Exception as e:
            return self.errorResponse(e)

    def errorResponse(self, exception):
        self.notify.warning('Internal error has occured: %s' % exception)
        print(traceback.format_exc())

        return {
            'code': RPCGlobals.ResponseCodes.INTERNAL_ERROR,
            'message': 'An internal error has occured',
            'exception': str(exception),
            'trace': traceback.format_exc()
        }