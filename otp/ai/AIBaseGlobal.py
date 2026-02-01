from otp.ai.AIBase import *

__builtins__['base'] = AIBase()
__builtins__['ostream'] = Notify.out()
__builtins__['run'] = base.run
__builtins__['taskMgr'] = base.taskMgr
__builtins__['jobMgr'] = base.jobMgr
__builtins__['eventMgr'] = base.eventMgr
__builtins__['messenger'] = base.messenger
__builtins__['bboard'] = base.bboard
__builtins__['config'] = base.config
__builtins__['directNotify'] = directNotify

from direct.showbase import Loader
base.loader = Loader.Loader(base)
__builtins__['loader'] = base.loader
directNotify.setDconfigLevels()


def inspect(anObject):
    from direct.tkpanels import Inspector
    Inspector.inspect(anObject)


__builtins__['inspect'] = inspect
if not __debug__ and __dev__:
    notify = directNotify.newCategory('ShowBaseGlobal')
    notify.error("You must set 'want-dev' to false in non-debug mode.")

taskMgr.finalInit()
