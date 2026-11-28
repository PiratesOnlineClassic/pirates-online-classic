from direct.directnotify import DirectNotifyGlobal

from pirates.pvp.PVPGameBaseAI import PVPGameBaseAI


class PVPGameShipBattleAI(PVPGameBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameShipBattleAI')
