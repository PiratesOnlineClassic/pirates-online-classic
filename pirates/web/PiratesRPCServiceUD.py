import traceback
import inspect
import json
import sys

from direct.directnotify.DirectNotifyGlobal import *
from direct.task import Task
from direct.stdpy.threading2 import Thread

from pirates.web.PiratesRPCServerUD import PiratesRPCServerUD
from pirates.web.RPCGlobals import instancebook

class PiratesRPCServiceUD(Thread):
    notify = directNotify.newCategory('PiratesRPCServiceUD')
    notify.setInfo(True)

    def __init__(self, air):
        Thread.__init__(self)

        self.air = air
        self.hostname = config.GetString('rpc-hostname', '127.0.0.1')
        self.port = config.GetInt('rpc-port', 6484)
        self.poll_interval = config.GetFloat('rpc-poll-interval', 0.001)
        self.running = True
        self.server = PiratesRPCServerUD(self, (self.hostname, self.port))
        self.server.register_introspection_functions()
        self.server.register_multicall_functions()
        self.instances = []
        self.registerInstances()

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

        for instanceName in instancebook.instances:
            instance = instancebook.instances[instanceName]
            newInstance = instance(self.air)
            self.instances.append(newInstance)

            self.notify.info('Registering RPC handler: %s' % instance.__name__)
            methods = inspect.getmembers(newInstance, predicate=inspect.ismethod)
            for method in methods:
                methodName, methodFunc = method
                if methodName.startswith('_'):
                    continue
                
                rpcName = '%s.%s' % (instanceName, methodName)
                self.notify.debug(' - %s' % rpcName)
                self.server.register_function(methodFunc, rpcName)
