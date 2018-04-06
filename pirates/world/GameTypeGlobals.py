# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.GameTypeGlobals
import types

from otp.otpbase import OTPGlobals
from pandac.PandaModules import *
from pandac.PandaModules import ConfigVariable
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.uberdog import DistributedInventoryBase
from pirates.uberdog.UberDogGlobals import InventoryType

GAME_DURATION_SHORT = 0
GAME_DURATION_MED = 1
GAME_DURATION_LONG = 2
GAME_OPTION_DURATION = 0
GAME_OPTION_MATCH_COUNT = 1
GAME_OPTION_PASSWORD = 2
GAME_OPTION_NPC_PLAYERS = 3
GAME_OPTION_LOCATION = 4
GAME_OPTION_USE_CURR_CREW = 5
GAME_OPTION_MIN_BET = 6
GAME_OPTION_MIN_PLAYERS = 7
GAME_OPTION_DESIRED_PLAYERS = 8
GAME_OPTION_MAX_PLAYERS = 9
GAME_OPTION_MAX_CREW_SIZE = 10
GAME_OPTION_MAX_CREW_SHIP = 11
GAME_OPTION_VIP_PASS = 12
GAME_OPTION_CREW_INFO = 13
GAME_OPTION_TM_ID = 14
GAME_OPTION_SOLO_PLAY = 15
MATCH_CHANCE_LOW = 1
MATCH_CHANCE_MODERATE = 25
MATCH_CHANCE_HIGH = 75
GAME_TYPE_2_INSTANCE_TYPE = {PiratesGlobals.GAME_TYPE_PG: PiratesGlobals.INSTANCE_PG, PiratesGlobals.GAME_TYPE_PVP: PiratesGlobals.INSTANCE_PVP, PiratesGlobals.GAME_TYPE_HSA: PiratesGlobals.INSTANCE_MAIN, PiratesGlobals.GAME_TYPE_TM: PiratesGlobals.INSTANCE_TM, PiratesGlobals.GAME_TYPE_CREW: PiratesGlobals.INSTANCE_MAIN, PiratesGlobals.GAME_TYPE_QUEST: PiratesGlobals.INSTANCE_MAIN}

def gameType2InstanceType(gameType):
    instanceType = GAME_TYPE_2_INSTANCE_TYPE.get(gameType)
    return instanceType


GameTypeRanking = {PiratesGlobals.GAME_STYLE_CTF: InventoryType.CTFGame, PiratesGlobals.GAME_STYLE_CTL: InventoryType.CTLGame, PiratesGlobals.GAME_STYLE_PIRATEER: InventoryType.PTRGame, PiratesGlobals.GAME_STYLE_BATTLE: InventoryType.BTLGame, PiratesGlobals.GAME_STYLE_TEAM_BATTLE: InventoryType.TBTGame, PiratesGlobals.GAME_STYLE_SHIP_BATTLE: InventoryType.SBTGame, PiratesGlobals.GAME_STYLE_ARMADA: InventoryType.ARMGame, PiratesGlobals.GAME_STYLE_TKP: InventoryType.TKPGame, PiratesGlobals.GAME_STYLE_BTB: InventoryType.BTBGame, PiratesGlobals.GAME_STYLE_BLACKJACK: InventoryType.BlackjackGame, PiratesGlobals.GAME_STYLE_POKER: InventoryType.PokerGame}
GameTypeStrings = {'type': {PiratesGlobals.GAME_TYPE_PVP: PLocalizer.PVPGame, PiratesGlobals.GAME_TYPE_PG: PLocalizer.ParlorGame, PiratesGlobals.GAME_TYPE_HSA: PLocalizer.HSAGame, PiratesGlobals.GAME_TYPE_TM: PLocalizer.TMGame, PiratesGlobals.GAME_TYPE_CREW: PLocalizer.CrewGame, PiratesGlobals.GAME_TYPE_QUEST: PLocalizer.QuestGame}, 'typeBrief': {PiratesGlobals.GAME_TYPE_PVP: PLocalizer.PVPGameBrief, PiratesGlobals.GAME_TYPE_PG: PLocalizer.ParlorGameBrief, PiratesGlobals.GAME_TYPE_HSA: PLocalizer.HSAGameBrief, PiratesGlobals.GAME_TYPE_TM: PLocalizer.TMGameBrief, PiratesGlobals.GAME_TYPE_CREW: PLocalizer.CrewGameBrief, PiratesGlobals.GAME_TYPE_QUEST: PLocalizer.QuestGameBrief}, 'description': {PiratesGlobals.GAME_TYPE_PVP: PLocalizer.PVPGameDesc, PiratesGlobals.GAME_TYPE_PG: PLocalizer.ParlorGameDesc, PiratesGlobals.GAME_TYPE_HSA: PLocalizer.HSAGameDesc, PiratesGlobals.GAME_TYPE_TM: PLocalizer.TMGameDesc, PiratesGlobals.GAME_TYPE_CREW: PLocalizer.CrewGameDesc, PiratesGlobals.GAME_TYPE_QUEST: PLocalizer.QuestGameDesc}, 'descriptionStyle': {PiratesGlobals.GAME_STYLE_BATTLE: PLocalizer.GameStyleBattleDesc, PiratesGlobals.GAME_STYLE_TEAM_BATTLE: PLocalizer.GameStyleTeamBattleDesc, PiratesGlobals.GAME_STYLE_SHIP_BATTLE: PLocalizer.GameStyleShipBattleDesc, PiratesGlobals.GAME_STYLE_CTF: PLocalizer.GameStyleCTFDesc, PiratesGlobals.GAME_STYLE_CTL: PLocalizer.GameStyleCTLDesc, PiratesGlobals.GAME_STYLE_PIRATEER: PLocalizer.GameStylePirateer, PiratesGlobals.GAME_STYLE_POKER: PLocalizer.GameStylePoker, PiratesGlobals.GAME_STYLE_BLACKJACK: PLocalizer.GameStyleBlackjack, PiratesGlobals.CREW_STYLE_FIND_A_CREW: PLocalizer.CrewStyleFindACrewDesc, PiratesGlobals.CREW_STYLE_FIND_A_PVP_CREW: PLocalizer.CrewStyleFindAPVPCrewDesc, PiratesGlobals.CREW_STYLE_RECRUIT_MEMBERS: PLocalizer.CrewStyleRecruitMembersDesc}, 'icon': {PiratesGlobals.GAME_TYPE_PVP: 'lookout_win_pvp_game_icon', PiratesGlobals.GAME_TYPE_PG: 'lookout_win_parlor_game_icon', PiratesGlobals.GAME_TYPE_HSA: None, PiratesGlobals.GAME_TYPE_TM: 'lookout_win_treasuremap_icon', PiratesGlobals.GAME_TYPE_CREW: 'lookout_win_friend_icon', PiratesGlobals.GAME_TYPE_QUEST: None}, 'iconStyle': {PiratesGlobals.GAME_STYLE_BATTLE: None, PiratesGlobals.GAME_STYLE_TEAM_BATTLE: None, PiratesGlobals.GAME_STYLE_SHIP_BATTLE: None, PiratesGlobals.GAME_STYLE_CTF: None, PiratesGlobals.GAME_STYLE_CTL: None, PiratesGlobals.GAME_STYLE_PIRATEER: None, PiratesGlobals.GAME_STYLE_POKER: None, PiratesGlobals.GAME_STYLE_BLACKJACK: None}, 'style': {PiratesGlobals.GAME_STYLE_ANY: PLocalizer.AnyGame, PiratesGlobals.GAME_STYLE_CTF: PLocalizer.CTFGame, PiratesGlobals.GAME_STYLE_CTL: PLocalizer.CTLGame, PiratesGlobals.GAME_STYLE_PIRATEER: PLocalizer.PTRGame, PiratesGlobals.GAME_STYLE_BATTLE: PLocalizer.BTLGame, PiratesGlobals.GAME_STYLE_TEAM_BATTLE: PLocalizer.TBTGame, PiratesGlobals.GAME_STYLE_SHIP_BATTLE: PLocalizer.SBTGame, PiratesGlobals.GAME_STYLE_ARMADA: PLocalizer.ARMGame, PiratesGlobals.GAME_STYLE_TKP: PLocalizer.TKPGame, PiratesGlobals.GAME_STYLE_BTB: PLocalizer.BTBGame, PiratesGlobals.GAME_STYLE_BLACKJACK: PLocalizer.BlackjackGame, PiratesGlobals.GAME_STYLE_POKER: PLocalizer.PokerGame, PiratesGlobals.CREW_STYLE_FIND_A_CREW: PLocalizer.FindACrew, PiratesGlobals.CREW_STYLE_FIND_A_PVP_CREW: PLocalizer.FindAPVPCrew, PiratesGlobals.CREW_STYLE_RECRUIT_MEMBERS: PLocalizer.RecruitCrewMembers}, 'option': {GAME_OPTION_DURATION: PLocalizer.GameDuration, GAME_OPTION_MATCH_COUNT: PLocalizer.GameMatchCount, GAME_OPTION_PASSWORD: PLocalizer.GamePassword, GAME_OPTION_MIN_BET: PLocalizer.GameMinBet, GAME_OPTION_NPC_PLAYERS: PLocalizer.GameNPCPlayers, GAME_OPTION_LOCATION: PLocalizer.GameLocation, GAME_OPTION_USE_CURR_CREW: PLocalizer.GameUseCrew, GAME_OPTION_MIN_PLAYERS: PLocalizer.GameMinPlayers, GAME_OPTION_DESIRED_PLAYERS: PLocalizer.GameDesPlayers, GAME_OPTION_MAX_PLAYERS: PLocalizer.GameMaxPlayers, GAME_OPTION_MAX_CREW_SIZE: PLocalizer.GameMaxCrew, GAME_OPTION_MAX_CREW_SHIP: PLocalizer.GameMaxShip, GAME_OPTION_VIP_PASS: PLocalizer.GameVIPPass, GAME_OPTION_SOLO_PLAY: PLocalizer.GameSoloPlay}, 'optionVal': {GAME_DURATION_SHORT: PLocalizer.GameDurationShort, GAME_DURATION_MED: PLocalizer.GameDurationMed, GAME_DURATION_LONG: PLocalizer.GameDurationLong}}

def gatherGameStyleInfo(gameType, gameStyle, callback):
    styleInfo = {}
    if gameType == PiratesGlobals.GAME_TYPE_TM:

        def gatherTMInfo(inventory):
            if inventory:
                treasureMaps = inventory.getTreasureMapsList()
            else:
                treasureMaps = []
            tmsOwned = {}
            for currTM in treasureMaps:
                tmsOwned[currTM.mapId] = currTM.getOptions()

            callback(tmsOwned)

        if callback:
            if game.process == 'client':
                invRequest = DistributedInventoryBase.DistributedInventoryBase.getInventory(localAvatar.inventoryId, gatherTMInfo)
            else:
                tmsAvailable = {}
                if gameStyle != None:
                    numPlayers = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[PiratesGlobals.GAME_TYPE_TM][gameStyle].get('NumPlayers')
                    if numPlayers and len(numPlayers) > 1:
                        options = {GAME_OPTION_MAX_PLAYERS: numPlayers}
                        tmsAvailable[gameStyle] = options
                        styleInfo = {'options': options}
                callback(tmsAvailable)
    return styleInfo


GameTypes = {PiratesGlobals.GAME_TYPE_CREW: {'style': {PiratesGlobals.CREW_STYLE_FIND_A_CREW: {'options': {'execute': 'find'}}, PiratesGlobals.CREW_STYLE_FIND_A_PVP_CREW: {'options': {'execute': 'findPvp'}}, PiratesGlobals.CREW_STYLE_RECRUIT_MEMBERS: {'options': {'execute': 'recruit'}}}}, PiratesGlobals.GAME_TYPE_PVP: {'style': {PiratesGlobals.GAME_STYLE_CTL: {'options': {GAME_OPTION_MIN_PLAYERS: [PiratesGuiGlobals.UIItemType_ListItem, ['2', '3', '4', '5', '6']]}}, PiratesGlobals.GAME_STYLE_PIRATEER: {'options': {GAME_OPTION_MIN_PLAYERS: [PiratesGuiGlobals.UIItemType_ListItem, ['2', '3', '4', '5', '6']]}}, PiratesGlobals.GAME_STYLE_TEAM_BATTLE: {'options': {GAME_OPTION_MIN_PLAYERS: [PiratesGuiGlobals.UIItemType_ListItem, ['4', '6']], GAME_OPTION_MAX_PLAYERS: [PiratesGuiGlobals.UIItemType_Hidden, '8']}}, PiratesGlobals.GAME_STYLE_BATTLE: {'options': {GAME_OPTION_MIN_PLAYERS: [PiratesGuiGlobals.UIItemType_ListItem, ['2', '3', '4', '5', '6']], GAME_OPTION_MAX_PLAYERS: [PiratesGuiGlobals.UIItemType_Hidden, '8']}}, PiratesGlobals.GAME_STYLE_SHIP_BATTLE: {'options': {GAME_OPTION_MAX_CREW_SIZE: [PiratesGuiGlobals.UIItemType_Hidden], GAME_OPTION_MAX_CREW_SHIP: [PiratesGuiGlobals.UIItemType_Hidden]}}}}, PiratesGlobals.GAME_TYPE_PG: {'style': {PiratesGlobals.GAME_STYLE_BLACKJACK: {'options': {GAME_OPTION_MAX_PLAYERS: [PiratesGuiGlobals.UIItemType_Hidden, '6']}}, PiratesGlobals.GAME_STYLE_POKER: {'options': {GAME_OPTION_MAX_PLAYERS: [PiratesGuiGlobals.UIItemType_Hidden, '6']}}}}, PiratesGlobals.GAME_TYPE_TM: {'style': gatherGameStyleInfo, 'hidden': True}}
pvpMode = base.config.GetBool('pvp-testing-level', False)
if pvpMode < 1:
    del GameTypes[PiratesGlobals.GAME_TYPE_PVP]['style'][PiratesGlobals.GAME_STYLE_CTL]
if pvpMode < 2:
    del GameTypes[PiratesGlobals.GAME_TYPE_PVP]['style'][PiratesGlobals.GAME_STYLE_PIRATEER]
if pvpMode < 3:
    del GameTypes[PiratesGlobals.GAME_TYPE_PVP]['style'][PiratesGlobals.GAME_STYLE_SHIP_BATTLE]

def getGameTypes():
    return list(GameTypes.keys())


def getGameStyles(gameType, gameStyle=None, callback=None):
    if gameType in GameTypes and 'style' in GameTypes[gameType]:
        styleInfo = GameTypes[gameType]['style']
        if _styleInfoIsDynamic(styleInfo):
            return list(styleInfo(gameType, gameStyle, callback).keys())
        callback(list(styleInfo.keys()))
        return list(styleInfo.keys())


def styleInfoIsDynamic(gameType):
    styleInfo = GameTypes[gameType]['style']
    return _styleInfoIsDynamic(styleInfo)


def _styleInfoIsDynamic(styleInfo):
    return type(styleInfo) == types.MethodType or type(styleInfo) == types.FunctionType


def getGameOptions(gameType, gameStyle=None, callback=None):
    gameOptions = {}
    if gameType in GameTypes:
        if 'options' in GameTypes[gameType]:
            return GameTypes[gameType]['options']
        elif gameStyle != None and 'style' in GameTypes[gameType]:
            styleInfo = GameTypes[gameType]['style']
            if _styleInfoIsDynamic(styleInfo):

                def extractOptions(tmsOwned):
                    if callback:
                        foundOptions = {}
                        if tmsOwned:
                            foundOptions = tmsOwned[gameStyle].get('options', {})
                        callback(foundOptions)

                gameOptions = styleInfo(gameType, gameStyle, extractOptions).get('options', {})
            elif gameStyle in styleInfo:
                gameOptions = styleInfo[gameStyle]['options']
                if callback:
                    callback(gameOptions)
    return gameOptions


def getGameTypeString(value, type, category=None):
    if category != None and category in PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS:
        typeInfo = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[category].get(value)
        if typeInfo:
            if type == 'style':
                return typeInfo.get('Name')
            elif type == 'descriptionStyle':
                return typeInfo.get('Desc')
    values = GameTypeStrings.get(type)
    foundStr = None
    if values:
        foundStr = values.get(value)
    return foundStr


def getGameTypeRanking(value):
    foundIt = GameTypeRanking.get(value)
    return foundIt


def gameTypeAccessable(gameCat, gameType, gameAccess):
    if gameAccess == OTPGlobals.AccessFull or gameAccess == OTPGlobals.AccessUnknown:
        return True
    else:
        if gameCat == PiratesGlobals.GAME_TYPE_PVP and gameType == PiratesGlobals.GAME_STYLE_BATTLE or gameCat == PiratesGlobals.GAME_TYPE_PG and gameType == PiratesGlobals.GAME_STYLE_BLACKJACK:
            return True
    return False
# okay decompiling .\pirates\world\GameTypeGlobals.pyc
