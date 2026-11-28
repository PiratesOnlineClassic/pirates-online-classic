import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from panda3d.core import Filename, NodePath, VirtualFileSystem, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

# these tests exercise the real skill tables, they need the game resources...
HAVE_RESOURCES = VirtualFileSystem.getGlobalPtr().exists(Filename('../resources/phase_2/etc/WeaponGlobals.pkl'))

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

with patch.object(builtins.loader, 'loadFont', Mock()):
    from pirates.battle import BattleManagerAI as battle_manager_module
    from pirates.battle.BattleManagerAI import BattleManagerAI

from pirates.battle.BattleRandom import BattleRandom
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

WeaponGlobals = battle_manager_module.WeaponGlobals


class FakeInventory:

    def __init__(self, stacks=None):
        self.stacks = dict(stacks or {})

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity


class FakeClock:

    def __init__(self):
        self.now = 1000.0

    def getFrameTime(self):
        return self.now


def makeAvatar(cls=DistributedBattleAvatarAI, doId=100, level=10, hp=500, isNpc=False, world=True):
    avatar = cls.__new__(cls)
    NodePath.__init__(avatar, 'avatar-%d' % doId)
    DistributedBattleAvatarAI.__init__(avatar, MagicMock())
    avatar.doId = doId
    avatar.isNpc = isNpc
    avatar.level = level
    avatar.hp = hp
    avatar.maxHp = hp
    avatar.mojo = 100
    avatar.maxMojo = 100
    avatar.swiftness = 1
    avatar.maxSwiftness = 1
    avatar.battleRandom = BattleRandom(doId)
    avatar.sendUpdate = Mock()
    avatar.getWorld = Mock(return_value=Mock() if world else None)
    avatar.getDamagable = Mock(return_value=True)
    avatar.getInventory = Mock(return_value=FakeInventory())
    return avatar


def makePlayer(doId=100, stacks=None, weaponId=InventoryType.CutlassWeaponL1, **kwargs):
    player = makeAvatar(DistributedPlayerPirateAI, doId=doId, **kwargs)
    player.inventory = FakeInventory(stacks)
    player.getInventory = lambda: player.inventory
    player.currentWeaponId = weaponId
    player.isWeaponDrawn = True
    player.zombie = 0
    player.stickyTargets = []
    player.skillRechargeTimes = {}
    player._team = PiratesGlobals.PLAYER_TEAM
    return player


@unittest.skipUnless(HAVE_RESOURCES, 'the game resources are required')
class SkillEffectIdTests(unittest.TestCase):

    def test_effect_ids_come_from_the_buff_list(self):
        avatar = makeAvatar()
        avatar.skillEffects = [[WeaponGlobals.C_POISON, 10, 0, 5], [WeaponGlobals.C_POISON, 10, 0, 6],
            [WeaponGlobals.C_CURSE, 60, 0, 5]]
        self.assertEqual(avatar.getSkillEffectIds(), [WeaponGlobals.C_POISON, WeaponGlobals.C_CURSE])

        # the required field getter still returns the buffs the client expects
        self.assertEqual(len(avatar.getSkillEffects()), 3)

    def test_blind_attacker_hits_less(self):
        manager = BattleManagerAI.__new__(BattleManagerAI)
        attacker = makeAvatar(isNpc=True)
        target = makePlayer(doId=200)
        attacker.battleRandom = Mock(getRandom=Mock(return_value=0.8))

        # pistol shot accuracy is 80, a roll of 0.8 still hits...
        self.assertEqual(manager.willWeaponHit(attacker, target, InventoryType.PistolShoot, 0, 0), WeaponGlobals.RESULT_HIT)
        attacker.skillEffects = [[WeaponGlobals.C_BLIND, 10, 0, 200]]
        self.assertEqual(manager.willWeaponHit(attacker, target, InventoryType.PistolShoot, 0, 0), WeaponGlobals.RESULT_MISS)

    def test_curse_and_take_cover_modify_damage(self):
        manager = BattleManagerAI.__new__(BattleManagerAI)
        attacker = makePlayer(level=10)
        target = makeAvatar(doId=200, isNpc=True, level=10)
        target.avatarType = Mock(isA=Mock(return_value=False))
        attacker.battleRandom = Mock(getRandom=Mock(return_value=1.0))
        with patch.object(battle_manager_module.EnemyGlobals, 'getMonsterClass', Mock(return_value=None)):
            base = manager.getModifiedSkillEffects(attacker, target, InventoryType.CutlassHack, 0)[1][0]
            target.skillEffects = [[WeaponGlobals.C_CURSE, 60, 0, 300]]
            cursed = manager.getModifiedSkillEffects(attacker, target, InventoryType.CutlassHack, 0)[1][0]
            target.skillEffects = [[WeaponGlobals.C_TAKECOVER, 10, 0, 300]]
            covered = manager.getModifiedSkillEffects(attacker, target, InventoryType.CutlassHack, 0)[1][0]

        self.assertLess(base, 0)
        self.assertEqual(cursed, base + int(base * WeaponGlobals.CURSED_DAM_AMP))
        # take cover zeroes the damage, the comparative level modifier still deals 1
        self.assertEqual(covered, -1)


if __name__ == '__main__':
    unittest.main()
