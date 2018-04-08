from panda3d.core import *
from pirates.piratesbase import PiratesGlobals

StateDict = {
    PiratesGlobals.TOD_DAWN: 'Dawn',
    PiratesGlobals.TOD_DAWN2DAY: 'Dawn2Day',
    PiratesGlobals.TOD_DAY: 'Day',
    PiratesGlobals.TOD_DAY2DUSK: 'Day2Dusk',
    PiratesGlobals.TOD_DUSK: 'Dusk',
    PiratesGlobals.TOD_DUSK2NIGHT: 'Dusk2Night',
    PiratesGlobals.TOD_NIGHT: 'Night',
    PiratesGlobals.TOD_NIGHT2STARS: 'Night2Stars',
    PiratesGlobals.TOD_STARS: 'Stars',
    PiratesGlobals.TOD_STARS2DAWN: 'Stars2Dawn',
    PiratesGlobals.TOD_DAY2STORM: 'Day2Storm',
    PiratesGlobals.TOD_HALLOWEEN: 'HalloweenNight',
    PiratesGlobals.TOD_FULLMOON: 'FullMoon',
    PiratesGlobals.TOD_HALF2FULLMOON: 'Half2FullMoon',
    PiratesGlobals.TOD_FULL2HALFMOON: 'Full2HalfMoon',
    }
TOD_REGULAR_CYCLE = 0
TOD_HALLOWEEN_CYCLE = 1
TOD_JOLLYCURSE_CYCLE = 2
StartingStates = {TOD_REGULAR_CYCLE: PiratesGlobals.TOD_DAY,
                  TOD_HALLOWEEN_CYCLE: PiratesGlobals.TOD_HALLOWEEN,
                  TOD_JOLLYCURSE_CYCLE: PiratesGlobals.TOD_HALF2FULLMOON}
CycleStateTimeList = {TOD_REGULAR_CYCLE: [
    (PiratesGlobals.TOD_DAWN, 1),
    (PiratesGlobals.TOD_DAWN2DAY, 1),
    (PiratesGlobals.TOD_DAY, 7),
    (PiratesGlobals.TOD_DAY2DUSK, 1),
    (PiratesGlobals.TOD_DUSK, 2),
    (PiratesGlobals.TOD_DUSK2NIGHT, 1),
    (PiratesGlobals.TOD_NIGHT, 4),
    (PiratesGlobals.TOD_NIGHT2STARS, 2),
    (PiratesGlobals.TOD_STARS, 4),
    (PiratesGlobals.TOD_STARS2DAWN, 1),
    ], TOD_HALLOWEEN_CYCLE: [(PiratesGlobals.TOD_HALLOWEEN, 24)],
        TOD_JOLLYCURSE_CYCLE: [(PiratesGlobals.TOD_HALF2FULLMOON, 2),
                               (PiratesGlobals.TOD_FULLMOON, 4),
                               (PiratesGlobals.TOD_FULL2HALFMOON, 2),
                               (PiratesGlobals.TOD_HALLOWEEN, 16)]}
StateBreakdownList = {}
StateBeginTimeList = {}
NumStates = {}
cycles = CycleStateTimeList.keys()
for cycleKey in cycles:
    totalHours = 0.0
    StateBreakdownList[cycleKey] = {}
    StateBeginTimeList[cycleKey] = {}
    cycle = CycleStateTimeList.get(cycleKey)
    NumStates[cycleKey] = len(cycle)
    for state in cycle:
        StateBeginTimeList[cycleKey][state[0]] = totalHours / 24.0
        StateBreakdownList[cycleKey][state[0]] = state[1] / 24.0
        totalHours += state[1]


def getStartingState(cycleId):
    return StartingStates.get(cycleId)


def getStateDuration(cycleId, stateId):
    return StateBreakdownList.get(cycleId).get(stateId)


def getStateBeginTime(cycleId, stateId):
    return StateBeginTimeList.get(cycleId).get(stateId)


def getNumStates(cycleId):
    return NumStates.get(cycleId)


def getStateName(stateId):
    return StateDict.get(stateId)


def getStateId(stateName):
    stateKeys = StateDict.keys()
    for stateId in stateKeys:
        if StateDict.get(stateId) == stateName:
            return stateId

    return


def getNextStateId(cycleId, stateId):
    cycle = CycleStateTimeList.get(cycleId)
    numStates = NumStates.get(cycleId)
    for i in range(numStates - 1):
        if cycle[i][0] == stateId and i + 1 < numStates:
            return cycle[i + 1][0]

    return cycle[0][0]


def isStateIdValid(cycleId, stateId):
    cycle = CycleStateTimeList.get(cycleId)
    for state in cycle:
        if state[0] == stateId:
            return True

    return False


ENV_DEFAULT = 0
ENV_FOREST = 1
ENV_SWAMP = 2
ENV_CAVE = 3
ENV_LAVACAVE = 4
ENV_INTERIOR = 5
ENV_OFF = 6
DAWN_AMBIENT_COLOR = Vec4(0.45, 0.53, 0.65, 1)
DAWN_DIRECTIONAL_COLOR = Vec4(0.55, 0.46, 0.35, 1)
DAWN_FOG_COLOR = Vec4(0.3, 0.2, 0.15, 1)
DAWN_FOG_EXP = 0.0001
DAY_AMBIENT_COLOR = Vec4(0.54, 0.5, 0.63, 1)
DAY_DIRECTIONAL_COLOR = Vec4(0.46, 0.46, 0.37, 1)
DAY_FOG_COLOR = Vec4(0.6, 0.7, 0.9, 1)
DAY_FOG_EXP = 0.0001
DUSK_AMBIENT_COLOR = Vec4(0.4, 0.45, 0.5, 1)
DUSK_DIRECTIONAL_COLOR = Vec4(0.6, 0.34, 0.1, 1)
DUSK_FOG_COLOR = Vec4(0.3, 0.18, 0.15, 1)
DUSK_FOG_EXP = 0.0001
NIGHT_AMBIENT_COLOR = Vec4(0.44, 0.45, 0.56, 1)
NIGHT_DIRECTIONAL_COLOR = Vec4(0.46, 0.48, 0.45, 1)
NIGHT_FOG_COLOR = Vec4(0.15, 0.2, 0.35, 1)
NIGHT_FOG_EXP = 0.0001
STARS_AMBIENT_COLOR = Vec4(0.39, 0.42, 0.54, 1)
STARS_DIRECTIONAL_COLOR = Vec4(0.42, 0.42, 0.4, 1)
STARS_FOG_COLOR = Vec4(0.05, 0.06, 0.17, 1)
STARS_FOG_EXP = 0.0002
HALLOWEEN_AMBIENT_COLOR = Vec4(0.34, 0.28, 0.41, 1)
HALLOWEEN_DIRECTIONAL_COLOR = Vec4(0.66, 0.76, 0.05, 1)
HALLOWEEN_FOG_COLOR = Vec4(0.1, 0.12, 0.03, 1)
HALLOWEEN_FOG_EXP = 0.00025
CAVE_HALLOWEEN_AMBIENT_COLOR = Vec4(0.2, 0.5, 0.25, 1)
CAVE_HALLOWEEN_DIRECTIONAL_COLOR = Vec4(0.7, 0.6, 0.25, 1)
DAWN_FOG_COLOR.setW(0.0)
DAY_FOG_COLOR.setW(0.0)
DUSK_FOG_COLOR.setW(0.0)
NIGHT_FOG_COLOR.setW(0.0)
STARS_FOG_COLOR.setW(0.0)
HALLOWEEN_FOG_COLOR.setW(0.0)
ON_ALPHA = Vec4(1, 1, 1, 1)
OFF_ALPHA = Vec4(1, 1, 1, 0)
FOREST_AMBIENT_COLOR = Vec4(0.35, 0.45, 0.4, 1)
FOREST_DIRECTIONAL_COLOR = Vec4(0.5, 0.45, 0.4, 1)
FOREST_DAWN_FOG_COLOR = Vec4(0.38, 0.3, 0.3, 1)
FOREST_DAY_FOG_COLOR = Vec4(0.35, 0.4, 0.5, 1)
FOREST_DUSK_FOG_COLOR = Vec4(0.38, 0.3, 0.35, 1)
FOREST_NIGHT_FOG_COLOR = Vec4(0.1, 0.15, 0.25, 1)
FOREST_STARS_FOG_COLOR = Vec4(0.02, 0.02, 0.1, 1)
FOREST_FOG_EXP = 0.0015
FOREST_NIGHT_FOG_EXP = 0.002
SWAMP_AMBIENT_COLOR = Vec4(0.3, 0.4, 0.45, 1)
SWAMP_DIRECTIONAL_COLOR = Vec4(0.2, 0.4, 0.4, 1)
SWAMP_FOG_COLOR = Vec4(0.2, 0.25, 0.3, 1)
SWAMP_FOG_EXP = 0.005
CAVE_AMBIENT_COLOR = Vec4(0.4, 0.3, 0.6, 1)
CAVE_DIRECTIONAL_COLOR = Vec4(0.15, 0.2, 0, 1)
CAVE_FOG_COLOR = Vec4(0.05, 0.05, 0.075, 1)
CAVE_FOG_EXP = 0.002
LAVACAVE_AMBIENT_COLOR = Vec4(0.6, 0.3, 0.4, 1)
LAVACAVE_DIRECTIONAL_COLOR = Vec4(0.2, 0.15, 0, 1)
LAVACAVE_FOG_COLOR = Vec4(0.075, 0.05, 0.025, 1)
LAVACAVE_FOG_EXP = 0.002
ShadowColorTable = [
    (0, 1.0),
    (10, 1.0),
    (15, 0.8),
    (30, 0.7),
    (60, 0.6),
    (90, 0.5),
    (120, 0.6),
    (150, 0.7),
    (165, 0.8),
    (170, 1.0),
    (195, 1.0),
    (225, 1.0),
    (225, 1.0),
    (240, 0.8),
    (330, 0.8),
    (345, 1.0),
    (360, 1.0),
    ]
AmbientLightColors = {
    ENV_DEFAULT: {
        PiratesGlobals.TOD_DAWN: DAWN_AMBIENT_COLOR,
        PiratesGlobals.TOD_DAY: DAY_AMBIENT_COLOR,
        PiratesGlobals.TOD_DUSK: DUSK_AMBIENT_COLOR,
        PiratesGlobals.TOD_NIGHT: NIGHT_AMBIENT_COLOR,
        PiratesGlobals.TOD_STARS: STARS_AMBIENT_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_AMBIENT_COLOR,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_AMBIENT_COLOR,
        },
    ENV_FOREST: {
        PiratesGlobals.TOD_DAWN: FOREST_AMBIENT_COLOR,
        PiratesGlobals.TOD_DAY: FOREST_AMBIENT_COLOR,
        PiratesGlobals.TOD_DUSK: FOREST_AMBIENT_COLOR,
        PiratesGlobals.TOD_NIGHT: FOREST_AMBIENT_COLOR,
        PiratesGlobals.TOD_STARS: FOREST_AMBIENT_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_AMBIENT_COLOR,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_AMBIENT_COLOR,
        },
    ENV_SWAMP: {
        PiratesGlobals.TOD_DAWN: SWAMP_AMBIENT_COLOR,
        PiratesGlobals.TOD_DAY: SWAMP_AMBIENT_COLOR,
        PiratesGlobals.TOD_DUSK: SWAMP_AMBIENT_COLOR,
        PiratesGlobals.TOD_NIGHT: SWAMP_AMBIENT_COLOR,
        PiratesGlobals.TOD_STARS: SWAMP_AMBIENT_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_AMBIENT_COLOR,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_AMBIENT_COLOR,
        },
    ENV_CAVE: {
        PiratesGlobals.TOD_DAWN: CAVE_AMBIENT_COLOR,
        PiratesGlobals.TOD_DAY: CAVE_AMBIENT_COLOR,
        PiratesGlobals.TOD_DUSK: CAVE_AMBIENT_COLOR,
        PiratesGlobals.TOD_NIGHT: CAVE_AMBIENT_COLOR,
        PiratesGlobals.TOD_STARS: CAVE_AMBIENT_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: CAVE_HALLOWEEN_AMBIENT_COLOR,
        PiratesGlobals.TOD_FULLMOON: CAVE_HALLOWEEN_AMBIENT_COLOR,
        },
    ENV_LAVACAVE: {
        PiratesGlobals.TOD_DAWN: LAVACAVE_AMBIENT_COLOR,
        PiratesGlobals.TOD_DAY: LAVACAVE_AMBIENT_COLOR,
        PiratesGlobals.TOD_DUSK: LAVACAVE_AMBIENT_COLOR,
        PiratesGlobals.TOD_NIGHT: LAVACAVE_AMBIENT_COLOR,
        PiratesGlobals.TOD_STARS: LAVACAVE_AMBIENT_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: CAVE_HALLOWEEN_AMBIENT_COLOR,
        PiratesGlobals.TOD_FULLMOON: CAVE_HALLOWEEN_AMBIENT_COLOR,
        },
    }
DirectionalLightColors = {
    ENV_DEFAULT: {
        PiratesGlobals.TOD_DAWN: DAWN_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_DAY: DAY_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_DUSK: DUSK_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_NIGHT: NIGHT_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_STARS: STARS_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_DIRECTIONAL_COLOR,
        },
    ENV_FOREST: {
        PiratesGlobals.TOD_DAWN: FOREST_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_DAY: FOREST_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_DUSK: FOREST_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_NIGHT: FOREST_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_STARS: FOREST_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_DIRECTIONAL_COLOR,
        },
    ENV_SWAMP: {
        PiratesGlobals.TOD_DAWN: SWAMP_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_DAY: SWAMP_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_DUSK: SWAMP_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_NIGHT: SWAMP_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_STARS: SWAMP_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_DIRECTIONAL_COLOR,
        },
    ENV_CAVE: {
        PiratesGlobals.TOD_DAWN: CAVE_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_DAY: CAVE_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_DUSK: CAVE_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_NIGHT: CAVE_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_STARS: CAVE_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: CAVE_HALLOWEEN_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_FULLMOON: CAVE_HALLOWEEN_DIRECTIONAL_COLOR,
        },
    ENV_LAVACAVE: {
        PiratesGlobals.TOD_DAWN: LAVACAVE_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_DAY: LAVACAVE_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_DUSK: LAVACAVE_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_NIGHT: LAVACAVE_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_STARS: LAVACAVE_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: CAVE_HALLOWEEN_DIRECTIONAL_COLOR,
        PiratesGlobals.TOD_FULLMOON: CAVE_HALLOWEEN_DIRECTIONAL_COLOR,
        },
    }
GrassLightColors = {
    PiratesGlobals.TOD_DAWN: DAWN_DIRECTIONAL_COLOR,
    PiratesGlobals.TOD_DAY: DAY_DIRECTIONAL_COLOR,
    PiratesGlobals.TOD_DUSK: DUSK_DIRECTIONAL_COLOR,
    PiratesGlobals.TOD_NIGHT: NIGHT_DIRECTIONAL_COLOR,
    PiratesGlobals.TOD_STARS: STARS_DIRECTIONAL_COLOR,
    PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_DIRECTIONAL_COLOR,
    }
FogColors = {
    ENV_DEFAULT: {
        PiratesGlobals.TOD_DAWN: DAWN_FOG_COLOR,
        PiratesGlobals.TOD_DAY: DAY_FOG_COLOR,
        PiratesGlobals.TOD_DUSK: DUSK_FOG_COLOR,
        PiratesGlobals.TOD_NIGHT: NIGHT_FOG_COLOR,
        PiratesGlobals.TOD_STARS: STARS_FOG_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_FOG_COLOR,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_FOG_COLOR,
        },
    ENV_FOREST: {
        PiratesGlobals.TOD_DAWN: FOREST_DAWN_FOG_COLOR,
        PiratesGlobals.TOD_DAY: FOREST_DAY_FOG_COLOR,
        PiratesGlobals.TOD_DUSK: FOREST_DUSK_FOG_COLOR,
        PiratesGlobals.TOD_NIGHT: FOREST_NIGHT_FOG_COLOR,
        PiratesGlobals.TOD_STARS: FOREST_STARS_FOG_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_FOG_COLOR,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_FOG_COLOR,
        },
    ENV_SWAMP: {
        PiratesGlobals.TOD_DAWN: SWAMP_FOG_COLOR,
        PiratesGlobals.TOD_DAY: SWAMP_FOG_COLOR,
        PiratesGlobals.TOD_DUSK: SWAMP_FOG_COLOR,
        PiratesGlobals.TOD_NIGHT: SWAMP_FOG_COLOR,
        PiratesGlobals.TOD_STARS: SWAMP_FOG_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_FOG_COLOR,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_FOG_COLOR,
        },
    ENV_CAVE: {
        PiratesGlobals.TOD_DAWN: CAVE_FOG_COLOR,
        PiratesGlobals.TOD_DAY: CAVE_FOG_COLOR,
        PiratesGlobals.TOD_DUSK: CAVE_FOG_COLOR,
        PiratesGlobals.TOD_NIGHT: CAVE_FOG_COLOR,
        PiratesGlobals.TOD_STARS: CAVE_FOG_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_FOG_COLOR,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_FOG_COLOR,
        },
    ENV_LAVACAVE: {
        PiratesGlobals.TOD_DAWN: LAVACAVE_FOG_COLOR,
        PiratesGlobals.TOD_DAY: LAVACAVE_FOG_COLOR,
        PiratesGlobals.TOD_DUSK: LAVACAVE_FOG_COLOR,
        PiratesGlobals.TOD_NIGHT: LAVACAVE_FOG_COLOR,
        PiratesGlobals.TOD_STARS: LAVACAVE_FOG_COLOR,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_FOG_COLOR,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_FOG_COLOR,
        },
    }
FogExps = {
    ENV_DEFAULT: {
        PiratesGlobals.TOD_DAWN: DAWN_FOG_EXP,
        PiratesGlobals.TOD_DAY: DAY_FOG_EXP,
        PiratesGlobals.TOD_DUSK: DUSK_FOG_EXP,
        PiratesGlobals.TOD_NIGHT: NIGHT_FOG_EXP,
        PiratesGlobals.TOD_STARS: STARS_FOG_EXP,
        PiratesGlobals.TOD_HALLOWEEN: HALLOWEEN_FOG_EXP,
        PiratesGlobals.TOD_FULLMOON: HALLOWEEN_FOG_EXP,
        },
    ENV_FOREST: {
        PiratesGlobals.TOD_DAWN: FOREST_FOG_EXP,
        PiratesGlobals.TOD_DAY: FOREST_FOG_EXP,
        PiratesGlobals.TOD_DUSK: FOREST_FOG_EXP,
        PiratesGlobals.TOD_NIGHT: FOREST_FOG_EXP,
        PiratesGlobals.TOD_STARS: FOREST_NIGHT_FOG_EXP,
        PiratesGlobals.TOD_HALLOWEEN: FOREST_NIGHT_FOG_EXP,
        PiratesGlobals.TOD_FULLMOON: FOREST_NIGHT_FOG_EXP,
        },
    ENV_SWAMP: {
        PiratesGlobals.TOD_DAWN: SWAMP_FOG_EXP,
        PiratesGlobals.TOD_DAY: SWAMP_FOG_EXP,
        PiratesGlobals.TOD_DUSK: SWAMP_FOG_EXP,
        PiratesGlobals.TOD_NIGHT: SWAMP_FOG_EXP,
        PiratesGlobals.TOD_STARS: SWAMP_FOG_EXP,
        PiratesGlobals.TOD_HALLOWEEN: SWAMP_FOG_EXP,
        PiratesGlobals.TOD_FULLMOON: SWAMP_FOG_EXP,
        },
    ENV_CAVE: {
        PiratesGlobals.TOD_DAWN: CAVE_FOG_EXP,
        PiratesGlobals.TOD_DAY: CAVE_FOG_EXP,
        PiratesGlobals.TOD_DUSK: CAVE_FOG_EXP,
        PiratesGlobals.TOD_NIGHT: CAVE_FOG_EXP,
        PiratesGlobals.TOD_STARS: CAVE_FOG_EXP,
        PiratesGlobals.TOD_HALLOWEEN: CAVE_FOG_EXP,
        PiratesGlobals.TOD_FULLMOON: CAVE_FOG_EXP,
        },
    ENV_LAVACAVE: {
        PiratesGlobals.TOD_DAWN: LAVACAVE_FOG_EXP,
        PiratesGlobals.TOD_DAY: LAVACAVE_FOG_EXP,
        PiratesGlobals.TOD_DUSK: LAVACAVE_FOG_EXP,
        PiratesGlobals.TOD_NIGHT: LAVACAVE_FOG_EXP,
        PiratesGlobals.TOD_STARS: LAVACAVE_FOG_EXP,
        PiratesGlobals.TOD_HALLOWEEN: LAVACAVE_FOG_EXP,
        PiratesGlobals.TOD_FULLMOON: LAVACAVE_FOG_EXP,
        },
    }
SkyColors = {
    PiratesGlobals.TOD_DAWN: Vec4(0.72, 0.72, 0.52, 1),
    PiratesGlobals.TOD_DAY: Vec4(0.4, 0.6, 0.85, 1),
    PiratesGlobals.TOD_DUSK: Vec4(0.65, 0.55, 0.5, 1),
    PiratesGlobals.TOD_NIGHT: Vec4(0.075, 0.13, 0.26, 1),
    PiratesGlobals.TOD_STARS: Vec4(0.075, 0.13, 0.26, 1) * 0.3,
    PiratesGlobals.TOD_HALLOWEEN: Vec4(0.075, 0.05, 0.12, 1),
    PiratesGlobals.TOD_SWAMP: Vec4(0.2, 0.25, 0.3, 1),
    }
