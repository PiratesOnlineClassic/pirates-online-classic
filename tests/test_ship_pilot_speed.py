"""
Drives the client's ShipPilot2 controls through the same avatar physics
setup PiratesBase uses (viscosity + control force) to make sure player
steered ships actually reach their ship class's speeds without ~run.
"""
import builtins
from types import SimpleNamespace
import unittest

from panda3d.core import ClockObject, NodePath, Vec3, loadPrcFileData
from panda3d.physics import (ActorNode, AngularEulerIntegrator, ForceNode,
                             LinearControlForce, LinearEulerIntegrator,
                             LinearFrictionForce, PhysicsManager)


class _Debug:
    def add(self, *args):
        pass

    def append(self, *args):
        pass


def _install_builtins():
    loadPrcFileData('', 'want-avatar-physics-indicator 0')
    from panda3d.core import ConfigVariableBool

    class _Config:
        def GetBool(self, name, default=0):
            return ConfigVariableBool(name, default).getValue()

    fakeBase = SimpleNamespace(config=_Config(), localAvatar=SimpleNamespace(getTurbo=lambda: 0),
                               destroy=lambda: None)
    builtins.base = fakeBase
    builtins.render = NodePath('render')
    builtins.onScreenDebug = _Debug()
    builtins.messenger = SimpleNamespace(send=lambda *args, **kw: None)
    return fakeBase


class ShipPilotSpeedTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = _install_builtins()
        from pirates.ship.ShipPilot2 import ShipPilot2
        from pirates.ship import ShipGlobals
        cls.ShipPilot2 = ShipPilot2
        cls.stats = ShipGlobals.getHullStats(ShipGlobals.INTERCEPTORL1)

    def setUp(self):
        from direct.showbase.InputStateGlobal import inputState
        self.inputState = inputState
        for name in ('forward', 'reverse', 'turnLeft', 'turnRight', 'debugRunning'):
            inputState.set(name, False)

        # same avatar physics setup as PiratesBase:
        mgr = PhysicsManager()
        mgr.attachLinearIntegrator(LinearEulerIntegrator())
        mgr.attachAngularIntegrator(AngularEulerIntegrator())
        fn = ForceNode('ship viscosity')
        render.attachNewNode(fn)
        viscosity = LinearFrictionForce(0.0, 1.0, 0)
        viscosity.setCoef(0.5)
        viscosity.setAmplitude(2)
        fn.addForce(viscosity)
        mgr.addLinearForce(viscosity)
        fn = ForceNode('avatarControls')
        render.attachNewNode(fn)
        controlForce = LinearControlForce()
        controlForce.setAmplitude(5)
        fn.addForce(controlForce)
        mgr.addLinearForce(controlForce)
        self.base.controlForce = controlForce
        self.mgr = mgr

        actor = ActorNode('ship')
        shipNp = render.attachNewNode(actor)
        mgr.attachPhysicalNode(actor)
        controlForce.setPhysicsObject(actor.getPhysicsObject())

        s = self.stats
        self.ship = SimpleNamespace(
            acceleration=s['acceleration'], maxSpeed=s['maxSpeed'],
            reverseAcceleration=s['reverseAcceleration'],
            maxReverseSpeed=s['maxReverseSpeed'], turnRate=s['turn'],
            maxTurn=s['maxTurn'], Sp=100, maxSp=100,
            getIsAutoSailing=lambda: 0, worldVelocity=Vec3(0))

        pilot = self.ShipPilot2()
        pilot.actorNode = actor
        pilot.avatarNodePath = shipNp
        pilot.ship = self.ship
        pilot.avatarRadius = 1.4
        self.pilot = pilot

        self.clock = ClockObject.getGlobalClock()
        self.clock.setMode(ClockObject.MNonRealTime)

    def tearDown(self):
        self.clock.setMode(ClockObject.MNormal)
        for name in ('forward', 'reverse', 'debugRunning'):
            self.inputState.set(name, False)

    def sail(self, seconds, fps=60.0):
        dt = 1.0 / fps
        self.clock.setDt(dt)
        for i in range(int(seconds * fps)):
            self.clock.tick()
            self.clock.setDt(dt)
            # same order as the client, the physics-avatar task (sort 0)
            # runs before the ship controls task (sort 25):
            self.mgr.doPhysics(dt)
            self.pilot.handleAvatarControls(None)
        return self.pilot.actorNode.getPhysicsObject().getVelocity().length()

    def test_forward_reaches_class_speed(self):
        self.inputState.set('forward', True)
        speed = self.sail(4.0)
        # the ship should be well under way after a few seconds:
        self.assertGreater(speed, self.ship.maxSpeed * 0.5)
        speed = self.sail(30.0)
        # sailing straight gets the ship up to it's top speed, never past it:
        self.assertAlmostEqual(speed, self.ship.maxSpeed, delta=0.5)

    def test_speed_is_framerate_independent(self):
        self.inputState.set('forward', True)
        fast = self.sail(3.0, fps=60.0)
        self.setUp()
        self.inputState.set('forward', True)
        slow = self.sail(3.0, fps=20.0)
        self.assertAlmostEqual(fast, slow, delta=fast * 0.1)

    def test_reverse_capped(self):
        self.inputState.set('reverse', True)
        speed = self.sail(20.0)
        self.assertGreater(speed, 0.0)
        self.assertLessEqual(speed, self.ship.maxReverseSpeed + 0.01)

    def test_debug_running_still_boosts(self):
        self.inputState.set('forward', True)
        self.inputState.set('debugRunning', True)
        speed = self.sail(10.0)
        self.assertGreater(speed, self.ship.maxSpeed * 1.5)


if __name__ == '__main__':
    unittest.main()
