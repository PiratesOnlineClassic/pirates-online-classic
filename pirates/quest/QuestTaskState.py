from direct.showbase.PythonUtil import ParamObj

from pirates.pirate import AvatarTypes

class QuestTaskState(ParamObj):

    class ParamSet(ParamObj.ParamSet):
        Params = {
            'taskType': 0,
            'progress': 0,
            'goal': 1,
            'attempts': 0,
            'enemyType': AvatarTypes.AnyAvatar,
            'faction': AvatarTypes.AnyAvatar,
            'hull': None,
            'containersSearched': None}

    def acquire(self):
        if not hasattr(self, '_refcount'):
            self._refcount = 0

        self._refcount += 1

    def release(self):
        self._refcount -= 1
        if self._refcount <= 0:
            self.destroy()

    def handleParamChange(self, params):
        self.modified = True

    def isModified(self):
        return getattr(self, 'modified', False)

    def resetModified(self):
        self.modified = False

    def handleProgress(self, num = 1):
        self.setProgress(min(self.progress + num, self.goal))

    def forceComplete(self):
        self.setProgress(self.goal)

    def isComplete(self):
        return self.progress >= self.goal

    def hasSearchedContainer(self, containerId):
        return self.containersSearched is not None and containerId in self.containersSearched

    def searchedContainer(self, containerId):
        if self.containersSearched is None:
            self.containersSearched = []
        elif containerId in self.containersSearched:
            return False

        self.containersSearched.append(containerId)
        return True
