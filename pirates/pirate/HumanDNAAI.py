from direct.directnotify.DirectNotifyGlobal import *
from otp.ai.MagicWordGlobal import *

from pirates.pirate.HumanDNA import HumanDNA


class HumanDNAAI(HumanDNA):
    notify = directNotify.newCategory('HumanDNAAI')

    def d_setTutorial(self, tutorial):
        self.sendUpdate('setTutorial', [tutorial])

    def b_setTutorial(self, tutorial):
        self.setTutorial(tutorial)
        self.d_setTutorial(tutorial)

    def d_setGender(self, gender):
        self.sendUpdate('setGender', [gender])

    def b_setGender(self, gender):
        self.setGender(gender)
        self.d_setGender(gender)

    def d_setHairHair(self, val):
        self.sendUpdate('setHairHair', [val])

    def b_setHairHair(self, val):
        self.setHairHair(val)
        self.d_setHairHair(val)
        self.d_setHair()

    def d_setHairBeard(self, val):
        self.sendUpdate('setHairBeard', [val])

    def b_setHairBeard(self, val):
        self.setHairBeard(val)
        self.d_setHairBeard(val)
        self.d_setHair()

    def d_setHairMustache(self, val):
        self.sendUpdate('setHairMustache', [val])

    def b_setHairMustache(self, val):
        self.setHairMustache(val)
        self.d_setHairMustache(val)
        self.d_setHair()

    def d_setHairColor(self, val):
        self.sendUpdate('setHairColor', [val])

    def b_setHairColor(self, val):
        self.setHairColor(val)
        self.d_setHairColor(val)
        self.d_setHair()

    def d_setHair(self):
        self.sendUpdate('setHair', [self.getHairHair(), self.getHairBeard(), self.getHairMustache(), self.getHairColor()])

    def sendMolecularUpdate(self, fieldName, atomics):
        # Every atomic field is sent so the database stores the change, the
        # molecular field then has the clients rebuild the avatar once...
        args = []
        for atomicName, values in atomics:
            values = list(values)
            self.sendUpdate(atomicName, values)
            args.extend(values)

        self.sendUpdate(fieldName, args)

    def d_setClothes(self):
        self.sendMolecularUpdate('setClothes', [
            ('setHatIdx', [self.getHatIdx()]),
            ('setHatTexture', [self.getHatTexture()]),
            ('setHatColor', [self.getHatColor()]),
            ('setClothesShirt', self.getClothesShirt()),
            ('setClothesVest', self.getClothesVest()),
            ('setClothesCoat', self.getClothesCoat()),
            ('setClothesBelt', self.getClothesBelt()),
            ('setClothesPant', self.getClothesPant()),
            ('setClothesShoe', self.getClothesShoe()),
            ('setClothesTopColor', self.getClothesTopColor()),
            ('setClothesBotColor', self.getClothesBotColor())])

    def d_setJewelry(self):
        self.sendMolecularUpdate('setJewelry', [
            ('setJewelryZone1', self.getJewelryZone1()),
            ('setJewelryZone2', self.getJewelryZone2()),
            ('setJewelryZone3', self.getJewelryZone3()),
            ('setJewelryZone4', self.getJewelryZone4()),
            ('setJewelryZone5', self.getJewelryZone5()),
            ('setJewelryZone6', self.getJewelryZone6()),
            ('setJewelryZone7', self.getJewelryZone7()),
            ('setJewelryZone8', self.getJewelryZone8())])

    def d_setTattoos(self):
        self.sendMolecularUpdate('setTattoos', [
            ('setTattooChest', self.getTattooChest()),
            ('setTattooZone2', self.getTattooZone2()),
            ('setTattooZone3', self.getTattooZone3()),
            ('setTattooZone4', self.getTattooZone4()),
            ('setTattooZone5', self.getTattooZone5()),
            ('setTattooZone6', self.getTattooZone6()),
            ('setTattooZone7', self.getTattooZone7()),
            ('setTattooZone8', self.getTattooZone8())])


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str, int])
def dna(dnaType, val=0):
    target = spellbook.getTarget()

    # TODO: Implement a check to see if the value is not in the range of the dna type.
    # TODO: clothing, tattoo, jewelry, etc.
    if dnaType == 'hair':
        target.b_setHairHair(val)
        return 'Hair value set to: %s' % val
    elif dnaType == 'mustache':
        target.b_setHairMustache(val)
        return 'Mustache value set to: %s' % val
    elif dnaType == 'beard':
        target.b_setHairBeard(val)
        return 'Beard value set to: %s' % val
    else:
        return 'DNA Type: %s is not yet supported!' % dnaType

