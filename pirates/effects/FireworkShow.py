# Embedded file name: pirates.effects.FireworkShow
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.effects import FireworkGlobals
from pirates.effects.FireworkGlobals import *
from pirates.effects.Firework import Firework
import random
colors = [
 Vec4(1, 1, 1, 1), Vec4(1, 0, 0, 1), Vec4(0, 1, 0, 1), Vec4(0.3, 1, 0.3, 1), Vec4(0.2, 0.2, 1, 1), Vec4(1, 1, 0, 1), Vec4(1, 0.5, 0, 1), Vec4(1, 0, 1, 1), Vec4(0, 1, 1, 1), Vec4(0, 0.5, 1, 1)]

class FireworkShow(NodePath):

    def __init__(self, showType):
        NodePath.__init__(self, 'FireworkShow')
        self.showType = showType
        self.sectionIvals = []
        self.fireworks = []

        def r():
            return random.randint(8, 12) / 10.0

        def rV():
            return Vec3(random.randint(-100, 100), random.randint(-100, 100), random.randint(400, 600))

        def rP():
            return Point3(random.randint(-250, 250), random.randint(-50, 50), 0)

        def rS():
            return 0.75 + random.random() / 2.0

        def rC():
            return random.choice(colors)

        def rT():
            return random.randint(12, 20) / 10.0

        def rD():
            return random.randint(1, 20) / 10.0

        self.showData = {FireworkShowType.FourthOfJuly: [[FireworkType.BasicBlast, Vec3(0, 0, 450), Point3(0, 0, 0), 1.0, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 1), 2.0, 3.0], [FireworkType.BasicBlast, Vec3(-60, 20, 550), Point3(-120, 0, 0), 0.8, Vec4(1, 1, 0, 1), -1, 1.8, 0.2], [FireworkType.BasicBlast, Vec3(30, -20, 470), Point3(120, 0, 0), 0.8, rC(), -1, 1.8, 2.5], [FireworkType.LongBlast, Vec3(-120, 20, 500), Point3(-200, 0, 0), 1.0, Vec4(1, 0, 0, 1), -1, rT(), 0.25], [FireworkType.LongBlast, Vec3(0, 0, 500), Point3(0, 0, 0), 1.0, Vec4(0, 1, 0, 1), -1, rT(), 0.25], [FireworkType.LongBlast, Vec3(120, -20, 500), Point3(200, 0, 0), 1.0, Vec4(0.1, 0.1, 1, 1), -1, rT(), 2.5], [FireworkType.BasicBlast, Vec3(-50, 50, 450) * r(), Point3(0, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.LongBlast, Vec3(50, -50, 450) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.BasicBlast, Vec3(-100, 0, 450) * r(), Point3(-200, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.LongBlast, Vec3(100, 50, 450) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.BasicBlast, Vec3(100, -50, 450) * r(), Point3(0, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.LongBlast, Vec3(0, 0, 450) * r(), Point3(-200, 0, 0), 1.0, rC(), -1, rT(), 3.0], [FireworkType.AmericanFlag, None, Point3(0, 0, 0), 1.0, None, None, None, 4.0], [FireworkType.GlowFlare, Vec3(-100, 0, 500), Point3(-400, 0, 0), 1.25, Vec4(1, 1, 1, 1), -1, 3.0, 0.0], [FireworkType.GlowFlare, Vec3(100, 0, 500), Point3(400, 0, 0), 1.25, Vec4(1, 1, 1, 1), -1, 3.0, 0.5], [FireworkType.GlowFlare, Vec3(-50, 0, 500), Point3(-250, 0, 0), 1.25, Vec4(0, 1, 0, 1), -1, 3.0, 0.0], [FireworkType.GlowFlare, Vec3(50, 0, 500), Point3(250, 0, 0), 1.25, Vec4(0, 1, 0, 1), -1, 3.0, 0.5], [FireworkType.GlowFlare, Vec3(-25, 0, 500), Point3(-100, 0, 0), 1.25, Vec4(1, 0, 0, 1), -1, 3.0, 0.0], [FireworkType.GlowFlare, Vec3(25, 0, 500), Point3(100, 0, 0), 1.25, Vec4(1, 0, 0, 1), -1, 3.0, 1.0], [FireworkType.RingBlast, Vec3(0, 0, 550), Point3(0, 0, 0), 1.25, Vec4(1, 1, 1, 1), -1, 1.5, 2.0], [FireworkType.RingBlast, Vec3(-100, 50, 500) * r(), Point3(-200, 0, 0), 1.0, rC(), -1, rT(), 0.5], [FireworkType.RingBlast, Vec3(100, -50, 500) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), 1.5], [FireworkType.RingBlast, Vec3(0, 0, 550), Point3(0, 50, 0), 1.0, rC(), -1, rT(), 1.5], [FireworkType.RingBlast, Vec3(-250, 50, 450), Point3(200, 0, 0), 1.0, rC(), rC(), 1.7, 0.5], [FireworkType.RingBlast, Vec3(250, -50, 450), Point3(-200, 0, 0), 1.0, rC(), rC(), 1.7, 1.5], [FireworkType.BasicBlast, Vec3(-150, 100, 500) * r(), Point3(-200, 0, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.LongBlast, Vec3(-50, 100, 500) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.BasicBlast, Vec3(-150, -100, 500) * r(), Point3(0, 50, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.LongBlast, Vec3(150, 100, 500) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.RingBlast, Vec3(-50, -100, 500) * r(), Point3(-200, 0, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicBlast, Vec3(0, 100, 500) * r(), Point3(0, 0, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.LongBlast, Vec3(50, 100, 500) * r(), Point3(-200, 0, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicBlast, Vec3(150, 100, 500) * r(), Point3(0, 0, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.LongBlast, Vec3(-100, 100, 500) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), 3.0], [FireworkType.Mickey, None, Point3(0, 0, 0), 1.0, rC(), -1, None, 3.0], [FireworkType.NoiseBall, Vec3(0, 0, 550), Point3(0, 0, 0), 1.2, rC(), -1, 1.7, 2.0], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.NoiseBall, Vec3(-100, 50, 500) * r(), Point3(-200, 50, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.NoiseBall, Vec3(-50, 0, 500) * r(), Point3(0, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.NoiseBall, Vec3(100, -50, 500) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.LongBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.NoiseBall, rV(), rP(), 1.0, rC(), -1, rT(), rD()], [FireworkType.LongBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.NoiseBall, rV(), rP(), 1.0, rC(), -1, rT(), rD()], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.NoiseBall, rV(), rP(), 1.0, rC(), -1, rT(), rD()], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.LongBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 3.5], [FireworkType.PalmTree, Vec3(-150, 50, 300), rP(), 1.0, Vec4(0, 1, 0, 1), rC(), 1.75, 2.0], [FireworkType.PalmTree, Vec3(160, 50, 320), rP(), 1.0, Vec4(0, 1, 0, 1), rC(), 1.75, 2.0], [FireworkType.NoiseBall, rV(), rP(), 1.0, rC(), -1, rT(), 2.0], [FireworkType.PalmTree, Vec3(-150, -50, 350), Point3(-250, 0, 0), 1.2, Vec4(0, 1, 0, 1), rC(), 1.75, 2.0], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.75], [FireworkType.NoiseBall, rV(), rP(), 1.0, rC(), -1, rT(), 0.5], [FireworkType.LongBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.3], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.25], [FireworkType.NoiseBall, rV(), rP(), 1.0, rC(), -1, rT(), 0.5], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.3], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.LongBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.6], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.LongBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.6], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.25], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.25], [FireworkType.NoiseBall, rV(), rP(), 1.0, rC(), -1, rT(), 0.6], [FireworkType.LongBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.5], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.25], [FireworkType.NoiseBall, rV(), rP(), 1.0, rC(), -1, rT(), 0.3], [FireworkType.BasicBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.LongBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 0.5], [FireworkType.RingBlast, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.LongBlast, rV(), rP(), 1.0, rC(), rC(), rT(), 2.5], [FireworkType.PirateSkull, None, Point3(0, 0, 0), 1.0, Vec4(1, 1, 1, 1), -1, None, 2.0]]}
        self.sectionData = {FireworkShowType.FourthOfJuly: [(0, 12), (12, 34), (34, 56), (56, 95)]}
        del r
        del rV
        del rP
        del rS
        del rC
        del rT
        del rD
        return None

    def beginSection(self, startIndex, endIndex, offset):
        taskMgr.remove('beginSection' + str(startIndex) + str(endIndex))
        sectionIval = Parallel()
        time = 2.0
        sectionData = self.showData.get(self.showType)[startIndex:endIndex]
        for fireworkInfo in sectionData:
            typeId = fireworkInfo[0]
            velocity = fireworkInfo[1]
            pos = fireworkInfo[2]
            scale = fireworkInfo[3]
            color1 = fireworkInfo[4]
            color2 = fireworkInfo[5]
            if color2 == -1:
                color2 = color1
            trailDur = fireworkInfo[6]
            delay = fireworkInfo[7]
            firework = Firework(typeId, velocity, scale, color1, color2, trailDur)
            firework.reparentTo(self)
            firework.setPos(pos)
            self.fireworks.append(firework)
            sectionIval.append(Sequence(Wait(time), firework.generateFireworkIval()))
            time += delay

        if endIndex == len(self.showData.get(self.showType)):
            sectionIval.append(Sequence(Wait(time + 5.0), Func(self.cleanupShow)))
        sectionIval.start(offset)
        self.sectionIvals.append(sectionIval)

    def begin(self, timestamp):
        time = 0.0
        for section in self.sectionData.get(self.showType):
            startIndex = section[0]
            endIndex = section[1]
            sectionDur = self.getDuration(startIndex, endIndex)
            if timestamp < sectionDur:
                timestamp = max(0.0, timestamp)
                taskMgr.doMethodLater(time, self.beginSection, 'beginSection' + str(startIndex) + str(endIndex), extraArgs=[startIndex, endIndex, timestamp])
                time = time + sectionDur - timestamp
            timestamp -= sectionDur

    def getDuration(self, startIndex=0, endIndex=None):
        duration = 0.0
        if endIndex == None:
            endIndex = len(self.showData.get(self.showType))
        for firework in self.showData.get(self.showType)[startIndex:endIndex]:
            duration += firework[7]

        return duration

    def cleanupShow(self):
        for section in self.sectionData.get(self.showType):
            startIndex = section[0]
            endIndex = section[1]
            taskMgr.remove('beginSection' + str(startIndex) + str(endIndex))

        for ival in self.sectionIvals:
            ival.pause()
            ival = None

        self.sectionIvals = []
        for firework in self.fireworks:
            firework.cleanup()
            firework = None

        self.fireworks = []
        return