from direct.directnotify import DirectNotifyGlobal

from pirates.pvp.PVPGameBaseAI import PVPGameBaseAI


class PVPGameBattleAI(PVPGameBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameBattleAI')
