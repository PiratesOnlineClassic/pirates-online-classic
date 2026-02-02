from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from pirates.tutorial import TutorialGlobals


class DistributedPiratesTutorialAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPiratesTutorialAI')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedPiratesTutorialAI')

        self.avatarId = None
        self.exteriorDoor = None
        self.interiorDoor = None
        self.interior = None  # Set by TutorialFSM for interior teleport

    def setAvatarId(self, avatarId):
        """Set the avatar this tutorial handler is for"""
        self.avatarId = avatarId

    def getAvatar(self):
        """Get the avatar object"""
        if self.avatarId:
            return self.air.doId2do.get(self.avatarId)
        return None

    # --------------------------------------------------
    # Client -> AI messages (airecv clsend)
    # --------------------------------------------------

    def clientEnterAct0Tutorial(self):
        """Client has entered Act0Tutorial state - client is ready for interior teleport"""
        avatar = self.getAvatar()
        if not avatar:
            self.notify.warning('clientEnterAct0Tutorial: No avatar found')
            return

        self.notify.info('Avatar %d entered Act0Tutorial, triggering interior teleport' % self.avatarId)
        
        # Teleport the player into the jail interior now that the client is ready
        if self.interior:
            self.teleportToJailInterior(self.interior)
        
        self.request('Act0Tutorial')

    def makeAPirateComplete(self):
        """Client finished the Make-A-Pirate customization"""
        avatar = self.getAvatar()
        if not avatar:
            self.notify.warning('makeAPirateComplete: No avatar found')
            return

        self.notify.info('Avatar %d completed Make-A-Pirate' % self.avatarId)

        # complete the quest
        self.air.questMgr.completeQuest(avatar, self.quest)
        self.d_makeAPirateCompleteResp()

    def autoVisit(self, npcDoId):
        """Client triggered an auto-visit with an NPC"""
        avatar = self.getAvatar()
        if not avatar:
            return

        self.notify.info('Avatar %d auto-visiting NPC %d' % (self.avatarId, npcDoId))
        # Could trigger NPC interaction here

    def tutorialSeachestFinished(self):
        """Client finished the seachest tutorial"""
        avatar = self.getAvatar()
        if not avatar:
            return

        self.notify.info('Avatar %d finished seachest tutorial' % self.avatarId)

    def boardedTutorialShip(self):
        """Client boarded the tutorial ship (Stumpy's boat)"""
        avatar = self.getAvatar()
        if not avatar:
            return

        self.notify.info('Avatar %d boarded tutorial ship' % self.avatarId)
        self.request('BoardedShip')

    def startSailingStumpy(self):
        """Client started sailing with Stumpy"""
        avatar = self.getAvatar()
        if not avatar:
            return

        self.notify.info('Avatar %d started sailing with Stumpy' % self.avatarId)
        self.request('Sailing')

    def targetPracticeDone(self):
        """Client finished target practice with the cannon"""
        avatar = self.getAvatar()
        if not avatar:
            return

        self.notify.info('Avatar %d finished target practice' % self.avatarId)
        self.request('TargetPracticeDone')

    def giveInitQuest(self, questType):
        """Client requests initial quest"""
        avatar = self.getAvatar()
        if not avatar:
            return

        self.notify.info('Avatar %d requesting quest type %d' % (self.avatarId, questType))

    # --------------------------------------------------
    # AI -> Client messages (broadcast ram)
    # --------------------------------------------------

    def d_makeAPirateCompleteResp(self):
        """Tell client that Make-A-Pirate is complete"""
        self.sendUpdate('makeAPirateCompleteResp', [])

    def d_inventoryFailed(self):
        """Tell client that inventory creation failed"""
        self.sendUpdate('inventoryFailed', [])

    # --------------------------------------------------
    # FSM States
    # --------------------------------------------------

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterAct0Tutorial(self):
        """Player is in the jail, starting the tutorial"""
        self.notify.info('Entering Act0Tutorial state')

        # Find and open the jail doors so player can exit
        self._setupJailDoors()

    def exitAct0Tutorial(self):
        pass

    def _setupJailDoors(self):
        """Find the jail doors by UID, unlock them, and teleport avatar into the jail interior"""
        # Look up the exterior door doId from uidMgr
        doorDoId = self.air.uidMgr.getDoId(TutorialGlobals.JAIL_EXTERIOR_DOOR)
        if doorDoId:
            self.exteriorDoor = self.air.doId2do.get(doorDoId)
            if self.exteriorDoor:
                self.notify.info('Found jail exterior door: %s' % self.exteriorDoor)
                # Unlock the exterior door so player can exit later
                if hasattr(self.exteriorDoor, 'locked'):
                    self.exteriorDoor.locked = 0

        # Also look up and unlock the interior door
        interiorDoorDoId = self.air.uidMgr.getDoId(TutorialGlobals.JAIL_INTERIOR_DOOR)
        if interiorDoorDoId:
            self.interiorDoor = self.air.doId2do.get(interiorDoorDoId)
            if self.interiorDoor and hasattr(self.interiorDoor, 'locked'):
                self.interiorDoor.locked = 0
                self.notify.info('Unlocked interior door for avatar %d' % self.avatarId)

        # Teleport the avatar into the jail interior
        self._teleportToJailInterior()

    def _teleportToJailInterior(self):
        """Teleport the avatar into the jail interior using the door's method"""
        avatar = self.getAvatar()
        if not avatar:
            self.notify.warning('Cannot teleport to jail - no avatar found')
            return

        # Get the jail interior
        interiorDoId = self.air.uidMgr.getDoId(TutorialGlobals.JAIL_INTERIOR)
        if not interiorDoId:
            self.notify.warning('Cannot find jail interior UID: %s' % TutorialGlobals.JAIL_INTERIOR)
            return

        interior = self.air.doId2do.get(interiorDoId)
        if not interior:
            self.notify.warning('Cannot find jail interior object: %d' % interiorDoId)
            return

        self.notify.info('Found jail interior: %s (parentId=%d, zoneId=%d, doId=%d)' % (
            interior, interior.parentId, interior.zoneId, interior.doId))

        # Use the exterior door to send the avatar into the interior
        if self.exteriorDoor and hasattr(self.exteriorDoor, 'd_setPrivateInteriorInstance'):
            self.exteriorDoor.d_setPrivateInteriorInstance(
                self.avatarId,
                interior.parentId,
                interior.zoneId,
                interior.doId,
                autoFadeIn=false
            )
            self.notify.info('Sent avatar %d into jail interior via door' % self.avatarId)
        else:
            # Fallback: Send the message directly to the avatar if door not available
            self.notify.warning('Exterior door not available, cannot teleport to interior')

    def enterBoardedShip(self):
        """Player boarded Stumpy's ship"""
        self.notify.info('Entering BoardedShip state')

    def exitBoardedShip(self):
        pass

    def enterSailing(self):
        """Player is sailing with Stumpy"""
        self.notify.info('Entering Sailing state')

    def exitSailing(self):
        pass

    def enterTargetPracticeDone(self):
        """Player finished cannon target practice"""
        self.notify.info('Entering TargetPracticeDone state')

    def exitTargetPracticeDone(self):
        pass

    def openExteriorDoor(self):
        """Open the jail exterior door so the player can enter"""
        # Look up the exterior door doId from uidMgr
        doorDoId = self.air.uidMgr.getDoId(TutorialGlobals.JAIL_EXTERIOR_DOOR)
        if not doorDoId:
            self.notify.warning('Could not find jail exterior door UID: %s' % TutorialGlobals.JAIL_EXTERIOR_DOOR)
            return

        self.exteriorDoor = self.air.doId2do.get(doorDoId)
        if not self.exteriorDoor:
            self.notify.warning('Could not find jail exterior door doId: %d' % doorDoId)
            return

        self.notify.info('Found jail exterior door: %s' % self.exteriorDoor)

        # Unlock the door
        if hasattr(self.exteriorDoor, 'locked'):
            self.exteriorDoor.locked = 0

        # Open the door for the avatar
        if self.avatarId and hasattr(self.exteriorDoor, 'request'):
            self.exteriorDoor.request('Opened', self.avatarId)
            self.notify.info('Opened exterior door for avatar %d' % self.avatarId)

    def teleportToJailInterior(self, interior):
        """Teleport the avatar into the jail interior by adding interest first"""
        if not interior:
            self.notify.warning('Cannot teleport to jail - no interior provided')
            return

        avatar = self.getAvatar()
        if not avatar:
            self.notify.warning('Cannot teleport to jail - no avatar found')
            return

        # Store interior for callback
        self._pendingInterior = interior

        # First find the exterior door and its parent (island)
        doorDoId = self.air.uidMgr.getDoId(TutorialGlobals.JAIL_EXTERIOR_DOOR)
        if doorDoId:
            self.exteriorDoor = self.air.doId2do.get(doorDoId)
            if self.exteriorDoor and hasattr(self.exteriorDoor, 'locked'):
                self.exteriorDoor.locked = 0

        if not self.exteriorDoor:
            self.notify.warning('Cannot find exterior door for interior teleport')
            return

        # Get the door's parent (island) to add interest
        doorParent = self.exteriorDoor.getParentObj()
        if not doorParent:
            self.notify.warning('Cannot find exterior door parent')
            return

        # Get the zone where the door is located
        doorZoneId = self.exteriorDoor.zoneId

        self.notify.info('Adding interest to door zone %d on parent %s for avatar %d' % (
            doorZoneId, doorParent, self.avatarId))

        # Use WorldGridManagerAI to add interest to the door's zone
        # When interest is added, the callback will trigger the interior teleport
        self.air.worldGridManager.handleLocationChanged(
            doorParent, avatar, doorZoneId, 
            callback=self._onDoorInterestComplete
        )

    def _onDoorInterestComplete(self):
        """Called when interest to the door zone has been set up"""
        self.notify.info('Door interest complete for avatar %d, sending to interior' % self.avatarId)

        interior = getattr(self, '_pendingInterior', None)
        if not interior:
            self.notify.warning('No pending interior for teleport')
            return

        self.notify.info('Teleporting avatar %d to jail interior: %s (parentId=%d, zoneId=%d, doId=%d)' % (
            self.avatarId, interior, interior.parentId, interior.zoneId, interior.doId))

        # Use the exterior door to send the avatar into the interior
        if self.exteriorDoor and hasattr(self.exteriorDoor, 'd_setPrivateInteriorInstance'):
            self.exteriorDoor.d_setPrivateInteriorInstance(
                self.avatarId,
                interior.parentId,
                interior.zoneId,
                interior.doId,
                autoFadeIn=True
            )
            self.notify.info('Sent avatar %d into jail interior via door' % self.avatarId)
            
            # Schedule the Jack Sparrow cutscene to play after player arrives in interior
            from direct.task.TaskManagerGlobal import taskMgr
            taskMgr.doMethodLater(1.5, self._startJackSparrowCutscene, 
                                  'startJackSparrowCutscene-%d' % self.avatarId)
        else:
            self.notify.warning('Exterior door not available for teleport to interior')

        self._pendingInterior = None

    def _startJackSparrowCutscene(self, task=None):
        """Create the first quest and trigger the Jack Sparrow cutscene"""
        avatar = self.getAvatar()
        if not avatar:
            self.notify.warning('Cannot start cutscene - no avatar found')
            return

        self.notify.info('Starting Jack Sparrow cutscene for avatar %d' % self.avatarId)

        # Create the first tutorial quest (Chapter1.rung1)
        # The quest has no tasks, just finalizeInfo with the cutscenes
        def _questCreated(quest=None):
            if not quest:
                self.notify.warning('Failed to create first quest for avatar %d' % self.avatarId)
                return

            self.notify.info('First quest created for avatar %d, triggering cutscene' % self.avatarId)
            
            # Trigger the finalize cutscene (Jack Sparrow jail break)
            # The quest has 2 cutscene stages: 1.1.1 and 1.1.2
            # No NPC giver for this quest (player is alone in jail cell)
            self.quest = quest
            self.air.questMgr.finalizeCutscene(avatar, quest, finalizeIndex=0, npc=None)

        self.air.questMgr.createQuest(avatar, TutorialGlobals.FIRST_QUEST, callback=_questCreated)

