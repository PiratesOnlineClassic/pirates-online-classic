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

class InstanceBook:
    """
    The instance book manages all rpc handlers in the system
    """

    notify = directNotify.newCategory('InstanceBook')

    def __init__(self):
        self.instances = []

    def addInstance(self, instanceCls):
        if instanceCls in self.instances:
            self.notify.warning('Attempted to double register instance handler: %s' % instanceCls.__name__)
            return
        
        self.instances.append(instanceCls)

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

    def __call__(self, instance):
        instancebook.addInstance(instance)
        return instance

rpcservice = RPCInstanceDecorator