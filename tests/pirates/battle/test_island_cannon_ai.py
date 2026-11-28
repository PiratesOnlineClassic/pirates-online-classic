import builtins
import importlib
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')


def _stubModule(name, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)

    packageName, moduleName = name.rsplit('.', 1)
    sys.modules[name] = module
    setattr(importlib.import_module(packageName), moduleName, module)


def _ensureTestModules():
    # WeaponGlobals and ObjectList need game resources (pkl files, libotp)
    # which are not available to the unit tests.
    try:
        importlib.import_module('pirates.battle.WeaponGlobals')
    except (IOError, OSError):
        _stubModule('pirates.battle.WeaponGlobals', getAttackHullHP=lambda *args: 0,
            getAttackSailHP=lambda *args: 0, HULL_HP_INDEX=0, SAIL_HP_INDEX=1,
            WEAPON_MOVIE_CLEAR=0, WEAPON_MOVIE_START=1, WEAPON_MOVIE_STOP=2,
            **{'__skillInfo': {}})

    try:
        importlib.import_module('pirates.leveleditor.ObjectList')
    except ImportError:
        _stubModule('pirates.leveleditor.ObjectList')


_ensureTestModules()

from pirates.battle import WeaponGlobals
from pirates.battle.DistributedIslandCannonAI import DistributedIslandCannonAI
from pirates.battle.DistributedFortCannonAI import DistributedFortCannonAI
from pirates.piratesbase import PiratesGlobals


def makeCannon(cls=DistributedIslandCannonAI):
    cannon = cls.__new__(cls)
    cls.__init__(cannon, SimpleNamespace(
        dclassesByName={cls.__name__: None},
        doId2do={},
        getAvatarExitEvent=lambda avatarId: 'distObjDelete-%d' % avatarId,
        getAvatarIdFromSender=Mock(return_value=0),
        logPotentialHacker=Mock()))
    cannon.doId = 700
    cannon.sendUpdate = Mock()
    cannon.sendUpdateToAvatarId = Mock()
    cannon.acceptOnce = Mock()
    cannon.ignore = Mock()
    return cannon


class DistributedIslandCannonAITests(unittest.TestCase):

    def test_required_fields(self):
        cannon = makeCannon()
        cannon.b_setCannonIndex(3)
        cannon.b_setIslandId(20)
        cannon.b_setIsDestructable(1)
        self.assertEqual(cannon.getCannonIndex(), 3)
        self.assertEqual(cannon.getIslandId(), 20)
        self.assertEqual(cannon.getIsDestructable(), 1)
        self.assertEqual(cannon.getDestructState(), PiratesGlobals.CANNON_STATE_NORMAL)
        self.assertEqual(cannon.sendUpdate.call_args_list, [
            call('setCannonIndex', [3]), call('setIslandId', [20]), call('setIsDestructable', [1])])

    def test_interaction_starts_and_stops_weapon(self):
        cannon = makeCannon()
        avatar = SimpleNamespace(doId=10)
        self.assertEqual(cannon.handleRequestInteraction(avatar, 0, 0), cannon.ACCEPT)
        cannon.sendUpdateToAvatarId.assert_called_with(10, 'setMovie', [WeaponGlobals.WEAPON_MOVIE_START, 10])
        cannon.userId = 10

        # somebody else can't jump on the cannon while it is used
        self.assertEqual(cannon.handleRequestInteraction(SimpleNamespace(doId=11), 0, 0), cannon.DENY)

        self.assertEqual(cannon.handleRequestExit(avatar), cannon.ACCEPT)
        cannon.sendUpdateToAvatarId.assert_called_with(10, 'setMovie', [WeaponGlobals.WEAPON_MOVIE_STOP, 10])

    def test_user_leaving_district_frees_cannon(self):
        cannon = makeCannon()
        cannon.handleRequestInteraction(SimpleNamespace(doId=10), 0, 0)
        cannon.userId = 10
        cannon._handleUserExit(10)
        self.assertEqual(cannon.userId, 0)
        self.assertEqual(cannon.getMovie(), [WeaponGlobals.WEAPON_MOVIE_CLEAR, 0])
        self.assertEqual(cannon.handleRequestInteraction(SimpleNamespace(doId=11), 0, 0), cannon.ACCEPT)

    def test_indestructable_cannon_ignores_hits(self):
        cannon = makeCannon()
        cannon.air.doId2do[10] = SimpleNamespace(doId=10)
        cannon.air.getAvatarIdFromSender.return_value = 10
        cannon.hitByProjectile()
        self.assertFalse(cannon.isDestroyed())
        cannon.air.logPotentialHacker.assert_called_once()

    def test_hit_destroys_ejects_and_repairs(self):
        cannon = makeCannon()
        cannon.setIsDestructable(1)
        cannon.userId = 11
        cannon.mode = WeaponGlobals.WEAPON_MOVIE_START
        cannon.air.doId2do[10] = SimpleNamespace(doId=10)
        cannon.air.getAvatarIdFromSender.return_value = 10

        with patch.object(builtins, 'taskMgr', create=True) as taskMgr:
            cannon.hitByProjectile()
            taskMgr.doMethodLater.assert_called_once_with(cannon.repairTime, cannon._repairCannonTask,
                cannon.uniqueName('repairCannon'))

            self.assertTrue(cannon.isDestroyed())
            self.assertEqual(cannon.userId, 0)
            cannon.sendUpdate.assert_any_call('setDestructState', [PiratesGlobals.CANNON_STATE_DESTRUCT])
            cannon.sendUpdateToAvatarId.assert_any_call(11, 'setMovie', [WeaponGlobals.WEAPON_MOVIE_STOP, 11])

            # a destroyed cannon can't be used
            self.assertEqual(cannon.handleRequestInteraction(SimpleNamespace(doId=10), 0, 0), cannon.DENY)

            cannon.repairCannon()

        self.assertFalse(cannon.isDestroyed())
        cannon.sendUpdate.assert_called_with('setDestructState', [PiratesGlobals.CANNON_STATE_NORMAL])


class DistributedFortCannonAITests(unittest.TestCase):

    def test_fort_cannon_stays_destroyed_with_fort(self):
        cannon = makeCannon(DistributedFortCannonAI)
        fort = Mock()
        fort.isDestroyed.return_value = True
        cannon.air.doId2do[50] = fort
        cannon.b_setFortId(50)
        self.assertEqual(cannon.getFort(), fort)
        cannon.sendUpdate.assert_called_with('setFortId', [50])

        with patch.object(builtins, 'taskMgr', create=True):
            cannon.destroyCannon(repair=False)
            cannon.repairCannon()

        self.assertTrue(cannon.isDestroyed())

        fort.isDestroyed.return_value = False
        with patch.object(builtins, 'taskMgr', create=True):
            cannon.repairCannon()

        self.assertFalse(cannon.isDestroyed())


if __name__ == '__main__':
    unittest.main()
