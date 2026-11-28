import importlib.util
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch
from tests import REPO_ROOT

questConstants = types.ModuleType('pirates.quest.QuestConstants')
questConstants.CANCEL_QUEST = -1

with patch.dict(sys.modules, {'pirates.quest.QuestConstants': questConstants}):
    spec = importlib.util.spec_from_file_location('_test_DistributedQuestGiverAI',
        REPO_ROOT / 'pirates/quest/DistributedQuestGiverAI.py')
    giverModule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(giverModule)
    giverModule.QuestConstants = questConstants


class QuestGiverTests(unittest.TestCase):
    def setUp(self):
        self.giver = giverModule.DistributedQuestGiverAI.__new__(giverModule.DistributedQuestGiverAI)
        self.giver.doId = 22
        self.giver.avatar2offers = {}
        self.giver.sendUpdateToAvatarId = Mock()
        self.avatar = SimpleNamespace(doId=100)
        self.giver.air = SimpleNamespace(doId2do={100: self.avatar},
            getAvatarIdFromSender=lambda: 100,
            questMgr=SimpleNamespace(hasQuest=Mock(return_value=False), createQuest=Mock()),
            logPotentialHacker=Mock())
        self.offers = [SimpleNamespace(getQuestId=lambda: 'q1'), SimpleNamespace(getQuestId=lambda: 'q2')]

    def test_accepted_offer_creates_quest(self):
        self.giver.d_setQuestOffer(100, self.offers)
        self.giver.setOfferResponse(1, 0)
        self.giver.air.questMgr.createQuest.assert_called_once_with(self.avatar, 'q2')
        self.assertIsNone(self.giver.getOffers(100))

    def test_cancelled_offer_creates_nothing(self):
        self.giver.d_setQuestLadderOffer(100, self.offers, 1)
        self.giver.setOfferResponse(-1, 1)
        self.giver.air.questMgr.createQuest.assert_not_called()

    def test_unsolicited_or_invalid_response_is_rejected(self):
        self.giver.setOfferResponse(0, 0)
        self.giver.d_setQuestOffer(100, self.offers)
        self.giver.setOfferResponse(5, 0)
        self.giver.air.questMgr.createQuest.assert_not_called()
        self.giver.air.logPotentialHacker.assert_called_once()


if __name__ == '__main__':
    unittest.main()
