from direct.task import Task

class Target:
    
    def __init__(self, ship):
        self.ship = ship
        self.time = 0
        self.priority = 0
        self.targets = None
        self.removeTask = None

    def update(self, targets, priority):
        self.targets = targets
        if priority >= self.priority:
            self.priority = priority
            self.time = globalClock.getRealTime()
        
        if self.removeTask:
            self.removeTask.remove()
        
        self.removeTask = taskMgr.doMethodLater(20, self.remove, 'remove')

    def destroy(self):
        self.remove()
        self.ship = None

    def remove(self, task = None):
        if self.targets:
            self.targets.remove(self)
            self.targets = None
        
        if self.removeTask:
            self.removeTask.remove()
            self.removeTask = None
        



class ShipTargets:
    
    def __init__(self, ship):
        self.ship = ship
        self.primary = None
        self.secondary = None
        self.targets = []

    def destroy(self):
        self.ship = None
        self.primary = None
        self.secondary = None
        self.targets = []

    def hide(self):
        if self.primary:
            self.primary.hide()
        
        if self.secondary:
            self.secondary.hide()

    def show(self):
        if self.primary:
            self.primary.show()
        
        if self.secondary:
            self.secondary.show()

    def assignPrimary(self, target):
        if self.primary != target:
            targetPanel = target.ship.getTargetPanel()
            targetPanel.reparentTo(base.a2dTopCenter)
            targetPanel.setPos(-0.2, 0, -0.1)
            targetPanel.setScale(1.0)
            self.primary = targetPanel
        
        self.primary.show()
    
    def assignSecondary(self, target):
        if self.secondary != target:
            targetPanel = target.ship.getTargetPanel()
            targetPanel.reparentTo(base.a2dTopCenter)
            targetPanel.setPos(-0.16, 0, -0.28)
            targetPanel.setScale(0.8)
            self.secondary = targetPanel
        
        self.secondary.show()

    def hidePrimary(self):
        if self.primary:
            self.primary.hide()
            self.primary = None

    def hideSecondary(self):
        if self.secondary:
            self.secondary.hide()
            self.secondary = None
    
    def add(self, target, priority = 0):
        target.update(self, priority)
        if target not in self.targets:
            self.targets.append(target)
        
        self.update()

    def remove(self, target):
        if target in self.targets:
            self.targets.remove(target)
            self.update()
    
    def update(self):
        self.targets.sort(self.sortTargets)
        numTargets = len(self.targets)
        self.hidePrimary()
        if numTargets > 0:
            self.assignPrimary(self.targets[0])
    
    def sortTargets(self, t1, t2):
        if t1.priority == t2.priority:
            return int(t2.time - t1.time)
        else:
            return t2.priority - t1.priority


