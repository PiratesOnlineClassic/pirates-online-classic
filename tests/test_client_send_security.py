import builtins
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')


def _stubModule(name, **attrs):
    module = types.ModuleType(name)
    module.__dict__.update(attrs)
    return module


# Without the game resources (WeaponGlobals.pkl) and libotp the full AI import
# chain cannot load; stand in for the few leaf modules that need them while the
# avatar module is imported, then drop everything imported here so other tests
# in the same session get the real modules.
_stubs = {
    'pirates.world.DistributedGameAreaAI': _stubModule('pirates.world.DistributedGameAreaAI',
        DistributedGameAreaAI=type('DistributedGameAreaAI', (object,), {})),
    'pirates.leveleditor.ObjectList': _stubModule('pirates.leveleditor.ObjectList'),
    'otp.avatar.Avatar': _stubModule('otp.avatar.Avatar', Avatar=type('Avatar', (object,), {})),
}

try:
    from pirates.battle import WeaponGlobals
except Exception:
    WeaponGlobals = _stubModule('pirates.battle.WeaponGlobals')
    WeaponGlobals.__getattr__ = lambda name: (lambda *args, **kw: 0)
    _stubs['pirates.battle.WeaponGlobals'] = WeaponGlobals

_previousModules = set(sys.modules)
_replacedModules = {name: sys.modules.get(name) for name in _stubs}
sys.modules.update(_stubs)
try:
    with patch.object(builtins.loader, 'loadFont', Mock()):
        from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI
        from pirates.pirate.HumanDNA import HumanDNA
        from pirates.pirate.HumanDNAAI import HumanDNAAI
finally:
    for _name in set(sys.modules) - _previousModules:
        sys.modules.pop(_name, None)

    for _name, _module in _replacedModules.items():
        if _module is not None:
            sys.modules[_name] = _module

from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


AV_ID = 100000001
ACCOUNT_ID = 5


def makeAir(senderAvId=AV_ID, accountId=ACCOUNT_ID):
    sender = (accountId << 32) | senderAvId
    return SimpleNamespace(
        getAccountIdFromSender=lambda: (sender >> 32) & 0xFFFFFFFF,
        getAvatarIdFromSender=lambda: sender & 0xFFFFFFFF,
        logPotentialHacker=Mock(),
        questMgr=Mock())


class FakeDNAAvatar(HumanDNAAI):

    def __init__(self, air, tutorial):
        HumanDNA.__init__(self)
        self.air = air
        self.doId = AV_ID
        self.tutorial = tutorial
        self.sendUpdate = Mock()


class SetTutorialTests(unittest.TestCase):

    def testServerUpdatesAreApplied(self):
        # required fields from the state server have no client sender
        av = FakeDNAAvatar(makeAir(accountId=0, senderAvId=0), PiratesGlobals.TUT_STARTED)
        av.setTutorial(PiratesGlobals.TUT_FINISHED)
        self.assertEqual(av.getTutorial(), PiratesGlobals.TUT_FINISHED)
        av.sendUpdate.assert_not_called()

    def testLegitimateClientCheckpoints(self):
        av = FakeDNAAvatar(makeAir(), PiratesGlobals.TUT_STARTED)
        av.setTutorial(PiratesGlobals.TUT_MADE_PIRATE)
        self.assertEqual(av.getTutorial(), PiratesGlobals.TUT_MADE_PIRATE)

        av = FakeDNAAvatar(makeAir(), PiratesGlobals.TUT_CHAPTER3_STARTED)
        av.setTutorial(PiratesGlobals.TUT_INTRODUCTION_TO_FRIENDS)
        self.assertEqual(av.getTutorial(), PiratesGlobals.TUT_INTRODUCTION_TO_FRIENDS)
        av.air.logPotentialHacker.assert_not_called()
        av.sendUpdate.assert_not_called()

    def testTutorialSkipIsReverted(self):
        av = FakeDNAAvatar(makeAir(), PiratesGlobals.TUT_STARTED)
        av.setTutorial(PiratesGlobals.TUT_FINISHED)
        self.assertEqual(av.getTutorial(), PiratesGlobals.TUT_STARTED)
        av.sendUpdate.assert_called_once_with('setTutorial', [PiratesGlobals.TUT_STARTED])
        av.air.logPotentialHacker.assert_called_once()

    def testTutorialRollbackIsReverted(self):
        av = FakeDNAAvatar(makeAir(), PiratesGlobals.TUT_GOT_SHIP)
        av.setTutorial(PiratesGlobals.TUT_MADE_PIRATE)
        self.assertEqual(av.getTutorial(), PiratesGlobals.TUT_GOT_SHIP)
        av.sendUpdate.assert_called_once_with('setTutorial', [PiratesGlobals.TUT_GOT_SHIP])

    def testOtherAvatarIsReverted(self):
        av = FakeDNAAvatar(makeAir(senderAvId=AV_ID + 1), PiratesGlobals.TUT_STARTED)
        av.setTutorial(PiratesGlobals.TUT_MADE_PIRATE)
        self.assertEqual(av.getTutorial(), PiratesGlobals.TUT_STARTED)
        av.air.logPotentialHacker.assert_called_once()

    def testAIUpdatesBypassValidation(self):
        # the AI advances the tutorial while handling client messages
        av = FakeDNAAvatar(makeAir(), PiratesGlobals.TUT_STARTED)
        av.b_setTutorial(PiratesGlobals.TUT_GOT_CUTLASS)
        self.assertEqual(av.getTutorial(), PiratesGlobals.TUT_GOT_CUTLASS)
        av.air.logPotentialHacker.assert_not_called()


def makePirate(air, **attributes):
    av = SimpleNamespace(air=air, doId=AV_ID, notify=Mock(), sendUpdate=Mock(), **attributes)
    for name in ('_isSenderSelf', '_setGMNameTag', 'getGMNameTag', 'd_updateGMNameTag'):
        setattr(av, name, getattr(DistributedPlayerPirateAI, name).__get__(av))
    return av


class GMNameTagTests(unittest.TestCase):

    def testClientWithoutGMNameTagIsReverted(self):
        av = makePirate(makeAir(), gmNameTagAllowed=False)
        DistributedPlayerPirateAI.updateGMNameTag(av, 1, 'red', 'Game Master')
        self.assertFalse(hasattr(av, 'gmNameTagState'))
        av.sendUpdate.assert_called_once_with('updateGMNameTag', [0, '', ''])
        av.air.logPotentialHacker.assert_called_once()

    def testAllowedClientIsApplied(self):
        av = makePirate(makeAir(), gmNameTagAllowed=True)
        DistributedPlayerPirateAI.updateGMNameTag(av, 1, 'red', 'Game Master')
        self.assertEqual(av.getGMNameTag(), [1, 'red', 'Game Master'])
        av.sendUpdate.assert_not_called()

    def testMagicWordToggleOff(self):
        # toggleGM disallows the nametag and then turns it off from the AI
        av = makePirate(makeAir(), gmNameTagAllowed=False)
        DistributedPlayerPirateAI.b_updateGMNameTag(av, 0, 'red', 'Game Master')
        self.assertEqual(av.getGMNameTag(), [0, 'red', 'Game Master'])
        av.air.logPotentialHacker.assert_not_called()


class GiveDefaultQuestTests(unittest.TestCase):

    def makeAvatar(self, air, tutorial=PiratesGlobals.TUT_STARTED):
        av = makePirate(air, getTutorial=lambda: tutorial, getInventory=lambda: Mock(),
            getQuestHistory=lambda: [])
        air.questMgr.getQuest.return_value = None
        return av

    def testGivenOnce(self):
        air = makeAir()
        av = self.makeAvatar(air)
        DistributedPlayerPirateAI.giveDefaultQuest(av)
        DistributedPlayerPirateAI.giveDefaultQuest(av)
        self.assertEqual(air.questMgr._giveRewards.call_count, 1)
        self.assertEqual(air.questMgr.createQuest.call_count, 1)
        air.logPotentialHacker.assert_not_called()

    def testOtherAvatarRejected(self):
        air = makeAir(senderAvId=AV_ID + 1)
        av = self.makeAvatar(air)
        DistributedPlayerPirateAI.giveDefaultQuest(av)
        air.questMgr.createQuest.assert_not_called()
        air.logPotentialHacker.assert_called_once()

    def testTutorialSkipRejected(self):
        air = makeAir()
        av = self.makeAvatar(air, tutorial=PiratesGlobals.TUT_GOT_SEACHEST)
        DistributedPlayerPirateAI.giveDefaultQuest(av)
        air.questMgr._giveRewards.assert_not_called()
        air.logPotentialHacker.assert_called_once()

    def testActiveQuestNotDuplicated(self):
        air = makeAir()
        av = self.makeAvatar(air)
        air.questMgr.getQuest.return_value = Mock()
        DistributedPlayerPirateAI.giveDefaultQuest(av)
        air.questMgr._giveRewards.assert_not_called()


class AvatarRequestTests(unittest.TestCase):

    def testSpendSkillPointForOtherAvatarRejected(self):
        air = makeAir(senderAvId=AV_ID + 1)
        inventory = Mock()
        av = makePirate(air, getInventory=lambda: inventory)
        DistributedPlayerPirateAI.spendSkillPoint(av, InventoryType.begin_WeaponSkillCutlass)
        inventory.b_setStackQuantity.assert_not_called()
        air.logPotentialHacker.assert_called_once()

    def testDrawUnownedWeaponRejected(self):
        air = makeAir()
        inventory = Mock()
        inventory.getStackQuantity.return_value = 0
        av = makePirate(air, weapon=Mock(), getInventory=lambda: inventory,
            b_setCurrentWeapon=Mock())
        DistributedPlayerPirateAI.requestCurrentWeapon(av, InventoryType.CutlassWeaponL6, 1)
        av.b_setCurrentWeapon.assert_not_called()
        air.logPotentialHacker.assert_called_once()

    def testDrawOwnedWeapon(self):
        air = makeAir()
        inventory = Mock()
        inventory.getStackQuantity.return_value = 1
        av = makePirate(air, weapon=Mock(), getInventory=lambda: inventory,
            b_setCurrentWeapon=Mock())
        DistributedPlayerPirateAI.requestCurrentWeapon(av, InventoryType.CutlassWeaponL1, 1)
        av.b_setCurrentWeapon.assert_called_once_with(InventoryType.CutlassWeaponL1, 1)

    def testSheathUnownedWeaponAllowed(self):
        av = makePirate(makeAir(), weapon=Mock(), getInventory=lambda: Mock(
            getStackQuantity=Mock(return_value=0)), b_setCurrentWeapon=Mock())
        DistributedPlayerPirateAI.requestCurrentWeapon(av, InventoryType.CutlassWeaponL1, 0)
        av.b_setCurrentWeapon.assert_called_once_with(InventoryType.CutlassWeaponL1, 0)

    def testUseTonicRejectsNonTonics(self):
        air = makeAir()
        inventory = Mock()
        inventory.getStackQuantity.return_value = 10
        av = makePirate(air, b_setHp=Mock())
        with patch.object(builtins, 'base', SimpleNamespace(air=SimpleNamespace(
                inventoryManager=SimpleNamespace(getInventory=lambda doId: inventory))), create=True):
            DistributedPlayerPirateAI.useTonic(av, InventoryType.ShipRepairKit)

        inventory.b_setStackQuantity.assert_not_called()
        av.b_setHp.assert_not_called()
        air.logPotentialHacker.assert_called_once()


if __name__ == '__main__':
    unittest.main()
