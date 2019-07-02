from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import PythonUtil
from direct.showbase.PythonUtil import Functor, DelayedCall, ScratchPad
from direct.showbase.InputStateGlobal import inputState
from direct.task import Task
from direct.distributed.ClockDelta import *

from otp.ai.MagicWordGlobal import *
from libotp import *

lastClickedNametag = None


class MagicWordManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('MagicWordManager')
    neverDisable = 1

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.accept('magicWord', self.handleMagicWord)

    def disable(self):
        self.ignore('magicWord')
        DistributedObject.DistributedObject.disable(self)

    def handleMagicWord(self, magicWord):
        if not self.cr.wantMagicWords:
            return

        if magicWord.startswith('~~'):
            if lastClickedNametag == None:
                target = base.localAvatar
            else:
                target = lastClickedNametag

            magicWord = magicWord[2:]

        if magicWord.startswith('~'):
            target = base.localAvatar
            magicWord = magicWord[1:]

        targetId = target.doId
        if target == base.localAvatar:
            response = spellbook.process(self, base.localAvatar, target, magicWord)
            if response:
                self.sendMagicWordResponse(response)

                # Log the usage to the event logger
                self.cr.centralLogger.writeClientEvent(
                    'magic-word %s used' %
                    magicWord, targetAvId=base.localAvatar.doId)

                return

        self.sendUpdate('sendMagicWord', [magicWord, targetId])

    def sendMagicWordResponse(self, response):
        self.notify.info(response)

        base.localAvatar.setChatAbsolute('Spellbook: ' + str(response), CFSpeech | CFTimeout, quiet = 1)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def docs():
    """
    Generates helpful documentation regarding available client commands in a CSV file
    """

    import csv
    rows = [['Name', 'Documentation', 'Types', 'Access']]
    for magicwordKey in spellbook.words:
        magicword = spellbook.words[magicwordKey]
        access = magicword.access if magicword.access else '0'
        rows.append([magicword.name, magicword.doc, magicword.types, access])

    with open('clientdocs.csv', 'w') as docsFile:
        writer = csv.writer(docsFile, delimiter=',', lineterminator='\n')
        writer.writerows(rows)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def oobe():
    """
    Toggles OOBE mode
    """

    base.oobe()
    return 'Toggled OOBE'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def oobeCull():
    """
    Toggles OOBE Cull mode
    """

    base.oobeCull()
    return 'Toggled OOBE Cull'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def tex():
    """
    Toggles base texture mode
    """

    base.toggleTexture()
    return 'Toggled Texture'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def wire():
    """
    Toggles wireframe mode
    """

    base.toggleWireframe()
    return 'Toggled Wireframe'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def net():
    """
    """

    if self.cr.networkPlugPulled():
        self.cr.restoreNetworkPlug()
        self.cr.startHeartbeat()
        response = 'Network restored.'
    else:
        self.cr.pullNetworkPlug()
        self.cr.stopHeartbeat()
        response = 'Network disconnected.'
    return response

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def disconnect():
    """
    Disconnects from the Client Agent
    """

    base.cr.distributedDistrict.sendUpdate('broadcastMessage')

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def model(path):
    """
    Loads a model into the world locally
    """

    model = loader.loadModel(path)
    model.reparentTo(localAvatar)
    model.wrtReparentTo(render)
    return 'Loaded: %s' % path

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def axis():
    """
    Loads in the XYZ axis model
    """

    axis = loader.loadModel('models/misc/xyzAxis.bam')
    axis.reparentTo(render)
    axis.setPos(base.localAvatar, 0, 0, 0)
    axis.setHpr(render, 0, 0, 0)
    axis10 = loader.loadModel('models/misc/xyzAxis.bam')
    axis10.reparentTo(render)
    axis10.setPos(base.localAvatar, 0, 0, 0)
    axis10.setScale(10)
    axis10.setHpr(render, 0, 0, 0)
    axis10.setColorScale(1, 1, 1, 0.4)
    axis10.setTransparency(1)

    return 'Loaded Axis model'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def clearAxis():
    """
    Clears the loaded axis models
    """

    render.findAllMatches('**/xyzAxis.egg').detach()
    return 'Axis cleared'

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def taskprofileflush(name):
    """
    Flushes the requested AI task profile
    """

    taskMgr.flushTaskProfiles(name)
    response = 'flushed AI task profiles%s' % choice(name, ' for %s' % name, '')
    return response

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def objectcount():
    """
    Logs the clients DO count
    """

    base.cr.printObjectCount()
    return 'logging client distributed object count...'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def taskMgr():
    """
    Logs the client's task manager
    """

    print taskMgr
    return 'logging client taskMgr...'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def jobMgr():
    """
    Logs the client's job manager
    """

    print jobMgr
    return 'logging client jobMgr...'

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[float])
def jobtime(time):
    """
    Sets the client jobMgr timeslice
    """

    response = ''
    if time is None:
        time = jobMgr.getDefaultTimeslice()
        response = 'reset client jobMgr timeslice to %s ms' % time
    else:
        response = 'set client jobMgr timeslice to %s ms' % time
        time = time / 1000.0
    jobMgr.setTimeslice(time)
    return response

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def detectleaks():
    """
    Starts the client leak detector
    """

    started = self.cr.startLeakDetector()
    return choice(started, 'leak detector started', 'leak detector already started')

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[float])
def taskthreshold(threshold):
    """
    Sets the task manager duration threshold
    """

    response = ''
    if threshold is None:
        threshold = taskMgr.DefTaskDurationWarningThreshold
        response = 'reset task duration warning threshold to %s' % threshold
    else:
        response = 'set task duration warning threshold to %s' % threshold
    taskMgr.setTaskDurationWarningThreshold(threshold)
    return response

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def messenger():
    """
    Logs the client messenger
    """

    print messenger
    self.setMagicWordResponse('logging client messenger...')

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def clientcrash():
    """
    Simulates a client crash
    """

    DelayedCall(Functor(self.notify.error, '~clientcrash: simulating a client crash'))

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def badDelete():
    """
    Performs a bad delete operation
    """

    doId = 0
    while doId in base.cr.doId2do:
        doId += 1
    DelayedCall(Functor(base.cr.deleteObjectLocation, ScratchPad(doId = doId), 1, 1))
    return 'doing bad delete'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def idTags():
    """
    Enables idTags
    """

    messenger.send('nameTagShowAvId', [])
    base.idTags = 1

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def nameTags():
    """
    Disables idTags
    """

    messenger.send('nameTagShowName', [])
    base.idTags = 0

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def flush():
    """
    Flushes all client data caches
    """

    base.cr.doDataCache.flush()
    base.cr.cache.flush()

    return 'Client object and data caches flushed'

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[float])
def camerafar(far):
    """
    Sets the cameras far value
    """

    lens = base.camLens
    lens.setFar(far)

    return 'Primary camera set to a max distance of %s' % far