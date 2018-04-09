# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesbase.MusicManager
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.piratesbase import AmbientManagerBase
from pirates.uberdog import UberDogGlobals

musicDict = {'combat_a': 'audio/music_combat_a.mp3', 'combat_b': 'audio/music_combat_b.mp3', 'combat_c': 'audio/music_combat_c.mp3', 'final_battle': 'audio/music_final_battle.mp3', 'tavern_a': 'audio/music_tavern_a.mp3', 'tavern_b': 'audio/music_tavern_b.mp3', 'tavern_c': 'audio/music_tavern_c.mp3', 'he_is_a_pirate': 'audio/he_is_a_pirate.mp3', 'will_and_elizabeth': 'audio/will_and_elizabeth.mp3', 'ship-sailing-a': 'audio/music_sailing_a.mp3', 'ship-sailing-b': 'audio/music_sailing_b.mp3', 'ship-sailing-c': 'audio/music_sailing_c.mp3', 'ship-adrift': 'audio/music_sailing_e.mp3', 'ship-docked': 'audio/music_sailing_e.mp3', 'ship-pinned': 'audio/music_wheel_10.mp3', 'ship-ensnared': 'audio/music_wheel_08.mp3', 'ship-sinking': 'audio/music_wheel_08_short.mp3', 'ship-positioned': 'audio/music_wheel_12.mp3', 'death': 'audio/music_wheel_08_short.mp3', 'levelup': 'audio/music_wheel_02_short.mp3', 'victory': 'audio/music_wheel_02.mp3', 'make-a-pirate': 'audio/music_jack_01.mp3', 'avchooser-theme': 'audio/will_and_elizabeth.mp3', 'searching': 'audio/music_wheel_03.mp3', 'island-padre-del-fuego': 'audio/music_madre_del_fuego.mp3', 'island-port-royal': 'audio/music_port_royal.mp3', 'island-tortuga': 'audio/music_tortuga.mp3', 'island-cuba': 'audio/music_cuba.mp3', 'island-devils-anvil': 'audio/music_devils_anvil.mp3', 'island-driftwood': 'audio/music_driftwood.mp3', 'island-kingshead': 'audio/music_kingshead.mp3', 'island-outcast': 'audio/music_outcast.mp3', 'island-perdida': 'audio/music_perdida.mp3', 'island-rumrunner': 'audio/music_rumrunner.mp3', 'island-tormenta': 'audio/music_tormenta.mp3', 'island-cangrejos': 'audio/music_cangrejos.mp3', 'island-cutthroat': 'audio/music_cutthroat.mp3', 'island-general': 'audio/music_creepy_c.mp3', 'cave': 'audio/music_creepy_a.mp3', 'jungle': 'audio/music_creepy_b.mp3', 'swamp': 'audio/music_creepy_c.mp3', 'kraken-sink-ship': 'audio/music_kraken_sink_ship.mp3', 'performers-02': 'audio/music_performers_02.mp3', 'performers-07': 'audio/music_performers_07.mp3', 'performers-09': 'audio/music_performers_09.mp3', 'performers-10': 'audio/music_performers_10.mp3'}
songItem2MusicLabel = {UberDogGlobals.InventoryType.Song_1: 'island-driftwood', UberDogGlobals.InventoryType.Song_2: 'island-cangrejos', UberDogGlobals.InventoryType.Song_3: 'island-outcast', UberDogGlobals.InventoryType.Song_4: 'performers-02', UberDogGlobals.InventoryType.Song_5: 'performers-10', UberDogGlobals.InventoryType.Song_6: 'death', UberDogGlobals.InventoryType.Song_7: 'death', UberDogGlobals.InventoryType.Song_8: 'death', UberDogGlobals.InventoryType.Song_9: 'death', UberDogGlobals.InventoryType.Song_10: 'death', UberDogGlobals.InventoryType.Song_11: 'performers-07', UberDogGlobals.InventoryType.Song_12: 'performers-09', UberDogGlobals.InventoryType.Song_13: 'island-cutthroat', UberDogGlobals.InventoryType.Song_14: 'island-kingshead', UberDogGlobals.InventoryType.Song_15: 'island-rumrunner', UberDogGlobals.InventoryType.Song_16: 'death', UberDogGlobals.InventoryType.Song_17: 'death', UberDogGlobals.InventoryType.Song_18: 'death', UberDogGlobals.InventoryType.Song_19: 'death', UberDogGlobals.InventoryType.Song_20: 'death'}
musicLabel2Length = {'island-driftwood': 62, 'island-cangrejos': 63, 'island-outcast': 61, 'death': 16, 'performers-02': 64, 'performers-07': 68, 'performers-09': 62, 'performers-10': 65, 'island-cutthroat': 61, 'island-kingshead': 67, 'island-rumrunner': 59}

class MusicManager(AmbientManagerBase.AmbientManagerBase):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('MusicManager')

    class MusicData:
        __module__ = __name__

        def __init__(self, name, priority=0, looping=1, volume=0.8):
            self.name = name
            self.priority = priority
            self.looping = looping
            self.volume = volume

    def __init__(self):
        AmbientManagerBase.AmbientManagerBase.__init__(self)
        self.current = None
        self.playlist = []
        self.wantMusic = base.config.GetBool('audio-music-active', 1)
        return

    def delete(self):
        AmbientManagerBase.AmbientManagerBase.delete(self)
        self.current = None
        self.playlist = []
        return

    def load(self, name, looping=True):
        if musicDict.has_key(name):
            path = musicDict[name]
            retval = AmbientManagerBase.AmbientManagerBase.load(self, name, path, isMusic=True, looping=looping)
            if self.ambientDict[name].sfx == None:
                self.notify.warning('music: %s failed to load' % name)
                del self.ambientDict[name]
                return 0
        return 1

    def unload(self, name):
        AmbientManagerBase.AmbientManagerBase.unload(self, name)
        if self.current and self.current.name == name:
            self.current = None
        for song in self.playlist:
            if song.name == name:
                self.playlist.remove(song)
                break

        return

    def request(self, name, priority=0, looping=True, volume=0.8):
        if not self.ambientDict.has_key(name):
            if not self.load(name, looping):
                return
        found = 0
        for song in self.playlist:
            if song.name == name:
                song.priority = priority
                found = 1

        if found == 0:
            song = self.MusicData(name, priority, looping, volume)
            self.playlist.append(song)
        self.update()

    def stop(self, name):
        if self.current:
            if self.current.name == name:
                self.requestFadeOut(name, 0, removeFromPlaylist=True)
                self.current = None
        for song in self.playlist:
            if song.name == name:
                self.playlist.remove(song)
                break

        self.update()
        return

    def update(self):
        self.notify.debug('playlistLength = %d' % len(self.playlist))
        if len(self.playlist) == 0:
            return

        def compFunc(a, b):
            if a.priority < b.priority:
                return 1
            else:
                if a.priority > b.priority:
                    return -1
            return 0

        self.playlist.sort(compFunc)
        self.notify.debug('playlist == ')
        for musicData in self.playlist:
            self.notify.debug('    musicData=%s' % musicData.name)

        if self.current == self.playlist[0]:
            return
        else:
            if self.current != None:
                if self.ambientDict[self.current.name].finalVolume > 0:
                    self.notify.debug('calling requestFadeOut on %s' % self.current.name)
                    self.requestFadeOut(self.current.name, removeFromPlaylist=False)
        self.current = self.playlist[0]
        if self.wantMusic:
            songLength = musicLabel2Length.get(self.current.name)
            if self.current.looping == False:
                if songLength is not None:
                    self.doMethodLater(songLength, self.handleCurrentTrackFinished, 'currentTrackFinished')
                else:
                    self.notify.warning('non-looping song %s has no length!' % self.current.name)
            self.requestFadeIn(self.current.name, finalVolume=self.current.volume)
        return

    def requestFadeOut(self, name, duration=3, finalVolume=0.0, priority=0, removeFromPlaylist=True):
        self.requestChangeVolume(name, duration, finalVolume, priority, removeFromPlaylist)

    def requestChangeVolume(self, name, duration, finalVolume, priority=0, removeFromPlayList=False):
        AmbientManagerBase.AmbientManagerBase.requestChangeVolume(self, name, duration, finalVolume, priority)
        if finalVolume == 0:
            needToDoUpdate = False
            if removeFromPlayList:
                for song in self.playlist:
                    if song.name == name:
                        self.playlist.remove(song)
                        needToDoUpdate = True
                        break

            if needToDoUpdate:
                self.notify.debug('requestChangeVolume doing update')
                self.update()

    def requestCurMusicFadeOut(self, duration=3, finalVolume=0.0, removeFromPlaylist=False):
        if self.playlist and self.current:
            curMusic = self.current.name
            self.requestFadeOut(curMusic, duration, finalVolume, removeFromPlaylist=removeFromPlaylist)

    def requestCurMusicFadeIn(self, duration=3, finalVolume=1.0):
        if self.playlist and self.current:
            curMusic = self.current.name
            self.requestFadeIn(curMusic, duration, finalVolume)

    def handleCurrentTrackFinished(self, task=None):
        self.requestCurMusicFadeOut(duration=0, removeFromPlaylist=True)
        return Task.done
# okay decompiling .\pirates\piratesbase\MusicManager.pyc
