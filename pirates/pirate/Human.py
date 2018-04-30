import random

from direct.actor import Actor
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import FSM
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.interval.IntervalGlobal import *
from direct.showbase import ShadowPlacer
from direct.showbase.PythonUtil import quickProfile
from direct.task import Task
from panda3d.core import *
from pirates.battle import WeaponGlobals
from pirates.makeapirate import PirateFemale, PirateMale
from pirates.pirate import Biped, HumanBase, HumanDNA
from pirates.pirate.HumanAnimationMixer import HumanAnimationMixer
from pirates.piratesbase import PiratesGlobals

TX = 0
TY = 1
TZ = 2
RX = 3
RY = 4
RZ = 5
SX = 6
SY = 7
SZ = 8
AnimDict = {}
AnimListDict = {'sf': Biped.DefaultAnimList, 'ms': Biped.DefaultAnimList, 'mi': Biped.DefaultAnimList, 'tp': Biped.DefaultAnimList, 'tm': Biped.DefaultAnimList}
CustomAnimDict = {'msf': Biped.msfCustomAnimList, 'mms': Biped.mmsCustomAnimList, 'mmi': Biped.mmiCustomAnimList, 'mtp': Biped.mtpCustomAnimList, 'mtm': Biped.mtmCustomAnimList, 'fsf': Biped.fsfCustomAnimList, 'fms': Biped.fmsCustomAnimList, 'fmi': Biped.fmiCustomAnimList, 'ftp': Biped.ftpCustomAnimList, 'ftm': Biped.ftmCustomAnimList}
CastAnimDict = {'models/char/js': Biped.jsCustomAnimList, 'models/char/wt': Biped.wtCustomAnimList, 'models/char/es': Biped.esCustomAnimList, 'models/char/td': Biped.tdCustomAnimList, 'models/char/cb': Biped.cbCustomAnimList, 'models/char/jg': Biped.jgCustomAnimList, 'models/char/jr': Biped.jrCustomAnimList, 'models/char/plf': Biped.plfCustomAnimList, 'models/char/pls': Biped.plsCustomAnimList}
NewModelDict = {'sf': 'sf', 'ms': 'ms', 'mi': 'mi', 'tp': 'tp', 'tm': 'tm'}
TempDict = [
 'sf', 'ms', 'mi', 'tp', 'tm']
PrebuiltAnimDict = {}
HeadPositions = [
 [
  VBase3(0.0, 0.0, 0.0), VBase3(0.0, 0.0, -0.08), VBase3(0.0, 0.0, 0.0), VBase3(0.0, 0.0, -0.08), VBase3(0.0, 0.0, 0.0)], [VBase3(0, 0, 0.0), VBase3(0, 0, 0.0), VBase3(0, 0, 0.0), VBase3(0, 0, 0.0), VBase3(0, 0, 0.0)]]
HeadScales = [
 [
  1.05, 0.8, 0.85, 0.82, 0.88], [1.1, 0.9, 0.95, 0.97, 0.95]]
BodyScales = [
 [
  0.87, 0.98, 1.0, 0.98, 1.05], [0.88, 0.9, 1.02, 1.07, 0.98]]
PlayerNames = [
 "Cap'n Bruno Cannonballs", 'Bad-run Thomas', 'Carlos Saggingsails', 'Smugglin Willy Hawkins']

class Human(HumanBase.HumanBase, Biped.Biped):
    
    notify = DirectNotifyGlobal.directNotify.newCategory('Human')
    prebuiltAnimData = {}

    def __init__(self, other=None):
        Biped.Biped.__init__(self, other, HumanAnimationMixer)
        self.zombie = False
        self.flattenPending = None
        self.optimizeLOD = base.config.GetBool('optimize-avatar-lod', 1)
        self.loaded = 0
        self.playingRate = None
        self.shadowFileName = 'models/misc/drop_shadow'
        self.setFont(PiratesGlobals.getInterfaceFont())
        self.__blinkName = 'blink-' + str(self.this)
        self.eyeLids = None
        self.eyeBalls = None
        self.eyeIris = None
        self.reducedAnimList = None
        self.headNode = None
        self.extraNode = None
        self.scaleNode = None
        self.rootNode = None
        self.floorOffsetZ = 0.0
        self.headFudgeHpr = Vec3(0, 0, 0)
        self.randGen = random.Random()
        self.randGen.seed(random.random())
        self.eyeFSM = ClassicFSM('eyeFSM', [
         State('off', self.enterEyeFSMOff, self.exitEyeFSMOff, [
            'open', 'closed']),

         State('open', self.enterEyeFSMOpen, self.exitEyeFSMOpen, [
            'closed', 'off']),

         State('closed', self.enterEyeFSMClosed, self.exitEyeFSMClosed, [
            'open', 'off'])], 'off', 'off')

        self.eyeFSM.enterInitialState()
        if other != None:
            self.copyHuman(other)

    def removeCopiedNodes(self):
        self.dropShadow = self.find('**/drop_shadow*')
        if not self.dropShadow.isEmpty():
            self.deleteDropShadow()

        billboardNode = self.find('**/billboardNode')
        if not billboardNode.isEmpty():
            billboardNode.removeNode()

        self.getGeomNode().getParent().removeNode()

    def flattenHuman(self):
        self.getLOD('500').flattenStrong()
        self.getWeaponJoints()

    def __doneFlattenHuman(self, models):
        self.flattenPending = None
        self.getWeaponJoints()
        return

    def copyHuman(self, other):
        self.gender = other.gender
        self.loaded = other.loaded
        self.loadAnimatedHead = other.loadAnimatedHead
        self.scale = other.scale
        self.flattenHuman()

    def delete(self):
        try:
            self.Human_deleted
        except:
            self.Human_deleted = 1
            taskMgr.remove(self.__blinkName)
            if self.dropShadow and not self.dropShadow.isEmpty():
                self.deleteDropShadow()
            del self.eyeFSM
            self.controlShapes = None
            self.sliderNames = None
            Biped.Biped.delete(self)

    def isDeleted(self):
        try:
            self.Human_deleted
            if self.Human_deleted == 1:
                return True
        except:
            return False

    def setupExtraNodes(self):
        idx = 0
        if self.gender == 'f':
            idx = 1

        jointName = 'def_head01'
        jointNameExtra = 'def_extra_jt'
        jointNameScale = 'def_scale_jt'
        lods = self.getLODNames()
        self.headNode = self.controlJoint(None, 'legs', jointName, lods[0])
        self.extraNode = self.controlJoint(None, 'legs', jointNameExtra, lods[0])
        self.scaleNode = self.controlJoint(None, 'legs', jointNameScale, lods[0])
        self.rootNode = self.getLOD('2000').find('**/dx_root')
        for lod in lods[1:]:
            self.controlJoint(self.headNode, 'legs', jointName, lod)
            self.controlJoint(self.extraNode, 'legs', jointNameExtra, lod)
            self.controlJoint(self.scaleNode, 'legs', jointNameScale, lod)
            exposedHeadJoint = self.getLOD(lod).find('**/def_head01')
            if not exposedHeadJoint.isEmpty():
                exposedHeadJoint.removeNode()

        self.headNode.setScale(HeadScales[idx][self.style.getBodyShape()])
        self.setGlobalScale(self.calcBodyScale())

    def undoExtraNodes(self):
        jointNameExtra = 'def_extra_jt'
        jointNameScale = 'def_scale_jt'
        joints = self.findAllMatches('**/*' + jointNameExtra)
        if not joints.isEmpty():
            joints.detach()
            joints.clear()

        joints = self.findAllMatches('**/*' + jointNameScale)
        if not joints.isEmpty():
            joints.detach()
            joints.clear()

        if self.scaleNode:
            self.scaleNode.removeNode()
            self.scaleNode = None
            self.rootNode = None

    def fixEyes(self):
        self.eyeLids = {}
        self.eyeBalls = {}
        self.eyeIris = {}
        for lodName in self.getLODNames():
            geom = self.getPart('head', lodName)
            self.eyeLids[lodName] = geom.findAllMatches('**/*eyelid*')
            self.eyeBalls[lodName] = geom.findAllMatches('**/eye_ball*')
            self.eyeIris[lodName] = geom.findAllMatches('**/eye_iris*')
            self.eyeLids[lodName].stash()
            self.eyeBalls[lodName].unstash()
            self.eyeIris[lodName].unstash()

    def makeAnimDict(self, gender, animNames):
        self.animTable = []
        for currAnim in animNames:
            anim = animNames.get(currAnim)
            for currAnimName in anim:
                self.animTable.append([currAnimName, currAnimName])

        self.reducedAnimList = self.animTable

    def forceLoadAnimDict(self):
        for anim in self.animDict.keys():
            self.getAnimControls(anim)

    def createAnimDict(self, customList=None):
        self.type = TempDict[self.style.body.shape]
        filePrefix = 'models/char/m'
        genderPrefix = 'm'
        if self.style.gender == 'f':
            filePrefix = 'models/char/f'
            genderPrefix = 'f'

        if self.reducedAnimList is None:
            self.animDict = self.prebuiltAnimData[genderPrefix + self.type]
            return

        filePrefix += 'p'
        animList = self.reducedAnimList
        if animList is None:
            animList = AnimListDict[self.type]

        self.animDict = {}
        for anim in animList:
            animSuffix = ''
            for i in range(0, len(CustomAnimDict[genderPrefix + self.type])):
                if anim[0] == CustomAnimDict[genderPrefix + self.type][i]:
                    animSuffix = '_' + genderPrefix + NewModelDict.get(self.type)
                    break

            self.animDict[anim[0]] = filePrefix + '_' + anim[1] + animSuffix

        if self.reducedAnimList is None:
            self.animDict.pop('intro')

        return filePrefix

    def getIsPaid(self):
        return True

    def loadHuman(self, other):
        other.style = self.style
        other.gender = self.style.gender
        other.model.dna = self.style
        self.createAnimDict()
        if self.style.gender == 'f':
            self.headFudgeHpr = Vec3(0, 0, 0)
            idx = 1
        else:
            self.headFudgeHpr = Vec3(0, 0, 0)
            idx = 0

        other.zombie = self.zombie
        yieldThread('anim dict')
        other.isPaid = self.getIsPaid()
        other.showLOD(2000)
        yieldThread('showLOD')
        if other.zombie:
            other.showZombie()

        if hasattr(self, 'motionFSM'):
            self.motionFSM.setAvatar(self)

        yieldThread('zombie')
        other.applyBodyShaper()
        yieldThread('body shaper')
        other.applyHeadShaper()
        yieldThread('head shaper')
        if self.zombie:
            other.model.eyeBalls.stash()
            other.model.irises.stash()

        self.copyActor(other)
        self.floorOffsetZ = other.rootNode.getZ()
        yieldThread('copyActor')
        self.copyHuman(other)
        if self.zombie:
            other.model.eyeBalls.unstash()
            other.model.irises.unstash()

        self.rootNode = self.getLOD('2000').find('**/dx_root')
        self.headNode = self.getLOD('2000').find('**/def_head01')
        self.scaleNode = self.controlJoint(None, 'legs', 'def_scale_jt', '2000')
        for lod in ['1000', '500']:
            self.controlJoint(self.scaleNode, 'legs', 'def_scale_jt', lod)

        self.setGlobalScale(self.calcBodyScale())
        yieldThread('copyHuman')
        self.loadAnimsOnAllLODs(self.animDict, 'modelRoot')
        yieldThread('loadAnims')
        other.zombie = 0
        other.showNormal()
        yieldThread('show normal')
        self.initializeNametag3d()
        self.initializeDropShadow()
        self.setName(self.getName())
        yieldThread('misc nodes')
        self.loaded = 1

    def setGlobalScale(self, scale):
        self.scaleNode.setScale(scale)
        self.scaleNode.setZ(-(self.floorOffsetZ * (1 - scale)))

    def initializeMiscNodes(self):
        self.initializeNametag3d()
        self.initializeDropShadow()

    def undoControlJoints(self):
        self.getGeomNode().getParent().findAllMatches('def_*').detach()
        self.getGeomNode().getParent().findAllMatches('trs_*').detach()
        self.findAllMatches('def_*').detach()
        self.findAllMatches('trs_*').detach()

    def cleanupHuman(self, gender='m'):
        self.eyeFSM.request('off')
        self.undoControlJoints()
        self.removeCopiedNodes()
        self.eyeLids = {}
        self.eyeBalls = {}
        self.eyeIris = {}
        self.flush()
        self.loaded = 0
        self.master = 0

    def generateHuman(self, gender, others):
        if gender == 'f':
            other = others[1]
        else:
            other = others[0]

        if self.loaded:
            self.cleanupHuman()

        self.loadHuman(other)
        if self.isLocal():
            self.renderReflection = True

        self.setRenderReflection()
        self.resetEffectParent()

    def getShadowJoint(self):
        return self.nametagNodePath

    def getNametagJoints(self):
        joints = []
        for lodName in self.getLODNames():
            bundle = self.getPartBundle('modelRoot', lodName)
            joint = bundle.findChild('name_tag')
            if joint:
                joints.append(joint)

        return joints

    def __blinkOpenEyes(self, task):
        if self.eyeFSM.getCurrentState().getName() == 'closed':
            self.eyeFSM.request('open')

        r = self.randGen.random()
        if r < 0.1:
            t = 0.2
        else:
            t = r * 4.0 + 1.0

        taskMgr.doMethodLater(t, self.__blinkCloseEyes, self.__blinkName)
        return Task.done

    def __blinkCloseEyes(self, task):
        if self.eyeFSM.getCurrentState().getName() != 'open':
            taskMgr.doMethodLater(4.0, self.__blinkCloseEyes, self.__blinkName)
        else:
            self.eyeFSM.request('closed')
            taskMgr.doMethodLater(0.125, self.__blinkOpenEyes, self.__blinkName)

        return Task.done

    def startBlink(self):
        taskMgr.remove(self.__blinkName)
        if self.eyeLids:
            self.openEyes()

        taskMgr.doMethodLater(self.randGen.random() * 4.0 + 1,  self.__blinkCloseEyes,
            self.__blinkName)

    def stopBlink(self):
        taskMgr.remove(self.__blinkName)
        if self.eyeLids:
            self.eyeFSM.request('open')

    def closeEyes(self):
        self.eyeFSM.request('closed')

    def openEyes(self):
        self.eyeFSM.request('open')

    def enterEyeFSMOff(self):
        pass

    def exitEyeFSMOff(self):
        pass

    def enterEyeFSMOpen(self):
        for lodName in self.getLODNames():
            self.eyeLids[lodName].hide()
            self.eyeBalls[lodName].show()
            self.eyeIris[lodName].show()

    def exitEyeFSMOpen(self):
        pass

    def enterEyeFSMClosed(self):
        return
        for lodName in self.getLODNames():
            self.eyeLids[lodName].show()
            self.eyeBalls[lodName].hide()
            self.eyeIris[lodName].hide()

    def exitEyeFSMClosed(self):
        pass

    def getGlobalScale(self):
        return self.scale

    def calcBodyScale(self):
        idx = 0
        if self.gender == 'f':
            idx = 1

        mappedValue = (0.8 + (1 + self.style.getBodyHeight()) * 0.2) * BodyScales[
            idx][self.style.getBodyShape()]

        return mappedValue

    @classmethod
    def setupAnimDicts(cls):
        for t in TempDict:
            cls.storeAnimDict('models/char/fp', 'f', t)
            cls.storeAnimDict('models/char/mp', 'm', t)

    @classmethod
    def storeAnimDict(cls, prefix, gender, type):
        qualifier = gender + type
        animList = AnimListDict[type]
        cls.prebuiltAnimData[qualifier] = {}
        for anim in animList:
            animSuffix = ''
            for i in range(0, len(CustomAnimDict[qualifier])):
                if anim[0] == CustomAnimDict[qualifier][i]:
                    animSuffix = '_' + gender + NewModelDict.get(type)
                    break

            cls.prebuiltAnimData[qualifier][anim[0]] = prefix + '_' + anim[1] + animSuffix

        cls.prebuiltAnimData[qualifier].pop('intro')

Human.setupAnimDicts()
