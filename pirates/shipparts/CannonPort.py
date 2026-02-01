from pirates.piratesbase.PiratesGlobals import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from panda3d.core import *
from direct.actor import Actor
from pirates.ship import ShipGlobals
from pirates.effects.Bonfire import Bonfire
CannonPortDict = {
    InventoryType.CannonL1: 'models/shipparts/cannon_port',
    InventoryType.CannonL2: 'models/shipparts/cannon_port',
    InventoryType.CannonL3: 'models/shipparts/cannon_port',
    InventoryType.CannonL4: 'models/shipparts/cannon_port',
    ShipGlobals.BPCANNON: 'models/shipparts/cannon_bp_port',
    ShipGlobals.SKEL_CANNON_L1: 'models/shipparts/GP_cannonPort',
    ShipGlobals.SKEL_CANNON_L2: 'models/shipparts/GP_cannonPort',
    ShipGlobals.SKEL_CANNON_L3: 'models/shipparts/GP_cannonPort' }
DefaultAnimDict = (('zero', '_zero'), ('Fire', '_fire'), ('Open', '_open'), ('Close', '_close'))

class CannonPort(NodePath):
    notify = directNotify.newCategory('cannonPort')

    def __init__(self, cannonType, parent, locator, side, index):
        NodePath.__init__(self, 'cannonPort')
        self.cannonType = cannonType
        self.side = side
        self.index = index
        self.__parent = parent
        self.locator = locator
        self.bf = None
        self.collSphereNodePath = None
        self.CannonPortAnimDict = {}
        self._loadModel(self.cannonType)
        self.loaded = False
        self._isEnabled = 1
        self._isTargetable = 0
        if cannonType in [
            InventoryType.CannonL4]:
            self._isTargetable = 1
            self._addCollisionSphere(parent, side, index)

    def _loadModel(self, cannonType):
        if config.GetBool('disable-ship-geom', 0):
            return

        filePrefix = CannonPortDict.get(cannonType)
        self.prop = ShipGlobals.getActor(filePrefix)[1]
        self.openIval = Sequence(self.prop.actorInterval('Open'))
        self.closeIval = Sequence(self.prop.actorInterval('Close'))
        self.fireIval = Sequence(self.prop.actorInterval('Fire'))
        self.geom_Low = NodePath('broadsides')
        self.geom_Medium = self.prop.getLOD('med')
        self.geom_High = self.prop.getLOD('hi')
        self.loaded = True

    def _addCollisionSphere(self, parent, side, index):
        radius = 3.0
        collSphere = CollisionSphere(0, 0, 0, radius)
        collSphere.setTangible(1)
        self.cSphereStr = parent.uniqueName('cannonPortSphere') + '-' + str(side) + '-' + str(index)
        self.collSphereEvent = 'enter' + self.cSphereStr
        collSphereNode = CollisionNode(self.cSphereStr)
        collSphereNode.setFromCollideMask(BitMask32.allOff())
        collSphereNode.setIntoCollideMask(PiratesGlobals.TargetBitmask)
        collSphereNode.setTag('objType', str(PiratesGlobals.COLL_CANNON))
        collSphereNode.setTag('broadsideId', str(self.__parent.doId))
        collSphereNode.setTag('sideId', str(side))
        collSphereNode.setTag('portId', str(index))
        collSphereNode.addSolid(collSphere)
        self.collSphereNodePath = parent.ship.root.attachNewNode(collSphereNode)
        self.collSphereNodePath.setPos(self.locator.getPos())
        self.collSphereNodePath.setHpr(self.locator.getHpr())
        self.collSphereNodePath.stash()
        self.openIval.append(Func(self.collSphereNodePath.unstash))
        self.closeIval.append(Func(self.collSphereNodePath.stash))

    def delete(self):
        if self.prop:
            self.prop.clearPythonData()

        self.prop.removeNode()
        self.removeNode()
        self.__parent = None
        if self.collSphereNodePath:
            self.collSphereNodePath.removeNode()

        self.collSphereNodePath = None
        self.ship = None

    def playOpen(self, offset = 0):
        if self._isEnabled:
            self.openIval.start(offset, playRate = 2.0)

    def playClosed(self, offset = 0):
        if self._isEnabled:
            self.closeIval.start(offset)

    def playFire(self, offset = 0):
        if self._isEnabled:
            self.fireIval.start(offset)

    def setEnabled(self, state):
        if self._isEnabled != state:
            if state == 0:
                bf = Bonfire()
                bf.reparentTo(self.locator)
                bf.startLoop()
                self.bf = bf
            elif state == 1:
                if self.bf:
                    self.bf.removeNode()
                    self.bf = None

            self._isEnabled = state

    def isEnabled(self):
        return self._isEnabled
