from direct.directnotify import DirectNotifyGlobal

from pirates.pvp.PVPGameBaseAI import PVPGameBaseAI


class PVPGameTeamBattleAI(PVPGameBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameTeamBattleAI')
