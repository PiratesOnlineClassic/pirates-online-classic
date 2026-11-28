import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

# reuse the WeaponGlobals fallback used by the battle tests
from tests.pirates.battle import test_battle_npc_ai  # noqa: F401

from pirates.npc import DistributedNPCTownfolkAI as townfolk_module
from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.piratesbase import PiratesGlobals


class FakeQuest:

    def __init__(self, giverId, complete):
        self.giverId = giverId
        self.complete = complete

    def getGiverId(self):
        return self.giverId

    def isComplete(self):
        return self.complete


class TownfolkInteractTests(unittest.TestCase):

    def setUp(self):
        self.avatar = SimpleNamespace(doId=42)
        self.questMgr = SimpleNamespace(requestInteract=Mock(), quests={})
        self.npc = DistributedNPCTownfolkAI.__new__(DistributedNPCTownfolkAI)
        self.npc.air = SimpleNamespace(questMgr=self.questMgr)
        self.npc.uniqueId = 'npc-uid'
        self.npc.sendUpdateToAvatarId = Mock()

    def test_hostile_interaction_is_denied_without_quest_events(self):
        result = self.npc.handleRequestInteraction(self.avatar, PiratesGlobals.INTERACT_TYPE_HOSTILE, False)
        self.assertEqual(result, self.npc.DENY)
        self.questMgr.requestInteract.assert_not_called()
        self.npc.sendUpdateToAvatarId.assert_not_called()

    def test_friendly_interaction_greets_the_avatar(self):
        result = self.npc.handleRequestInteraction(self.avatar, PiratesGlobals.INTERACT_TYPE_FRIENDLY, False)
        self.assertEqual(result, self.npc.ACCEPT)
        self.questMgr.requestInteract.assert_called_once_with(self.avatar, self.npc)
        self.npc.sendUpdateToAvatarId.assert_any_call(42, 'triggerInteractShow', [0])
        self.npc.sendUpdateToAvatarId.assert_called_with(42, 'offerOptions',
            [townfolk_module.NPC_DIALOG_GREETING])

    def test_avatar_on_this_npcs_quest_is_encouraged(self):
        self.questMgr.quests[42] = {1: FakeQuest('other-uid', False), 2: FakeQuest('npc-uid', False)}
        self.npc.handleRequestInteraction(self.avatar, PiratesGlobals.INTERACT_TYPE_FRIENDLY, False)
        self.npc.sendUpdateToAvatarId.assert_called_with(42, 'offerOptions',
            [townfolk_module.NPC_DIALOG_ENCOURAGE])

    def test_completed_quests_are_greeted(self):
        self.questMgr.quests[42] = {2: FakeQuest('npc-uid', True)}
        self.npc.handleRequestInteraction(self.avatar, PiratesGlobals.INTERACT_TYPE_FRIENDLY, False)
        self.npc.sendUpdateToAvatarId.assert_called_with(42, 'offerOptions',
            [townfolk_module.NPC_DIALOG_GREETING])

    def test_healer_only_heals_a_groggy_avatar_to_its_adjusted_max_hp(self):
        from pirates.distributed import InteractGlobals

        inventory = SimpleNamespace(gold=100)
        inventory.getGoldInPocket = lambda: inventory.gold
        inventory.setGoldInPocket = lambda gold: setattr(inventory, 'gold', gold)
        avatar = SimpleNamespace(doId=42, hp=75, getAdjMaxHp=lambda: 75, getMaxHp=lambda: 100,
            b_setHp=Mock())
        self.npc.air.doId2do = {42: avatar}
        self.npc.air.getAvatarIdFromSender = lambda: 42
        self.npc.air.inventoryManager = SimpleNamespace(getInventory=lambda doId: inventory)

        self.npc.selectOption(InteractGlobals.HEAL_HP)
        avatar.b_setHp.assert_not_called()
        self.assertEqual(inventory.gold, 100)

        avatar.hp = 50
        self.npc.selectOption(InteractGlobals.HEAL_HP)
        avatar.b_setHp.assert_called_once_with(75)
        self.assertLess(inventory.gold, 100)

    def test_npcs_can_be_used_by_many_avatars(self):
        self.assertTrue(DistributedNPCTownfolkAI.MULTIUSE)


if __name__ == '__main__':
    unittest.main()
