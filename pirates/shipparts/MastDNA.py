from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from otp.speedchat import ColorSpace
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals
notify = directNotify.newCategory('MastDNA')
MastDict = {
    ShipGlobals.MAINMASTL1: 'models/char/mainmast_square_',
    ShipGlobals.MAINMASTL2: 'models/char/mainmast_square_',
    ShipGlobals.MAINMASTL3: 'models/char/mainmast_square_',
    ShipGlobals.MAINMASTL4: 'models/char/mainmast_square_',
    ShipGlobals.MAINMASTL5: 'models/char/mainmast_square_',
    ShipGlobals.TRIMASTL1: 'models/char/mainmast_tri_',
    ShipGlobals.TRIMASTL2: 'models/char/mainmast_tri_',
    ShipGlobals.TRIMASTL3: 'models/char/mainmast_tri_',
    ShipGlobals.TRIMASTL4: 'models/char/mainmast_tri_',
    ShipGlobals.TRIMASTL5: 'models/char/mainmast_tri_',
    ShipGlobals.FOREMASTL1: 'models/char/foremast_tri_',
    ShipGlobals.FOREMASTL2: 'models/char/foremast_multi_',
    ShipGlobals.FOREMASTL3: 'models/char/foremast_multi_',
    ShipGlobals.AFTMASTL1: 'models/char/aftmast_tri_',
    ShipGlobals.AFTMASTL2: 'models/char/aftmast_tri_',
    ShipGlobals.AFTMASTL3: 'models/char/aftmast_tri_',
    ShipGlobals.SKEL_MAINMASTL1_A: 'models/char/mainmastA_ghost_',
    ShipGlobals.SKEL_MAINMASTL2_A: 'models/char/mainmastA_ghost_',
    ShipGlobals.SKEL_MAINMASTL3_A: 'models/char/mainmastA_ghost_',
    ShipGlobals.SKEL_MAINMASTL4_A: 'models/char/mainmastA_ghost_',
    ShipGlobals.SKEL_MAINMASTL5_A: 'models/char/mainmastA_ghost_',
    ShipGlobals.SKEL_MAINMASTL1_B: 'models/char/mainmastB_ghost_',
    ShipGlobals.SKEL_MAINMASTL2_B: 'models/char/mainmastB_ghost_',
    ShipGlobals.SKEL_MAINMASTL3_B: 'models/char/mainmastB_ghost_',
    ShipGlobals.SKEL_MAINMASTL4_B: 'models/char/mainmastB_ghost_',
    ShipGlobals.SKEL_MAINMASTL5_B: 'models/char/mainmastB_ghost_',
    ShipGlobals.SKEL_TRIMASTL1: 'models/char/mainmastA_tri_ghost_',
    ShipGlobals.SKEL_TRIMASTL2: 'models/char/mainmastA_tri_ghost_',
    ShipGlobals.SKEL_TRIMASTL3: 'models/char/mainmastA_tri_ghost_',
    ShipGlobals.SKEL_TRIMASTL4: 'models/char/mainmastA_tri_ghost_',
    ShipGlobals.SKEL_TRIMASTL5: 'models/char/mainmastA_tri_ghost_',
    ShipGlobals.SKEL_FOREMASTL1: 'models/char/foremastA_ghost_',
    ShipGlobals.SKEL_FOREMASTL2: 'models/char/foremastA_ghost_',
    ShipGlobals.SKEL_FOREMASTL3: 'models/char/foremastA_ghost_',
    ShipGlobals.SKEL_AFTMASTL1: 'models/char/aftmastA_ghost_',
    ShipGlobals.SKEL_AFTMASTL2: 'models/char/aftmastA_ghost_',
    ShipGlobals.SKEL_AFTMASTL3: 'models/char/aftmastA_ghost_'}
MastFlatDict = {
    ShipGlobals.MAINMASTL1: 'models/shipparts/flat_mainmast_square',
    ShipGlobals.MAINMASTL2: 'models/shipparts/flat_mainmast_square',
    ShipGlobals.MAINMASTL3: 'models/shipparts/flat_mainmast_square',
    ShipGlobals.MAINMASTL4: 'models/shipparts/flat_mainmast_square',
    ShipGlobals.MAINMASTL5: 'models/shipparts/flat_mainmast_square',
    ShipGlobals.TRIMASTL1: 'models/shipparts/flat_mainmast_tri',
    ShipGlobals.TRIMASTL2: 'models/shipparts/flat_mainmast_tri',
    ShipGlobals.TRIMASTL3: 'models/shipparts/flat_mainmast_tri',
    ShipGlobals.TRIMASTL4: 'models/shipparts/flat_mainmast_tri',
    ShipGlobals.TRIMASTL5: 'models/shipparts/flat_mainmast_tri',
    ShipGlobals.FOREMASTL1: 'models/shipparts/flat_foremast_tri',
    ShipGlobals.FOREMASTL2: 'models/shipparts/flat_foremast_multi',
    ShipGlobals.FOREMASTL3: 'models/shipparts/flat_foremast_multi',
    ShipGlobals.AFTMASTL1: 'models/shipparts/flat_aftmast_tri',
    ShipGlobals.AFTMASTL2: 'models/shipparts/flat_aftmast_tri',
    ShipGlobals.AFTMASTL3: 'models/shipparts/flat_aftmast_tri',
    ShipGlobals.SKEL_MAINMASTL1_A: 'models/shipparts/flat_mainmastA_ghost',
    ShipGlobals.SKEL_MAINMASTL2_A: 'models/shipparts/flat_mainmastA_ghost',
    ShipGlobals.SKEL_MAINMASTL3_A: 'models/shipparts/flat_mainmastA_ghost',
    ShipGlobals.SKEL_MAINMASTL4_A: 'models/shipparts/flat_mainmastA_ghost',
    ShipGlobals.SKEL_MAINMASTL5_A: 'models/shipparts/flat_mainmastA_ghost',
    ShipGlobals.SKEL_MAINMASTL1_B: 'models/shipparts/flat_mainmastB_ghost',
    ShipGlobals.SKEL_MAINMASTL2_B: 'models/shipparts/flat_mainmastB_ghost',
    ShipGlobals.SKEL_MAINMASTL3_B: 'models/shipparts/flat_mainmastB_ghost',
    ShipGlobals.SKEL_MAINMASTL4_B: 'models/shipparts/flat_mainmastB_ghost',
    ShipGlobals.SKEL_MAINMASTL5_B: 'models/shipparts/flat_mainmastB_ghost',
    ShipGlobals.SKEL_TRIMASTL1: 'models/shipparts/flat_mainmast_tri',
    ShipGlobals.SKEL_TRIMASTL2: 'models/shipparts/flat_mainmast_tri',
    ShipGlobals.SKEL_TRIMASTL3: 'models/shipparts/flat_mainmast_tri',
    ShipGlobals.SKEL_TRIMASTL4: 'models/shipparts/flat_mainmast_tri',
    ShipGlobals.SKEL_TRIMASTL5: 'models/shipparts/flat_mainmast_tri',
    ShipGlobals.SKEL_FOREMASTL1: 'models/shipparts/flat_foremastA_ghost',
    ShipGlobals.SKEL_FOREMASTL2: 'models/shipparts/flat_foremastA_ghost',
    ShipGlobals.SKEL_FOREMASTL3: 'models/shipparts/flat_foremastA_ghost',
    ShipGlobals.SKEL_AFTMASTL1: 'models/shipparts/flat_aftmastA_ghost',
    ShipGlobals.SKEL_AFTMASTL2: 'models/shipparts/flat_aftmastA_ghost',
    ShipGlobals.SKEL_AFTMASTL3: 'models/shipparts/flat_aftmastA_ghost'}
MastSegment0Anims = (('break0A', 'break0A'),)
MastSegment1Anims = (('break1A', 'break1A'),)
MastSegment2Anims = (('break2A', 'break2A'),)
MastSegment3Anims = (('break3A', 'break3A'),)
MastSegment4Anims = (('break4A', 'break4A'),)
MastAnimListByHeight = [
    [
        'break0A'],
    [
        'break0A',
        'break1A'],
    [
        'break0A',
        'break1A',
        'break2A'],
    [
        'break0A',
        'break1A',
        'break2A',
        'break3A'],
    [
        'break0A',
        'break1A',
        'break2A',
        'break3A',
        'break4A']]
DefaultAnimDict = (('Idle', 'idle'), ('Hidden', 'hidden'))
AllMastAnims = [
    'break0A',
    'break1A',
    'break2A',
    'break3A',
    'break4A']
RiggingDict = {
    ShipGlobals.WARSHIPL1: 'models/char/warshipL1-rigging_',
    ShipGlobals.WARSHIPL2: 'models/char/warshipL2-rigging_',
    ShipGlobals.WARSHIPL3: 'models/char/warshipL3-rigging_',
    ShipGlobals.WARSHIPL4: 'models/char/warshipL4-rigging_',
    ShipGlobals.MERCHANTL1: 'models/char/merchantL1-rigging_',
    ShipGlobals.MERCHANTL2: 'models/char/merchantL2-rigging_',
    ShipGlobals.MERCHANTL3: 'models/char/merchantL3-rigging_',
    ShipGlobals.MERCHANTL4: 'models/char/merchantL4-rigging_',
    ShipGlobals.INTERCEPTORL1: 'models/char/interceptorL1-rigging_',
    ShipGlobals.INTERCEPTORL2: 'models/char/interceptorL2-rigging_',
    ShipGlobals.INTERCEPTORL3: 'models/char/interceptorL3-rigging_',
    ShipGlobals.INTERCEPTORL4: 'models/char/interceptorL4-rigging_',
    ShipGlobals.BLACK_PEARL: 'models/char/blackpearl-rigging_',
    ShipGlobals.GOLIATH: 'models/char/goliath-rigging_'}
MastColors = [
    VBase4(1.0, 1.0, 1.0, 1.0),
    VBase4(0.0, 0.0, 0.0, 1.0),
    VBase4(0.933594, 0.265625, 0.28125, 1.0),
    VBase4(0.863281, 0.40625, 0.417969, 1.0),
    VBase4(0.710938, 0.234375, 0.4375, 1.0),
    VBase4(0.992188, 0.480469, 0.167969, 1.0),
    VBase4(0.996094, 0.898438, 0.320312, 1.0),
    VBase4(0.550781, 0.824219, 0.324219, 1.0),
    VBase4(0.242188, 0.742188, 0.515625, 1.0),
    VBase4(0.433594, 0.90625, 0.835938, 1.0),
    VBase4(0.347656, 0.820312, 0.953125, 1.0),
    VBase4(0.191406, 0.5625, 0.773438, 1.0)
]
TextureDict = {
    200: 'ad_ship_bp_mast_composite'}

class MastDNA(AvatarDNA.AvatarDNA):
    
    def __init__(self):
        self.shipClass = 0
        self.modelClass = 0
        self.baseTeam = PiratesGlobals.INVALID_TEAM
        self.mastType = 0
        self.posIndex = 0
        self.textureIndex = 0
        self.sailTextureIndex = 0
        self.sailLogoIndex = 0
        self.colorIndex = 0
        self.sailConfig = []

    def __str__(self):
        string = 'shipClass %s, mastType %s, posIndex %s, colorIndex %s, sailConfig %s' % (self.shipClass, self.mastType, self.posIndex, self.colorIndex, self.sailConfig)
        return string

    def setShipClass(self, val):
        self.shipClass = val
        self.modelClass = ShipGlobals.getModelClass(val)

    def setBaseTeam(self, val):
        self.baseTeam = val

    def setMastType(self, val):
        self.mastType = val

    def setPosIndex(self, val):
        self.posIndex = val

    def setColorIndex(self, val):
        self.colorIndex = val

    def setSailConfig(self, val):
        self.sailConfig = val

    def setTextureIndex(self, val):
        self.textureIndex = val

    def getShipClass(self):
        return self.shipClass

    def getModelClass(self):
        return self.modelClass

    def getBaseTeam(self):
        return self.baseTeam

    def getMastType(self):
        return self.mastType

    def getPosIndex(self):
        return self.posIndex

    def getColorIndex(self):
        return self.colorIndex

    def getSailConfig(self):
        return self.sailConfig

    def getTextureIndex(self):
        return self.textureIndex

