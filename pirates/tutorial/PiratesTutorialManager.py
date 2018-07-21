from direct.distributed import DistributedObject

class PiratesTutorialManager(DistributedObject.DistributedObject):
    notify = directNotify.newCategory('PiratesTutorialManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.accept('requestTutorial', self.d_requestTutorial)

    def disable(self):
        self.ignoreAll()
        DistributedObject.DistributedObject.disable(self)

    def d_requestTutorial(self):
        self.sendUpdate('requestTutorial', [])

    def enterTutorial(self, tutorialZone):
        base.localAvatar.inTutorial = 1
        messenger.send('startTutorial', [tutorialZone])
        self.acceptOnce('stopTutorial', self.__handleStopTutorial)

    def __handleStopTutorial(self):
        base.localAvatar.inTutorial = 2
        self.d_allDone()

    def d_allDone(self):
        self.sendUpdate('allDone', [])

    def d_toonArrived(self):
        self.sendUpdate('toonArrived', [])
