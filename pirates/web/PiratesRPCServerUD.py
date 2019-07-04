import traceback
import json
import sys

from direct.directnotify.DirectNotifyGlobal import *
from direct.task import Task
from direct.stdpy.threading2 import Thread

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

from pirates.web.PiratesRPCHandler import PiratesRPCHandler
from pirates.web.RPCGlobals import instancebook

class PiratesRPCServerUD(Thread):
    notify = directNotify.newCategory('PiratesRPCServerUD')
    notify.setInfo(True)

    def __init__(self, air):
        Thread.__init__(self)

        self.air = air
        self.hostname = config.GetString('rpc-hostname', '127.0.0.1')
        self.port = config.GetInt('rpc-port', 6484)
        self.poll_interval = config.GetFloat('rpc-poll-interval', 0.001)
        logRequests = config.GetBool('rpc-log-requests', True)
        self.running = True
        self.server = SimpleXMLRPCServer((self.hostname, self.port),
            logRequests=logRequests, requestHandler=PiratesRPCHandler)
        self.server.register_introspection_functions()
        self.registerInstances()
        self.server.register_multicall_functions()

    def registerFunction(self, function, name=None):
        self.server.register_function(function, name)

    def run(self):
        self.notify.info('Starting RPC server at %s:%d/PRPC2' % (self.hostname, self.port))
        self.server.serve_forever(poll_interval=self.poll_interval)

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()

    def registerInstances(self):
        if not len(instancebook.instances):
            self.notify.warning('No RPC handlers to register.')
            return

        for instance in instancebook.instances:
            newInstance = instance(self.air)
            self.notify.info('Registering RPC handler: %s' % instance.__name__)
            self.server.register_instance(newInstance)