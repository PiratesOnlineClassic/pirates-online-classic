import string

from direct.showbase.ShowBaseGlobal import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.distributed.ClockDelta import *
from direct.showbase import PythonUtil
from otp.avatar import Avatar
from otp.chat import ChatManager
from otp.otpbase import OTPGlobals
from otp.ai import MagicWordManager
from otp.ai.MagicWordGlobal import *

from pirates.pirate import DistributedPlayerPirate
from direct.distributed import DistributedCartesianGrid
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.RadarUtil import RadarUtil
from pirates.cutscene import Cutscene, CutsceneData
from pirates.effects.Fireflies import Fireflies
from pirates.effects.GroundFog import GroundFog
from pirates.effects.Bonfire import Bonfire
from pirates.effects.CeilingDust import CeilingDust
from pirates.effects.CeilingDebris import CeilingDebris
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.DarkWaterFog import DarkWaterFog
from pirates.ship.ShipModel import ShipModel
from pirates.effects.FireworkGlobals import *
from pirates.effects.FireworkShowManager import FireworkShowManager
from pirates.piratesbase import PLocalizer

class PiratesMagicWordManager(MagicWordManager.MagicWordManager):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesMagicWordManager')
    neverDisable = 1
    GameAvatarClass = DistributedPlayerPirate.DistributedPlayerPirate

    def __init__(self, cr):
        MagicWordManager.MagicWordManager.__init__(self, cr)
        self.pendingCameraReparent = None
        self.originalLocation = None
        self.groundFog = None
        self.fireflies = None
        self.crewTutorial = None

    def generate(self):
        MagicWordManager.MagicWordManager.generate(self)
        self.accept('requestServerTime', self.d_requestServerTime)

    def disable(self):
        self.ignore('requestServerTime')
        MagicWordManager.MagicWordManager.disable(self)
        if self.pendingCameraReparent:
            base.cr.relatedObjectMgr.abortRequest(self.pendingCameraReparent)
            self.pendingCameraReparent = None

    def cameraFollowTgt(self, target, parentId):
        targetObj = base.cr.doId2do[target.getDoId()]
        localAvatar.cTrav.removeCollider(localAvatar.cFloorNodePath)
        localAvatar.controlManager.use('observer', localAvatar)
        localAvatar.controlManager.currentControls.disableAvatarControls()
        localAvatar.reparentTo(targetObj)
        localAvatar.setScale(1)
        parentObj = base.cr.doId2do[parentId]
        parentObj.visAvatar = targetObj
        localAvatar.setPos(0, 0, 0)
        localAvatar.setHpr(render, targetObj.getHpr(render))
        localAvatar.stash()

    def cameraReparent(self, targetId, targetParentId, zoneId):
        if self.originalLocation == None:
            self.originalLocation = [
                localAvatar.getLocation(),
                localAvatar.getPos()]

        if targetParentId not in base.cr.doId2do:
            self.notify.debug('Parent of target object to reparent avatar/camera to does not yet exist, skipping reparent request')
            return None

        if isinstance(base.cr.doId2do[targetParentId], DistributedCartesianGrid.DistributedCartesianGrid):
            base.cr.doId2do[targetParentId].visAvatar = localAvatar

        localAvatar.b_setLocation(targetParentId, zoneId, teleport = 1)
        if targetId in base.cr.doId2do:
            self.cameraFollowTgt(base.cr.doId2do[targetId], targetParentId)
        else:
            self.pendingCameraReparent = base.cr.relatedObjectMgr.requestObjects([
                targetId], eachCallback = lambda param = None, param2 = targetParentId: self.cameraFollowTgt(param, param2))
        localAvatar.stash()

    def d_requestServerTime(self):
        self.sendUpdate('requestServerTime', [])

    def recvServerTime(self, sinceEpoch):
        base.chatAssistant.receiveGameMessage(PLocalizer.getServerTimeString(sinceEpoch))

    def sendMagicWordResponse(self, response):
        MagicWordManager.MagicWordManager.sendMagicWordResponse(self, response)
        base.chatAssistant.receiveGameMessage('Spellbook: %s' % response)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def walk():
    """
    Sets the local avatar's state to LandRoam
    """

    localAvatar.b_setGameState('LandRoam')
    localAvatar.motionFSM.on()

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def topten():
    """
    Requests the top ten leaderboard for guilds
    """

    base.cr.guildManager.requestLeaderboardTopTen()

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def pilot():
    """
    """

    ships = base.cr.doFindAll('ship-')
    from pirates.ship.DistributedShip import DistributedShip
    ships = [ship for ship in ships if isinstance(ship, DistributedShip)]
    print(ships)
    closestShip = ships[0]
    closestDist = Vec3(closestShip.getPos(localAvatar)).lengthSquared()
    print(closestShip, closestDist)
    for ship in ships[1:]:
        dist = Vec3(ship.getPos(localAvatar)).lengthSquared()
        print(ship, dist)
        if dist < closestDist:
            closestShip = ship
            closestDist = dist

    wheel = closestShip.find('**/wheel')
    localAvatar.setPos(wheel, 0, 0, 0)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def bonfire():
    """
    Spawns a bonefire particle effect where the player is standing
    """

    bf = Bonfire()
    bf.reparentTo(render)
    bf.setPos(localAvatar, 0, 0, 0)
    bf.startLoop()

    message = 'bonfire at %s, %s' % (localAvatar.getPos(), localAvatar.getHpr())
    print(message)
    return message

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def mario():
    """
    Toggles the local client's Mario mode
    """

    localAvatar.toggleMario()
    return 'Mario toggled'

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def islandShips(state):
    if state:
        localAvatar.getParentObj().setOceanVisEnabled(1)
        localAvatar.getParentObj().setFlatShips(0)
    else:
        localAvatar.getParentObj().setOceanVisEnabled(0)

    return 'Island ship visibility set to: %d' % state

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def swamp():
    """
    Toggles swamp particle effects
    """

    magicMgr = spellbook.getManager()
    if magicMgr.fireflies:
        magicMgr.fireflies.destroy()
        magicMgr.fireflies = None
        magicMgr.groundFog.destroy()
        magicMgr.groundFog = None
    else:
        magicMgr.fireflies = Fireflies()
        if magicMgr.fireflies:
            magicMgr.fireflies.reparentTo(localAvatar)
            magicMgr.fireflies.startLoop()

        magicMgr.groundFog = GroundFog()
        if magicMgr.groundFog:
            magicMgr.groundFog.reparentTo(localAvatar)
            magicMgr.groundFog.startLoop()

    return 'Swamp effects toggled'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def darkfog():
    """
    Toggles the dark fog particle effects
    """

    magicMgr = spellbook.getManager()
    if magicMgr.groundFog:
        magicMgr.groundFog.destroy()
        magicMgr.groundFog = None
    else:
        magicMgr.groundFog = DarkWaterFog()
        if magicMgr.groundFog:
            magicMgr.groundFog.reparentTo(localAvatar)
            magicMgr.groundFog.startLoop()

    return 'Darkfog effects toggled'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def dust():
    """
    Spawns dust particles at the players location
    """

    effect = CeilingDust.getEffect()
    if effect:
        effect.reparentTo(localAvatar)
        effect.setPos(0, 0, 10)
        effect.play()

    effect = CeilingDebris.getEffect()
    if effect:
        effect.reparentTo(localAvatar)
        effect.setPos(0, 0, 20)
        effect.play()

    cameraShakerEffect = CameraShaker()
    cameraShakerEffect.reparentTo(localAvatar)
    cameraShakerEffect.setPos(0, 0, 0)
    cameraShakerEffect.shakeSpeed = 0.05
    cameraShakerEffect.shakePower = 4.5
    cameraShakerEffect.numShakes = 2
    cameraShakerEffect.scalePower = 1
    cameraShakerEffect.play(80.0)

    return 'Boom!'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def turbo():
    """
    Toggles the local avatar's turbo mode
    """

    localAvatar.toggleTurbo()

    return 'Turbo toggled'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def joincrew():
    """
    Requests a new crew with the crew manager
    """

    base.cr.crewManager.requestNewCrew()
    return 'New crew requested'

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def fireworks(showType=FireworkShowType.FourthOfJuly):
    """
    Locally enables or disables Fourth of July fireworks
    """

    timestamp = globalClockDelta.localElapsedTime(base.cr.timeOfDayManager.startingTime, bits=32)
    if base.cr.activeWorld:
        if not base.cr.activeWorld.fireworkShowMgr:
            base.cr.activeWorld.enableFireworkShow(timestamp, showType)
        else:
            base.cr.activeWorld.disableFireworkShow()

    return "Toggled fireworks show with type: %d" % showType

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def te():
    """
    Sets the local avatar's teleport out state
    """

    if localAvatar.gameFSM.getCurrentOrNextState() == 'LandRoam':
        localAvatar.b_setGameState('TeleportOut')
    elif localAvatar.gameFSM.getCurrentOrNextState() == 'TeleportOut':
        localAvatar.b_setGameState('LandRoam')

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, int, int])
def shipModel(shipClass, team, wantCollisions):
    """
    Spawns a ship model at the players location
    """

    sm = ShipModel(base.cr, shipClass, team, wantCollisions)
    sm.reparentTo(localAvatar)
    sm.setY(100)
    sm.setH(90)
    sm.wrtReparentTo(render)

    return 'ShipModel (%s) spawned' % shipClass

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def deployShip(shipIndex):
    """
    Deploys the users requested ship index
    """

    if not localAvatar.getInventory():
        return

    if not localAvatar.getInventory().getShipDoIdList():
        return

    if localAvatar.getActiveShipId():
        shipId = localAvatar.getActiveShipId()
        localAvatar.d_requestReturnShip(shipId)
    else:
        shipId = localAvatar.getInventory().getShipDoIdList()[shipIndex]
        localAvatar.d_requestDeployShip(shipId)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def lfa(activityName):
    """
    Requests the avatars current activity
    """

    if activityName == 'blackjack':
        localAvatar.requestActivity(PiratesGlobals.GAME_STYLE_BLACKJACK)
    elif activityName == 'poker':
        localAvatar.requestActivity(PiratesGlobals.GAME_STYLE_POKER)
    elif activityName == 'pvp':
        localAvatar.requestActivity(PiratesGlobals.GAME_TYPE_PVP)
    elif activityName == 'tm':
        localAvatar.requestActivity(PiratesGlobals.GAME_TYPE_TM)
    elif activityName == 'hsa':
        localAvatar.requestActivity(PiratesGlobals.GAME_TYPE_HSA)
    elif activityName == 'mmp':
        base.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld')

@magicWord(name='term', category=CATEGORY_SYSTEM_ADMIN)
@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def terminator():
    """
    """

    localAvatar.setEquippedWeapons([
        10103,
        10106,
        10115])
    localAvatar.d_requestEquipWeapons([
        10103,
        10106,
        10115])

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def battleRandom(command):
    if command == 'resync':
        localAvatar.battleRandom.resync()
        message = 'Client Battle random resynced, counter=0'
    else:
        counter = localAvatar.battleRandom.counter
        message = 'Client Battle random counter=%s' % counter

    spellbook.getManager().notify.info(message)
    return message

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def cutscene(csId):
    """
    Plays the requested cutscene id
    """

    if csId >= len(CutsceneData.CutsceneNames):
        return

    name = CutsceneData.CutsceneNames[csId]
    cs = PythonUtil.ScratchPad()

    def destroyCutscene(cs = cs):
        cs.cutscene.destroy()

    c = Cutscene.Cutscene(base.cr, name, PythonUtil.DelayedFunctor(destroyCutscene, '~cutscene-destroy'))
    cs.cutscene = c
    c.play()
    destroyCutscene = None

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def forceLod():
    """
    Forces all LOD states to the highest
    """

    for n in render.findAllMatches('**/+LODNode'):
        n.node().forceSwitch(n.node().getHighestSwitch())

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[float, float, float, float])
def setwave(num, amplitude, wavelength, speed):
    """
    Sets the requested SeaPatch wave settings
    """

    patch.enableWave(num)
    patch.setWaveTarget(num, SeaPatchRoot.WTZ)
    patch.setWaveFunc(num, SeaPatchRoot.WFSin)
    patch.setChoppyK(num, 0)
    patch.setWaveAmplitude(num, amplitude)
    patch.setWaveLength(num, wavelength)
    patch.setWaveSpeed(num, speed)
    return 'wave %s modified' % num

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def wave():
    """
    Retrieves current SeaPatch wave settings
    """

    response = '~wave num amplitude wavelength speed'
    numWaves = patch.getNumWaves()
    num = 0
    while numWaves > 0:
        if patch.isWaveEnabled(num):
            numWaves -= 1
            if patch.getWaveTarget(num) != SeaPatchRoot.WTZ or patch.getWaveFunc(num) != SeaPatchRoot.WFSin:
                response = '%s\n%s NON-SINE-WAVE' % (response, num)
            else:
                response = '%s\n%s amp=%s len=%s spd=%s' % (response, num, patch.getWaveAmplitude(num), patch.getWaveLength(num), patch.getWaveSpeed(num))

        num += 1

    return response

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[float, float])
def roll(mass, roll):
    """
    Sets a ships fake mass and adds a roll value
    """

    if localAvatar.ship is None:
        response = 'not on a ship'
    else:
        localAvatar.ship._rocker.setFakeMass(mass)
        localAvatar.ship.addRoll(roll)
        response = 'rolling!'

    return response

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def ru():
    """
    Toggles the local radar utility
    """

    if hasattr(spellbook.getManager(), 'radarUtil') and spellbook.getManager().radarUtil and not spellbook.getManager().radarUtil.isDestroyed():
        spellbook.getManager().radarUtil.destroy()
    else:
        spellbook.getManager().radarUtil = RadarUtil()

@magicWord(name='pvpinfamy', category=CATEGORY_SYSTEM_ADMIN)
@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def pvpmoney():
    """
    Shows the users pvp infamy details
    """

    if localAvatar.ship and localAvatar.ship.renownDisplay:
        taskMgr.doMethodLater(2.0, localAvatar.ship.renownDisplay.loadRank, 'pvp-infamy-display', [])

    if localAvatar.guiMgr and localAvatar.guiMgr.pvpPanel and hasattr(localAvatar.guiMgr.pvpPanel, 'renownDisplay') and localAvatar.guiMgr.pvpPanel.renownDisplay:
        taskMgr.doMethodLater(2.0, localAvatar.guiMgr.pvpPanel.renownDisplay.loadRank, 'pvp-infamy-display', [])

    if localAvatar.guiMgr and localAvatar.guiMgr.titlesPage:
        taskMgr.doMethodLater(2.0, localAvatar.guiMgr.titlesPage.refresh, 'titles-refresh', [])

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def liveCam(camNum=-1):
    """
    GameMaster Utility for viewing points of interest around a game area
    """

    LiveCamTransforms = {'1': [Vec3(-385.776, -2369.64, 52.4644), Vec3(-18.0412, -3.24766, 0), 39.3076, 0],
                         '2': [Vec3(79.1195, -2521.26, 52.4644), Vec3(-18.0412, -3.24766, 0), 39.3076, 0],
                         '3': [Vec3(2858.35, 931.111, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1],
                         '4': [Vec3(3551.93, 532.437, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1],
                         '5': [Vec3(4245.52, 133.763, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1],
                         '6': [Vec3(4939.1, -264.911, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1]}
    lodNodes = render.findAllMatches('**/+LODNode')
    for i in range(0, lodNodes.getNumPaths()):
        lodNodes[i].node().forceSwitch(lodNodes[i].node().getHighestSwitch())

    localAvatar.clearInterestNamed(None, [
        'liveCam'])
    localAvatar.getParentObj().setOceanVisEnabled(0)

    if camNum > -1:
        camData = LiveCamTransforms[camNum]
        localAvatar.cameraFSM.request('Control')
        if camData[3]:
            camParent = render
        else:
            camParent = localAvatar.getParentObj()
        base.cam.reparentTo(camParent)
        base.cam.setPos(camData[0])
        base.cam.setHpr(camData[1])
        base.camLens.setFov(camData[2])
        if camData[3] == 0:
            localAvatar.setInterest(localAvatar.getParentObj().doId, [
                11622,
                11621,
                11443,
                11442,
                11620,
                11619,
                11441,
                11086,
                11085,
                11263,
                11264,
                11265,
                11444,
                11266,
                11267,
                11445,
                11446,
                11268,
                11269,
                11447,
                11449,
                11270,
                11448,
                11271,
                11272,
                11450,
                11451,
                11273,
                11095,
                11093,
                11094,
                11092,
                11091,
                11090,
                11089,
                11088,
                11087,
                11623,
                11624,
                11625,
                11626,
                11627,
                11628,
                11629,
                11807,
                11630,
                11452,
                11274,
                11096,
                11275,
                11277,
                11276,
                11099,
                11098,
                11097,
                11455,
                11454,
                11453,
                11631,
                11632,
                11633,
                11100,
                11278,
                11456,
                11634,
                11990,
                11812,
                11811,
                11989,
                11988,
                11987,
                11809,
                11810,
                11808,
                11986,
                11985,
                12164,
                12163,
                12162,
                11984,
                11806,
                11805,
                11983,
                12161,
                12160,
                11982,
                11804,
                11803,
                11981,
                11980,
                12159,
                11802,
                11801,
                11979,
                12158,
                12157,
                12156,
                11978,
                11799,
                11800,
                11977,
                11798,
                11976,
                11975,
                11797,
                11796,
                11974,
                11084,
                11262,
                11440,
                11618,
                11795,
                11617,
                11439,
                11261,
                11083,
                11082,
                11260,
                11438,
                11616,
                11794,
                11793,
                11615,
                11437,
                11081,
                11259,
                11080,
                11258,
                11436,
                11614,
                11435,
                11257,
                11079,
                11973,
                11972,
                12155,
                12154,
                12153], [
                'liveCam'])
        else:
            localAvatar.getParentObj().setOceanVisEnabled(1)
            localAvatar.getParentObj().setFlatShips(0)
    else:
        localAvatar.cameraFSM.request('FPS')
        base.cam.reparentTo(camera)
        base.cam.setPos(0, 0, 0)
        base.cam.setHpr(0, 0, 0)
        base.camLens.setFov(63.742)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def showCams():
    """
    Shows all the available live cameras 
    """

    render.findAllMatches('**/liveCamParent*').detach()
    LiveCamTransforms = {'1': [Vec3(-385.776, -2369.64, 52.4644), Vec3(-18.0412, -3.24766, 0), 39.3076, 0],
                         '2': [Vec3(79.1195, -2521.26, 52.4644), Vec3(-18.0412, -3.24766, 0), 39.3076, 0],
                         '3': [Vec3(2858.35, 931.111, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1],
                         '4': [Vec3(3551.93, 532.437, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1],
                         '5': [Vec3(4245.52, 133.763, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1],
                         '6': [Vec3(4939.1, -264.911, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1]}
    camModel = NodePath('camera')
    lens = PerspectiveLens()
    lens.setFov(base.camLens.getFov())
    lens.setFov(39.3076)
    g = lens.makeGeometry()
    gn = GeomNode('frustum')
    gn.addGeom(g)
    gnp = camModel.attachNewNode(gn)
    if not localAvatar.getShip():
        for camNum in range(1, 3):
            camData = LiveCamTransforms[str(camNum)]
            camParent = localAvatar.getParentObj().attachNewNode('liveCamParent-%s' % camNum)
            camParent.setPos(camData[0])
            camParent.setHpr(camData[1])
            camParent.setScale(10)
            camModel.instanceTo(camParent)

    else:
        for camNum in range(3, 7):
            camData = LiveCamTransforms[str(camNum)]
            camParent = render.attachNewNode('liveCamParent-%s' % camNum)
            camParent.setPos(camData[0])
            camParent.setHpr(camData[1])
            camParent.setScale(10)
            camModel.instanceTo(camParent)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def hideCams():
    """
    Hides all the area live cameras
    """

    render.findAllMatches('**/liveCamParent*').detach()

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def dropBlockers():
    """
    Stashes all blocker nodes in the scene
    """

    ga = localAvatar.getParentObj()
    blockers = ga.findAllMatches('**/blocker_*')
    blockers.stash()

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def stayTuned(questId=0):
    """
    Displays the Stay Tuned popup dialog
    """

    localAvatar.guiMgr.showStayTuned(quest = questId, focus = 0)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def crewtut():
    """
    Displays the unused original crew tutorial
    """

    from pirates.tutorial.CrewTutorial import CrewTutorial
    spellbook.getManager().crewTutorial = CrewTutorial()

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def dumpinstance():
    """
    Dumps the current instance object to a BAM file
    """

    parent = localAvatar.getParent()
    parent = parent.getParent()
    parent.writeBamFile('dump.bam')

    return 'Instance Dumped'