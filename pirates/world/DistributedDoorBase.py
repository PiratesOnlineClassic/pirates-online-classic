from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.quest.QuestConstants import LocationIds
from pirates.piratesbase import Freebooter
import string

class DistributedDoorBase(DistributedInteractive.DistributedInteractive):
    notify = directNotify.newCategory('DistributedDoorBase')
    notify.setDebug(0)
    
    def __init__(self, cr, name = 'DistributedDoorBase'):
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        NodePath.__init__(self, name)
        self.doorState = PiratesGlobals.DOOR_CLOSED
        self.doorTrack = None
        self.fadeInTrack = None
        self.fadeOutTrack = None
        self.openOtherDoorIval = None
        self.closeOtherDoorIval = None
        self.soundNode = render
        self.closeSfx = None
        self.locked = False
        self.hasDoors = 0
        self.tOpen = 0.5
    
    def delete(self):
        DistributedInteractive.DistributedInteractive.delete(self)
    
    def disable(self):
        self.ignoreAll()
        if self.doorTrack:
            self.doorTrack.pause()
            self.doorTrack = None
        
        self.openDoorIval.pause()
        del self.openDoorIval
        self.closeDoorIval.pause()
        del self.closeDoorIval
        if self.closeOtherDoorIval:
            self.closeOtherDoorIval.pause()
            self.closeOtherDoorIval = None
        
        if self.openOtherDoorIval:
            self.openOtherDoorIval.pause()
            self.openOtherDoorIval = None
        
        self.fadeOutTrack = None
        self.fadeInTrack = None
        if not self.noDoors:
            del self.openSfx
            del self.closeSfx
        
        DistributedInteractive.DistributedInteractive.disable(self)
    
    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        self.setupDoors()
        self.setInteractOptions(proximityText = self.getPrompt(), diskRadius = 12.0, sphereScale = 7.0, endInteract = 0, allowInteract = self.allowInteract)
    
    def getPrompt(self):
        return PLocalizer.InteractOpenDoor

    def setDoorIndex(self, doorIndex):
        self.doorIndex = doorIndex
        doorIndexStr = ''
        if doorIndex > 0:
            doorIndexStr = '_' + str(doorIndex + 1)
        
        self.doorLeftStr = '**/door_left' + doorIndexStr
        self.doorRightStr = '**/door_right' + doorIndexStr
        self.doorLocatorStr = '**/door_locator' + doorIndexStr
    
    def setBuildingUid(self, buildingUid):
        self.buildingUid = buildingUid
    
    def setMovie(self, mode, avId, timestamp):
        if avId == localAvatar.doId:
            return
        
        if timestamp is None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        if mode == PiratesGlobals.DOOR_OPEN and self.hasDoors:
            if self.doorTrack:
                self.doorTrack.pause()
                self.doorTrack = None
            
            self.doorTrack = Sequence(Func(base.playSfx, self.openSfx, node = self.soundNode, volume = 0.7, cutoff = 100), self.openDoorIval, Wait(2.0), self.closeDoorIval, Func(base.playSfx, self.closeSfx, node = self.soundNode, volume = 0.7, cutoff = 100))
            self.doorTrack.start(ts)

    def getParentModel(self):
        pass
    
    def setupDoors(self):
        self.openDoorIval = Parallel()
        self.closeDoorIval = Parallel()
        parent = self.getParentModel()
        if not parent or parent.isEmpty():
            self.noDoors = True
            return
        else:
            self.noDoors = False
        doorLeft = parent.find(self.doorLeftStr)
        doorRight = parent.find(self.doorRightStr)
        if not doorLeft.isEmpty():
            self.openDoorIval.append(LerpHprInterval(doorLeft, self.tOpen, Vec3(-90, 0, 0)))
            self.closeDoorIval.append(LerpHprInterval(doorLeft, self.tOpen, Vec3(0, 0, 0)))
        
        if not doorRight.isEmpty():
            self.openDoorIval.append(LerpHprInterval(doorRight, self.tOpen, Vec3(90, 0, 0)))
            self.closeDoorIval.append(LerpHprInterval(doorRight, self.tOpen, Vec3(0, 0, 0)))
        
        doorLocator = parent.find(self.doorLocatorStr)
        modelName = ''
        self.soundNode = doorLocator
        if not doorLocator.isEmpty():
            self.reparentTo(doorLocator)
            self.setPos(0, 0, 0)
            self.wrtReparentTo(self.getParentObj())
            modelName = doorLocator.getParent().getParent().getName()
        elif not doorLeft.isEmpty() and not doorRight.isEmpty():
            doorPos = doorRight.getPos(doorLeft) * 0.5
            self.reparentTo(doorLeft)
            self.setPos(doorPos)
            self.wrtReparentTo(self.getParentObj())
            modelName = doorLeft.getParent().getParent().getName()
            self.soundNode = doorRight
        elif not doorLeft.isEmpty():
            self.reparentTo(doorLeft)
            self.setPos(4, 0, 0)
            self.wrtReparentTo(self.getParentObj())
            modelName = doorLeft.getParent().getParent().getName()
            self.soundNode = doorLeft
        elif not doorRight.isEmpty():
            self.reparentTo(doorRight)
            self.setPos(-4, 0, 0)
            self.wrtReparentTo(self.getParentObj())
            modelName = doorRight.getParent().getParent().getName()
            self.soundNode = doorRight
        
        if doorLeft.isEmpty() and doorRight.isEmpty():
            self.hasDoors = 0
            self.openDoorIval.append(Wait(self.tOpen))
            self.closeDoorIval.append(Wait(self.tOpen))
        else:
            self.hasDoors = 1
        if string.find(modelName, 'english') >= 0:
            self.openSfx = base.loader.loadSfx('audio/sfx_door_english_open.mp3')
        elif string.find(modelName, 'shanty') >= 0:
            self.openSfx = base.loader.loadSfx('audio/sfx_door_shanty_open.mp3')
        elif string.find(modelName, 'spanish') >= 0:
            self.openSfx = base.loader.loadSfx('audio/sfx_door_spanish_open.mp3')
        else:
            self.openSfx = base.loader.loadSfx('audio/sfx_door_english_open.mp3')
        self.closeSfx = base.loader.loadSfx('audio/sfx_door_shanty_slam.mp3')
        self.openDoorIval.append(Func(base.playSfx, self.openSfx, node = self.soundNode, volume = 0.7, cutoff = 100))

    def getOtherSideParentModel(self):
        pass
    
    def setupOtherSideDoors(self):
        otherParent = self.getOtherSideParentModel()
        doorLeft = otherParent.find(self.doorLeftStr)
        doorRight = otherParent.find(self.doorRightStr)
        self.openOtherDoorIval = Parallel()
        self.closeOtherDoorIval = Parallel()
        if not doorLeft.isEmpty():
            self.openOtherDoorIval.append(LerpHprInterval(doorLeft, self.tOpen, Vec3(-90, 0, 0)))
            self.closeOtherDoorIval.append(LerpHprInterval(doorLeft, self.tOpen, Vec3(0, 0, 0)))
        
        if not doorRight.isEmpty():
            self.openOtherDoorIval.append(LerpHprInterval(doorRight, self.tOpen, Vec3(90, 0, 0)))
            self.closeOtherDoorIval.append(LerpHprInterval(doorRight, self.tOpen, Vec3(0, 0, 0)))
        
        if self.closeSfx is not None:
            self.closeOtherDoorIval.append(Sequence(Wait(0.25), Func(base.playSfx, self.closeSfx, node = self.soundNode, volume = 0.7, cutoff = 100)))

    def requestInteraction(self, avId, interactType = 0):
        if self.buildingUid == LocationIds.KINGSHEAD_DOOR and not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
            base.localAvatar.guiMgr.showNonPayer(quest = 'Restricted_Location', focus = 0)
            return
        
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)
        if avId == base.localAvatar.doId:
            self.fadeOut()

    def fadeOut(self):
        base.transitions.setFadeColor(0, 0, 0)
        
        def doFadeOut():
            if base.transitions.fadeOutActive():
                return
            
            base.transitions.fadeOut(self.tOpen)

        if localAvatar.gameFSM is None:
            return None
        
        si = Sequence(Func(localAvatar.gameFSM.request, 'DoorInteract', [
            self.hasDoors]), Func(doFadeOut), self.openDoorIval, self.closeDoorIval, Func(self.loadOtherSide))
        self.fadeOutTrack = si
        self.fadeOutTrack.start()

    def fadeIn(self):
        sf = Sequence(Func(localAvatar.gameFSM.request, 'DoorInteract'), Func(base.transitions.fadeIn, self.tOpen), self.openOtherDoorIval, self.closeOtherDoorIval, Func(localAvatar.gameFSM.request, 'LandRoam'))
        self.fadeInTrack = sf
        self.fadeInTrack.start()

    def setLocked(self, locked):
        self.setAllowInteract(not locked)
        self.locked = locked

    def showProximityStuff(self):
        DistributedInteractive.DistributedInteractive.showProximityStuff(self)
        base.cr.interactionMgr.useLifter(self.disk)

    def turnOn(self):
        pass

    def turnOff(self):
        pass


