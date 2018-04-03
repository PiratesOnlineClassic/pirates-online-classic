# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.TitleGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PLocalizer
ShipPVPTitle = 1
LandPVPTitle = 2
FounderTitle = 3
CollectorTitle = 4
shipPVPIcons = {0: None, 1: 'sail_come_about', 2: 'pistol_eagle_eye', 3: 'dagger_dodge', 4: 'dagger_throw_dirt', 5: 'grenade_determination2', 6: 'grenade_determination', 7: 'sail_come_about'}
founderIcons = {0: None, 1: 'founders_coin'}
standardScale = 1.1
foundersScale = 2.9
RenownBreakpointsSea = [
 0, 25, 100, 500, 2000, 8000, 16000, 32000]
RenownBreakpointsLand = [0, 25, 100, 500, 2000, 8000, 16000, 32000]
TestBreakpoints1 = [
 0, 5, 10, 40, 60, 200, 564, 2323]
TestBreakpoints2 = [0, 500, 501, 502, 503, 504, 564, 2323]
FounderBreakpoints = [
 0, 1]
TitlesDict = {ShipPVPTitle: ('models/textureCards/skillIcons', shipPVPIcons, standardScale, PLocalizer.PVPTitleSeaName, PLocalizer.PVPTitleSeaRanks, PLocalizer.PVPTitleSeaDesc, RenownBreakpointsSea, InventoryType.PVPTotalInfamySea, 0), LandPVPTitle: ('models/textureCards/skillIcons', shipPVPIcons, standardScale, PLocalizer.PVPTitleLandName, PLocalizer.PVPTitleLandRanks, PLocalizer.PVPTitleLandDesc, RenownBreakpointsLand, InventoryType.PVPTotalInfamyLand, 0), FounderTitle: ('models/gui/toplevel_gui', founderIcons, foundersScale, PLocalizer.FounderTitleName, PLocalizer.FounderTitleRanks, PLocalizer.FounderTitleDesc, FounderBreakpoints, None, 1)}

def isBooleanTitle(title):
    return TitlesDict[title][8]


def getScale(title):
    return TitlesDict[title][2]


def getBreakpoints(title):
    return TitlesDict[title][6]


def getInventoryType(title):
    return TitlesDict[title][7]


def getTitleName(title):
    return TitlesDict[title][3]


def getTitleRankName(title, exp):
    rank = getRank(title, exp)
    if not TitlesDict[title][4][rank]:
        return PLocalizer.NoTitle
    if isBooleanTitle(title):
        return TitlesDict[title][4][rank]
    return TitlesDict[title][4][rank] + ' (%s)' % rank


def getTitleDesc(title):
    return TitlesDict[title][5]


def getIconName(title, rank):
    titleAttr = TitlesDict[title]
    iconNames = titleAttr[1]
    return iconNames[rank]


def getIconList(title):
    return TitlesDict[title][1]


def getModelPath(title):
    return TitlesDict[title][0]


def getRank(title, expPoints):
    if not title:
        return 0
    titleAttr = TitlesDict[title]
    if not titleAttr:
        return 0
    breakpoints = titleAttr[6]
    if not breakpoints:
        return 0
    if title == FounderTitle:
        if expPoints:
            return 1
        else:
            return 0
    high = 0
    for testValue in breakpoints:
        if testValue > expPoints:
            return high - 1
        high += 1

    return high - 1


def getMaxRank(title):
    if not title:
        return 0
    titleAttr = TitlesDict[title]
    if not titleAttr:
        return 0
    breakpoints = titleAttr[6]
    if not breakpoints:
        return 0
    return len(breakpoints) - 1
# okay decompiling .\pirates\pirate\TitleGlobals.pyc
