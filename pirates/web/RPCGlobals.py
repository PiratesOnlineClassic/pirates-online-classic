from direct.directnotify.DirectNotifyGlobal import *

class ResponseCodes:
    """
    Standardized response codes
    """

    SUCCESS = 200
    INVALID_FUNCTION = 300
    INTERNAL_ERROR = 400
    ENCODING_NOT_SUPPORTED = 501
    UNAUTHORIZED = 502
    INVALID_ARGUMENT = 503

class InstanceBook:
    """
    The instance book manages all rpc handlers in the system
    """

    notify = directNotify.newCategory('InstanceBook')

    def __init__(self):
        self.instances = {}

    def addInstance(self, serviceName, instanceCls):
        if serviceName in self.instances:
            self.notify.warning('Attempted to double register instance handler: %s' % instanceCls.__name__)
            return
        
        self.instances[serviceName] = instanceCls

    def __repr__(self):
        r = ''

        for instance in self.instances:
            r += 'Instance: %s\n' % (instance.__name__)

        return r

instancebook = InstanceBook()

class RPCInstanceDecorator:
    """
    Registers RPC instance handlers with the instance book
    """

    def __init__(self, serviceName=None):
        self.serviceName = serviceName

    def __call__(self, instance):
        serviceName = self.serviceName if self.serviceName else instance.__name__
        instancebook.addInstance(serviceName, instance)
        return instance

rpcservice = RPCInstanceDecorator