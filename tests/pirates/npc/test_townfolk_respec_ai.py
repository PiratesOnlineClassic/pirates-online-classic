import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

# reuse the WeaponGlobals fallback used by the battle tests
from tests.pirates.battle import test_battle_npc_ai  # noqa: F401

from pirates.distributed import InteractGlobals
from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.pirate import AvatarTypes


class TownfolkRespecTests(unittest.TestCase):

    def test_respec_options_are_handled_by_the_trainer(self):
        avatar = SimpleNamespace(doId=42)
        inventory = Mock()
        npc = DistributedNPCTownfolkAI.__new__(DistributedNPCTownfolkAI)
        npc.air = SimpleNamespace(doId2do={42: avatar}, getAvatarIdFromSender=lambda: 42,
            inventoryManager=SimpleNamespace(getInventory=lambda avatarId: inventory))
        npc.avatarType = AvatarTypes.Trainer
        npc.handleRespec = Mock()

        npc.selectOption(InteractGlobals.RESPEC_DOLL)
        npc.handleRespec.assert_called_once_with(avatar, inventory, InteractGlobals.RESPEC_DOLL)

        npc.handleRespec.reset_mock()
        npc.selectOption(InteractGlobals.CANCEL)
        npc.handleRespec.assert_not_called()


if __name__ == '__main__':
    unittest.main()
