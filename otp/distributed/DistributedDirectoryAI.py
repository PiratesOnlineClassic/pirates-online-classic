from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class DistributedDirectoryAI(DistributedObjectAI):
    """
    An empty object used as a parent for other objects, such as the game root
    the UberDOG generates. Parenting rules were an OTP server concept that
    Astron does not use, so they are only stored.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDirectoryAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.parentingRules = ('', '')

    def setParentingRules(self, rule, data):
        self.parentingRules = (rule, data)

    def d_setParentingRules(self, rule, data):
        self.sendUpdate('setParentingRules', [rule, data])

    def b_setParentingRules(self, rule, data):
        self.setParentingRules(rule, data)
        self.d_setParentingRules(rule, data)

    def getParentingRules(self):
        return self.parentingRules
