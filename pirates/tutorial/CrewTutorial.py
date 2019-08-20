import time
import random
from pandac.PandaModules import *
from direct.showbase import DirectObject
from pirates.piratesbase import PiratesGlobals
from pirates.tutorial import TutorialGlobals
from pirates.piratesgui import NewTutorialPanel

class CrewTutorial(DirectObject.DirectObject):
    notify = directNotify.newCategory('CrewTutorial')
    
    def __init__(self):
        self.stage = 0
        self.panel1 = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        self.contentPart1 = 'crew_tut1'
        self.contentPart2 = 'crew_tut2'
        self.contentPart3 = 'crew_tut3'
        self.contentPart4 = 'crew_tut4'
        self.showPart1()
    
    def __handleOKButton1(self):
        messenger.send('closeTutorialWindow')
        self.showPart2()
    
    def __handleOKButton2(self):
        messenger.send('closeTutorialWindow')
        self.showPart3()

    def __handleOKButton3(self):
        messenger.send('closeTutorialWindow')
        self.showPart4()
    
    def __handleOKButton4(self):
        self.panelCleanup()
        self.ignoreAll()
        self.destroy()
    
    def showPart1(self):
        if self.stage != 0:
            return
        
        self.panel1 = NewTutorialPanel.NewTutorialPanel([self.contentPart1, 'test1'])
        self.panel1.activate()
        self.panel1.setYesCommand(self.__handleOKButton1)
        self.updateTutorialState()
        self.stage = 1
    
    def showPart2(self):
        if self.stage != 1:
            return
        
        self.panel2 = NewTutorialPanel.NewTutorialPanel([self.contentPart2, 'test2'])
        self.panel2.activate()
        self.panel2.setYesCommand(self.__handleOKButton2)
        self.stage = 2
    
    def showPart3(self):
        if self.stage != 2:
            return
        
        self.panel3 = NewTutorialPanel.NewTutorialPanel([self.contentPart3, 'test3'])
        self.panel3.activate()
        self.panel3.setYesCommand(self.__handleOKButton3)
        self.stage = 3
    
    def showPart4(self):
        if self.stage != 3:
            return
        
        self.panel4 = NewTutorialPanel.NewTutorialPanel([self.contentPart4, 'test4'])
        self.panel4.activate()
        self.panel4.setYesCommand(self.__handleOKButton4)
        self.stage = 4
    
    def updateTutorialState(self):
        base.localAvatar.b_setTutorial(PiratesGlobals.TUT_INTRODUCTION_TO_FRIENDS)

    def panelCleanup(self):
        messenger.send('closeTutorialWindowAll')
    
    def destroy(self):
        del self.stage
        del self.panel1
        del self.panel2
        del self.panel3
        del self.panel4
        del self.contentPart1
        del self.contentPart2
        del self.contentPart3
        del self.contentPart4
    
    def doNothing(self):
        pass

