from types import SimpleNamespace
import unittest
from pickle import PicklingError
from unittest.mock import Mock, patch

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.showbase.Messenger import Messenger
from otp.distributed.NetMessenger import NetMessenger
from pirates.distributed.PiratesMsgTypes import netMessages
from pirates.uberdog.DistributedInventoryManagerUD import (
    CreateInventoryFSM,
    DistributedInventoryManagerUD,
)
from pirates.uberdog.DistributedInventoryUD import DistributedInventoryUD


_responseResults = []


def _recordInventoryResponse(value):
    _responseResults.append(value)


class FakeAir:
    def __init__(self):
        self.registeredChannels = []
        self.sentDatagrams = []
        self.ourChannel = 12345

    def registerForChannel(self, channel):
        self.registeredChannels.append(channel)

    def send(self, datagram):
        self.sentDatagrams.append(datagram)


def make_net_messenger():
    air = FakeAir()
    net_messenger = NetMessenger(air)
    for code, message in enumerate(netMessages):
        net_messenger.register(code, message)
    air.netMessenger = net_messenger
    return net_messenger


class InventoryUDTests(unittest.TestCase):
    def test_inventory_responses_have_one_process_wide_listener(self):
        net_messenger = make_net_messenger()
        air = SimpleNamespace(netMessenger=net_messenger)

        with patch.object(DistributedObjectUD, 'announceGenerate'):
            for do_id in (101, 102):
                inventory = object.__new__(DistributedInventoryUD)
                inventory.air = air
                inventory.doId = do_id
                inventory.announceGenerate()

        manager = object.__new__(DistributedInventoryManagerUD)
        manager.air = air
        with patch.object(DistributedObjectGlobalUD, 'announceGenerate'):
            manager.announceGenerate()

        for event in (
            'getAccumulatorsResponse',
            'getAccumulatorResponse',
            'getStackLimitResponse',
            'getStackResponse',
            'getOwnerIdResponse',
        ):
            with self.subTest(event=event):
                _responseResults.clear()
                net_messenger.send(event, [_recordInventoryResponse, 42])
                self.assertEqual(_responseResults, [42])

    def test_manager_delete_ignores_only_its_net_messenger_listeners(self):
        net_messenger = make_net_messenger()
        manager = object.__new__(DistributedInventoryManagerUD)
        manager.air = SimpleNamespace(netMessenger=net_messenger)
        manager.avatar2fsm = {}
        with patch.object(DistributedObjectGlobalUD, 'announceGenerate'):
            manager.announceGenerate()

        observed = []
        observer = SimpleNamespace()
        net_messenger.accept(
            'getStackResponse',
            observer,
            lambda callback, value: observed.append((callback, value)))

        _responseResults.clear()
        net_messenger.send('getStackResponse', [_recordInventoryResponse, 42])
        self.assertEqual(_responseResults, [42])
        self.assertEqual(len(observed), 1)

        with patch.object(DistributedObjectGlobalUD, 'delete'):
            manager.delete()

        net_messenger.send('getStackResponse', [_recordInventoryResponse, 84])
        self.assertEqual(_responseResults, [42])
        self.assertEqual(len(observed), 2)

    def test_inventory_response_names_are_appended_without_shifting_legacy_ids(self):
        self.assertEqual(netMessages[28:30], [
            'getStackLimitResponse',
            'getStackResponse',
        ])
        self.assertEqual(netMessages[-2:], [
            'getAccumulatorsResponse',
            'getAccumulatorResponse',
        ])
        self.assertEqual(
            netMessages[27],
            'getAccumulatorsResponsegetAccumulatorResponse')

    def test_local_callback_cannot_be_pickled_for_net_messenger(self):
        net_messenger = make_net_messenger()
        inventory = object.__new__(DistributedInventoryUD)
        inventory.air = SimpleNamespace(netMessenger=net_messenger)
        inventory.doId = 101

        with self.assertRaises((AttributeError, PicklingError)):
            inventory.getStack(42, lambda value: None)

    def test_inventory_link_failure_returns_failure_to_caller(self):
        fsm = object.__new__(CreateInventoryFSM)
        fsm._finished = False
        fsm.inventoryId = 9001
        fsm.avatarId = 7001
        fsm._finish = Mock()
        fsm.notify = SimpleNamespace(warning=Mock())
        fsm.air = SimpleNamespace(
            dbId=1,
            dclassesByName={
                'DistributedPlayerPirateUD': object(),
                'PirateInventoryUD': object(),
            },
            dbInterface=SimpleNamespace(
                updateObject=Mock(side_effect=RuntimeError('database unavailable'))))

        fsm.inventoryCreatedCallback(9001)

        fsm._finish.assert_called_once_with(0)
        self.assertIn(
            'database unavailable',
            fsm.notify.warning.call_args.args[0])


if __name__ == '__main__':
    unittest.main()
