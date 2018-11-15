from pandac.PandaModules import VBase3
from pirates.battle import EnemyGlobals
from pirates.battle.EnemySkills import *
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType

BOSS_NPC_LIST = {
  '': {
    'AvatarType': None,
    'HpScale': 5,
    'MpScale': 1,
    'Level': None,
    'Weapon': None,
    'WeaponLevel': 0,
    'Skills': [],
    'SkillLevel': 0,
    'GoldScale': 2,
    'ModelScale': 1.1,
    'DamageScale': 1,
    'HighlightColor': VBase3(1)
  },
  'dynamicBoss_1': {
    'AvatarType': AvatarTypes.Muck,
    'Level': 14,
    'Weapon': EnemyGlobals.CUTLASS,
    'Skills': (InventoryType.CutlassSlash, EnemySkills.CUTLASS_CHOP, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassCleave, EnemySkills.CUTLASS_DOUBLESLASH),
    'HpScale': 5,
    'GoldScale': 2,
    'ModelScale': 1.3,
    'HighlightColor': VBase3(1, 0.5, 0.5)
  },
  '1154059362.19Shochet': {
    'Skills': (EnemySkills.DUAL_CLAW, ),
    'HpScale': 2,
    'GoldScale': 2,
    'ModelScale': 3,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '1154059366.69Shochet': {
    'Skills': (EnemySkills.FLYTRAP_SPIT, ),
    'HpScale': 2,
    'GoldScale': 2,
    'ModelScale': 3,
    'HighlightColor': VBase3(1, 0, 1)
  },
  '1169616489.03Shochet': {
    'Skills': (EnemySkills.STUMP_STOMP, ),
    'HpScale': 2,
    'GoldScale': 2,
    'ModelScale': 3,
    'HighlightColor': VBase3(1, 0, 0.5)
  },
  '1219428571.98mtucker': {
    'HpScale': 5,
    'MpScale': 3,
    'GoldScale': 2,
    'ModelScale': 1.75,
    'DamageScale': 1.5,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '1220906480.53mtucker': {
    'HpScale': 5,
    'MpScale': 3,
    'GoldScale': 2,
    'ModelScale': 1.75,
    'DamageScale': 1.5,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '1219434293.16mtucker': {
    'HpScale': 5,
    'MpScale': 3,
    'GoldScale': 2,
    'ModelScale': 1.75,
    'DamageScale': 1.5,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '1219424341.05mtucker': {
    'HpScale': 5,
    'MpScale': 3,
    'GoldScale': 2,
    'ModelScale': 1.75,
    'DamageScale': 1.5,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '1219425030.24mtucker': {
    'HpScale': 5,
    'MpScale': 3,
    'GoldScale': 2,
    'ModelScale': 1.25,
    'DamageScale': 1.5,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '1219426331.38mtucker': {
    'HpScale': 5,
    'MpScale': 3,
    'GoldScale': 2,
    'ModelScale': 1.5,
    'DamageScale': 1.5,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '1219352693.09mtucker': {
    'HpScale': 5,
    'MpScale': 3,
    'GoldScale': 2,
    'ModelScale': 1.5,
    'DamageScale': 1.5,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '1219367627.94mtucker': {
    'HpScale': 5,
    'MpScale': 3,
    'GoldScale': 2,
    'ModelScale': 1.5,
    'DamageScale': 1.5,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '1219339266.79mtucker': {
    'HpScale': 5,
    'MpScale': 3,
    'GoldScale': 2,
    'ModelScale': 1.1,
    'DamageScale': 1.5,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '1219277508.79mtucker': {
    'HpScale': 5,
    'MpScale': 3,
    'GoldScale': 2,
    'ModelScale': 1.5,
    'DamageScale': 1.5,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '1218760328.71mtucker': {
    'HpScale': 5,
    'MpScale': 3,
    'GoldScale': 2,
    'ModelScale': 1.0,
    'DamageScale': 1.5,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '.mtucker': {
    'HpScale': 2,
    'MpScale': 2,
    'Skills': [],
    'Level': 23,
    'GoldScale': 2,
    'ModelScale': 2,
    'DamageScale': 1,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '.mtucker': {
    'HpScale': 2,
    'MpScale': 2,
    'Skills': [],
    'Level': 23,
    'GoldScale': 2,
    'ModelScale': 2,
    'DamageScale': 1,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '.mtucker': {
    'HpScale': 2,
    'MpScale': 2,
    'Skills': [],
    'Level': 23,
    'GoldScale': 2,
    'ModelScale': 2,
    'DamageScale': 1,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '.mtucker': {
    'HpScale': 2,
    'MpScale': 2,
    'Skills': [],
    'Level': 23,
    'GoldScale': 2,
    'ModelScale': 2,
    'DamageScale': 1,
    'HighlightColor': VBase3(0, 1, 0.5)
  },
  '.mtucker': {
    'HpScale': 2,
    'MpScale': 2,
    'Skills': [],
    'Level': 23,
    'GoldScale': 2,
    'ModelScale': 2,
    'DamageScale': 1,
    'HighlightColor': VBase3(0, 1, 0.5)
  }
}