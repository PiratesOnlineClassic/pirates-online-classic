from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
HAIR = 0
BEARD = 1
MUSTACHE = 2
barberTypes = [
    HAIR,
    BEARD,
    MUSTACHE]
MALE_HAIR = 0
MALE_BEARD = 10000
MALE_MUSTACHE = 20000
FEMALE_HAIR = 30000
FEMALE_BEARD = 40000
FEMALE_MUSTACHE = 50000
stores = {
    PiratesGlobals.PORT_ROYAL_DEFAULTS: [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        10001,
        10002,
        10003,
        10004,
        10005,
        10006,
        10007,
        10008,
        10009,
        10010,
        10011,
        20000,
        20001,
        20002,
        20003,
        20004,
        20005,
        20006,
        30000,
        30001,
        30002,
        30003,
        30004,
        30005,
        30006,
        30007,
        30008,
        30009,
        30010,
        30011,
        30012,
        30013,
        30014,
        30015,
        30016,
        30017,
        30018],
    PiratesGlobals.PORT_ROYAL_THRIFT: [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        10001,
        10002,
        10003,
        10004,
        10005,
        10006,
        10007,
        10008,
        10009,
        10010,
        10011,
        20000,
        20001,
        20002,
        20003,
        20004,
        20005,
        20006,
        30000,
        30001,
        30002,
        30003,
        30004,
        30005,
        30006,
        30007,
        30008,
        30009,
        30010,
        30011,
        30012,
        30013,
        30014,
        30015,
        30016,
        30017,
        30018],
    PiratesGlobals.TORTUGA_DEFAULTS: [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        10001,
        10002,
        10003,
        10004,
        10005,
        10006,
        10007,
        10008,
        10009,
        10010,
        10011,
        20000,
        20001,
        20002,
        20003,
        20004,
        20005,
        20006,
        30000,
        30001,
        30002,
        30003,
        30004,
        30005,
        30006,
        30007,
        30008,
        30009,
        30010,
        30011,
        30012,
        30013,
        30014,
        30015,
        30016,
        30017,
        30018],
    PiratesGlobals.CUBA_DEFAULTS: [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        10001,
        10002,
        10003,
        10004,
        10005,
        10006,
        10007,
        10008,
        10009,
        10010,
        10011,
        20000,
        20001,
        20002,
        20003,
        20004,
        20005,
        20006,
        30000,
        30001,
        30002,
        30003,
        30004,
        30005,
        30006,
        30007,
        30008,
        30009,
        30010,
        30011,
        30012,
        30013,
        30014,
        30015,
        30016,
        30017,
        30018],
    PiratesGlobals.DEL_FUEGO_DEFAULTS: [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        10001,
        10002,
        10003,
        10004,
        10005,
        10006,
        10007,
        10008,
        10009,
        10010,
        10011,
        20000,
        20001,
        20002,
        20003,
        20004,
        20005,
        20006,
        30000,
        30001,
        30002,
        30003,
        30004,
        30005,
        30006,
        30007,
        30008,
        30009,
        30010,
        30011,
        30012,
        30013,
        30014,
        30015,
        30016,
        30017,
        30018]}
barber_id = {
    0: [
        0,
        HAIR,
        PLocalizer.BarberShortStrings.get(0),
        PLocalizer.BarberLongStrings.get(0),
        100,
        None],
    1: [
        1,
        HAIR,
        PLocalizer.BarberShortStrings.get(1),
        PLocalizer.BarberLongStrings.get(1),
        200,
        None],
    2: [
        2,
        HAIR,
        PLocalizer.BarberShortStrings.get(1),
        PLocalizer.BarberLongStrings.get(1),
        200,
        None],
    3: [
        3,
        HAIR,
        PLocalizer.BarberShortStrings.get(1),
        PLocalizer.BarberLongStrings.get(1),
        200,
        None],
    4: [
        4,
        HAIR,
        PLocalizer.BarberShortStrings.get(1),
        PLocalizer.BarberLongStrings.get(1),
        200,
        None],
    5: [
        5,
        HAIR,
        PLocalizer.BarberShortStrings.get(2),
        PLocalizer.BarberLongStrings.get(2),
        250,
        None],
    6: [
        6,
        HAIR,
        PLocalizer.BarberShortStrings.get(2),
        PLocalizer.BarberLongStrings.get(2),
        250,
        None],
    7: [
        7,
        HAIR,
        PLocalizer.BarberShortStrings.get(2),
        PLocalizer.BarberLongStrings.get(3),
        300,
        None],
    8: [
        8,
        HAIR,
        PLocalizer.BarberShortStrings.get(2),
        PLocalizer.BarberLongStrings.get(3),
        300,
        None],
    9: [
        9,
        HAIR,
        PLocalizer.BarberShortStrings.get(3),
        PLocalizer.BarberLongStrings.get(4),
        200,
        None],
    10: [
        10,
        HAIR,
        PLocalizer.BarberShortStrings.get(2),
        PLocalizer.BarberLongStrings.get(5),
        300,
        None],
    11: [
        11,
        HAIR,
        PLocalizer.BarberShortStrings.get(1),
        PLocalizer.BarberLongStrings.get(6),
        300,
        None],
    12: [
        12,
        HAIR,
        PLocalizer.BarberShortStrings.get(1),
        PLocalizer.BarberLongStrings.get(6),
        300,
        None],
    13: [
        13,
        HAIR,
        PLocalizer.BarberShortStrings.get(4),
        PLocalizer.BarberLongStrings.get(7),
        500,
        None],
    10001: [
        0,
        BEARD,
        PLocalizer.BarberShortStrings.get(0),
        PLocalizer.BarberLongStrings.get(0),
        100,
        None],
    10002: [
        1,
        BEARD,
        PLocalizer.BarberShortStrings.get(5),
        PLocalizer.BarberLongStrings.get(8),
        250,
        None],
    10003: [
        2,
        BEARD,
        PLocalizer.BarberShortStrings.get(5),
        PLocalizer.BarberLongStrings.get(9),
        500,
        None],
    10004: [
        3,
        BEARD,
        PLocalizer.BarberShortStrings.get(5),
        PLocalizer.BarberLongStrings.get(10),
        300,
        None],
    10005: [
        4,
        BEARD,
        PLocalizer.BarberShortStrings.get(5),
        PLocalizer.BarberLongStrings.get(11),
        300,
        None],
    10006: [
        5,
        BEARD,
        PLocalizer.BarberShortStrings.get(5),
        PLocalizer.BarberLongStrings.get(12),
        200,
        None],
    10007: [
        6,
        BEARD,
        PLocalizer.BarberShortStrings.get(5),
        PLocalizer.BarberLongStrings.get(13),
        500,
        None],
    10008: [
        7,
        BEARD,
        PLocalizer.BarberShortStrings.get(5),
        PLocalizer.BarberLongStrings.get(14),
        500,
        None],
    10009: [
        8,
        BEARD,
        PLocalizer.BarberShortStrings.get(5),
        PLocalizer.BarberLongStrings.get(15),
        400,
        None],
    10010: [
        9,
        BEARD,
        PLocalizer.BarberShortStrings.get(5),
        PLocalizer.BarberLongStrings.get(16),
        300,
        None],
    10011: [
        10,
        BEARD,
        PLocalizer.BarberShortStrings.get(5),
        PLocalizer.BarberLongStrings.get(17),
        750,
        None],
    20000: [
        0,
        MUSTACHE,
        PLocalizer.BarberShortStrings.get(0),
        PLocalizer.BarberLongStrings.get(0),
        100,
        None],
    20001: [
        1,
        MUSTACHE,
        PLocalizer.BarberShortStrings.get(6),
        PLocalizer.BarberLongStrings.get(18),
        200,
        None],
    20002: [
        2,
        MUSTACHE,
        PLocalizer.BarberShortStrings.get(6),
        PLocalizer.BarberLongStrings.get(19),
        200,
        None],
    20003: [
        3,
        MUSTACHE,
        PLocalizer.BarberShortStrings.get(6),
        PLocalizer.BarberLongStrings.get(20),
        200,
        None],
    20004: [
        4,
        MUSTACHE,
        PLocalizer.BarberShortStrings.get(6),
        PLocalizer.BarberLongStrings.get(21),
        300,
        None],
    20005: [
        5,
        MUSTACHE,
        PLocalizer.BarberShortStrings.get(6),
        PLocalizer.BarberLongStrings.get(22),
        500,
        None],
    20006: [
        6,
        MUSTACHE,
        PLocalizer.BarberShortStrings.get(6),
        PLocalizer.BarberLongStrings.get(23),
        750,
        None],
    30000: [
        0,
        HAIR,
        PLocalizer.BarberShortStrings.get(7),
        PLocalizer.BarberLongStrings.get(24),
        200,
        None],
    30001: [
        1,
        HAIR,
        PLocalizer.BarberShortStrings.get(7),
        PLocalizer.BarberLongStrings.get(25),
        250,
        None],
    30002: [
        2,
        HAIR,
        PLocalizer.BarberShortStrings.get(7),
        PLocalizer.BarberLongStrings.get(26),
        300,
        None],
    30003: [
        3,
        HAIR,
        PLocalizer.BarberShortStrings.get(2),
        PLocalizer.BarberLongStrings.get(27),
        500,
        None],
    30004: [
        4,
        HAIR,
        PLocalizer.BarberShortStrings.get(2),
        PLocalizer.BarberLongStrings.get(28),
        600,
        None],
    30005: [
        5,
        HAIR,
        PLocalizer.BarberShortStrings.get(2),
        PLocalizer.BarberLongStrings.get(29),
        700,
        None],
    30006: [
        6,
        HAIR,
        PLocalizer.BarberShortStrings.get(8),
        PLocalizer.BarberLongStrings.get(30),
        200,
        None],
    30007: [
        7,
        HAIR,
        PLocalizer.BarberShortStrings.get(8),
        PLocalizer.BarberLongStrings.get(31),
        300,
        None],
    30008: [
        8,
        HAIR,
        PLocalizer.BarberShortStrings.get(7),
        PLocalizer.BarberLongStrings.get(32),
        300,
        None],
    30009: [
        9,
        HAIR,
        PLocalizer.BarberShortStrings.get(2),
        PLocalizer.BarberLongStrings.get(33),
        500,
        None],
    30010: [
        10,
        HAIR,
        PLocalizer.BarberShortStrings.get(8),
        PLocalizer.BarberLongStrings.get(34),
        300,
        None],
    30011: [
        11,
        HAIR,
        PLocalizer.BarberShortStrings.get(8),
        PLocalizer.BarberLongStrings.get(35),
        750,
        None],
    30012: [
        12,
        HAIR,
        PLocalizer.BarberShortStrings.get(8),
        PLocalizer.BarberLongStrings.get(36),
        800,
        None],
    30013: [
        13,
        HAIR,
        PLocalizer.BarberShortStrings.get(8),
        PLocalizer.BarberLongStrings.get(37),
        850,
        None],
    30014: [
        14,
        HAIR,
        PLocalizer.BarberShortStrings.get(8),
        PLocalizer.BarberLongStrings.get(38),
        200,
        None],
    30015: [
        15,
        HAIR,
        PLocalizer.BarberShortStrings.get(8),
        PLocalizer.BarberLongStrings.get(39),
        300,
        None],
    30016: [
        16,
        HAIR,
        PLocalizer.BarberShortStrings.get(8),
        PLocalizer.BarberLongStrings.get(40),
        350,
        None],
    30017: [
        17,
        HAIR,
        PLocalizer.BarberShortStrings.get(1),
        PLocalizer.BarberLongStrings.get(41),
        500,
        None],
    30018: [
        18,
        HAIR,
        PLocalizer.BarberShortStrings.get(1),
        PLocalizer.BarberLongStrings.get(42),
        400,
        None]}
