from direct.directnotify.DirectNotifyGlobal import *

import json

class RPCServiceUD:
    """
    Base class for all RPC Handlers
    """

    notify = directNotify.newCategory('RPCServiceUD')

    def __init__(self, air):
        self.air = air

    def _formatResults(self, code=200, message='Success', **kwargs):
        results = {
            'code': code,
            'message': message,
        }

        for kwarg in kwargs:
            results[kwarg] = kwargs[kwarg]

        return json.dumps(results)