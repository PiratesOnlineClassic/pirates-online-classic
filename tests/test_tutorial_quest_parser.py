import subprocess
import sys
import unittest
from tests import REPO_ROOT


class TutorialQuestParserTests(unittest.TestCase):
    def test_client_import_reads_quest_scripts_from_vfs(self):
        script = """
from panda3d.core import loadPrcFileData
loadPrcFileData('tutorial-test', 'window-type none\\naudio-library-name null')
from direct.showbase.ShowBase import ShowBase
ShowBase(windowType='none')
from pirates.quest import QuestParser
assert 'quest_tut_blacksmith_intro_100_v2' in QuestParser.lineDict
"""
        subprocess.run(
            [sys.executable, '-c', script],
            cwd=str(REPO_ROOT),
            check=True,
        )


if __name__ == '__main__':
    unittest.main()
