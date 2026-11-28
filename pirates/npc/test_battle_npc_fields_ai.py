import builtins
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

# reuse the WeaponGlobals fallback used by the battle tests
from pirates.battle import test_battle_npc_ai  # noqa: F401

from pirates.npc.DistributedNPCPirateAI import DistributedNPCPirateAI
from pirates.distributed.DistributedTargetableObjectAI import DistributedTargetableObjectAI
from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI
from pirates.uberdog.PirateInventoryAI import PirateInventoryAI
from pirates.uberdog.UberDogGlobals import InventoryType


class NPCFieldTests(unittest.TestCase):
    def test_npc_pirate_dna_string(self):
        npc = DistributedNPCPirateAI.__new__(DistributedNPCPirateAI)
        npc.sendUpdate = Mock()
        npc.b_setDNAString(b'dna')
        self.assertEqual(npc.getDNAString(), b'dna')
        npc.sendUpdate.assert_called_once_with('setDNAString', [b'dna'])

    def test_moving_object_sends_correct_aggro_field(self):
        obj = DistributedMovingObjectAI.__new__(DistributedMovingObjectAI)
        obj.sendUpdate = Mock()
        obj.b_setAggroMode(2)
        obj.sendUpdate.assert_called_once_with('setAggroMode', [2])

    def makeTargetable(self, hasTarget=True, hasAttacker=True):
        obj = DistributedTargetableObjectAI.__new__(DistributedTargetableObjectAI)
        obj.doId = 1000
        avatar = SimpleNamespace(doId=42)
        targetMgr = Mock()
        targetMgr.hasTarget.return_value = hasTarget
        targetMgr.hasAttacker.return_value = hasAttacker
        obj.air = SimpleNamespace(doId2do={42: avatar}, getAvatarIdFromSender=lambda: 42, targetMgr=targetMgr)
        return obj, avatar, targetMgr

    def test_request_and_remove_target(self):
        obj, avatar, targetMgr = self.makeTargetable()
        obj.requestTarget()
        targetMgr.addAttacker.assert_called_once_with(avatar, obj)
        obj.removeTarget()
        targetMgr.removeAttacker.assert_called_once_with(avatar, obj)

    def test_request_target_on_untargetable_object(self):
        obj, avatar, targetMgr = self.makeTargetable(hasTarget=False)
        obj.requestTarget()
        targetMgr.addAttacker.assert_not_called()

    def test_give_cards_uses_inventory_type(self):
        inventory = PirateInventoryAI.__new__(PirateInventoryAI)
        avatar = Mock()
        inventory.ownerId = 42
        inventory.air = SimpleNamespace(doId2do={42: avatar})
        inventory.getStackQuantity = Mock(return_value=1)
        inventory.b_setStackQuantity = Mock()
        inventory.giveCards(InventoryType.AceOfSpades, 1)
        avatar.giveCardMessage.assert_called_once_with(InventoryType.AceOfSpades)
        inventory.b_setStackQuantity.assert_called_once_with(InventoryType.AceOfSpades, 2)


if __name__ == '__main__':
    unittest.main()
