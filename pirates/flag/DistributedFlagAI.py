from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.flag import FlagGlobals
from pirates.flag.FlagDNA import FlagDNA
from pirates.uberdog.UberDogGlobals import InventoryCategory


def getValidatedFlagDNAString(dnaStr):
    """
    Parses the flag DNA string sent by a client, returning the re-packed DNA string
    if every value is within the ranges the flag designer can produce, otherwise None.
    """

    dna = FlagDNA()
    try:
        dna.setDNAString(dnaStr)
    except Exception:
        return None

    if not 0 <= dna.getShapeStyle() < FlagGlobals.ShapeCount:
        return None

    bgStyle, color0, color1, color2, color3, hFlip, vFlip = dna.bgData
    if not 0 <= bgStyle < FlagGlobals.BackgroundCount:
        return None

    for color in (color0, color1, color2, color3):
        if not 0 <= color < len(FlagGlobals.Colors):
            return None

    if hFlip not in (0, 1) or vFlip not in (0, 1):
        return None

    layoutStyle = dna.getLayoutStyle()
    if not 0 <= layoutStyle < FlagGlobals.LayoutCount:
        return None

    if dna.getNumEmblems() > FlagGlobals.MaxEmblemCount:
        return None

    for index in dna.getEmblemIndices():
        if not 0 <= dna.getEmblemStyle(index) < FlagGlobals.EmblemCount:
            return None

        if not 0 <= dna.getEmblemColor(index) < len(FlagGlobals.Colors):
            return None

        if not 0 <= dna.getEmblemPos(index) < len(FlagGlobals.LayoutOffsets[layoutStyle]):
            return None

    return dna.getDNAString()


class DistributedFlagAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlagAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.dnaString = b''

    def setDNAString(self, dnaString):
        self.dnaString = dnaString

    def d_setDNAString(self, dnaString):
        self.sendUpdate('setDNAString', [dnaString])

    def b_setDNAString(self, dnaString):
        self.setDNAString(dnaString)
        self.d_setDNAString(dnaString)

    def getDNAString(self):
        return self.dnaString

    def requestDNAString(self, dnaString):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)
        if not inventory or self.doId not in inventory.getDoIdListCategory(InventoryCategory.FLAGS):
            self.air.writeServerEvent('suspicious', avId=avatar.doId,
                issue='Tried to change the design of flag %d they do not own!' % self.doId)

            return

        dnaString = getValidatedFlagDNAString(dnaString)
        if dnaString is None:
            self.air.writeServerEvent('suspicious', avId=avatar.doId,
                issue='Sent an invalid flag design for flag %d!' % self.doId)

            return

        self.b_setDNAString(dnaString)
