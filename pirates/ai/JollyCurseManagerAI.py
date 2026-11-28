from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject

from pirates.piratesbase import PiratesGlobals, TODGlobals

# LocalPirate.setCurseStatus values, see NewsManager.messages...
CURSE_STATUS_JAIL = 0
CURSE_STATUS_OUTDOORS = 1
CURSE_STATUS_INDOORS = 2


class JollyCurseManagerAI(DirectObject):
    """
    Jolly Roger's Curse: while the time of day is running the jolly curse cycle
    every pirate that is outdoors on land when the moon becomes full is turned
    Undead. Pirates indoors or in jail are safe from the curse. Cursed pirates
    who are defeated (and so are thrown in jail) are restored, and everyone
    else is restored once the moon starts to wane or the cycle ends.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('JollyCurseManagerAI')

    def __init__(self, air):
        DirectObject.__init__(self)
        self.air = air
        self.curseActive = False

        # the avatars this full moon has cursed Undead...
        self.cursedAvatars = set()

    def start(self):
        timeOfDayMgr = self.air.timeOfDayMgr
        timeOfDayMgr.addTimeOfDayStateMethod(PiratesGlobals.TOD_FULLMOON, 'JollyCurse-Curse', self.processTimeChange)
        timeOfDayMgr.addTimeOfDayStateMethod(PiratesGlobals.TOD_HALF2FULLMOON, 'JollyCurse-Lift-Half2Full', self.processTimeChange)
        timeOfDayMgr.addTimeOfDayStateMethod(PiratesGlobals.TOD_FULL2HALFMOON, 'JollyCurse-Lift-Full2Half', self.processTimeChange)

        # the curse is broken when the holiday stops and the time of day
        # switches back to another cycle in the middle of the full moon...
        self.accept('timeOfDayCycleChanged', self.processCycleChange)

    def stop(self):
        self.ignoreAll()
        self.liftCurse()

    def isCurseActive(self):
        return self.curseActive

    def isAvatarCursed(self, avatarId):
        return avatarId in self.cursedAvatars

    def processTimeChange(self, cycleType, todState, stateTime):
        if cycleType == TODGlobals.TOD_JOLLYCURSE_CYCLE and todState == PiratesGlobals.TOD_FULLMOON:
            self.castCurse()
        else:
            self.liftCurse()

    def processCycleChange(self, cycleType):
        if cycleType != TODGlobals.TOD_JOLLYCURSE_CYCLE:
            self.liftCurse()

    def getPlayerAvatars(self):
        from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI

        return [obj for obj in list(self.air.doId2do.values()) if isinstance(obj, DistributedPlayerPirateAI)]

    def getAvatarLocationStatus(self, avatar):
        """
        Returns the curse status for the avatar's current location, or None
        when the avatar is somewhere the curse never reaches (at sea, aboard a
        ship or in an instance outside of the main world)
        """

        from pirates.world.DistributedIslandAI import DistributedIslandAI
        from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
        from pirates.world.DistributedJailInteriorAI import DistributedJailInteriorAI

        parentObj = avatar.getParentObj()
        if isinstance(parentObj, DistributedJailInteriorAI) or avatar.testTeleportFlag(PiratesGlobals.TFInJail):
            return CURSE_STATUS_JAIL

        if isinstance(parentObj, DistributedGAInteriorAI):
            return CURSE_STATUS_INDOORS

        if isinstance(parentObj, DistributedIslandAI):
            world = avatar.getWorld()
            if world and world.getType() == PiratesGlobals.INSTANCE_MAIN:
                return CURSE_STATUS_OUTDOORS

        return None

    def castCurse(self):
        if self.curseActive:
            return

        self.notify.info('The moon is full, casting Jolly Roger\'s Curse!')
        self.curseActive = True
        for avatar in self.getPlayerAvatars():
            self.curseAvatar(avatar)

    def curseAvatar(self, avatar):
        status = self.getAvatarLocationStatus(avatar)
        if status is None:
            return

        if status == CURSE_STATUS_OUTDOORS:
            # pirates that have been defeated are on their way to jail,
            # they've escaped the curse...
            if avatar.getHp()[0] <= 0:
                return

            self.cursedAvatars.add(avatar.doId)
            if not avatar.getZombie():
                avatar.b_setZombie(1, 1)

        avatar.d_setCurseStatus(status)

    def liftCurse(self):
        if not self.curseActive and not self.cursedAvatars:
            return

        if self.curseActive:
            self.notify.info('The moon is waning, Jolly Roger\'s Curse is broken!')

        self.curseActive = False
        cursedAvatars, self.cursedAvatars = self.cursedAvatars, set()
        for avatarId in cursedAvatars:
            avatar = self.air.doId2do.get(avatarId)
            if avatar:
                self.restoreAvatar(avatar)

    def restoreAvatar(self, avatar):
        self.cursedAvatars.discard(avatar.doId)

        # zombies made by the zombie magic word stay zombies...
        if avatar.getZombie() and not avatar.forcedZombie:
            avatar.b_setZombie(0, 0)

    def avatarChangedLocation(self, avatar, parentObj):
        # cursed pirates that are defeated are restored once they have been
        # thrown in jail, so they can go save the town from the other Undead...
        from pirates.world.DistributedJailInteriorAI import DistributedJailInteriorAI

        if avatar.doId not in self.cursedAvatars:
            return

        if isinstance(parentObj, DistributedJailInteriorAI):
            self.restoreAvatar(avatar)
            avatar.d_setCurseStatus(CURSE_STATUS_JAIL)

    def avatarLeft(self, avatar):
        self.cursedAvatars.discard(avatar.doId)
