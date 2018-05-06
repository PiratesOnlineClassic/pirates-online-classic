import struct
import json
import time
import socket
import random
import sys
import os

from direct.directnotify import DirectNotifyGlobal
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PLocalizer, PiratesGlobals
from pirates.world import WorldGlobals
from otp.ai.MagicWordGlobal import *

class PresenceActions:
    Landroam = 1
    Sailing = 2
    Poker = 3
    Battle = 4
    PVP = 5
    Searching = 6
    Digging = 7

class DiscordPresence:
    notify = DirectNotifyGlobal.directNotify.newCategory('DiscordPresence')
    notify.setInfo(True)

    discordLocations = {
        '1164135492.81dzlu': 'ga_devils_anvil',
        '1156359855.24bbathen': 'ga_cangrejos',
        '1160614528.73sdnaik': 'ga_cuba',
        '1173382404.64sdnaik': 'ga_cutthroat',
        '1142018473.22dxschafe': 'ga_padres_del_fuego',
        '1164763706.66sdnaik': 'ga_driftwood',
        '1164157132.99dzlu': 'ga_perdida',
        '1159933206.48sdnaik': 'ga_kings_head',
        '1173381952.2sdnaik': 'ga_outcast',
        '1150922126.8dzlu': 'ga_port_royal',
        '1161282725.84kmuller': 'ga_rumrunners',
        '1164150392.42dzlu': 'ga_tormenta',
        '1156207188.95dzlu': 'ga_tortuga',
        '1172209006.11sdnaik': 'ga_barbosas_cave',
        '1196970035.53sdnaik': 'ga_spanish_pvp',
        '1196970080.56sdnaik': 'ga_french_pvp',
        #TODO: Add images for interiors
    }

    largeImages = [
        'ga_barbosas_cave',
        'ga_cangrejos',
        'ga_cave',
        'ga_cave_lava',
        'ga_cave2',
        'ga_cutthroat',
        'ga_devils_anvil',
        'ga_driftwood',
        'ga_french_pvp',
        'ga_ocean',
        'ga_outcast',
        'ga_padres_del_fuego',
        'ga_perdida',
        'ga_port_royal',
        'ga_rumrunners',
        'ga_spanish_pvp',
        'ga_tormenta',
        'ga_tortuga',
        'game_logo',
        'sc_sailing'
    ]

    smallImages = [
        'coin_green',
        'coin_red',
        'coin_white',
        'halfmoon',
        'jollymoon',
        'moon',
        'poker',
        'skill_wheel'
    ]

    WEAPON_TYPE_IMAGE = 'image'
    WEAPON_TYPE_MESSAGE = 'message'

    weaponTypes = {
        'wheel': {
            WEAPON_TYPE_IMAGE: 'skill_wheel',
            WEAPON_TYPE_MESSAGE: 'Sailing'
        },
        'cannon': {
            WEAPON_TYPE_IMAGE: 'skill_cannon',
            WEAPON_TYPE_MESSAGE: PLocalizer.ShipCannonShort
        },
        WeaponGlobals.MELEE: {
            WEAPON_TYPE_IMAGE: 'skill_wheel',
            WEAPON_TYPE_MESSAGE: 'Sword'
        },
        WeaponGlobals.FIREARM: {
            WEAPON_TYPE_IMAGE: 'skill_wheel',
            WEAPON_TYPE_MESSAGE: 'Gun'
        },
        WeaponGlobals.GRENADE: {
            WEAPON_TYPE_IMAGE: 'skill_wheel',
            WEAPON_TYPE_MESSAGE: PLocalizer.GrenadeShort
        },
        WeaponGlobals.VOODOO: {
            WEAPON_TYPE_IMAGE: 'skill_wheel',
            WEAPON_TYPE_MESSAGE: 'Voodoo Doll'
        },
        WeaponGlobals.STAFF: {
            WEAPON_TYPE_IMAGE: 'skill_wheel',
            WEAPON_TYPE_MESSAGE: 'Voodoo Staff'
        },
        WeaponGlobals.MELEE: {
            WEAPON_TYPE_IMAGE: 'skill_wheel',
            WEAPON_TYPE_MESSAGE: 'THEIR BARE HANDS'
        },
        WeaponGlobals.THROWING: {
            WEAPON_TYPE_IMAGE: 'skill_wheel',
            WEAPON_TYPE_MESSAGE: 'Daggers'
        }
    }

    def __init__(self):
        self._clientId = config.GetString('discord-client-id', '')
        self._version = config.GetInt('discord-rpc-version', 1)
        self._allowTeleportFromDiscord = config.GetBool('allow-teleport-from-discord', False)
        self._wantDevelopmentMessage = config.GetBool('discord-development-message', False)
        self._changeTime = None
        self._pipe = None

        self._currentLocation = None
        self._locationInterior = False
        self._currentWeapon = None

        self._lastAction = None
        self._currentAction = PresenceActions.Landroam

        self._stateOverride = None
        self._detailsOverride = None

        self._currentCountdown = None

        self._currentCrew = (0, 0)
        self._canJoin = True

        self._afk = False
        self._cursed = False

    @property
    def running(self):
        return self._pipe != None

    @property
    def allowTeleportFromDiscord(self):
        return self._allowTeleportFromDiscord

    def __get_ipc_path(self, pipe=0):
        ipc_path = None
        if sys.platform == 'linux' or sys.platform == 'darwin':
            ipc_path = (os.environ.get('XDG_RUNTIME_DIR',None) or os.environ.get('TMPDIR',None) or os.environ.get('TMP',None) or os.environ.get('TEMP',None) or '/tmp') + '/discord-ipc-' + str(pipe)
        elif sys.platform == 'win32':
            ipc_path = r'\\?\pipe\discord-ipc-' + str(pipe)
        return ipc_path

    def start(self):

        # Verify we want Discord rich presence
        if not config.GetBool('want-discord-rich-presence', True):
            return

        # Check to see if we are already running
        if self.running:
            self.notify.warning('Attempting to start an already started DiscordPresence')
            return

        if not self._clientId or self._clientId == '':
            self.notify.warning('Failed to start Discord Rich Presence; ClientId not specified')
            return

        self.notify.info('Connecting to Discord...')

        self.__connect()
        self.__handshake()

    def __connect(self):
        ipc_path = self.__get_ipc_path()
        if sys.platform == 'linux' or sys.platform == 'darwin':
            self._pipe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._pipe.connect(ipc_path)
        else:
            self._pipe = open(ipc_path, 'r+b')

    def disconnect(self, clean=True):
        if clean and self._pipe:
            self.__send(2, {})

        if self._pipe:

            if sys.platform == 'linux' or sys.platform == 'darwin':
                self._pipe.shutdown(socket.SHUT_RDWR)

            self._pipe.close()
            self._pipe = None
            self.notify.info('Disconnected from Discord')

    def __handshake(self):
        return self.__send(0, {"v": self._version, "client_id": self._clientId})

    def __read(self):
        response = None
        try:
            if sys.platform == 'linux' or sys.platform == 'darwin':
                received_data = self._pipe.recv(1024)
                encoded_header = received_data[:8]
                decoded_header = struct.unpack("<ii", encoded_header)
                encoded_data = received_data[8:]
                response = json.loads(encoded_data.decode('utf-8'))
            else:
                encoded_header = b""
                header_remaining_size = 8

                while header_remaining_size:
                    encoded_header += self._pipe.read(header_remaining_size)
                    header_remaining_size -= len(encoded_header)

                decoded_header = struct.unpack("<ii", encoded_header)
                encoded_data = b""
                packet_remaining_size = int(decoded_header[1])

                while packet_remaining_size:
                    encoded_data += self._pipe.read(packet_remaining_size)
                    packet_remaining_size -= len(encoded_data)

                response = json.loads(encoded_data.decode('utf-8'))
                self._pipe.seek(0, 2)
        except Exception as e:
            self.notify.warning('Failed to read data from Discord')
            self.disconnect()
        finally:
            self.notify.debug('Received Rich Presence response: %s' % str(response))
            return response

    def __send(self, opcode, payload):
        if not self.running:
            self.notify.warning('Failed send payload to Discord; Not running')
            return

        self.notify.debug('Sending Presence update: %s' % str(payload))
        payload = json.dumps(payload)
        encoded_data = struct.pack("<ii", opcode, len(payload)) + payload.encode("utf-8")
        try:
            if sys.platform == 'linux' or sys.platform == 'darwin':
                self._pipe.sendall(encoded_data)
            else:
                self._pipe.write(encoded_data)
                self._pipe.flush()
        except Exception as e:
            self.notify.warning('Failed to send update to Discord')
            self.disconnect(clean=False)
        finally:
            return self.__read()

    def __remove_none(self, d):
        for item in d.copy():
            if isinstance(d[item], dict):
                if len(d[item]):
                    d[item] = self.__remove_none(d[item])
                else:
                    del d[item]
            elif d[item] is None:
                del d[item]
        return d

    def update(self, pid=os.getpid(), state=None, details=None, start=None, end=None, large_image=None, large_text=None, small_image=None, \
        small_text=None, party_id=None, party_size=None, join=None, spectate=None, match=None, instance=True):
        current_time = time.time()

        # Set default image if not present
        if not large_image:
            large_image = 'game_logo'

        if large_image not in self.largeImages and large_image != None:
            self.notify.warning('Failed to set Large Image; %s is not a registered image!' % large_image)
            large_image = None
            large_text = None

        if small_image not in self.smallImages and small_image != None:
            self.notify.warning('Failed to set Small Image; %s is not a registered image' % small_image)
            small_image = None
            small_text = None

        # Do we want the since last change timer?
        if config.GetBool('discord-want-elapsed', False):
            self._changeTime = time.time()

        if not start and not self._currentCountdown:
            start=self._changeTime

        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": pid,
                "activity": {
                    "state": state,
                    "details": details,
                    "timestamps": {
                        "start": start,
                        "end": end
                    },
                    "assets": {
                        "large_image": large_image,
                        "large_text": large_text,
                        "small_image": small_image,
                        "small_text": small_text
                    },
                    "party": {
                        "id": party_id,
                        "size": party_size
                    },
                    "secrets": {
                        "join": join,
                        "spectate": spectate,
                        "match": match
                    },
                    "instance": instance,
                },
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        payload = self.__remove_none(payload)
        response = self.__send(1, payload)

        self.notify.info('Updated Discord Rich Presence state')
        if self.notify.getDebug() or \
            (config.GetBool('discord-print-response', False) and __debug__):
            print(response)
        return response

    def __getOceanName(self):
        if not base.localAvatar:
            return None
        avatarPos = base.localAvatar.getPos()
        oceanId = WorldGlobals.getOceanZone(avatarPos.x, avatarPos.y)
        return PLocalizer.OceanZoneNames.get(oceanId, None)

    def __getMessage(self):
        state = None
        details = None

        district = None
        if base.cr.distributedDistrict:
            district = base.cr.distributedDistrict.getName()
        
        if self._stateOverride:
            state = self._stateOverride
        elif self._wantDevelopmentMessage and __debug__:
            messages = [
                'Developing the game',
                'Working on source code'
            ]
            state = random.choice(messages)
        elif district:
            state = '%s: %s' % (PLocalizer.Ocean, district)

        locationName = PLocalizer.LocationNames.get(self._currentLocation, None)
        if self._detailsOverride:
            details = self._detailsOverride
        elif self._afk:
            messages = [
                'Currently AFK', 
                'Asleep on the Job',
                'Away from Keyboard']

            if self._currentAction == PresenceActions.Sailing:
                if self._currentWeapon == 'wheel':
                    messages += [
                        'Fallen asleep at the wheel'
                    ]
            
            details = random.choice(messages)
        elif self._cursed and self._currentAction != PresenceActions.PVP:
            details = 'Cursed by Jolly Roger'
        elif self._currentAction == PresenceActions.PVP:
            messages = [
                'Battling Cursed Pirates',
                'Battling Their Fellow Pirates'
            ]
            details = random.choice(messages)
        elif self._currentAction == PresenceActions.Sailing:
            oceanName = self.__getOceanName()
            messages = [
                'Sailing the Caribbean',
                'Sailing the Seven Seas'
            ]
            if not oceanName:
                details = random.choice(messages)
            else:
                details = 'Sailing in %s' % oceanName
        elif self._currentAction == PresenceActions.Poker:
            messages = [
                'Playing Card Games', 
                'Playing Cards',
                'Playing Parlor Games',
                'Cheating The Dealer',
                'Cheating their Way to Victory'
            ]
            details = random.choice(messages)
        elif self._currentAction == PresenceActions.Battle:
            details = 'Battling enemies'
        elif self._currentAction == PresenceActions.Landroam and locationName:
            if self._locationInterior:
                details = 'Currently in %s' % locationName
            else:
                details = 'Currently on %s' % locationName
        elif self._currentAction == PresenceActions.Digging:
            messages = [
                'Digging for buried treasure',
                'Digging for treasure',
                'Digging for lost treasure'
            ]
            details = random.choice(messages)
        elif self._currentAction == PresenceActions.Searching:
            messages = [
                'Searching for gold!',
                'Searching for treasure',
                'Searching for lost treasure',
                'Searching for lost goods'
            ]
            details = random.choice(messages)
        else:
            self.notify.warning('Failed to choose the correct details; Lets just enjoy the Caribbean...')
            details = 'Enjoying the Caribbean'

        return (state, details)

    def __getLargeDetails(self):
        image = None
        text = None
    
        if self._currentAction == PresenceActions.Sailing:
            image = 'ga_ocean'
            text = PLocalizer.LoadingScreen_Ocean
        elif self._currentLocation:
            image = self.discordLocations.get(self._currentLocation, None)
            if image:
                text = locationName = PLocalizer.LocationNames.get(self._currentLocation, None)
            else:
                self.notify.warning('Failed to locate image key for location: %s' % self._currentLocation)

        return (image, text)

    def __getSmallDetails(self):
        image = None
        text = None

        if self._cursed:
            image = 'halfmoon'
            text = 'Cursed'
        elif self._currentAction == PresenceActions.PVP:
            team = base.localAvatar.getPVPTeam()
            if team == PiratesGlobals.PVP_FRIEND:
                image = 'coin_green'
                text = 'Green Team'
            elif team == PiratesGlobals.PVP_ENEMY:
                image = 'coin_red'
                text = 'Red Team'
            else:
                image = 'coin_white'
        elif self._currentAction == PresenceActions.Poker:
            image= 'poker'
            text = 'Parlor Games' #TODO: Display name of current parlor game?
        elif self._currentWeapon:
            data = {}
            weaponCategory = WeaponGlobals.getWeaponCategory(self._currentWeapon)
            if self._currentWeapon in self.weaponTypes:
                data = self.weaponTypes[self._currentWeapon]
            elif weaponCategory in self.weaponTypes:
                data = self.weaponTypes[weaponCategory]
                
            image = data.get(self.WEAPON_TYPE_IMAGE, None)
            text = data.get(self.WEAPON_TYPE_MESSAGE, None)

        return (image, text)

    def setAFK(self, afk):
        if self._afk != afk:
            self._afk = afk
            self.refreshPresence()

    def setCursed(self, cursed):
        if self._cursed != cursed:
            self._cursed = cursed
            self.refreshPresence()

    def setCountdown(self, timestamp):
        if self._currentCountdown != timestamp:
            self._currentCountdown = timestamp
            self.refreshPresence()

    def setLocation(self, locationUid, interior=False):
        if self._currentLocation != locationUid or self._locationInterior != interior:
            self._currentLocation = locationUid
            self._locationInterior = interior
            self.refreshPresence()

    def setStateOverride(self, state=None):
        if self._stateOverride != state:
            self._stateOverride = state
            self.refreshPresence()

    def setDetailsOverride(self, details=None):
        if self._detailsOverride != details:
            self._detailsOverride = details
            self.refreshPresence()

    def setCurrentAction(self, action):
        if self._currentAction != action:
            self._lastAction = self._currentAction
            self._currentAction = action
            self.refreshPresence()

    def setLastAction(self):
        self.setCurrentAction(self._lastAction)

    def setLandRoam(self):
        self.setCurrentAction(PresenceActions.Landroam)

    def setSailing(self):
        self.setCurrentAction(PresenceActions.Sailing)

    def setPVP(self):
        self.setCurrentAction(PresenceActions.PVP)

    def setBattle(self):
        self.setCurrentAction(PresenceActions.Battle)

    def setParlorGame(self):
        self.setCurrentAction(PresenceActions.Poker)

    def setDigging(self):
        self.setCurrentAction(PresenceActions.Digging)

    def setSearching(self):
        self.setCurrentAction(PresenceActions.Searching)

    def setCurrentWeapon(self, weapon):
        if self._currentWeapon != weapon:
            self._currentWeapon = weapon
            self.refreshPresence()

    def setCurrentCrew(self, crewSize=0, crewMax=0):
        if self._currentCrew != (crewSize, crewMax):
            self._currentCrew = (crewSize, crewMax)
            self.refreshPresence()

    def setCanJoin(self, join):
        if self._canJoin != join:
            self._canJoin = join
            self.refreshPresence()

    def refreshPresence(self):
        state, details = self.__getMessage()
        large_image, large_text = self.__getLargeDetails()
        small_image, small_text = self.__getSmallDetails()

        # Check if the countdown expired
        if self._currentCountdown:
            if self._currentCountdown < self._changeTime:
                self._currentCountdown = None

        partySize = None
        crewSize, crewMax = self._currentCrew
        if crewSize > 0 or crewMax > 0:
            partySize = (crewSize, crewMax)

        join = None
        if self._allowTeleportFromDiscord and self._canJoin:
            try:
                join = str(base.localAvatar.doId)
            except:
                pass

        response = self.update(
            state=state,
            details=details,
            large_image=large_image,
            large_text=large_text,
            small_image=small_image,
            small_text=small_text,
            start=self._changeTime,
            party_id='POC-CREW', #TODO: Pull from actual party/crew data?
            party_size=partySize,
            join=join,
            end=self._currentCountdown)

        return response

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def discordCountdown(countdown):
    """
    Sets your discord countdown value
    """
    base.richPresence.setCountdown(countdown)
    return 'Countdown set to %d!' % countdown

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str, int])
def discordLocation(locationUid, interior):
    """
    Sets your discord location and interior state
    """

    base.richPresence.setLocation(locationUid, interior=interior)
    return 'Location set to %s!' % locationUid

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def discordAction(state):
    """
    Forces a Discord Rich Presence Action
    """
    states = {
        'landroam': PresenceActions.Landroam,
        'sailing': PresenceActions.Sailing,
        'poker': PresenceActions.Poker,
        'battle': PresenceActions.Battle,
        'pvp': PresenceActions.PVP,
        'searching': PresenceActions.Searching,
        'digging': PresenceActions.Digging
    }

    # Verify the state is valid
    if state not in states:
        return 'Invalid state: %s; Valid: (%s)' % (state, ','.join(states.keys()))

    stateId = states[state]
    base.richPresence.setCurrentAction(stateId)
    return 'Action set to %s (%d)' % (state, stateId)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def lastDiscordAction():
    """
    Reverts your Rich Presence state to the last action
    """
    base.richPresence.setLastAction()
    return 'Action set to last'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def testDiscordPVP():
    """
    Sets your state to the test PVP state
    """
    import datetime
    base.richPresence.setPVP()

    now = datetime.datetime.now()
    ahead = now + datetime.timedelta(minutes = 20)
    base.richPresence.setCountdown(time.mktime(ahead.timetuple()))
    return 'Test PVP State set!'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def testDiscordSailing():
    """
    Sets your state to the test sailing state
    """
    base.richPresence.setSailing()
    base.richPresence.setCurrentWeapon('wheel')
    return 'Test Sailing State set!'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def testDiscordPoker():
    """
    Sets your state to the test parlor games state
    """
    base.richPresence.setParlorGame()
    return 'Test Parlor Game state set!'

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def discordState(state):
    """
    Forces your discord state
    """
    base.richPresence.setStateOverride(state)
    return 'State set to "%s"!' % state

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def resetDiscordState():
    """
    Resets your discord state
    """
    base.richPresence.setStateOverride(None)
    return 'State reset!'    

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def discordDetails(details):
    """
    Forces your discord details
    """
    base.richPresence.setDetailsOverride(details)
    return 'Details set to "%s"!' % details

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def resetDiscordDetails():
    """
    Resets your discord details
    """
    base.richPresence.setDetailsOverride(None)
    return 'Details reset!'

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, int])
def discordCrew(current, max):
    """
    Sets your Discord crew size info
    """
    base.richPresence.setCurrentCrew(current, max)
    return 'Crew size set to: (%d, %d)' % (current, max) 

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def discordAllowJoin(join):
    """
    Allows you to be teleported to from Discord
    """
    base.richPresence.setCanJoin(join)
    return 'CanJoin state set to: %s' % join

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def discordCurrentWeapon(weapon):
    """
    Sets your current Discord weapon
    """
    words = [
        'wheel',
        'cannon'
    ]

    if weapon not in words:
        weapon = int(weapon)

    base.richPresence.setCurrentWeapon(weapon)
    return 'Current Weapon set to: %s' % weapon