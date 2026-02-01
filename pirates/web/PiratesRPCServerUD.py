from direct.directnotify.DirectNotifyGlobal import *

from pirates.web.PiratesRPCHandler import PiratesRPCHandler
from pirates.web import RPCGlobals

from xmlrpc.server import SimpleXMLRPCServer
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
        return SimpleXMLRPCServer._dispatch(self, method, params)
