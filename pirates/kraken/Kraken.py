from pandac.PandaModules import *
from direct.distributed.DistributedNode import DistributedNode
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pirates.kraken.DoomTentacle import DoomTentacle
from pirates.ship import ShipGlobals
import math
import time
import random

class Kraken(DistributedNode):
    
    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        NodePath.__init__(self, 'Kraken')
        self.grabberTentacles = {}
        self.holderTentacles = set()
        self.doomTentacle = None
        self.bodyId = None
        self.shipId = None
        self.shipRomRequest = None
        self.dampen = [
            0,
            0]
        self.rTask = None
        self.sinkCutsceneIval = None
        self.sinkShipIval = None
        self.sinkEffectsNode = None

    def disable(self):
        self.grabberTentacles = {}
        self.holderTentacles = {}
        if self.doomTentacle:
            self.doomTentacle.disable()
            self.doomTentacle = None
        
        self.body = None
        self.stopRangeTask()
        if self.shipRomRequest:
            self.cr.relatedObjectMgr.abortRequest(self.shipRomRequest)
            self.shipRomRequest = None
        
        if self.sinkCutsceneIval:
            self.sinkCutsceneIval.finish()
            self.sinkCutsceneIval = None
        
        if self.sinkShipIval:
            self.sinkShipIval.finish()
            self.sinkShipIval = None
        
        ship = self.getShip()
        if ship:
            ship.setKraken(None)
        
        DistributedNode.disable(self)
    
    def setShipId(self, shipId):
        self.shipId = shipId
        if self.shipRomRequest:
            self.cr.relatedObjectMgr.abortRequest(self.shipRomRequest)
            self.shipRomRequest = None
        
        def shipArrived(ship):
            self.shipRomRequest = None
            ship.setKraken(self)
            for grabber in self.grabberTentacles:
                grabber.attachToShipLocator()
                grabber.setupCollisions()
            

        self.shipRomRequest = self.cr.relatedObjectMgr.requestObjects((shipId,), eachCallback = shipArrived)
    
    def getShipId(self):
        return self.shipId
    
    def getShip(self):
        return self.cr.doId2do.get(self.shipId)

    def addGrabberTentacle(self, locId, grabber):
        self.grabberTentacles[locId] = grabber
        ship = self.getShip()
        if ship:
            startPos = grabber.getRandomPos()
            grabber.attachToShipLocator(pos = startPos)
            grabber.setupCollisions()

    def removeGrabberTentacle(self, grabber):
        self.grabberTentacles.discard(grabber)
    
    def getRollAngle(self):
        dampen = max([ grabber.getRockingDampen() for grabber in self.grabberTentacles.itervalues() ])
        if dampen:
            frameTime = globalClock.getFrameTime()
            self.dampen[1] = frameTime
        elif self.dampen[0]:
            frameTime = globalClock.getFrameTime()
            dt = globalClock.getFrameTime() - self.dampen[1]
            self.dampen[1] = frameTime
            dampen = max(0, self.dampen[0] - dt * 0.333)
        
        self.dampen[0] = dampen
        period = 5
        return 0

    def getDampenAmount(self):
        return self.dampen[0]

    def startRangeTask(self):
        self.rTask = taskMgr.add(self.rangeTask, self.uniqueName('rangeTask'))

    def stopRangeTask(self):
        if self.rTask:
            taskMgr.remove(self.rTask)
            self.rTask = None
    
    def rangeTask(self, task):
        t = task.time
        t = task.frame
        t /= 15
        t %= len(self.grabberTentacles)
        t = int(t)
        for grabber in self.grabberTentacles.itervalues():
            grabber.rangeCollisions.hide()
        
        self.grabberTentacles[t].rangeCollisions.show()
        return task.cont
    
    def spawnDoomTentacle(self):
        if not self.doomTentacle:
            self.doomTentacle = DoomTentacle(self.uniqueName)
            self.doomTentacle.reparentTo(self)
            self.doomTentacle.setScale(self.getShip().dimensions[1] / 400)
            self.doomTentacle.setEffectsScale(self.getShip().dimensions[1] / 100)
            self.doomTentacle.setPos(self.getShip(), -self.getShip().dimensions[0] / 1.3, -1 * ShipGlobals.getShipSplitOffset(self.getShip().shipClass) + 2, -15)
            self.doomTentacle.setHpr(self.getShip(), 90, 0, 0)
        
        self.doomTentacle.setPlayRate(1.2, 'emerge')
        self.doomTentacle.play('emerge')
    
    def hideSideTentacles(self, side):
        numTent = len(self.grabberTentacles) / 2
        for i in range(numTent):
            self.grabberTentacles[i + numTent * side].emerge(0)
        


