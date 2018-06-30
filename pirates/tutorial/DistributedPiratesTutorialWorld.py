import time

from direct.actor import Actor
from direct.fsm import FSM
from direct.showbase.PythonUtil import report
from direct.task import Task
from panda3d.core import *
from pirates.cutscene import CutsceneData
from pirates.instance import DistributedInstanceBase
from pirates.makeapirate import MakeAPirate
from pirates.npc import Skeleton
from pirates.pirate import HumanDNA, Pirate
from pirates.piratesbase import PiratesGlobals, TimeOfDayManager
from pirates.quest import QuestParser


class DistributedPiratesTutorialWorld(
        DistributedInstanceBase.DistributedInstanceBase):
    notify = directNotify.newCategory('DistributedPiratesTutorialWorld')

    def __init__(self, cr):
        DistributedInstanceBase.DistributedInstanceBase.__init__(self, cr)
        self.tutorialHandler = None
        self.tutorialHandlerId = 0

    def setTutorialHandlerId(self, doId):
        self.tutorialHandlerId = doId

        def tutorialHandlerExists(tutorialHandler):
            self.tutorialHandler = tutorialHandler
            self.tutorialHandler.setInstance(self)

        self.cr.relatedObjectMgr.requestObjects(
            [self.tutorialHandlerId], eachCallback=tutorialHandlerExists)

    @report(types=['frameCount', 'args'], dConfigParam='want-connector-report')
    def addWorldInterest(self, area=None):
        DistributedInstanceBase.DistributedInstanceBase.addWorldInterest(
            self, area)
        if area:
            area.turnOn(localAvatar)

    @report(types=['frameCount', 'args'], dConfigParam='want-connector-report')
    def removeWorldInterest(self, area=None):
        if not (area and area.gridVisContext):
            area = None
        DistributedInstanceBase.DistributedInstanceBase.removeWorldInterest(
            self, area)

    @report(types=['frameCount', 'args'], dConfigParam='want-connector-report')
    def turnOff(self, cacheIslands=[]):
        self._turnOffIslands(cacheIslands)
        DistributedInstanceBase.DistributedInstanceBase.turnOff(
            self, cacheIslands)

    @report(types=['frameCount', 'args'], dConfigParam='want-connector-report')
    def turnOn(self, av=None):
        DistributedInstanceBase.DistributedInstanceBase.turnOn(self, av)
        self._turnOnIslands()
