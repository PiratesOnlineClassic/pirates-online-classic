from direct.directnotify import DirectNotifyGlobal

from pirates.piratesbase import PiratesGlobals
from pirates.pvp.DistributedPVPInstanceAI import DistributedPVPInstanceAI
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedPVPBattleAI(DistributedPVPInstanceAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPVPBattleAI')

    GameStyle = PiratesGlobals.GAME_STYLE_BATTLE
    RankingType = InventoryType.BTLGame
    TimeLimit = config.GetInt('pvp-battle-time-limit', 600)
    ScoreLimit = config.GetInt('pvp-battle-score-limit', 15)

    def __init__(self, air):
        DistributedPVPInstanceAI.__init__(self, air)

        self.nextTeam = 1

    def getPlayerTeam(self, avatar, team):
        # every pirate fights for themselves in a battle, so each
        # player is given a team of their very own...
        team = self.nextTeam
        self.nextTeam += 1
        return team
