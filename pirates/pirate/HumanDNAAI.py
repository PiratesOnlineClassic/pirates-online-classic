from direct.directnotify.DirectNotifyGlobal import *

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
