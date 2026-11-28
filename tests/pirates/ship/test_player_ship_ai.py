import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import ANY, MagicMock, Mock, patch

from panda3d.core import NodePath

from tests.pirates.ship.test_ship_ai import makeAir, makeShip, trackGameState

from pirates.battle import WeaponGlobals
from pirates.battle.DistributedPCCannonAI import DistributedPCCannonAI
from pirates.battle.DistributedShipBroadsideAI import DistributedShipBroadsideAI
from pirates.battle.WeaponBaseAI import WeaponBaseAI
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import ItemId
from pirates.ship import ShipGlobals
from pirates.ship.NPCShipAI import NPCShipAI
from pirates.shipparts.DistributedSailAI import DistributedSailAI
from pirates.shipparts.DistributedSteeringWheelAI import DistributedSteeringWheelAI
from pirates.uberdog import DistributedShipLoaderUD as loader_ud
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.world.DistributedDinghyAI import DistributedDinghyAI


class FakeInventory:

    def __init__(self, stacks=None):
        self.stacks = dict(stacks or {})
        self.gold = 0

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity

    def getReputation(self, repType):
        return self.stacks.get(repType, 0)

    def setReputation(self, repType, quantity):
        self.stacks[repType] = quantity

    def getOverallRep(self):
        return self.getReputation(InventoryType.OverallRep)

    def setOverallRep(self, quantity):
        self.setReputation(InventoryType.OverallRep, quantity)

    def addGoldInPocket(self, gold):
        self.gold += gold


def makeAvatar(air, doId=42, stacks=None, paid=True, crewShipId=0, **kwargs):
    avatar = SimpleNamespace(doId=doId, air=air, inventory=FakeInventory(stacks), crewShipId=crewShipId,
        isPaid=lambda: paid, getLevel=lambda: 10, d_sendReputationMessage=Mock(),
        sendUpdateToAvatarId=Mock(), skillEffects=[])
    avatar.getInventory = lambda: avatar.inventory
    avatar.getCrewShipId = lambda: avatar.crewShipId
    avatar.addSkillEffect = Mock(side_effect=lambda effectId, *args: avatar.skillEffects.append(effectId))
    avatar.hasSkillEffect = lambda effectId: effectId in avatar.skillEffects
    avatar.removeSkillEffect = Mock()
    avatar.__dict__.update(kwargs)
    air.doId2do[doId] = avatar
    return avatar


class _ClockTestCase(unittest.TestCase):

    def setUp(self):
        self.time = 100.0
        self.taskMgr = Mock()
        clock = Mock(getFrameTime=lambda: self.time, getRealTime=lambda: self.time)
        self.patches = [
            patch.object(builtins, 'taskMgr', self.taskMgr, create=True),
            patch.object(builtins, 'globalClock', clock, create=True)]
        for item in self.patches:
            item.start()

    def tearDown(self):
        for item in self.patches:
            item.stop()


class SteeringWheelTests(_ClockTestCase):

    def makeWheel(self, gameState='Adrift'):
        air = makeAir(setAllowClientSend=Mock())
        self.ship = makeShip(air=air, captainId=42, crew=[42, 43], gameState=[gameState, 0, 0])
        trackGameState(self.ship)
        wheel = DistributedSteeringWheelAI.__new__(DistributedSteeringWheelAI)
        NodePath.__init__(wheel, 'wheel')
        wheel.air = air
        wheel.ship = self.ship
        wheel.userId = 0
        wheel.sendUpdate = Mock()
        wheel.sendUpdateToAvatarId = Mock()
        self.ship.steeringWheel = wheel
        self.captain = SimpleNamespace(doId=42)
        self.sailor = SimpleNamespace(doId=43)
        return wheel

    def interact(self, wheel, avatar):
        if wheel.handleRequestInteraction(avatar, 0, 0) != wheel.ACCEPT:
            return False

        wheel.userId = avatar.doId
        wheel.handlePostRequestInteraction(avatar)
        return True

    def exit(self, wheel, avatar):
        if wheel.handleRequestExit(avatar) != wheel.ACCEPT:
            return False

        wheel.userId = 0
        wheel.handlePostRequestExit(avatar)
        return True

    def test_only_crew_may_take_the_wheel(self):
        wheel = self.makeWheel()
        self.assertFalse(self.interact(wheel, SimpleNamespace(doId=99)))
        self.ship.air.writeServerEvent.assert_called_once()

    def test_sinking_ship_cannot_be_steered(self):
        wheel = self.makeWheel(gameState='Sinking')
        self.assertFalse(self.interact(wheel, self.captain))

    def test_captain_takes_the_wheel_from_the_crew(self):
        wheel = self.makeWheel()
        self.assertTrue(self.interact(wheel, self.sailor))
        self.ship.air.setAllowClientSend.assert_called_once_with(43, self.ship, wheel.SteeringFields)
        self.assertEqual(self.ship.clientControllerDoId, 43)

        # nobody else but the captain may take over:
        self.assertFalse(self.interact(wheel, SimpleNamespace(doId=44)))

        self.assertTrue(self.interact(wheel, self.captain))
        wheel.sendUpdateToAvatarId.assert_any_call(43, 'rejectExit', [])
        self.ship.air.setAllowClientSend.assert_called_with(43, self.ship, [])
        self.assertEqual(self.ship.clientControllerDoId, 42)
        self.assertEqual(self.ship.gameState[:2], ['ClientSteering', 42])

        # the displaced helmsman letting go must not release the captain's controls:
        self.assertFalse(self.exit(wheel, self.sailor))
        self.assertEqual(self.ship.clientControllerDoId, 42)

        self.assertTrue(self.exit(wheel, self.captain))
        self.assertEqual(self.ship.clientControllerDoId, 0)
        self.assertEqual(self.ship.gameState[0], 'Adrift')

    def test_letting_go_of_a_sinking_ship_keeps_it_sinking(self):
        wheel = self.makeWheel()
        self.interact(wheel, self.captain)
        self.ship.gameState = ['Sinking', 0, 0]
        self.ship.gameFSM.getCurrentOrNextState.return_value = 'Sinking'
        self.assertTrue(self.exit(wheel, self.captain))
        self.assertEqual(self.ship.clientControllerDoId, 0)
        self.assertEqual(self.ship.gameState[0], 'Sinking')

    def test_departing_helmsman_releases_the_wheel(self):
        wheel = self.makeWheel()
        self.interact(wheel, self.sailor)
        self.ship.ignore = Mock()
        self.ship.air.worldGridManager = Mock()
        self.ship.PutAwayWhenEmpty = False
        self.ship.getParentObj = lambda: None
        avatar = SimpleNamespace(doId=43, getDeleteEvent=lambda: 'delete-43', b_setShipId=Mock(),
            b_setActiveShipId=Mock(), b_setCrewShipId=Mock())
        with patch('pirates.ship.DistributedShipAI.DistributedPlayerPirateAI', SimpleNamespace):
            self.ship._playerDeparted(avatar)

        self.assertEqual(wheel.userId, 0)
        self.assertEqual(self.ship.clientControllerDoId, 0)


SKILL_DATA = {
    InventoryType.SailFullSail: dict(flag=WeaponGlobals.C_FULLSAIL, duration=10, recharge=90.0),
    InventoryType.SailRammingSpeed: dict(flag=WeaponGlobals.C_RAM, duration=5, recharge=90.0),
    InventoryType.SailOpenFire: dict(flag=WeaponGlobals.C_OPENFIRE, duration=6, recharge=60.0, free=0),
    InventoryType.SailBroadsideLeft: dict(flag=0, duration=0, recharge=15.0),
    InventoryType.SailBroadsideRight: dict(flag=0, duration=0, recharge=15.0),
    InventoryType.SailTaskmaster: dict(flag=0, duration=0, recharge=0.03, track=WeaponGlobals.PASSIVE_SKILL_INDEX),
}


def patchShipSkills():
    def get(key, default):
        return lambda skillId, *args: SKILL_DATA.get(skillId, {}).get(key, default)

    return [
        patch.object(WeaponGlobals, 'getSkillEffectFlag', get('flag', 0)),
        patch.object(WeaponGlobals, 'getAttackDuration', get('duration', 0)),
        patch.object(WeaponGlobals, 'getAttackRechargeTime', get('recharge', 0.0)),
        patch.object(WeaponGlobals, 'canFreeUse', get('free', 1)),
        patch.object(WeaponGlobals, 'getSkillTrack', get('track', 0))]


class ShipSkillTests(_ClockTestCase):

    def setUp(self):
        _ClockTestCase.setUp(self)
        for item in patchShipSkills():
            item.start()
            self.patches.append(item)

        air = makeAir()
        self.ship = makeShip(air=air, captainId=42, crew=[42, 43], clientControllerDoId=42)
        self.captain = makeAvatar(air, 42, {
            InventoryType.SailFullSail: 5,
            InventoryType.SailRammingSpeed: 2,
            InventoryType.SailOpenFire: 2,
            InventoryType.SailBroadsideLeft: 2,
            InventoryType.SailTaskmaster: 2}, crewShipId=1000)
        self.sailor = makeAvatar(air, 43, crewShipId=1000)

    def request(self, avatar, skillId):
        self.ship.air.getAvatarIdFromSender.return_value = avatar.doId
        WeaponBaseAI.requestShipSkill(avatar, skillId, 0, 0, self.ship.doId, 0)

    def test_ship_skill_buff_lasts_longer_with_each_rank(self):
        self.request(self.captain, InventoryType.SailFullSail)
        # rank 4: 10 + 10 * 3 / 4
        self.assertEqual(self.ship.skillEffects[0][:2], [WeaponGlobals.C_FULLSAIL, 17])
        self.assertIn(WeaponGlobals.C_FULLSAIL, self.ship.getSkillEffects())

    def test_ship_skill_recharges(self):
        self.request(self.captain, InventoryType.SailFullSail)
        self.ship.skillEffects = []
        self.time += 30
        self.request(self.captain, InventoryType.SailFullSail)
        self.assertEqual(self.ship.skillEffects, [])
        self.time += 60
        self.request(self.captain, InventoryType.SailFullSail)
        self.assertEqual(len(self.ship.skillEffects), 1)

    def test_only_the_helmsman_uses_learned_ship_skills(self):
        self.request(self.sailor, InventoryType.SailFullSail)
        self.assertEqual(self.ship.skillEffects, [])

        # unlearned skills (stack of 1) and passive skills are never used:
        self.captain.inventory.stacks[InventoryType.SailFullSail] = 1
        self.request(self.captain, InventoryType.SailFullSail)
        self.request(self.captain, InventoryType.SailTaskmaster)
        self.assertEqual(self.ship.skillEffects, [])

        # freebooters may not use paid skills:
        self.captain.isPaid = lambda: False
        self.request(self.captain, InventoryType.SailOpenFire)
        self.assertEqual(self.ship.skillEffects, [])

        # nor may an avatar use the skill on a ship they are not aboard:
        self.captain.notify = Mock()
        self.ship.crew = [43]
        self.captain.inventory.stacks[InventoryType.SailFullSail] = 2
        self.request(self.captain, InventoryType.SailFullSail)
        self.assertEqual(self.ship.skillEffects, [])

    def test_open_fire_buffs_the_crew(self):
        self.request(self.captain, InventoryType.SailOpenFire)
        self.assertIn(WeaponGlobals.C_OPENFIRE, self.ship.getSkillEffects())
        self.captain.addSkillEffect.assert_called_once_with(WeaponGlobals.C_OPENFIRE, 6, 42)
        self.sailor.addSkillEffect.assert_called_once_with(WeaponGlobals.C_OPENFIRE, 6, 42)
        self.taskMgr.doMethodLater.assert_any_call(6, self.ship._removeCrewSkillEffect, ANY,
            extraArgs=[WeaponGlobals.C_OPENFIRE, [42, 43]])

        self.ship._removeCrewSkillEffect(WeaponGlobals.C_OPENFIRE, [42, 43])
        self.sailor.removeSkillEffect.assert_called_once_with(WeaponGlobals.C_OPENFIRE)

    def test_ramming_speed_allows_the_ship_to_ram(self):
        target = makeShip(doId=2000, air=self.ship.air, maxHp=1000, hp=1000)
        parent = object()
        self.ship.getParentObj = target.getParentObj = lambda: parent
        self.ship.getDistance = lambda other: 100
        self.ship.air.battleMgr = Mock(getModifiedHullDamage=Mock(return_value=-300))

        self.ship.air.getAvatarIdFromSender.return_value = 42
        self.ship.requestShipRam(target.doId, (0, 0, 0), 0)
        self.assertEqual(target.hp, 1000)

        self.request(self.captain, InventoryType.SailRammingSpeed)
        self.ship.air.getAvatarIdFromSender.return_value = 42
        self.ship.requestShipRam(target.doId, (0, 0, 0), 0)
        self.assertEqual(target.hp, 700)
        self.assertNotIn(WeaponGlobals.C_RAM, self.ship.getSkillEffects())

    def test_broadside_is_fired_once_per_broadside_skill(self):
        broadside = DistributedShipBroadsideAI.__new__(DistributedShipBroadsideAI)
        broadside.air = self.ship.air
        broadside.shipId = self.ship.doId
        broadside.sendUpdate = Mock()
        self.ship.air.getAvatarIdFromSender.return_value = 42

        broadside.requestBroadside(ShipGlobals.BROADSIDE_LEFT, [0], [(0, 0, 0)], 0, 1)
        broadside.sendUpdate.assert_not_called()

        self.request(self.captain, InventoryType.SailBroadsideLeft)
        self.ship.air.getAvatarIdFromSender.return_value = 42
        broadside.requestBroadside(ShipGlobals.BROADSIDE_RIGHT, [0], [(0, 0, 0)], 0, 1)
        broadside.requestBroadside(ShipGlobals.BROADSIDE_LEFT, [0], [(0, 0, 0)], 0, 1)
        broadside.requestBroadside(ShipGlobals.BROADSIDE_LEFT, [0], [(0, 0, 0)], 0, 1)
        broadside.sendUpdate.assert_called_once_with('doBroadside',
            [ShipGlobals.BROADSIDE_LEFT, [0], [(0, 0, 0)], 0, 1, ANY])

    def test_taskmaster_shortens_the_broadside_recharge(self):
        self.assertAlmostEqual(self.ship.getShipSkillRechargeTime(self.captain, InventoryType.SailBroadsideLeft),
            15.0 * (1.0 - 0.03))
        self.ship.skillEffects = [[WeaponGlobals.C_RECHARGE, 10, 0, 42]]
        self.assertAlmostEqual(self.ship.getShipSkillRechargeTime(self.captain, InventoryType.SailFullSail),
            90.0 * WeaponGlobals.POWER_RECHARGE_RATE_REDUCTION)


class SailDamageTests(unittest.TestCase):

    def makeSail(self, ship):
        sail = DistributedSailAI.__new__(DistributedSailAI)
        sail.air = ship.air
        sail.ship = ship
        sail.shipId = ship.doId
        sail.maxHp = sail.hp = 500
        sail.animState = ''
        sail.sendUpdate = Mock()
        ship.air.battleMgr = Mock(getModifiedSailDamage=Mock(return_value=-200))
        return sail

    def test_sail_damage_slows_player_ships(self):
        ship = makeShip(maxSp=500, sp=500)
        sail = self.makeSail(ship)
        sail.projectileWeaponHit(InventoryType.CannonShoot, InventoryType.CannonChainShot, 0, [], 0, 0,
            [0, 0, 1], None)

        self.assertEqual(sail.hp, 300)
        self.assertEqual(ship.sp, 300)
        self.assertEqual(ship.hp, 1000)
        ship.sendUpdate.assert_any_call('setSp', [300])

    def test_npc_ship_sails_damage_the_ship(self):
        ship = makeShip(cls=NPCShipAI, maxSp=0, sp=0, npcShip=1)
        sail = self.makeSail(ship)
        with patch('pirates.shipparts.DistributedSailAI.ShipBalance.ArmorAbsorb.getValue', return_value=0.5):
            sail.projectileWeaponHit(InventoryType.CannonShoot, InventoryType.CannonRoundShot, 0, [], 0, 0,
                [0, 0, 1], None)

        self.assertEqual(ship.hp, 900)


class CannonAmmoTests(_ClockTestCase):

    def setUp(self):
        _ClockTestCase.setUp(self)
        infinite = (InventoryType.CannonRoundShot, InventoryType.CannonGrappleHook)
        ammoIds = {InventoryType.CannonChainShot: InventoryType.begin_WeaponCannonAmmo + 1}
        self.patches += [
            patch.object(WeaponGlobals, 'isInfiniteAmmo', lambda skillId: skillId in infinite),
            patch.object(WeaponGlobals, 'getSkillAmmoInventoryId', lambda skillId: ammoIds.get(skillId)),
            patch.object(WeaponGlobals, 'canFreeUse', lambda skillId: skillId != InventoryType.CannonFirebrand),
            patch.object(WeaponGlobals, 'getAttackVolley', lambda *args: 1.0),
            patch.object(WeaponBaseAI, 'requestProjectileSkill')]
        for item in self.patches[2:]:
            item.start()

        self.ammoId = ammoIds[InventoryType.CannonChainShot]
        self.air = makeAir(battleMgr=Mock(getModifiedReloadTime=Mock(return_value=3.4)))
        self.cannon = DistributedPCCannonAI.__new__(DistributedPCCannonAI)
        self.cannon.air = self.air
        self.cannon.doId = 3000
        self.cannon.userId = 42
        self.cannon.lastFireTimes = {}
        self.avatar = makeAvatar(self.air, 42, {
            InventoryType.CannonChainShot: 2, InventoryType.CannonFirebrand: 2, self.ammoId: 2})
        self.air.getAvatarIdFromSender.return_value = 42

    def fire(self, ammoSkillId):
        WeaponBaseAI.requestProjectileSkill.reset_mock()
        self.cannon.requestProjectileSkill(InventoryType.CannonShoot, ammoSkillId, [0] * 6, 0, 0)
        self.time += 5
        return WeaponBaseAI.requestProjectileSkill.called

    def test_limited_ammo_is_spent(self):
        self.assertTrue(self.fire(InventoryType.CannonChainShot))
        self.assertEqual(self.avatar.inventory.getStackQuantity(self.ammoId), 1)
        self.assertTrue(self.fire(InventoryType.CannonChainShot))
        self.assertFalse(self.fire(InventoryType.CannonChainShot))
        self.assertEqual(self.avatar.inventory.getStackQuantity(self.ammoId), 0)

        # round shot never runs out:
        self.assertTrue(self.fire(InventoryType.CannonRoundShot))

    def test_cannon_must_be_reloaded(self):
        self.assertTrue(self.fire(InventoryType.CannonRoundShot))
        self.time -= 4
        self.assertFalse(self.fire(InventoryType.CannonRoundShot))

    def test_a_volley_is_fired_before_reloading(self):
        with patch.object(WeaponGlobals, 'getAttackVolley', lambda *args: 3.0):
            for _ in range(3):
                self.assertTrue(self.fire(InventoryType.CannonRoundShot))
                self.time -= 4.5

            self.assertFalse(self.fire(InventoryType.CannonRoundShot))
            self.time -= 2
            self.assertTrue(self.fire(InventoryType.CannonRoundShot))

    def test_invalid_cannon_shots_are_rejected(self):
        self.avatar.inventory.stacks[InventoryType.CannonChainShot] = 1
        self.assertFalse(self.fire(InventoryType.CannonChainShot))

        self.avatar.isPaid = lambda: False
        self.assertFalse(self.fire(InventoryType.CannonFirebrand))

        self.assertFalse(self.fire(InventoryType.PistolShoot))

        self.cannon.userId = 43
        self.assertFalse(self.fire(InventoryType.CannonRoundShot))


class CargoTests(_ClockTestCase):

    def makeShip(self, crew=(42, 43), cargo=()):
        air = makeAir()
        ship = makeShip(air=air, ownerId=42, captainId=42, crew=list(crew), cargo=list(cargo),
            maxCargo=5)
        trackGameState(ship)
        self.avatars = [makeAvatar(air, avatarId) for avatarId in crew]
        return ship

    def test_cargo_is_sold_at_port_and_divided_amongst_the_crew(self):
        ship = self.makeShip(cargo=[ItemId.CARGO_CRATE, ItemId.CARGO_CHEST, ItemId.CARGO_SKCHEST])
        ship.missionStartTime = 40.0
        ship.shipKills = 2
        goods = [ItemId.RUM, ItemId.GOLD_BARS, ItemId.DIAMONDS]
        with patch.object(ship, 'unpackCargo', return_value=goods):
            ship.handleDockedAtPort(None)

        self.assertEqual(ship.cargo, [])
        ship.sendUpdate.assert_any_call('setCargo', [[]])

        captain, sailor = self.avatars
        # the captain is dealt the first and third goods and earns the captain's bonus:
        captainGold = EconomyGlobals.getCargoValue(ItemId.RUM) + EconomyGlobals.getCargoValue(ItemId.DIAMONDS)
        captainGold += int(captainGold * EconomyGlobals.CAPTAIN_LOOT_MULTIPLIER)
        self.assertEqual(captain.inventory.gold, captainGold)
        self.assertEqual(sailor.inventory.gold, EconomyGlobals.getCargoValue(ItemId.GOLD_BARS))

        teamData = [60, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, goods, 2]
        captain.sendUpdateToAvatarId.assert_called_once_with(42, 'endMissionPanel',
            [teamData, [60, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, [ItemId.RUM, ItemId.DIAMONDS], 2]])
        sailor.sendUpdateToAvatarId.assert_called_once_with(43, 'endMissionPanel',
            [teamData, [60, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, [ItemId.GOLD_BARS], 2]])

    def test_cargo_containers_hold_their_type_of_goods(self):
        ship = self.makeShip()
        for _ in range(20):
            crate, chest, royal = ship.unpackCargo([ItemId.CARGO_CRATE, ItemId.CARGO_CHEST, ItemId.CARGO_SKCHEST])
            self.assertEqual(EconomyGlobals.getCargoCategory(crate), ItemId.CARGO_CRATE)
            self.assertEqual(EconomyGlobals.getCargoCategory(chest), ItemId.CARGO_CHEST)
            self.assertEqual(EconomyGlobals.getCargoCategory(royal), ItemId.CARGO_SKCHEST)

    def test_cargo_is_lost_when_the_ship_sinks(self):
        ship = self.makeShip(cargo=[ItemId.CARGO_CRATE])
        ship.handleShipSinking()
        self.assertEqual(ship.cargo, [])

    def test_ship_under_attack_cannot_dock(self):
        ship = self.makeShip()
        ship.lastAttacked = self.time
        self.assertFalse(ship.canDock())
        self.time += 29
        self.assertTrue(ship.canDock())

        ship.lastAttacked = self.time
        ship.air.getAvatarIdFromSender.return_value = 42
        ship.handleDockedAtPort = Mock()
        ship.dropAnchor(5000)
        ship.handleDockedAtPort.assert_not_called()

    def test_deploying_starts_a_new_voyage(self):
        ship = self.makeShip()
        ship.shipKills = 3
        ship.setDeploy(1)
        self.assertEqual(ship.shipKills, 0)
        self.assertEqual(ship.missionStartTime, self.time)

    def test_crew_are_sent_home_when_the_ship_is_removed(self):
        ship = self.makeShip()
        ship.sendCrewToReturnLocation = Mock()
        for avatar in self.avatars:
            avatar.crewShipId = ship.doId
            avatar.b_setShipId = Mock()
            avatar.b_setActiveShipId = Mock()
            avatar.b_setCrewShipId = Mock()

        with patch('pirates.ship.DistributedShipAI.DistributedShipAI.delete'):
            ship.air.shipManager = Mock()
            ship.ignoreAll = Mock()
            ship.delete()

        ship.sendCrewToReturnLocation.assert_called_once_with(excludeIds=(42,))
        self.avatars[0].b_setCrewShipId.assert_not_called()
        self.avatars[1].b_setCrewShipId.assert_called_once_with(0)


class SinkRewardTests(_ClockTestCase):

    def test_sinking_crews_earn_reputation(self):
        air = makeAir(questMgr=Mock())
        npcShip = makeShip(cls=NPCShipAI, air=air, npcShip=1, shipClass=ShipGlobals.NAVY_FERRET)
        npcShip.plunderShip = Mock()
        npcShip.gameFSM._getShipLevel = lambda: 5
        playerShip = makeShip(doId=2000, air=air, crew=[42, 43])
        gunner = makeAvatar(air, 42, crewShipId=2000)
        sailor = makeAvatar(air, 43, crewShipId=2000)
        trackGameState(npcShip)

        npcShip.handleShipDamage(-100, gunner)
        self.assertEqual(npcShip.cannonAttackerIds, {42})
        npcShip.handleShipDamage(-5000, gunner)

        reputation = ShipGlobals.getShipExp(5)
        npcShip.plunderShip.assert_called_once_with(playerShip)
        # quest credit is given to every crew that damaged the ship once it begins
        # sinking (DistributedShipAI.handleShipSinking), not again by the npc ship...
        air.questMgr.shipSinking.assert_called_once_with(npcShip)
        air.questMgr.shipSunk.assert_not_called()
        self.assertEqual(playerShip.shipKills, 1)
        self.assertEqual(gunner.inventory.getReputation(InventoryType.CannonRep), reputation)
        self.assertEqual(gunner.inventory.getReputation(InventoryType.SailingRep), reputation)
        self.assertEqual(gunner.inventory.getOverallRep(), reputation * 2)
        self.assertEqual(sailor.inventory.getReputation(InventoryType.CannonRep), 0)
        self.assertEqual(sailor.inventory.getReputation(InventoryType.SailingRep), reputation)
        sailor.d_sendReputationMessage.assert_called_once_with(npcShip.doId, [InventoryType.SailingRep],
            [reputation], 0, 0, 0, 0)


class DinghyCrewShipTests(unittest.TestCase):

    def setUp(self):
        self.bandMember = SimpleNamespace(doId=7000)
        band = SimpleNamespace(getMember=lambda avatarId: self.bandMember if avatarId == 50 else None)
        self.air = makeAir(bandManager=SimpleNamespace(getBandFromAvatar=lambda avatarId: band),
            worldGridManager=Mock())
        self.ship = makeShip(air=self.air, captainId=50, crew=[50], bandId=[1, 2], name='Sea Dog',
            allowCrewState=True, allowGuildState=True)
        self.ship.getTimer = lambda: (0, 0)
        self.air.shipManager = SimpleNamespace(getPlayerShips=lambda: [self.ship],
            hasActiveShip=lambda shipId: shipId == self.ship.doId)
        makeAvatar(self.air, 50, getName=lambda: 'Captain', getGuildId=lambda: 9)
        self.avatar = makeAvatar(self.air, 42, getBandId=lambda: (1, 2), getGuildId=lambda: 9)
        self.dinghy = DistributedDinghyAI.__new__(DistributedDinghyAI)
        self.dinghy.air = self.air
        self.dinghy.sendUpdateToAvatarId = Mock()
        self.dinghy.sendAvatarToShip = Mock()

    def test_crew_and_guild_ships_are_offered(self):
        with patch('pirates.world.DistributedDinghyAI.globalClockDelta') as clockDelta:
            clockDelta.localElapsedTime.return_value = 0
            self.assertEqual(self.dinghy.getOfferBandOptions(self.avatar),
                [[7000, self.ship.doId, 1000, 500, 0, 1, 0, 0, 'Captain']])
            self.assertEqual(len(self.dinghy.getOfferGuildOptions(self.avatar)), 1)

        self.ship.allowCrewState = False
        self.assertEqual(self.dinghy.getOfferBandOptions(self.avatar), [])
        self.avatar.getGuildId = lambda: 0
        self.assertEqual(self.dinghy.getOfferGuildOptions(self.avatar), [])

    def test_crew_ship_selection(self):
        self.air.getAvatarIdFromSender.return_value = 42
        self.dinghy.selectBandShip(self.ship.doId)
        self.dinghy.sendAvatarToShip.assert_called_once_with(self.avatar, self.ship)

        # a crew member from another band is turned away:
        self.avatar.getBandId = lambda: (1, 3)
        self.dinghy.selectBandShip(self.ship.doId)
        self.dinghy.sendUpdateToAvatarId.assert_called_with(42, 'sendAvatarToShip', [0])

        self.dinghy.sendAvatarToShip.reset_mock()
        self.dinghy.selectGuildShip(self.ship.doId)
        self.dinghy.sendAvatarToShip.assert_called_once_with(self.avatar, self.ship)

        # full ships cannot be joined:
        self.ship.crew = [50, 51, 52, 53]
        self.dinghy.selectGuildShip(self.ship.doId)
        self.dinghy.sendUpdateToAvatarId.assert_called_with(42, 'sendAvatarToShip', [0])


class ShipLoaderOwnerTests(unittest.TestCase):

    def test_created_and_activated_ships_belong_to_their_owner(self):
        air = MagicMock(ourChannel=1)
        air.shipLoader.avatar2fsm = {}
        fsm = loader_ud.CreateShipFSM(air, 42)
        fsm.enterStart(ShipGlobals.INTERCEPTORL1, 'Sea Dog')
        fields = air.dbInterface.createObject.call_args[1]['fields']
        self.assertEqual(fields['setOwnerId'], (42,))

        fsm = loader_ud.ActivateShipFSM(air, 42)
        fsm.shipId = 1000
        fsm.inventoryId = 2000
        fsm.accountId = 1
        fsm._shipInventoryActivatedCallback(2000)
        activateFields = air.sendActivate.call_args[0][4]
        self.assertEqual(activateFields['setOwnerId'], (42,))
