import string

from direct.showbase.ShowBaseGlobal import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from otp.avatar import Avatar
from otp.chat import ChatManager
from direct.showbase import PythonUtil
from otp.otpbase import OTPGlobals
from direct.distributed.ClockDelta import *
from otp.ai import MagicWordManager
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
        self.rainDrops = None
        self.rainMist = None
        self.rainSplashes = None
        self.rainSplashes2 = None
        self.stormEye = None
        self.stormRing = None

    def generate(self):
        MagicWordManager.MagicWordManager.generate(self)
        self.accept('magicWord', self.b_setMagicWord)
        self.accept('requestServerTime', self.d_requestServerTime)

    def doLoginMagicWords(self):
        MagicWordManager.MagicWordManager.doLoginMagicWords(self)
        if base.config.GetBool('want-chat', 0):
            self.d_setMagicWord('~chat', localAvatar.doId, 0)

        if base.config.GetBool('want-run', 0) or base.config.GetBool('want-pirates-run', 0):
            self.toggleRun()

        if base.config.GetBool('immortal-mode', 0):
            self.d_setMagicWord('~immortal', localAvatar.doId, 0)

    def disable(self):
        taskMgr.remove('setGMNameTag')
        self.ignore('magicWord')
        self.ignore('requestServerTime')
        MagicWordManager.MagicWordManager.disable(self)
        if self.pendingCameraReparent:
            base.cr.relatedObjectMgr.abortRequest(self.pendingCameraReparent)
            self.pendingCameraReparent = None

    def doMagicWord(self, word, avId, zoneId):

        def wordIs(w, word=word):
            return word[:len(w) + 1] == '%s ' % w or word == w

        if MagicWordManager.MagicWordManager.doMagicWord(self, word, avId, zoneId) == 1:
            pass

        if word == '~walk':
            localAvatar.b_setGameState('LandRoam')
            localAvatar.motionFSM.on()
        elif word == '~collisions_on':
            pass
        elif word == '~collisions_off':
            pass
        elif word == '~topten':
            base.cr.guildManager.requestLeaderboardTopTen()
        elif word == '~airender':
            pass
        elif __dev__ and wordIs('~cr'):
            pass
        elif __dev__ and wordIs('~ccNPC') or wordIs('~ccShip'):
            pass
        elif wordIs('~pilot'):
            ships = base.cr.doFindAll('ship-')
            from pirates.ship.DistributedShip import DistributedShip
            ships = [ship for ship in ships if isinstance(ship, DistributedShip)]
            print ships
            closestShip = ships[0]
            closestDist = Vec3(closestShip.getPos(localAvatar)).lengthSquared()
            print closestShip, closestDist
            for ship in ships[1:]:
                dist = Vec3(ship.getPos(localAvatar)).lengthSquared()
                print ship, dist
                if dist < closestDist:
                    closestShip = ship
                    closestDist = dist

            wheel = closestShip.find('**/wheel')
            localAvatar.setPos(wheel, 0, 0, 0)
        elif wordIs('~bonfire'):
            bf = Bonfire()
            bf.reparentTo(render)
            bf.setPos(localAvatar, 0, 0, 0)
            bf.startLoop()
            print 'bonfire at %s, %s' % (localAvatar.getPos(), localAvatar.getHpr())
        elif __dev__ and wordIs('~mario'):
            localAvatar.toggleMario()
        elif wordIs('~islandShips'):
            args = word.split()

            try:
                if args[1] == '1':
                    localAvatar.getParentObj().setOceanVisEnabled(1)
                    localAvatar.getParentObj().setFlatShips(0)
                else:
                    localAvatar.getParentObj().setOceanVisEnabled(0)
            except:
                pass

        elif wordIs('~swamp'):
            if self.fireflies:
                self.fireflies.destroy()
                self.fireflies = None
                self.groundFog.destroy()
                self.groundFog = None
            else:
                self.fireflies = Fireflies()
                if self.fireflies:
                    self.fireflies.reparentTo(localAvatar)
                    self.fireflies.startLoop()

                self.groundFog = GroundFog()
                if self.groundFog:
                    self.groundFog.reparentTo(localAvatar)
                    self.groundFog.startLoop()

        elif wordIs('~darkfog'):
            if self.groundFog:
                self.groundFog.destroy()
                self.groundFog = None
            else:
                self.groundFog = DarkWaterFog()
                if self.groundFog:
                    self.groundFog.reparentTo(localAvatar)
                    self.groundFog.startLoop()

        elif wordIs('~dust'):
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
        elif wordIs('~rain'):
            if self.rainDrops:
                self.rainDrops.stopLoop()
                self.rainDrops = None
                if self.rainMist:
                    self.rainMist.stopLoop()
                    self.rainMist = None

                if self.rainSplashes:
                    self.rainSplashes.stopLoop()
                    self.rainSplashes = None

                if self.rainSplashes2:
                    self.rainSplashes2.stopLoop()
                    self.rainSplashes2 = None

            else:
                from pirates.effects.RainDrops import RainDrops
                self.rainDrops = RainDrops(base.camera)
                self.rainDrops.reparentTo(render)
                self.rainDrops.startLoop()
                from pirates.effects.RainMist import RainMist
                self.rainMist = RainMist(base.camera)
                self.rainMist.reparentTo(render)
                self.rainMist.startLoop()
                from pirates.effects.RainSplashes import RainSplashes
                self.rainSplashes = RainSplashes(base.camera)
                self.rainSplashes.reparentTo(render)
                self.rainSplashes.startLoop()
                from pirates.effects.RainSplashes2 import RainSplashes2
                self.rainSplashes2 = RainSplashes2(base.camera)
                self.rainSplashes2.reparentTo(render)
                self.rainSplashes2.startLoop()
        elif wordIs('~clouds'):
            args = word.split()
            if len(args) >= 2:
                level = int(args[1])
                base.cr.timeOfDayManager.skyGroup.transitionClouds(level).start()

        elif wordIs('~storm'):
            if self.stormEye:
                self.stormEye.stopLoop()
                self.stormEye = None
                if self.stormRing:
                    self.stormRing.stopLoop()
                    self.stormRing = None

            else:
                args = word.split()
                grid = 0
                if len(args) > 1:
                    grid = int(args[1])

                pos = Vec3(base.cr.doId2do[201100017].getZoneCellOrigin(grid)[0], base.cr.doId2do[201100017].getZoneCellOrigin(grid)[1], base.cr.doId2do[201100017].getZoneCellOrigin(grid)[2])
                from pirates.effects.StormEye import StormEye
                self.stormEye = StormEye()
                self.stormEye.reparentTo(render)
                self.stormEye.startLoop()
                from pirates.effects.StormRing import StormRing
                self.stormRing = StormRing()
                self.stormRing.reparentTo(render)
                self.stormRing.setZ(100)
                self.stormRing.startLoop()
        elif wordIs('~alight'):
            args = word.split()
            if len(args) > 3:
                color = Vec4(float(args[1]), float(args[2]), float(args[3]), 1)
                base.cr.timeOfDayManager.alight.node().setColor(color)

        elif wordIs('~dlight'):
            args = word.split()
            if len(args) > 3:
                color = Vec4(float(args[1]), float(args[2]), float(args[3]), 1)
                base.cr.timeOfDayManager.dlight.node().setColor(color)

        elif wordIs('~fog'):
            args = word.split()
            if len(args) > 3:
                color = Vec4(float(args[1]), float(args[2]), float(args[3]), 1)
                base.cr.timeOfDayManager.fog.setColor(color)

            if len(args) > 4:
                base.cr.timeOfDayManager.fog.setExpDensity(float(args[4]))

            if len(args) == 2:
                base.cr.timeOfDayManager.fog.setExpDensity(float(args[1]))

        elif __dev__ and wordIs('~turbo'):
            localAvatar.toggleTurbo()
        elif __dev__ and wordIs('~joincrew'):
            base.cr.crewManager.requestNewCrew()
        elif wordIs('~tm'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_TM, 'treasureMapCove')
        elif wordIs('~tml'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld')
        elif wordIs('~pg'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_PG, 'ParlorWorld')
        elif wordIs('~pgvip'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_PG, 'ParlorVIPWorld')
        elif wordIs('~pgl'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld')
        elif wordIs('~tutorial'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_TUTORIAL, 'RambleshackWorld', self.cr.playGame.handleTutorialGeneration)
        elif wordIs('~tutoriall'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld')
        elif wordIs('~pvp'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_PVP, 'pvp_captureWorld')
        elif wordIs('~pirateer'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_PVP, 'pirateerMap')
        elif wordIs('~pvpl'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld')
        elif wordIs('~tortuga'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'TortugaWorld')
        elif wordIs('~portRoyal'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'PortRoyalWorld')
        elif wordIs('~delFuego'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'DelFuegoWorld')
        elif wordIs('~bilgewater'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'BilgewaterWorld')
        elif wordIs('~kingshead'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'KingsheadWorld')
        elif wordIs('~cuba'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CubaWorld')
        elif wordIs('~rumrunner'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'RumrunnerWorld')
        elif wordIs('~wildisland'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'WildIslandWorld')
        elif wordIs('~caveA'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CaveAWorld')
        elif wordIs('~caveB'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CaveBWorld')
        elif wordIs('~caveC'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CaveCWorld')
        elif wordIs('~caveD'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CaveDWorld')
        elif wordIs('~caveE'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CaveEWorld')
        elif wordIs('~jungleA'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'JungleTestWorldA')
        elif wordIs('~jungleB'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'JungleTestWorld')
        elif wordIs('~jungleC'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'JungleTestWorldC')
        elif wordIs('~swampA'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'SwampTestWorld')
        elif wordIs('~mainWorld'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld')
        elif wordIs('~gameArea'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'GameAreaSandbox')
        elif wordIs('~blackpearl'):
            args = word.split()
            if len(args) == 1:
                self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_TM, 'BlackpearlWorld')

        elif wordIs('~fireworks'):
            showType = FireworkShowType.FourthOfJuly
            timestamp = 0.0
            args = word.split()
            if len(args) >= 2:
                showType = float(args[1])

            if len(args) >= 3:
                timestamp = float(args[2])

            if base.cr.activeWorld:
                if not (base.cr.activeWorld.fireworkShowMgr):
                    base.cr.activeWorld.enableFireworkShow(timestamp, showType)
                else:
                    base.cr.activeWorld.disableFireworkShow()

        elif wordIs('~te'):
            if localAvatar.gameFSM.getCurrentOrNextState() == 'LandRoam':
                localAvatar.b_setGameState('TeleportOut')
            elif localAvatar.gameFSM.getCurrentOrNextState() == 'TeleportOut':
                localAvatar.b_setGameState('LandRoam')

        elif wordIs('~shipModel'):
            args = word.split()
            shipClass = 23
            team = 0
            wantCollisions = 1

            try:
                shipClass = args[1]
                team = args[2]
                wantCollisions = args[3]
            except:
                pass

            sm = ShipModel(base.cr, shipClass, team, wantCollisions)
            sm.reparentTo(localAvatar)
            sm.setY(100)
            sm.setH(90)
            sm.wrtReparentTo(render)
        elif wordIs('~deployShip'):
            if not localAvatar.getInventory():
                return None

            if not localAvatar.getInventory().getShipDoIdList():
                return None

            if localAvatar.getActiveShipId():
                shipId = localAvatar.getActiveShipId()
                localAvatar.d_requestReturnShip(shipId)
            else:
                args = word.split()
                shipIndex = 0
                if len(args) >= 2:
                    shipIndex = int(args[1])

                shipId = localAvatar.getInventory().getShipDoIdList()[shipIndex]
                localAvatar.d_requestDeployShip(shipId)
        elif wordIs('~lfa'):
            args = word.split()
            activityName = None
            if len(args) >= 2:
                activityName = args[1]

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
                self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld')

        elif wordIs('~term') or wordIs('terminator'):
            localAvatar.setEquippedWeapons([
                10103,
                10106,
                10115])
            localAvatar.d_requestEquipWeapons([
                10103,
                10106,
                10115])
        elif wordIs('~battleRandom'):
            args = word.split()
            if len(args) >= 2:
                command = args[1]
                if command == 'resync':
                    localAvatar.battleRandom.resync()
                    self.notify.info('Client Battle random resynced, counter=0')

            else:
                counter = localAvatar.battleRandom.counter
                self.notify.info('Client Battle random counter=%s' % counter)
        elif wordIs('~cutscene'):
            args = word.split()
            name = None
            if len(args) >= 2:
                csId = args[1]
            else:
                csId = base.config.GetString('default-cutscene', '0')
            if int(csId) >= len(CutsceneData.CutsceneNames):
                return None

            name = CutsceneData.CutsceneNames[int(csId)]
            cs = PythonUtil.ScratchPad()

            def destroyCutscene(cs = cs):
                cs.cutscene.destroy()

            c = Cutscene.Cutscene(self.cr, name, PythonUtil.DelayedFunctor(destroyCutscene, '~cutscene-destroy'))
            cs.cutscene = c
            c.play()
            destroyCutscene = None
        elif wordIs('~forceLod'):
            for n in render.findAllMatches('**/+LODNode'):
                n.node().forceSwitch(n.node().getHighestSwitch())

        elif wordIs('~wave'):
            args = word.split()
            patch = base.cr.activeWorld.water.patch
            if len(args) < 4:
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
            else:
                num = int(args[1])
                amplitude = float(args[2])
                wavelength = float(args[3])
                speed = float(args[4])
                patch.enableWave(num)
                patch.setWaveTarget(num, SeaPatchRoot.WTZ)
                patch.setWaveFunc(num, SeaPatchRoot.WFSin)
                patch.setChoppyK(num, 0)
                patch.setWaveAmplitude(num, amplitude)
                patch.setWaveLength(num, wavelength)
                patch.setWaveSpeed(num, speed)
                response = 'wave %s modified' % num
            self.setMagicWordResponse(response)
        elif wordIs('~roll'):
            args = word.split()
            if len(args) < 2:
                response = '~roll angle [fakeMass]'
            elif localAvatar.ship is None:
                response = 'not on a ship'
            elif len(args) > 2:
                localAvatar.ship._rocker.setFakeMass(float(args[2]))

            localAvatar.ship.addRoll(float(args[1]))
            response = 'rolling!'
            self.setMagicWordResponse(response)
        elif wordIs('~ru'):
            if hasattr(self, 'radarUtil') and self.radarUtil and not self.radarUtil.isDestroyed():
                self.radarUtil.destroy()
            else:
                self.radarUtil = RadarUtil()
        elif __dev__ and wordIs('~todpanel'):
            tod = base.cr.timeOfDayManager
            from pirates.leveleditor import TimeOfDayPanel
            p = TimeOfDayPanel.TimeOfDayPanel(tod)
        elif __dev__ and wordIs('~kraken'):
            args = word.split()[1:]
            if args and args[0]:
                if not hasattr(base, 'oobeMode') or not (base.oobeMode):
                    base.oobe()
                    base.oobeCamera.wrtReparentTo(render)

        elif wordIs('~pvpmoney') or wordIs('~pvpinfamy'):
            if localAvatar.ship and localAvatar.ship.renownDisplay:
                taskMgr.doMethodLater(2.0, localAvatar.ship.renownDisplay.loadRank, 'pvp-infamy-display', [])

            if localAvatar.guiMgr and localAvatar.guiMgr.pvpPanel and hasattr(localAvatar.guiMgr.pvpPanel, 'renownDisplay') and localAvatar.guiMgr.pvpPanel.renownDisplay:
                taskMgr.doMethodLater(2.0, localAvatar.guiMgr.pvpPanel.renownDisplay.loadRank, 'pvp-infamy-display', [])

            if localAvatar.guiMgr and localAvatar.guiMgr.titlesPage:
                taskMgr.doMethodLater(2.0, localAvatar.guiMgr.titlesPage.refresh, 'titles-refresh', [])

        elif wordIs('~gmNameTag'):
            args = word.split()
            if len(args) < 2 and localAvatar.gmNameTagAllowed:
                response = PLocalizer.MAGICWORD_GMNAMETAG
                self.setMagicWordResponse(response)

            if len(args) >= 2 and localAvatar.gmNameTagAllowed:
                if args[1] == 'enable':
                    localAvatar.setGMNameTagState(1)
                elif args[1] == 'disable':
                    localAvatar.setGMNameTagState(0)
                elif args[1] == 'setString':
                    xCount = 0
                    stringToSet = ''
                    for i in args:
                        if xCount < 2:
                            pass

                        stringToSet = '%s %s' % (stringToSet, args[xCount])
                        xCount += 1

                    localAvatar.setGMNameTagString(stringToSet)
                elif args[1] == 'setColor':
                    localAvatar.setGMNameTagColor(args[2])

        elif wordIs('~liveCam'):
            LiveCamTransforms = {'1': [Vec3(-385.776, -2369.64, 52.4644), Vec3(-18.0412, -3.24766, 0), 39.3076, 0],
                                 '2': [Vec3(79.1195, -2521.26, 52.4644), Vec3(-18.0412, -3.24766, 0), 39.3076, 0],
                                 '3': [Vec3(2858.35, 931.111, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1],
                                 '4': [Vec3(3551.93, 532.437, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1],
                                 '5': [Vec3(4245.52, 133.763, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1],
                                 '6': [Vec3(4939.1, -264.911, 37.9564), Vec3(-29.8904, -7.12525, 0), 39.3076, 1]}
            lodNodes = render.findAllMatches('**/+LODNode')
            for i in xrange(0, lodNodes.getNumPaths()):
                lodNodes[i].node().forceSwitch(lodNodes[i].node().getHighestSwitch())

            localAvatar.clearInterestNamed(None, [
                'liveCam'])
            localAvatar.getParentObj().setOceanVisEnabled(0)
            args = word.split()
            if len(args) > 1:
                camNum = args[1]
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
        elif wordIs('~showCams'):
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

        elif wordIs('~hideCams'):
            render.findAllMatches('**/liveCamParent*').detach()
        elif wordIs('~dropBlockers'):
            ga = localAvatar.getParentObj()
            blockers = ga.findAllMatches('**/blocker_*')
            blockers.stash()

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

        if not base.cr.doId2do.has_key(targetParentId):
            self.notify.debug('Parent of target object to reparent avatar/camera to does not yet exist, skipping reparent request')
            return None

        if isinstance(base.cr.doId2do[targetParentId], DistributedCartesianGrid.DistributedCartesianGrid):
            base.cr.doId2do[targetParentId].visAvatar = localAvatar

        localAvatar.b_setLocation(targetParentId, zoneId, teleport = 1)
        if base.cr.doId2do.has_key(targetId):
            self.cameraFollowTgt(base.cr.doId2do[targetId], targetParentId)
        else:
            self.pendingCameraReparent = base.cr.relatedObjectMgr.requestObjects([
                targetId], eachCallback = lambda param = None, param2 = targetParentId: self.cameraFollowTgt(param, param2))
        localAvatar.stash()

    def shipCreated(self, shipId):
        print 'shipCreated(%s)' % shipId
        ship = base.cr.doId2do.get(shipId)
        if ship:
            print 'ship created: %s' % ship
            ship.localAvatarInstantBoard()
            ship.enableOnDeckInteractions()

    def d_requestServerTime(self):
        self.sendUpdate('requestServerTime', [])

    def recvServerTime(self, sinceEpoch):
        base.chatAssistant.receiveGameMessage(PLocalizer.getServerTimeString(sinceEpoch))
