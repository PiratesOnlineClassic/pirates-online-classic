"""
Chat is relayed by the AI (otp.chat.ChatRelayAI) rather than broadcast by the
State Server, which relies on two things the Astron Client Agent does:

 * it forwards a field update sent to a location channel to every client with
   interest in that location, whatever keywords the field has, and
 * it drops one whose sender is the receiving client's own channel, so the
   avatar who chatted doesn't get it echoed back.

AstronChatRelayTests checks both against a real astrond (on its own ports,
skipped when the binary isn't there); set ASTROND to point at one.
"""

import os
import socket
import struct
import subprocess
import tempfile
import time
import unittest
from types import SimpleNamespace

from panda3d.core import Filename
from panda3d.direct import DCFile

from otp.chat.ChatRelayAI import ChatRelayAI

RepoRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DClassFiles = [os.path.join(RepoRoot, 'astron', 'dclass', name) for name in ('otp.dc', 'pirates.dc')]

# Chat fields that must reach the AI first, and never be broadcast by the
# State Server straight from the client.
RelayedChatFields = {
    'DistributedPlayer': ['setChat', 'setWLChat', 'setSC', 'setSCCustom'],
    'DistributedPlayerPirate': ['setSCEmote', 'setSpeedChatQuest'],
    'DistributedBandMember': ['setChat', 'setWLChat', 'setSpeedChat', 'setSCQuestChat'],
}


class ChatFieldKeywordTests(unittest.TestCase):

    def test_chat_fields_are_relayed_by_the_ai(self):
        dcFile = DCFile()
        for filename in DClassFiles:
            self.assertTrue(dcFile.read(Filename.fromOsSpecific(filename)))

        for className, fieldNames in RelayedChatFields.items():
            dclass = dcFile.getClassByName(className)
            for fieldName in fieldNames:
                field = dclass.getFieldByName(fieldName)
                description = '%s.%s' % (className, fieldName)
                self.assertTrue(field.isOwnsend(), description)
                self.assertTrue(field.isAirecv(), description)
                self.assertFalse(field.isBroadcast(), description)
                self.assertFalse(field.isRam() or field.isRequired() or field.isDb(), description)


HarnessDC = '''
dclass HarnessUD {
  hello(uint32) clsend;
};

dclass Root {
};

dclass Player {
  setName(string) required broadcast ram;
  setChat(string, uint8, uint32) ownsend airecv;
  setSC(uint16) broadcast ownsend airecv;
};
'''

HarnessConfig = '''
messagedirector:
    bind: 127.0.0.1:%(md)d
general:
    dc_files:
        - harness.dc
uberdogs:
    - class: HarnessUD
      id: %(ud)d
      anonymous: true
roles:
    - type: clientagent
      bind: 127.0.0.1:%(ca)d
      version: harness
      client:
       relocate: true
       add_interest: enabled
       send_hash: false
      channels:
        min: 1000000000
        max: 1009999999
      tuning:
        interest_timeout: 500
    - type: stateserver
      control: %(ss)d
'''

# Not the ports the development cluster uses (7199, 6667).
MDPort, CAPort = 17199, 16667
StateServer = 10000
AIChannel = 5000
UberDogId = 4665
ParentId, ZoneId = 1000, 2000
AvatarId = 200000000
AccountChannel = (1 << 32) | AvatarId

CLIENT_HELLO = 1
CLIENT_HELLO_RESP = 2
CLIENT_OBJECT_SET_FIELD = 120
CLIENT_ENTER_OBJECT_REQUIRED = 142
CLIENT_ENTER_OBJECT_REQUIRED_OTHER_OWNER = 173
CLIENT_DONE_INTEREST_RESP = 204
CLIENTAGENT_SET_STATE = 1000
CLIENTAGENT_SET_CLIENT_ID = 1001
CLIENTAGENT_ADD_INTEREST = 1200
STATESERVER_CREATE_OBJECT_WITH_REQUIRED = 2000
STATESERVER_OBJECT_SET_FIELD = 2020
STATESERVER_OBJECT_SET_AI = 2050
STATESERVER_OBJECT_SET_OWNER = 2060
CONTROL_ADD_CHANNEL = 9000


def findAstrond():
    for path in (os.environ.get('ASTROND'), os.path.join(RepoRoot, 'astron', 'astrond')):
        if path and os.access(path, os.X_OK):
            return path

    return None


def portInUse(port):
    with socket.socket() as sock:
        return sock.connect_ex(('127.0.0.1', port)) == 0


def packString(value):
    value = value.encode()
    return struct.pack('<H', len(value)) + value


class Connection:

    def __init__(self, port):
        self.sock = socket.create_connection(('127.0.0.1', port), timeout=5)
        self.sock.settimeout(0.05)
        self.buffer = b''

    def close(self):
        self.sock.close()

    def send(self, payload):
        self.sock.sendall(struct.pack('<H', len(payload)) + payload)

    def receive(self, wait=0.5):
        messages = []
        end = time.time() + wait
        while time.time() < end:
            try:
                data = self.sock.recv(65536)
                if not data:
                    break

                self.buffer += data
            except socket.timeout:
                pass

            while len(self.buffer) >= 2:
                (length,) = struct.unpack('<H', self.buffer[:2])
                if len(self.buffer) < 2 + length:
                    break

                messages.append(self.buffer[2:2 + length])
                self.buffer = self.buffer[2 + length:]

        return messages


class MessageDirector(Connection):

    def control(self, msgType, payload):
        self.send(struct.pack('<BQH', 1, 1, msgType) + payload)

    def sendTo(self, channel, msgType, payload):
        self.send(struct.pack('<BQQH', 1, channel, AIChannel, msgType) + payload)

    def receiveUpdates(self, wait=0.5):
        """Returns (sender, doId, fieldId) for every field update we got."""

        updates = []
        for message in self.receive(wait):
            offset = 1 + 8 * message[0]
            sender, msgType = struct.unpack('<QH', message[offset:offset + 10])
            if msgType == STATESERVER_OBJECT_SET_FIELD:
                doId, fieldId = struct.unpack('<IH', message[offset + 10:offset + 16])
                updates.append((sender, doId, fieldId, message[offset + 16:]))

        return updates


@unittest.skipUnless(findAstrond(), 'astrond is not available')
class AstronChatRelayTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if portInUse(MDPort) or portInUse(CAPort):
            raise unittest.SkipTest('ports %d/%d are in use' % (MDPort, CAPort))

        cls.tempDir = tempfile.TemporaryDirectory()
        with open(os.path.join(cls.tempDir.name, 'harness.dc'), 'w') as dcFile:
            dcFile.write(HarnessDC)

        with open(os.path.join(cls.tempDir.name, 'astrond.yml'), 'w') as config:
            config.write(HarnessConfig % {'md': MDPort, 'ca': CAPort, 'ud': UberDogId, 'ss': StateServer})

        cls.dcFile = DCFile()
        cls.dcFile.read(Filename.fromOsSpecific(os.path.join(cls.tempDir.name, 'harness.dc')))
        cls.player = cls.dcFile.getClassByName('Player')

        cls.log = open(os.path.join(cls.tempDir.name, 'astrond.log'), 'w')
        cls.astrond = subprocess.Popen([findAstrond(), '-b', 'astrond.yml'], cwd=cls.tempDir.name,
                                       stdout=cls.log, stderr=subprocess.STDOUT)
        try:
            cls._setUpCluster()
        except Exception:
            cls.tearDownClass()
            raise

    @classmethod
    def _setUpCluster(cls):
        end = time.time() + 5
        while not (portInUse(MDPort) and portInUse(CAPort)):
            if time.time() > end or cls.astrond.poll() is not None:
                raise RuntimeError('astrond did not start')

            time.sleep(0.05)

        cls.md = MessageDirector(MDPort)
        cls.md.control(CONTROL_ADD_CHANNEL, struct.pack('<Q', AIChannel))
        cls.md.control(CONTROL_ADD_CHANNEL, struct.pack('<Q', UberDogId))

        # Two clients; each tells the anonymous "UberDOG" its number, so we
        # learn the channel the client agent gave it.
        hello = cls.dcFile.getClassByName('HarnessUD').getFieldByName('hello')
        cls.clients = []
        for index in range(2):
            client = Connection(CAPort)
            client.send(struct.pack('<HI', CLIENT_HELLO, cls.dcFile.getHash() & 0xFFFFFFFF) + packString('harness'))
            response = client.receive()
            assert response and struct.unpack('<H', response[0][:2])[0] == CLIENT_HELLO_RESP, response
            client.send(struct.pack('<HIHI', CLIENT_OBJECT_SET_FIELD, UberDogId, hello.getNumber(), index))
            cls.clients.append(client)

        channels = {}
        for sender, doId, fieldId, data in cls.md.receiveUpdates():
            channels[struct.unpack('<I', data[:4])[0]] = sender

        cls.chatter, cls.listener = cls.clients
        cls.listenerChannel = channels[1]

        # The chatter owns an avatar in the zone both clients have interest
        # in, with an account << 32 | avatar channel the way OTP sets it.
        cls.md.sendTo(StateServer, STATESERVER_CREATE_OBJECT_WITH_REQUIRED,
                      struct.pack('<IIIH', ParentId, 0, 0, cls.dcFile.getClassByName('Root').getNumber()))
        cls.md.sendTo(StateServer, STATESERVER_CREATE_OBJECT_WITH_REQUIRED,
                      struct.pack('<IIIH', AvatarId, ParentId, ZoneId, cls.player.getNumber()) + packString('Bob'))
        cls.md.sendTo(AvatarId, STATESERVER_OBJECT_SET_AI, struct.pack('<Q', AIChannel))
        cls.md.sendTo(channels[0], CLIENTAGENT_SET_CLIENT_ID, struct.pack('<Q', AccountChannel))
        for channel in (AccountChannel, cls.listenerChannel):
            cls.md.sendTo(channel, CLIENTAGENT_SET_STATE, struct.pack('<H', 2))

        cls.md.sendTo(AvatarId, STATESERVER_OBJECT_SET_OWNER, struct.pack('<Q', AccountChannel))
        for channel in (AccountChannel, cls.listenerChannel):
            # interest id, parent, zone, and whether to tell the client it's done
            cls.md.sendTo(channel, CLIENTAGENT_ADD_INTEREST, struct.pack('<HIIB', 1, ParentId, ZoneId, 1))

        for client in cls.clients:
            types = [struct.unpack('<H', m[:2])[0] for m in client.receive(1.0)]
            assert CLIENT_DONE_INTEREST_RESP in types, types

        cls.md.receive()

        # The relay under test, sending through our message director connection.
        air = SimpleNamespace(ourChannel=AIChannel, send=lambda dg: cls.md.send(bytes(dg.getMessage())))
        cls.relay = ChatRelayAI()
        cls.relay.air = air
        cls.relay.dclass = cls.player
        cls.relay.doId = AvatarId
        cls.relay.parentId = ParentId
        cls.relay.zoneId = ZoneId

    @classmethod
    def tearDownClass(cls):
        for client in getattr(cls, 'clients', []):
            client.close()

        if getattr(cls, 'md', None):
            cls.md.close()

        cls.astrond.terminate()
        cls.astrond.wait()
        cls.log.close()
        cls.tempDir.cleanup()

    def receivedFields(self, client):
        fields = []
        for message in client.receive():
            if struct.unpack('<H', message[:2])[0] == CLIENT_OBJECT_SET_FIELD:
                doId, fieldId = struct.unpack('<IH', message[2:8])
                fields.append((doId, self.dcFile.getFieldByIndex(fieldId).getName()))

        return fields

    def test_ownsend_airecv_chat_goes_only_to_the_ai(self):
        field = self.player.getFieldByName('setChat')
        self.chatter.send(struct.pack('<HIH', CLIENT_OBJECT_SET_FIELD, AvatarId, field.getNumber())
                          + packString('ahoy') + struct.pack('<BI', 1, 0))
        updates = self.md.receiveUpdates()
        self.assertEqual([(sender, doId, fieldId) for sender, doId, fieldId, data in updates],
                         [(AccountChannel, AvatarId, field.getNumber())])
        self.assertEqual(self.receivedFields(self.chatter), [])
        self.assertEqual(self.receivedFields(self.listener), [])

    def test_relay_as_sender_reaches_the_zone_but_not_the_sender(self):
        self.relay.sendUpdateToLocation('setChat', ['ahoy', 1, 0], AccountChannel)
        self.assertEqual(self.receivedFields(self.listener), [(AvatarId, 'setChat')])
        self.assertEqual(self.receivedFields(self.chatter), [])

    def test_relay_from_the_ai_reaches_everyone(self):
        self.relay.sendUpdateToLocation('setChat', ['ahoy', 1, 0])
        self.assertEqual(self.receivedFields(self.listener), [(AvatarId, 'setChat')])
        self.assertEqual(self.receivedFields(self.chatter), [(AvatarId, 'setChat')])

    def test_broadcast_reaches_others_before_the_ai_can_check_it(self):
        # What SpeedChat did before it was relayed: the State Server hands it
        # to the other clients at the same time as the AI, so booting the
        # sender afterwards can't stop a bad index reaching them.
        field = self.player.getFieldByName('setSC')
        self.chatter.send(struct.pack('<HIHH', CLIENT_OBJECT_SET_FIELD, AvatarId, field.getNumber(), 65535))
        self.assertEqual(self.receivedFields(self.listener), [(AvatarId, 'setSC')])
        self.assertEqual(self.receivedFields(self.chatter), [])
        self.assertEqual(len(self.md.receiveUpdates()), 1)


if __name__ == '__main__':
    unittest.main()
