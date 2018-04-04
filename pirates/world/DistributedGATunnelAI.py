
from pirates.world.DistributedGAConnectorAI import DistributedGAConnectorAI
from direct.directnotify import DirectNotifyGlobal

class DistributedGATunnelAI(DistributedGAConnectorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGATunnelAI')

    def __init__(self, air):
        DistributedGAConnectorAI.__init__(self, air)


    # sendLeaveTunnelDone() airecv clsend

    def sendLeaveTunnelDone(self, sendLeaveTunnelDone):
        pass


