import ast
import types
import unittest
from unittest.mock import Mock

from tests import REPO_ROOT
from tests.pirates.quest.test_quest_manager_ai_progression import manager_module
from pirates.piratesbase import PiratesGlobals
from pirates.quest import QuestDB
from pirates.quest.DistributedQuestAI import DistributedQuestAI


def loadCutsceneIds():
    # CutsceneData pulls in the client's actors and models, only read the
    # names of the cutscenes that have a CutsceneDesc...
    tree = ast.parse((REPO_ROOT / 'pirates/cutscene/CutsceneData.py').read_text())
    names = {}
    described = set()
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.targets[0], ast.Name):
            continue

        target = node.targets[0].id
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            names[target] = node.value.value
        elif target == 'CutsceneData' and isinstance(node.value, ast.Dict):
            described = set(names[key.id] for key in node.value.keys)

    return described


CutsceneIds = loadCutsceneIds()
FinalizeQuestIds = sorted(questId for questId, dna in QuestDB.QuestDict.items()
                          if dna.getFinalizeInfo())


class QuestFinalizeSceneTests(unittest.TestCase):
    def test_every_quest_cutscene_exists(self):
        for questId in FinalizeQuestIds:
            for info in QuestDB.QuestDict[questId].getFinalizeInfo():
                self.assertIn(info['type'], ('cutscene', 'dialog'), questId)
                if info['type'] != 'cutscene':
                    continue

                self.assertIn(info['sceneId'], CutsceneIds, questId)
                for preload in info.get('preloadInfo', []):
                    self.assertIn(preload, CutsceneIds, questId)

    def test_every_finalize_sequence_plays_through_and_completes(self):
        # finishing or skipping a scene on the client both end with
        # doneFinalizeScene, which must move on to the next scene...
        for questId in FinalizeQuestIds:
            manager = manager_module.QuestManagerAI(types.SimpleNamespace())
            events = {}
            manager.acceptOnce = lambda event, callback, extraArgs=[]: events.update(
                {event: lambda: callback(*extraArgs)})
            manager._giveRewards = Mock(return_value=True)
            manager.completeQuest = Mock()
            manager.tutorialJollyReady.add(5)

            avatar = types.SimpleNamespace(doId=1, getTutorial=lambda: PiratesGlobals.TUT_FINISHED,
                                           getQuestHistory=lambda: [],
                                           getConstructedShipDoId=lambda: 0,
                                           uniqueName=lambda event: '%s-1' % event)
            dna = QuestDB.QuestDict[questId]
            scenes = []
            quest = types.SimpleNamespace(
                doId=5, questDNA=dna, getQuestDNA=lambda: dna, getQuestId=lambda: questId,
                setFinalizeStateIndex=lambda idx: None,
                d_startFinalizeScene=lambda idx, giver: scenes.append(idx),
                d_amFinalized=Mock(), setFinalized=Mock(), completeRequiresVisit=lambda: False)
            npc = types.SimpleNamespace(doId=10, getUniqueId=lambda: 'npc')

            manager.finalizeCutscene(avatar, quest, npc=npc)
            for index in range(len(dna.getFinalizeInfo())):
                self.assertEqual(scenes, list(range(index + 1)), questId)
                events.pop('quest-finalize-5')()
                # Darby's closing dialog waits for the tutorial ship to be built...
                if 'tutorialShipConstructed-1' in events:
                    events.pop('tutorialShipConstructed-1')()

            self.assertNotIn('quest-finalize-5', events, questId)
            manager.completeQuest.assert_called_once_with(avatar, quest)


class DoneFinalizeSceneTests(unittest.TestCase):
    def makeQuest(self, senderId):
        quest = DistributedQuestAI.__new__(DistributedQuestAI)
        quest.doId = 5
        quest.ownerId = 1
        quest.air = Mock()
        quest.air.getAvatarIdFromSender.return_value = senderId
        return quest

    def test_owner_finishes_scene(self):
        import builtins
        from unittest.mock import patch

        messenger = Mock()
        with patch.object(builtins, 'messenger', messenger, create=True):
            self.makeQuest(1).doneFinalizeScene()

        messenger.send.assert_called_once_with('quest-finalize-5')

    def test_other_avatar_cannot_finish_scene(self):
        import builtins
        from unittest.mock import patch

        messenger = Mock()
        quest = self.makeQuest(2)
        with patch.object(builtins, 'messenger', messenger, create=True):
            quest.doneFinalizeScene()

        messenger.send.assert_not_called()
        quest.air.writeServerEvent.assert_called_once()


if __name__ == '__main__':
    unittest.main()
