from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import AmbientManagerBase

class PiratesAmbientManager(AmbientManagerBase.AmbientManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesAmbientManager')
    
    def __init__(self):
        AmbientManagerBase.AmbientManagerBase.__init__(self)
        self.load('jungle', 'phase_4/audio/sfx_jungle_mix.wav')
        self.load('cave', 'phase_4/audio/sfx_cave_drips.wav')
        self.load('swamp', 'phase_4/audio/sfx_swamp_mix.wav')
        self.load('spanish', 'phase_4/audio/sfx_town_npchouse-spanish.wav')
        self.load('shanty', 'phase_4/audio/sfx_town_npchouse-shanty.wav')
        self.load('ship-creak', 'audio/sfx_ship_idle.wav')
        self.load('jail_interior', 'phase_2/audio/sfx_jail_interior_loop.wav')
        self.volumeModifierDict = {
            'jungle': 0.6,
            'swamp': 0.75,
            'jail_interior': 1.25}

    def calcAmbientNameFromStr(self, str):
        retval = None
        if str:
            if 'jungle' in str:
                retval = 'jungle'
            elif 'cave' in str:
                retval = 'cave'
            elif 'swamp' in str:
                retval = 'swamp'
            elif 'spanish' in str:
                retval = 'spanish'
            elif 'shanty' in str:
                retval = 'shanty'
            elif 'jail_interior' in str:
                retval = 'jail_interior'
            else:
                self.notify.debug("don't know what to do with %s, using None" % str)
        
        return retval

    def requestChangeVolume(self, name, duration, finalVolume, priority = 0):
        newFinalVolume = finalVolume
        if name in list(self.volumeModifierDict.keys()):
            newFinalVolume = finalVolume * self.volumeModifierDict[name]
        
        AmbientManagerBase.AmbientManagerBase.requestChangeVolume(self, name, duration, newFinalVolume, priority)


