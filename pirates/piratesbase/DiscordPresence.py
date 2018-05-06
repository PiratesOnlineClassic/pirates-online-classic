import struct
import json
import time
import socket
import sys
import os

from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PLocalizer, PiratesGlobals

class DiscordPresence:
    notify = DirectNotifyGlobal.directNotify.newCategory('DiscordPresence')

    #TODO: finish location mapping
    discordLocations = {
        '1164135492.81dzlu': 'ga_devils_anvil',
        '1156359855.24bbathen': 'ga_cangrejos',
        '1160614528.73sdnaik': 'ga_cuba',
        '1173382404.64sdnaik': None,
        '1142018473.22dxschafe': 'ga_padres_del_fuego',
        '1164763706.66sdnaik': None,
        '1164157132.99dzlu': None,
        '1159933206.48sdnaik': 'ga_kings_head',
        '1173381952.2sdnaik': None,
        '1150922126.8dzlu': 'ga_port_royal',
        '1161282725.84kmuller': None,
        '1164150392.42dzlu': None,
        '1156207188.95dzlu': 'ga_tortuga',
        '1172209006.11sdnaik': 'ga_barbosas_cave',
        '1196970035.53sdnaik': 'ga_spanish_pvp',
        '1196970080.56sdnaik': 'ga_french_pvp',
    }

    def __init__(self):
        self._clientId = config.GetString('discord-client-id', '')
        self._version = config.GetInt('discord-rpc-version', 1)
        self._pipe = None
        self._pendingMessage = None
        self._lastLocation = None

    @property
    def running(self):
        return self._pipe != None

    def __get_ipc_path(self, pipe=0):
        ipc_path = None
        if sys.platform == 'linux' or sys.platform == 'darwin':
            ipc_path = (os.environ.get('XDG_RUNTIME_DIR',None) or os.environ.get('TMPDIR',None) or os.environ.get('TMP',None) or os.environ.get('TEMP',None) or '/tmp') + '/discord-ipc-' + str(pipe)
        elif sys.platform == 'win32':
            ipc_path = r'\\?\pipe\discord-ipc-' + str(pipe)
        return ipc_path

    def start(self):

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
        if clean:
            self.__send(2, {})

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

        return response

    def updateState(self, targetId=None, pvp=False, cards=False, sailing=0, afk=False):

        if targetId is None:
            targetId = self._lastLocation
        elif targetId != self._lastLocation:
            self._lastLocation = targetId

        state = None
        district = None
        if base.cr.distributedDistrict:
            district = base.cr.distributedDistrict.getName()
        if district:
            state = 'Ocean: %s' % district

        locationName = PLocalizer.LocationNames.get(targetId, 'Unknown')
        if afk:
            details = 'AFK on %s' % locationName
        elif pvp:
            details = 'Currently in PVP'
        elif sailing:
            details = 'Sailing the Caribbean'
        elif cards:
            detail = 'Playing Cards on %s' % locationName
        else:
            details = 'Currently on %s' % locationName

        large_image = self.discordLocations.get(targetId, None)
        if sailing:
            large_image = 'ga_ocean'

        small_image = None
        if pvp:
            team = base.localAvatar.getPVPTeam()
            if team == PiratesGlobals.PVP_FRIEND:
                small_image = 'coin_green'
            elif team == PiratesGlobals.PVP_ENEMY:
                small_image = 'coin_red'
            else:
                small_image = 'coin_white'
        elif cards:
            pass #TODO: add cards icon
        elif sailing:
            if sailing == 1:
                small_image = 'skill_wheel'
            elif sailing == 2:
                small_image = 'skill_cannon'

        response = self.update(
            state=state,
            details=details,
            large_image=large_image,
            large_text=locationName,
            small_image=small_image)

        return response
