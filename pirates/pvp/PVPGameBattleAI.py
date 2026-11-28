from direct.directnotify import DirectNotifyGlobal

from pirates.pvp import PVPGlobals
from pirates.pvp.PVPGameBaseAI import PVPGameBaseAI


class PVPGameBattleAI(PVPGameBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameBattleAI')

    TimeLimit = config.GetInt('pvp-battle-time-limit', 600)
    ScoreLimit = config.GetInt('pvp-battle-score-limit', 15)

    def handleDefeat(self, defeaterId, defeatedId):
        if defeaterId != defeatedId:
            self.addPlayerStat(defeaterId, PVPGlobals.SCORE, 1)
