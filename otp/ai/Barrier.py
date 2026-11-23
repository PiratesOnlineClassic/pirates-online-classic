from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr


class Barrier:
    def __init__(self, name, taskName, avIds, timeout, doneFunc):
        self.name = name
        self.taskName = taskName
        self.pendingAvatars = list(dict.fromkeys(avIds))
        self.readyAvatars = []
        self.doneFunc = doneFunc
        taskMgr.doMethodLater(timeout, self._timedOut, self.taskName)

    def clear(self, avId):
        if avId not in self.pendingAvatars:
            return
        self.pendingAvatars.remove(avId)
        self.readyAvatars.append(avId)
        if not self.pendingAvatars:
            self._finish()

    def _timedOut(self, task):
        self._finish()
        return Task.done

    def _finish(self):
        doneFunc = self.doneFunc
        self.cleanup()
        if doneFunc:
            doneFunc(self.readyAvatars[:])

    def cleanup(self):
        taskMgr.remove(self.taskName)
        self.doneFunc = None
