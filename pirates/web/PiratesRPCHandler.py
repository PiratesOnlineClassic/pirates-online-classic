
from panda3d.core import ConfigVariableList

from direct.directnotify.DirectNotifyGlobal import *

from pirates.web.RPCServiceUD import RPCServiceUD

from xmlrpc.server import SimpleXMLRPCRequestHandler


class PiratesRPCHandler(SimpleXMLRPCRequestHandler):
    notify = directNotify.newCategory('PiratesRPCHandler')
    notify.setInfo(True)

    rpc_paths = ('/', '/PRPC2')

    def __init__(self, request, client_address, server):
        self.notify.info('Received request from: %s:%s' % client_address)
        self.client_ip, self.client_port = client_address
        self.whitelist_ips = ConfigVariableList('rpc-whitelist-ip')
        SimpleXMLRPCRequestHandler.__init__(self, request, client_address, server)

    def decode_request_content(self, data):
        if self.client_ip not in self.whitelist_ips:
            return

        data = SimpleXMLRPCRequestHandler.decode_request_content(self, data)
        self.notify.debug('Received request: %s' % data)
        return data

    def log_request(self, code='-', size='-'):
        """Selectively log an accepted request."""

        if self.server.logRequests:
            self.notify.info('RPC request complete. Code (%s) Size(%s)' % (code, size))
