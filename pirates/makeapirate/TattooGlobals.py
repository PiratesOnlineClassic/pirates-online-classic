from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer

tattooNames = [
    'blank', 'arm_color_shark', 'arm_color_skull_pirate',
    'arm_color_skull_shield', 'arm_color_skull_stab', 'arm_color_snake',
    'arm_mono_dagger_fancy', 'arm_mono_flag_skull', 'arm_mono_key',
    'arm_mono_skull_ironcross', 'arm_mono_sword_hook', 'chest_color_8dagger',
    'chest_color_heart_screw', 'chest_color_key_lock',
    'chest_color_skull_dagger', 'chest_color_skullcrossbones',
    'chest_mono_anchor', 'chest_mono_compass', 'chest_mono_dagger',
    'chest_mono_ship_anchor', 'chest_mono_skullcrossbones', 'skull_face',
    'arm_color_nautical_star', 'arm_color_mayanface', 'arm_color_skull_octo',
    'arm_mono_skull_tribal', 'chest_color_squid_ship',
    'chest_color_saint_patricks', 'arm_mono_nativelizards',
    'arm_mono_tribal_01', 'arm_mono_tribal_bird',
    'arm_mono_tribal_jellyfish_01', 'arm_mono_tribal_jellyfish_02',
    'chest_mono_dd_africanface_01', 'chest_mono_dd_maoriface_01',
    'arm_color_asian_leaf', 'arm_color_ethnic_02', 'arm_color_maoriman',
    'arm_color_nativeleaf', 'arm_color_thai_01', 'face_color_face_2clovers',
    'face_color_face_horseshoeclovers', 'chest_color_celtic4leaf',
    'chest_color_ethniceagle', 'chest_color_flintlocks', 'chest_color_shamrock',
    'chest_color_thaimonkeyface', 'chest_color_tribalface_01',
    'chest_color_tribalface_04', 'chest_mono_dd_asianface_01',
    'chest_mono_dd_maoriface_02', 'chest_mono_tribal_01',
    'arm_color_celtic_knot', 'arm_color_chinese_knot',
    'arm_color_hawaiian_tiki', 'arm_color_sharks', 'arm_color_tribal_waves',
    'arm_mono_celtic_deer', 'arm_mono_hawaiian', 'arm_mono_petroglyph',
    'arm_mono_ravens', 'arm_mono_wave_fan', 'chest_color_hawaiian_pectoral',
    'chest_mono_tribal_yakuza', 'face_color_jacksparrow',
    'face_color_tribal_cheek', 'face_color_tribal_chin',
    'face_color_tribal_forehead', 'face_mono_maori_chin',
    'face_mono_maori_nose', 'face_mono_native_eye', 'face_mono_tribal_gotee',
    'face_color_eye_01', 'face_color_cheek', 'face_color_forehead',
    'face_color_greennose', 'face_color_tribal_mouth', 'face_mono_cheek',
    'face_mono_eye_01', 'face_mono_eye_02', 'face_mono_nose_01',
    'face_mono_tribal_beard', 'face_color_voodoo_01', 'face_color_voodoo_02',
    'face_color_voodoo_03', 'face_color_voodoo_04', 'face_color_voodoo_05',
    'face_mono_voodoo_01', 'face_mono_voodoo_02', 'face_mono_voodoo_03',
    'face_mono_voodoo_04', 'face_mono_voodoo_05',
    'arm_color_mothersday_flowers', 'arm_mono_mothersday_flowers',
    'arm_mono_mothersday_sparrows', 'arm_color_mothersday_sparrows',
    'chest_color_mothersday_classic', 'chest_mono_mothersday_classic',
    'face_color_mothersday_flower_sm', 'face_mono_mothersday_flower_sm',
    'face_color_mothersday_flower_lg', 'face_mono_mothersday_flower_lg',
    'face_color_mothersday_hearts', 'face_mono_mothersday_hearts',
    'pvp_icon_spanish', 'pvp_icon_french', 'scars_bulletholes_healed',
    'scars_piratebrand', 'scars_traintrack01', 'sleeve_color_bluebirds',
    'sleeve_color_koi', 'sleeve_color_octopus', 'sleeve_color_peacock',
    'sleeve_color_pinkphoenix', 'sleeve_color_pinktribal',
    'sleeve_color_seahorses', 'sleeve_color_tribal_orangegreen',
    'sleeve_color_tribal_rainbow', 'sleeve_color_tribal_yellowblue',
    'sleeve_mono_3butterflies', 'sleeve_mono_bflystars',
    'sleeve_mono_butterfly', 'sleeve_mono_kitty', 'sleeve_mono_tribal01',
    'sleeve_mono_tribal02', 'sleeve_mono_tribal03', 'sleeve_mono_tribal04',
    'sleeve_mono_tribal05', 'sleeve_mono_tribalshell', 'stitches_bulletholes',
    'stitches_x', 'stitches_y'
]
ZONE1 = 0
ZONE2 = 1
ZONE3 = 2
ZONE4 = 3
ZONE5 = 4
ZONE6 = 5
ZONE7 = 6
ZONE8 = 7
ZONE1_START = 0
ZONE2_START = 10000
ZONE3_START = 20000
ZONE4_START = 30000
ZONE5_START = 40000
ZONE6_START = 50000
ZONE7_START = 60000
ZONE8_START = 70000
TYPE = 0
OFFSETX = 1
OFFSETY = 2
SCALE = 3
ROTATE = 4
COLOR = 5
stores = {
    PiratesGlobals.PORT_ROYAL_DEFAULTS: [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19, 22, 10001,
        10002, 10003, 10005, 10006, 10007, 10008, 10010, 10011, 10012, 10013,
        10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024,
        10025, 10026, 10027, 10029, 10030, 10031, 10033, 10034, 10035, 10037,
        10040, 10041, 20001, 20002, 20003, 20005, 20006, 20007, 20008, 20010,
        20011, 20012, 20013, 20014, 20016, 20017, 20018, 20019, 20020, 20021,
        20022, 20023, 20024, 20025, 20026, 20027, 20029, 20030, 20031, 20033,
        20034, 20035, 20037, 20040, 20041, 30001, 30002, 30003, 30004, 30006,
        30007, 30008, 30009, 30010, 30012, 30013
    ],
    PiratesGlobals.PORT_ROYAL_THRIFT: [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19, 22, 10001,
        10002, 10003, 10005, 10006, 10007, 10008, 10010, 10011, 10012, 10013,
        10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024,
        10025, 10026, 10027, 10029, 10030, 10031, 10033, 10034, 10035, 10037,
        10040, 10041, 20001, 20002, 20003, 20005, 20006, 20007, 20008, 20010,
        20011, 20012, 20013, 20014, 20016, 20017, 20018, 20019, 20020, 20021,
        20022, 20023, 20024, 20025, 20026, 20027, 20029, 20030, 20031, 20033,
        20034, 20035, 20037, 20040, 20041, 30001, 30002, 30003, 30004, 30006,
        30007, 30008, 30009, 30010, 30012, 30013
    ],
    PiratesGlobals.TORTUGA_DEFAULTS: [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19, 22, 10001,
        10002, 10003, 10005, 10006, 10007, 10008, 10010, 10011, 10012, 10013,
        10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024,
        10025, 10026, 10027, 10029, 10030, 10031, 10033, 10034, 10035, 10037,
        10040, 10041, 20001, 20002, 20003, 20005, 20006, 20007, 20008, 20010,
        20011, 20012, 20013, 20014, 20016, 20017, 20018, 20019, 20020, 20021,
        20022, 20023, 20024, 20025, 20026, 20027, 20029, 20030, 20031, 20033,
        20034, 20035, 20037, 20040, 20041, 30001, 30002, 30003, 30004, 30006,
        30007, 30008, 30009, 30010, 30012, 30013
    ],
    PiratesGlobals.CUBA_DEFAULTS: [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19, 22, 10001,
        10002, 10003, 10005, 10006, 10007, 10008, 10010, 10011, 10012, 10013,
        10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024,
        10025, 10026, 10027, 10029, 10030, 10031, 10033, 10034, 10035, 10037,
        10040, 10041, 20001, 20002, 20003, 20005, 20006, 20007, 20008, 20010,
        20011, 20012, 20013, 20014, 20016, 20017, 20018, 20019, 20020, 20021,
        20022, 20023, 20024, 20025, 20026, 20027, 20029, 20030, 20031, 20033,
        20034, 20035, 20037, 20040, 20041, 30001, 30002, 30003, 30004, 30006,
        30007, 30008, 30009, 30010, 30012, 30013
    ],
    PiratesGlobals.DEL_FUEGO_DEFAULTS: [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19, 22, 10001,
        10002, 10003, 10005, 10006, 10007, 10008, 10010, 10011, 10012, 10013,
        10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024,
        10025, 10026, 10027, 10029, 10030, 10031, 10033, 10034, 10035, 10037,
        10040, 10041, 20001, 20002, 20003, 20005, 20006, 20007, 20008, 20010,
        20011, 20012, 20013, 20014, 20016, 20017, 20018, 20019, 20020, 20021,
        20022, 20023, 20024, 20026, 20027, 20029, 20030, 20031, 20033, 20034,
        20035, 20037, 20040, 20041, 30001, 30002, 30003, 30004, 30006, 30007,
        30008, 30009, 30010, 30012, 30013
    ],
    PiratesGlobals.PRIVATEER_TATTOOS: [
        23, 24, 25, 26, 27, 28, 10043, 10044, 10045, 10046, 10047, 10048, 20042,
        20043, 20044, 20045, 20046, 20047, 30014, 30015, 30016, 30017
    ]
}
SOLOMON_ODOUGAL_QUEST_A = 0
LALA_LOVEL_QUEST_A = 1
MERCEDES_CORAZON_QUEST_A = 2
SOLOMON_ODOUGAL_QUEST_B = 3
LALA_LOVEL_QUEST_B = 4
MERCEDES_CORAZON_QUEST_B = 5
SHIP_PVP_FRENCH_QUEST_A = 6
SHIP_PVP_SPANISH_QUEST_A = 7
questDrops = {
    SOLOMON_ODOUGAL_QUEST_A: [10032, 20032],
    SOLOMON_ODOUGAL_QUEST_B: [30011],
    LALA_LOVEL_QUEST_A: [18],
    LALA_LOVEL_QUEST_B: [10036, 20036],
    MERCEDES_CORAZON_QUEST_A: [10028, 20028],
    MERCEDES_CORAZON_QUEST_B: [30005],
    SHIP_PVP_FRENCH_QUEST_A: [21, 10039, 20039],
    SHIP_PVP_SPANISH_QUEST_A: [20, 10038, 20038]
}
quest_items = [
    18, 10028, 20028, 10032, 20032, 30011, 10036, 20036, 30005, 20, 21, 10038,
    10039, 20038, 20039, 22, 10040, 10041, 20040, 20041, 30012, 30013
]
tattoos = {
    1: [
        ZONE1, 11, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(11), 200, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    2: [
        ZONE1, 12, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(12), 300, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    3: [
        ZONE1, 13, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(13), 500, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    4: [
        ZONE1, 14, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(14), 200, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    5: [
        ZONE1, 15, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(15), 600, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    6: [
        ZONE1, 16, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(16), 100, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    7: [
        ZONE1, 17, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(17), 100, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    8: [
        ZONE1, 18, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(18), 100, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    9: [
        ZONE1, 19, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(19), 150, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    10: [
        ZONE1, 20, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(20), 150, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    11: [
        ZONE1, 26, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(26), 500, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    12: [
        ZONE1, 27, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(27), 0, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    13: [
        ZONE1, 42, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(42), 500, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], PiratesGlobals.SAINTPATRICKSDAY
    ],
    14: [
        ZONE1, 43, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(43), 500, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    15: [
        ZONE1, 44, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(44), 500, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    16: [
        ZONE1, 45, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(45), 500, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], PiratesGlobals.SAINTPATRICKSDAY
    ],
    17: [
        ZONE1, 46, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(46), 500, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    18: [
        ZONE1, 62, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(62), 0, [0.084, 0.211, 0.097, 37.463],
        [0.525, 0.871, 0.0443, 28.097], None
    ],
    19: [
        ZONE1, 63, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(63), 1000, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    20: [
        ZONE1, 104, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(104), 0, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    21: [
        ZONE1, 105, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(105), 0, [0.127, 0.203, 0.165, 0.0],
        [0.58, 0.862, 0.033, 0.0], None
    ],
    22: [
        ZONE1, 96, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(96), 500, [0.092, 0.263, 0.062, 0.0],
        [0.578, 0.862, 0.0417, 0.0], PiratesGlobals.MOTHERSDAY
    ],
    23: [
        ZONE1, 106, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(112), 20, [0.0837, 0.28, 0.036, 84.291],
        [0.291, 0.88, 0.033, 87.413], None
    ],
    24: [
        ZONE1, 107, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(113), 20, [0.049, 0.273, 0.0279, 346.528],
        [0.3, 0.871, 0.024, 0.0], None
    ],
    25: [
        ZONE1, 108, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(114), 50, [0.084, 0.29, 0.045, 74.925],
        [0.3, 0.88, 0.042, 78.047], None
    ],
    26: [
        ZONE1, 129, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(115), 50, [0.075, 0.272, 0.054, 81.169],
        [0.3, 0.871, 0.033, 90.534], None
    ],
    27: [
        ZONE1, 130, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(116), 100, [0.049, 0.263, 0.057, 262.238],
        [0.257, 0.862, 0.042, 93.746], None
    ],
    28: [
        ZONE1, 131, PLocalizer.TattooChest,
        PLocalizer.TattooStrings.get(117), 100, [0.075, 0.281, 0.071, 106.144],
        [0.3, 0.871, 0.042, 99.9], None
    ],
    10001: [
        ZONE2, 1, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(1), 200, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10002: [
        ZONE2, 2, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(2), 250, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10003: [
        ZONE2, 3, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(3), 200, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10004: [
        ZONE2, 4, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(4), 300, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10005: [
        ZONE2, 5, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(5), 300, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10006: [
        ZONE2, 6, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(6), 150, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10007: [
        ZONE2, 7, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(7), 150, [0.4, 0.57, 0.1, 271.1],
        [0.6, 0.79, 0.04, 271.1], None
    ],
    10008: [
        ZONE2, 8, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(8), 100, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10009: [
        ZONE2, 9, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(9), 100, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10010: [
        ZONE2, 10, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(10), 150, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10011: [
        ZONE2, 22, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(22), 500, [0.2, 0.57, 0.05, 271.1],
        [0.3, 0.79, 0.04, 271.1], None
    ],
    10012: [
        ZONE2, 23, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(23), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10013: [
        ZONE2, 24, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(24), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10014: [
        ZONE2, 25, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(25), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10015: [
        ZONE2, 27, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(27), 0, [0.2, 0.57, 0.05, 271.1],
        [0.3, 0.79, 0.04, 271.1], None
    ],
    10016: [
        ZONE2, 28, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(28), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10017: [
        ZONE2, 29, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(29), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10018: [
        ZONE2, 30, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(30), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10019: [
        ZONE2, 31, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(31), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10020: [
        ZONE2, 32, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(32), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10021: [
        ZONE2, 35, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(35), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10022: [
        ZONE2, 36, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(36), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10023: [
        ZONE2, 37, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(37), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10024: [
        ZONE2, 38, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(38), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10025: [
        ZONE2, 39, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(39), 500, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10026: [
        ZONE2, 42, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(42), 500, [0.2, 0.57, 0.05, 271.1],
        [0.3, 0.79, 0.04, 271.1], PiratesGlobals.SAINTPATRICKSDAY
    ],
    10027: [
        ZONE2, 45, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(45), 500, [0.2, 0.57, 0.05, 271.1],
        [0.3, 0.79, 0.04, 271.1], PiratesGlobals.SAINTPATRICKSDAY
    ],
    10028: [
        ZONE2, 54, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(54), 0, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10029: [
        ZONE2, 52, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(52), 1000, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10030: [
        ZONE2, 56, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(56), 1000, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10031: [
        ZONE2, 55, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(55), 1000, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10032: [
        ZONE2, 53, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(53), 0, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10033: [
        ZONE2, 61, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(61), 1000, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10034: [
        ZONE2, 57, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(57), 1000, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10035: [
        ZONE2, 58, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(58), 1000, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10036: [
        ZONE2, 59, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(59), 0, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10037: [
        ZONE2, 60, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(60), 1000, [0.105, 0.57, 0.05, 271.1],
        [0.15, 0.79, 0.04, 271.1], None
    ],
    10038: [
        ZONE2, 104, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(104), 0, [0.2, 0.57, 0.05, 271.1],
        [0.3, 0.79, 0.04, 271.1], None
    ],
    10039: [
        ZONE2, 105, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(105), 0, [0.2, 0.57, 0.05, 271.1],
        [0.3, 0.79, 0.04, 271.1], None
    ],
    10040: [
        ZONE2, 92, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(92), 500, [0.105, 0.57, 0.05, 271.1],
        [0.133, 0.781, 0.0488, 271.1], PiratesGlobals.MOTHERSDAY
    ],
    10041: [
        ZONE2, 95, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(95), 500, [0.105, 0.57, 0.05, 271.1],
        [0.133, 0.781, 0.0488, 271.1], PiratesGlobals.MOTHERSDAY
    ],
    10042: [
        ZONE2, 111, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(111), 500,
        [0.280700147152, 0.55680000782, 0.298780024052, 267.103973389],
        [0.199800059199, 0.80110001564, 0.351714193821, 84.2757949829], None
    ],
    10043: [
        ZONE2, 106, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(112), 20, [0.108, 0.577, 0.031, 255.49],
        [0.133, 0.79, 0.032, 90.031], None
    ],
    10044: [
        ZONE2, 107, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(113), 20, [0.108, 0.579, 0.027, 271.1],
        [0.133, 0.79, 0.0317, 255.491], None
    ],
    10045: [
        ZONE2, 108, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(114), 50, [0.116, 0.57, 0.062, 271.1],
        [0.143, 0.781, 0.0574, 249.247], None
    ],
    10046: [
        ZONE2, 129, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(115), 50, [0.108, 0.568, 0.053, 271.1],
        [0.141, 0.781, 0.04, 271.1], None
    ],
    10047: [
        ZONE2, 130, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(116), 100, [0.116, 0.57, 0.079, 271.1],
        [0.141, 0.781, 0.066, 83.787], None
    ],
    10048: [
        ZONE2, 131, PLocalizer.TattooLeftArm,
        PLocalizer.TattooStrings.get(117), 100, [0.108, 0.57, 0.079, 271.1],
        [0.141, 0.781, 0.066, 93.153], None
    ],
    20001: [
        ZONE3, 1, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(1), 200, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20002: [
        ZONE3, 2, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(2), 250, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20003: [
        ZONE3, 3, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(3), 200, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20004: [
        ZONE3, 4, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(4), 300, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20005: [
        ZONE3, 5, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(5), 300, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20006: [
        ZONE3, 6, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(6), 150, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20007: [
        ZONE3, 7, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(7), 150, [0.4, 0.84, 0.1, 271.1],
        [0.6, 0.614, 0.04, 271.1], None
    ],
    20008: [
        ZONE3, 8, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(8), 100, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20009: [
        ZONE3, 9, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(9), 100, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20010: [
        ZONE3, 10, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(10), 150, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20011: [
        ZONE3, 22, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(22), 500, [0.2, 0.84, 0.05, 271.1],
        [0.3, 0.614, 0.04, 271.1], None
    ],
    20012: [
        ZONE3, 23, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(23), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20013: [
        ZONE3, 24, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(24), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20014: [
        ZONE3, 25, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(25), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20015: [
        ZONE3, 27, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(27), 0, [0.2, 0.84, 0.05, 271.1],
        [0.3, 0.614, 0.04, 271.1], None
    ],
    20016: [
        ZONE3, 28, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(28), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20017: [
        ZONE3, 29, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(29), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20018: [
        ZONE3, 30, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(30), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20019: [
        ZONE3, 31, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(31), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20020: [
        ZONE3, 32, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(32), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20021: [
        ZONE3, 35, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(35), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20022: [
        ZONE3, 36, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(36), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20023: [
        ZONE3, 37, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(37), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20024: [
        ZONE3, 38, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(38), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20025: [
        ZONE3, 39, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(39), 500, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20026: [
        ZONE3, 42, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(42), 500, [0.2, 0.84, 0.05, 271.1],
        [0.3, 0.614, 0.04, 271.1], PiratesGlobals.SAINTPATRICKSDAY
    ],
    20027: [
        ZONE3, 45, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(45), 500, [0.2, 0.84, 0.05, 271.1],
        [0.3, 0.614, 0.04, 271.1], PiratesGlobals.SAINTPATRICKSDAY
    ],
    20028: [
        ZONE3, 54, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(54), 0, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20029: [
        ZONE3, 52, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(52), 1000, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20030: [
        ZONE3, 56, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(56), 1000, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20031: [
        ZONE3, 55, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(55), 1000, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20032: [
        ZONE3, 53, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(53), 0, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20033: [
        ZONE3, 61, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(61), 1000, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20034: [
        ZONE3, 57, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(57), 1000, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20035: [
        ZONE3, 58, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(58), 1000, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20036: [
        ZONE3, 59, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(59), 0, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20037: [
        ZONE3, 60, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(60), 1000, [0.11, 0.84, 0.05, 271.1],
        [0.15, 0.614, 0.04, 271.1], None
    ],
    20038: [
        ZONE3, 104, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(104), 0, [0.2, 0.84, 0.05, 271.1],
        [0.3, 0.614, 0.04, 271.1], None
    ],
    20039: [
        ZONE3, 105, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(105), 0, [0.2, 0.84, 0.05, 271.1],
        [0.3, 0.614, 0.04, 271.1], None
    ],
    20040: [
        ZONE3, 92, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(92), 500, [0.11, 0.84, 0.05, 271.1],
        [0.133, 0.62, 0.049, 271.1], PiratesGlobals.MOTHERSDAY
    ],
    20041: [
        ZONE3, 95, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(95), 500, [0.11, 0.84, 0.05, 271.1],
        [0.133, 0.62, 0.049, 271.1], PiratesGlobals.MOTHERSDAY
    ],
    20042: [
        ZONE3, 106, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(112), 20, [0.099, 0.837, 0.0275, 80.665],
        [0.133, 0.627, 0.032, 264.856], None
    ],
    20043: [
        ZONE3, 107, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(113), 20, [0.108, 0.83, 0.027, 264.856],
        [0.133, 0.627, 0.032, 271.1], None
    ],
    20044: [
        ZONE3, 108, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(114), 50, [0.116, 0.84, 0.07, 271.1],
        [0.141, 0.627, 0.066, 286.709], None
    ],
    20045: [
        ZONE3, 129, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(115), 50, [0.108, 0.848, 0.062, 271.1],
        [0.141, 0.619, 0.04, 89.491], None
    ],
    20046: [
        ZONE3, 130, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(116), 100, [0.108, 0.837, 0.079, 271.1],
        [0.141, 0.629, 0.066, 93.153], None
    ],
    20047: [
        ZONE3, 131, PLocalizer.TattooRightArm,
        PLocalizer.TattooStrings.get(117), 100, [0.108, 0.831, 0.079, 271.1],
        [0.141, 0.627, 0.075, 99.397], None
    ],
    30001: [
        ZONE4, 21, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(21), 500, [0.5, 0.5, 1.0, 0.0],
        [0.5, 0.44, 0.85, 0.0], None
    ],
    30002: [
        ZONE4, 40, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(40), 500, [0.75, 0.45, 0.3, 0.0],
        [0.7, 0.37, 0.25, 0.0], PiratesGlobals.SAINTPATRICKSDAY
    ],
    30003: [
        ZONE4, 41, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(41), 500, [0.75, 0.45, 0.3, 0.0],
        [0.7, 0.37, 0.25, 0.0], PiratesGlobals.SAINTPATRICKSDAY
    ],
    30004: [
        ZONE4, 67, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(67), 1000, [0.665, 0.665, 0.236, 15.609],
        [0.639, 0.595, 0.227, 0.0], None
    ],
    30005: [
        ZONE4, 65, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(65), 0, [0.691, 0.405, 0.382, 0.0],
        [0.656, 0.353, 0.27, 0.0], None
    ],
    30006: [
        ZONE4, 66, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(66), 1000, [0.498, 0.196, 0.33, 0.0],
        [0.499, 0.205, 0.245, 0.0], None
    ],
    30007: [
        ZONE4, 64, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(64), 1000, [0.498, 0.569, 0.383, 0.0],
        [0.499, 0.483, 0.356, 0.0], None
    ],
    30008: [
        ZONE4, 71, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(71), 1000, [0.498, 0.127, 0.272, 0.0],
        [0.499, 0.153, 0.21, 0.0], None
    ],
    30009: [
        ZONE4, 69, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(69), 1000, [0.504, 0.483, 0.22, 0.0],
        [0.499, 0.422, 0.141, 0.0], None
    ],
    30010: [
        ZONE4, 68, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(68), 1000, [0.495, 0.301, 0.332, 0.0],
        [0.499, 0.275, 0.339, 0.0], None
    ],
    30011: [
        ZONE4, 70, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(70), 0, [0.651, 0.595, 0.4, 9.366],
        [0.656, 0.524, 0.339, 3.122], None
    ],
    30012: [
        ZONE4, 100, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(100), 500, [0.239, 0.396, 0.262, 0.0],
        [0.327, 0.335, 0.236, 0.0], PiratesGlobals.MOTHERSDAY
    ],
    30013: [
        ZONE4, 102, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(102), 500, [0.239, 0.396, 0.219, 0.0],
        [0.327, 0.335, 0.184, 0.0], PiratesGlobals.MOTHERSDAY
    ],
    30014: [
        ZONE4, 107, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(113), 20, [0.387, 0.308, 0.099, 0.0],
        [0.334, 0.327, 0.099, 0.0], None
    ],
    30015: [
        ZONE4, 108, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(114), 50, [0.118, 0.387, 0.313, 171.703],
        [0.17, 0.342, 0.15, 109.266], None
    ],
    30016: [
        ZONE4, 130, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(116), 100, [0.327, 0.75, 0.236, 262.238],
        [0.335, 0.639, 0.184, 90.534], None
    ],
    30017: [
        ZONE4, 131, PLocalizer.TattooFace,
        PLocalizer.TattooStrings.get(117), 100, [0.118, 0.431, 0.256, 96.778],
        [0.153, 0.368, 0.15, 106.143], None
    ]
}
_tattoosInitialized = 0
TattooImages = []


def initTattooImages():
    global _tattoosInitialized
    tattoos = loader.loadModel('models/misc/tattoos')
    for i in range(len(tattooNames)):
        TattooImages.append(tattoos.find('**/tattoo_' + tattooNames[i]))

    _tattoosInitialized = 1


def getTattooImage(tattooNum):
    if _tattoosInitialized == 0:
        initTattooImages()
    if tattooNum >= len(tattooNames):
        np = TattooImages[0]
    else:
        np = TattooImages[tattooNum]
    if np:
        image = np.findAllTextures().getTexture(0)
        return image
