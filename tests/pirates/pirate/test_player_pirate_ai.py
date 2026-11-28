import builtins
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from panda3d.core import Filename, NodePath, VirtualFileSystem, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')


def _stubWeaponGlobals():
    # WeaponGlobals reads WeaponGlobals.pkl from the game resources at import
    # time; when the resources are unavailable fall back to a stub module.
    if 'pirates.battle.WeaponGlobals' in sys.modules:
        return

    searchPath = '../resources/phase_2/etc'
    if VirtualFileSystem.getGlobalPtr().exists(Filename(searchPath + '/WeaponGlobals.pkl')):
        return

    module = types.ModuleType('pirates.battle.WeaponGlobals')

    def __getattr__(name):
        if name.startswith('__'):
            raise AttributeError(name)

        value = MagicMock(name='WeaponGlobals.%s' % name)
        setattr(module, name, value)
        return value

    module.__getattr__ = __getattr__
    sys.modules['pirates.battle.WeaponGlobals'] = module
    import pirates.battle
    pirates.battle.WeaponGlobals = module


_stubWeaponGlobals()

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

with patch.object(builtins.loader, 'loadFont', Mock()):
    from pirates.battle import BattleManagerAI

from pirates.battle.Teamable import Teamable
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import PlayerPirateGameFSMAI as fsm_module
from pirates.pirate import DistributedPlayerPirateAI as player_pirate_module
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI
from pirates.pirate.PlayerPirateGameFSMAI import PlayerPirateGameFSMAI
from pirates.uberdog.UberDogGlobals import InventoryType
from otp.chat import ChatFilter

from pirates.uberdog import InventoryInit
from pirates.reputation import ReputationGlobals

# patch the WeaponGlobals module the code under test actually uses...
WeaponGlobals = player_pirate_module.WeaponGlobals


class FakeInventory:

    def __init__(self, stacks=None):
        self.stacks = dict(stacks or {})
        self.accumulators = {}

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def getStackLimit(self, stackType):
        return InventoryInit.StackLimits.get(stackType, 0)

    def getReputation(self, repType):
        return self.accumulators.get(repType, 0)

    def getGoldInPocket(self):
        return self.getStackQuantity(InventoryType.GoldInPocket)

    def setGoldInPocket(self, quantity):
        self.b_setStackQuantity(InventoryType.GoldInPocket, quantity)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity

    def getTonics(self):
        return dict((tonicId, self.getStackQuantity(tonicId)) for tonicId in InventoryType.Potions)


def makePlayer(doId=100, stacks=None, hp=100, maxHp=100, mojo=50, maxMojo=100, state='LandRoam'):
    player = DistributedPlayerPirateAI.__new__(DistributedPlayerPirateAI)
    NodePath.__init__(player, 'player-%d' % doId)
    Teamable.__init__(player)
    player.doId = doId
    player.isNpc = False
    player.currentWeaponId = 0
    player.isWeaponDrawn = False
    player._siegeTeam = 0
    player.currentAmmo = 0
    player.currentTarget = None
    player.hp = hp
    player.maxHp = maxHp
    player.quietly = False
    player.immortal = False
    player.mojo = mojo
    player.maxMojo = maxMojo
    player.power = 0
    player.maxPower = 0
    player.level = 10
    player.tutorial = PiratesGlobals.TUT_FINISHED
    player.weapon = None
    player.toonUpTask = None
    player.skillRechargeTimes = {}
    player.inventory = FakeInventory(stacks)
    player.getInventory = lambda: player.inventory
    player.isPaid = Mock(return_value=True)
    player.isGenerated = Mock(return_value=False)
    player.sendUpdate = Mock()
    player.sendUpdateToAvatarId = Mock()
    player.gameFSM = Mock(getCurrentOrNextState=Mock(return_value=state))
    player.air = SimpleNamespace(getAvatarIdFromSender=Mock(return_value=doId), logPotentialHacker=Mock(),
        battleMgr=Mock(getModifiedRechargeTime=Mock(return_value=50.0)),
        inventoryManager=Mock(getInventory=Mock(return_value=player.inventory)))
    return player


class WeaponTests(unittest.TestCase):

    def test_weapon_in_inventory_is_drawn(self):
        player = makePlayer(stacks={InventoryType.CutlassWeaponL1: 1})
        with patch.object(WeaponGlobals, 'getRepId', return_value=InventoryType.CutlassRep):
            player.requestCurrentWeapon(InventoryType.CutlassWeaponL1, 1)

        self.assertEqual(player.getCurrentWeapon(), [InventoryType.CutlassWeaponL1, True])
        player.sendUpdate.assert_called_with('setCurrentWeapon', [InventoryType.CutlassWeaponL1, True])

    def test_weapon_without_inventory_object_is_still_set(self):
        player = makePlayer(stacks={InventoryType.CutlassWeaponL1: 1})
        player.weapon = Mock()
        with patch.object(WeaponGlobals, 'getRepId', return_value=InventoryType.CutlassRep):
            player.requestCurrentWeapon(InventoryType.CutlassWeaponL1, 0)

        player.weapon.d_setMovie.assert_called_once_with(WeaponGlobals.WEAPON_MOVIE_STOP, player.doId)
        self.assertEqual(player.getCurrentWeapon(), [InventoryType.CutlassWeaponL1, False])

    def test_unowned_weapon_is_not_drawn(self):
        # a pirate who has not yet been given the cutlass by will turner...
        player = makePlayer()
        with patch.object(WeaponGlobals, 'getRepId', return_value=InventoryType.CutlassRep):
            player.requestCurrentWeapon(InventoryType.CutlassWeaponL1, 1)

        self.assertEqual(player.getCurrentWeapon(), [0, False])

    def test_fists_are_always_available(self):
        player = makePlayer()
        with patch.object(WeaponGlobals, 'getRepId', return_value=InventoryType.MeleeRep):
            player.requestCurrentWeapon(InventoryType.MeleeWeaponL1, 1)

        self.assertEqual(player.getCurrentWeapon(), [InventoryType.MeleeWeaponL1, True])

    def test_no_weapon_cannot_be_drawn(self):
        player = makePlayer()
        player.requestCurrentWeapon(0, 1)
        self.assertEqual(player.getCurrentWeapon(), [0, False])

    def test_weapon_request_from_another_avatar_is_rejected(self):
        player = makePlayer(stacks={InventoryType.CutlassWeaponL1: 1})
        player.air.getAvatarIdFromSender.return_value = 999
        player.requestCurrentWeapon(InventoryType.CutlassWeaponL1, 1)
        player.air.logPotentialHacker.assert_called_once()
        self.assertEqual(player.getCurrentWeapon(), [0, False])

    def test_current_ammo_must_match_weapon(self):
        player = makePlayer(stacks={InventoryType.PistolLeadShot: 2})
        player.currentWeaponId = InventoryType.PistolWeaponL1
        with patch.object(WeaponGlobals, 'getRepId', return_value=InventoryType.PistolRep), \
                patch.object(WeaponGlobals, 'getSkillReputationCategoryId', return_value=InventoryType.CutlassRep):
            player.requestCurrentAmmo(InventoryType.PistolLeadShot)

        self.assertEqual(player.getCurrentAmmo(), 0)
        with patch.object(WeaponGlobals, 'getRepId', return_value=InventoryType.PistolRep), \
                patch.object(WeaponGlobals, 'getSkillReputationCategoryId', return_value=InventoryType.PistolRep):
            player.requestCurrentAmmo(InventoryType.PistolLeadShot)

        self.assertEqual(player.getCurrentAmmo(), InventoryType.PistolLeadShot)


class TonicTests(unittest.TestCase):

    def useTonic(self, player, tonicId=InventoryType.Potion1, heal=50):
        with patch.object(WeaponGlobals, 'getAttackSelfHP', return_value=heal), \
                patch.object(WeaponGlobals, 'getAttackSelfMojo', return_value=0), \
                patch.object(WeaponGlobals, 'getAttackSelfPower', return_value=0):
            return player.useTonic(tonicId)

    def test_tonic_heals_and_is_consumed(self):
        player = makePlayer(stacks={InventoryType.Potion1: 2}, hp=20)
        self.assertTrue(self.useTonic(player))
        self.assertEqual(player.getHp()[0], 70)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.Potion1), 1)

    def test_tonic_recharges(self):
        player = makePlayer(stacks={InventoryType.Potion1: 2}, hp=20)
        self.assertTrue(self.useTonic(player))
        self.assertFalse(self.useTonic(player))
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.Potion1), 1)

    def test_invalid_or_missing_tonic(self):
        player = makePlayer(hp=20)
        self.assertFalse(self.useTonic(player, tonicId=InventoryType.CutlassWeaponL1))
        self.assertFalse(self.useTonic(player))
        self.assertEqual(player.air.logPotentialHacker.call_count, 2)

    def test_groggy_tonic_heals_to_adjusted_max(self):
        player = makePlayer(stacks={InventoryType.Potion1: 1, InventoryType.Vitae_Level: 1}, hp=20)
        self.assertTrue(self.useTonic(player, heal=500))
        self.assertEqual(player.getHp()[0], 75)

    def test_defeated_avatar_cannot_use_tonics(self):
        player = makePlayer(stacks={InventoryType.Potion1: 1}, hp=0)
        self.assertFalse(self.useTonic(player))

    def test_best_tonic_without_tonics(self):
        player = makePlayer(hp=20)
        self.assertEqual(player.getBestTonic(), 0)
        player.useBestTonic()
        player.air.logPotentialHacker.assert_not_called()


class RegenerationTests(unittest.TestCase):

    def test_toon_up_sends_whole_numbers(self):
        player = makePlayer(hp=10, mojo=10)
        player.toonUp(Mock())
        self.assertIsInstance(player.getHp()[0], int)
        self.assertEqual(player.getHp()[0], 10 + int(10 * 10 / 1.25))
        self.assertIsInstance(player.getMojo(), int)

    def test_toon_up_respects_groggy_and_defeat(self):
        player = makePlayer(stacks={InventoryType.Vitae_Level: 1}, hp=74, mojo=74)
        player.toonUp(Mock())
        self.assertEqual(player.getHp()[0], 75)
        self.assertEqual(player.getMojo(), 75)

        player = makePlayer(hp=0)
        player.toonUp(Mock())
        self.assertEqual(player.getHp()[0], 0)

    def test_only_voodoo_regenerates_while_targeting(self):
        player = makePlayer(hp=10, mojo=10)
        player.currentTarget = SimpleNamespace(doId=1000)
        player.toonUp(Mock())
        self.assertEqual(player.getHp()[0], 10)
        self.assertEqual(player.getMojo(), 10 + int(8 * 10 / 1.35) // player.BattleMojoRegenDivisor)

    def test_only_voodoo_regenerates_with_a_weapon_drawn(self):
        player = makePlayer(hp=10, mojo=10, state='Battle')
        player.toonUp(Mock())
        self.assertEqual(player.getHp()[0], 10)
        self.assertGreater(player.getMojo(), 10)

    def test_regeneration_runs_in_battle(self):
        player = makePlayer()
        player.startToonUp = Mock()
        player.stopToonUp = Mock()
        PlayerPirateGameFSMAI.enterBattle(SimpleNamespace(avatar=player))
        player.startToonUp.assert_called_once_with()
        PlayerPirateGameFSMAI.exitBattle(SimpleNamespace(avatar=player))
        player.stopToonUp.assert_called_once_with()

    def test_toon_up_does_not_start_when_defeated(self):
        player = makePlayer(state='Death')
        player.startToonUp = Mock()
        player.currentTarget = SimpleNamespace(resetComboLevel=Mock())
        player.air.doId2do = {}
        player.setCurrentTarget(0)
        player.startToonUp.assert_not_called()


class SkillPointTests(unittest.TestCase):

    def test_combo_skills_are_learned_in_order(self):
        player = makePlayer(stacks={InventoryType.UnspentCutlass: 2, InventoryType.CutlassSlash: 1,
            InventoryType.CutlassCleave: 1})
        player.spendSkillPoint(InventoryType.CutlassCleave)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassCleave), 1)

        player.inventory.stacks[InventoryType.CutlassSlash] = 2
        player.spendSkillPoint(InventoryType.CutlassCleave)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassCleave), 2)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.UnspentCutlass), 1)
        player.sendUpdateToAvatarId.assert_called_with(player.doId, 'spentSkillPoint', [InventoryType.CutlassCleave])

    def test_locked_skills_cannot_be_trained(self):
        player = makePlayer(stacks={InventoryType.UnspentCutlass: 2})
        player.spendSkillPoint(InventoryType.CutlassBladestorm)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassBladestorm), 0)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.UnspentCutlass), 2)

    def test_skill_rank_is_capped(self):
        player = makePlayer(stacks={InventoryType.UnspentCutlass: 2, InventoryType.CutlassSweep: 6})
        player.spendSkillPoint(InventoryType.CutlassSweep)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassSweep), 6)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.UnspentCutlass), 2)

    def test_freebooter_skill_spend_limit(self):
        # a level 10 freebooter has earned 9 skill points, having spent
        # six of them it may not spend any more, see SkillPage.addPoint...
        player = makePlayer(stacks={InventoryType.UnspentCutlass: 3, InventoryType.CutlassSweep: 1})
        player.isPaid.return_value = False
        player.inventory.accumulators[InventoryType.CutlassRep] = ReputationGlobals.TotalReputationAtLevel[10]
        with patch.object(WeaponGlobals, 'canFreeUse', return_value=True):
            player.spendSkillPoint(InventoryType.CutlassSweep)
            self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassSweep), 1)

            player.inventory.stacks[InventoryType.UnspentCutlass] = 4
            player.spendSkillPoint(InventoryType.CutlassSweep)
            self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassSweep), 2)

    def test_freebooter_cannot_train_paid_skills(self):
        player = makePlayer(stacks={InventoryType.UnspentCutlass: 2, InventoryType.CutlassSweep: 1})
        player.isPaid.return_value = False
        with patch.object(WeaponGlobals, 'canFreeUse', return_value=False):
            player.spendSkillPoint(InventoryType.CutlassSweep)

        self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassSweep), 1)


    def test_tutorial_pirate_trains_sweep_first(self):
        player = makePlayer(stacks={InventoryType.UnspentCutlass: 2, InventoryType.CutlassHack: 2,
            InventoryType.CutlassSweep: 1})
        player.tutorial = PiratesGlobals.TUT_MET_JOLLY_ROGER
        player.spendSkillPoint(InventoryType.CutlassHack)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassHack), 2)

        player.spendSkillPoint(InventoryType.CutlassSweep)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassSweep), 2)

        # once Sweep has been trained the other skills may be trained as well...
        player.spendSkillPoint(InventoryType.CutlassHack)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassHack), 3)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.UnspentCutlass), 0)

    def test_sweep_rule_ends_with_the_tutorial_cutlass(self):
        player = makePlayer(stacks={InventoryType.UnspentCutlass: 1, InventoryType.CutlassHack: 2,
            InventoryType.CutlassSweep: 1})
        player.tutorial = PiratesGlobals.TUT_GOT_CUTLASS
        player.spendSkillPoint(InventoryType.CutlassHack)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassHack), 3)


class AccessTests(unittest.TestCase):

    def test_access_follows_the_account(self):
        from otp.otpbase import OTPGlobals
        from pirates.piratesbase import MembershipGlobals

        player = DistributedPlayerPirateAI.__new__(DistributedPlayerPirateAI)
        self.assertEqual(player.getGameAccess(), OTPGlobals.AccessUnknown)
        player.setGameAccess(OTPGlobals.AccessVelvetRope)
        with patch.object(MembershipGlobals, 'wantMembership', return_value=False):
            self.assertTrue(player.isPaid())
            self.assertEqual(player.getAccess(), OTPGlobals.AccessFull)

        with patch.object(MembershipGlobals, 'wantMembership', return_value=True):
            self.assertFalse(player.isPaid())
            self.assertEqual(player.getAccess(), OTPGlobals.AccessVelvetRope)
            player.setGameAccess(OTPGlobals.AccessFull)
            self.assertTrue(player.isPaid())


class RespecTests(unittest.TestCase):

    def makeTrainedPlayer(self, gold=1000):
        return makePlayer(stacks={
            InventoryType.GoldInPocket: gold,
            InventoryType.UnspentCutlass: 1,
            InventoryType.CutlassHack: 4,
            InventoryType.CutlassSlash: 2,
            InventoryType.CutlassSweep: 3,
            InventoryType.CutlassCleave: 1})

    def test_reset_request_alone_does_not_respec(self):
        # the trainer performs and charges for the respec when its option is selected,
        # see tests/pirates/npc/test_townfolk_respec_ai.py...
        player = self.makeTrainedPlayer()
        player.resetSkillPoints(InventoryType.CutlassRep)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassHack), 4)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.UnspentCutlass), 1)
        self.assertEqual(player.inventory.getGoldInPocket(), 1000)

    def test_respec_of_invalid_weapon_is_rejected(self):
        player = self.makeTrainedPlayer()
        player.resetSkillPoints(InventoryType.MeleeRep)
        self.assertEqual(player.inventory.getGoldInPocket(), 1000)
        player.air.logPotentialHacker.assert_called_once()

    def test_freebooter_skill_cap(self):
        player = makePlayer(stacks={InventoryType.UnspentCutlass: 2, InventoryType.CutlassSweep: 3})
        player.isPaid.return_value = False
        player.spendSkillPoint(InventoryType.CutlassSweep)
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.CutlassSweep), 3)

    def test_flag_first_death(self):
        player = makePlayer()
        player.flagFirstDeath()
        self.assertEqual(player.inventory.getStackQuantity(InventoryType.FirstDeathToken), 1)


class DeathTests(unittest.TestCase):

    def makeFSM(self, player):
        fsm = PlayerPirateGameFSMAI.__new__(PlayerPirateGameFSMAI)
        fsm.avatar = player
        fsm.air = SimpleNamespace(targetMgr=Mock(), uidMgr=Mock())
        fsm.notify = Mock()
        player.getWorld = Mock(return_value=None)
        player.testTeleportFlag = Mock(return_value=False)
        player.clearSkillEffects = Mock()
        return fsm

    def test_alive_avatar_is_not_sent_to_jail(self):
        player = makePlayer(hp=50)
        fsm = self.makeFSM(player)
        player.getParentObj = Mock()
        fsm.enterDeath()
        player.getParentObj.assert_not_called()

    def test_death_away_from_a_game_area_does_not_crash(self):
        player = makePlayer(hp=0)
        fsm = self.makeFSM(player)
        player.getParentObj = Mock(return_value=SimpleNamespace(doId=5))
        fsm.enterDeath()
        fsm.air.targetMgr.clearAttacker.assert_called_once_with(player)
        player.clearSkillEffects.assert_called_once_with()

    def test_defeated_privateer_is_respawned_by_the_siege_manager(self):
        player = makePlayer(hp=0)
        player.setSiegeTeam(1)
        fsm = self.makeFSM(player)
        fsm.air.siegeManager = Mock(handleAvatarDefeated=Mock(return_value=True))
        fsm.air.questMgr = Mock()
        fsm.air.doId2do = {7: 'attacker'}
        fsm.air.targetMgr.getAttackers.return_value = [7]
        player.getParentObj = Mock()
        fsm.enterDeath()
        fsm.air.siegeManager.handleAvatarDefeated.assert_called_once_with(player)
        fsm.air.questMgr.shipPVPPirateDefeated.assert_called_once_with(player, ['attacker'])
        player.getParentObj.assert_not_called()

    def test_jail_restores_avatar(self):
        player = makePlayer(stacks={InventoryType.Vitae_Level: 1}, hp=0, mojo=0)
        fsm = self.makeFSM(player)
        player.testTeleportFlag.return_value = True
        world = Mock(getSpawnPt=Mock(return_value=(1, 2, 3, 4)))
        area = fsm_module.DistributedGameAreaAI.__new__(fsm_module.DistributedGameAreaAI)
        NodePath.__init__(area, 'area')
        area.doId, area.parentId, area.zoneId = 5, 6, 7
        area.getParentObj = Mock(return_value=world)
        area.getUniqueId = Mock(return_value='uid')
        player.getParentObj = Mock(return_value=area)
        player.jailCellIndex = 1
        fsm.enterThrownInJail()
        self.assertEqual(player.getHp()[0], 75)
        self.assertEqual(player.getMojo(), 75)
        world.d_setSpawnInfo.assert_called_once()



class SpeedChatTests(unittest.TestCase):
    """SpeedChat emotes and quest messages are relayed by the AI once checked."""

    SENDER = (5 << 32) | 100

    def makeChatter(self):
        player = makePlayer()
        player.parentId = 10
        player.zoneId = 20
        player.chatFlood = ChatFilter.ChatFlood(limit=10, window=5.0)
        player.air = Mock(ourChannel=4000)
        player.air.getAvatarIdFromSender.return_value = 100
        player.air.getMsgSender.return_value = self.SENDER
        player.dclass = Mock()
        return player

    def test_emote_relayed(self):
        from pirates.piratesbase import PLocalizer
        emoteId = sorted(PLocalizer.EmoteMessagesThirdPerson)[0]
        player = self.makeChatter()
        player.setSCEmote(emoteId)
        player.dclass.getFieldByName.assert_called_once_with('setSCEmote')
        player.dclass.getFieldByName.return_value.aiFormatUpdate.assert_called_once_with(
            100, (10 << 32) | 20, self.SENDER, [emoteId])
        player.air.kickChannel.assert_not_called()

    def test_invalid_emote_ejected_not_relayed(self):
        player = self.makeChatter()
        player.setSCEmote(65535)
        player.air.send.assert_not_called()
        player.air.kickChannel.assert_called_once()

    def test_quest_message_relayed(self):
        from pirates.quest import QuestDB
        questInt = next(q for q, questId in QuestDB.questIntDict.items()
                        if QuestDB.QuestDict.get(questId) and len(QuestDB.QuestDict[questId].getTasks()) == 1)
        player = self.makeChatter()
        player.setSpeedChatQuest(questInt, 1, 0)
        player.dclass.getFieldByName.return_value.aiFormatUpdate.assert_called_once_with(
            100, (10 << 32) | 20, self.SENDER, [questInt, 1, 0])

    def test_invalid_quest_message_ejected_not_relayed(self):
        player = self.makeChatter()
        player.setSpeedChatQuest(65535, 0, 0)
        player.air.send.assert_not_called()
        player.air.kickChannel.assert_called_once()


if __name__ == '__main__':
    unittest.main()
