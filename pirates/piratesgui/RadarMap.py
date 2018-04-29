# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.RadarMap
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import Func, LerpFunc, Parallel, Sequence
from panda3d.core import *
from pirates.map.MapConfig import RangeSlider

MapData = {'jungle_a_terrain.egg': [{'name': 'radar_jungle_a_0', 'pos': (-20, 32), 'scale': 480}], 'rum_runner_terrain.egg': [{'name': 'radar_rumrunner_0', 'pos': (-30, 155), 'scale': 825}], 'port_royal_terrain.egg': [{'name': 'radar_port_royal_0', 'pos': (48, -1407), 'scale': 1228}, {'name': 'radar_port_royal_1', 'pos': (100, -1380), 'scale': 495}, {'name': 'radar_port_royal_town_0', 'pos': (-76, -1724), 'scale': 253}, {'name': 'radar_port_royal_mansion_0', 'pos': (179, -1009), 'scale': 504}, {'name': 'radar_port_royal_mansion_1', 'pos': (173, -1043), 'scale': 166}]}

class RadarMap(DirectFrame):
    

    def __init__(self, av, *args, **kwargs):
        kwargs['frameSize'] = (-0.5, 0.5, -0.5, 0.5)
        DirectFrame.__init__(self, *args, **kwargs)
        self.initialiseoptions(RadarMap)
        self.texModel = loader.loadModel('models/gui/radar_maps')
        self.av = av
        self.mapTexName = ''
        self.mapScale = 1.0
        self.mapPos = Point2(0, 0)
        self.zoomScale = 1.0
        self.relNode = render.attachNewNode('radarMapRelNode')
        self.tex = None
        self.blank = None
        self.modelName = None
        cm = CardMaker('mapTexture')
        cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        self.geom = NodePath(cm.generate())
        self.geom.setTransparency(1)
        self.geom.reparentTo(self)
        self.clearAreaModel()
        return

    def destroy(self):
        self.clearAreaModel()
        self.relNode.removeNode()
        del self.relNode
        del self.texModel
        del self.av
        del self.tex
        del self.blank
        self.geom.removeNode()
        del self.geom
        DirectFrame.destroy(self)

    def setAreaModel(self, modelPath):
        if modelPath.isEmpty():
            return
        self.relNode.setTransform(render, modelPath.getTransform(render))
        self.modelName = modelPath.getName()
        self.setMap()
        self.geom.setColorScale(Vec4(1))
        self.startUpdateTask()

    def setMap(self):
        mapInfo = MapData.get(self.modelName)
        pos = self.av.getPos(self.relNode)
        pos = Point2(pos[0], pos[1])
        if mapInfo:
            validInfo = [ info for info in mapInfo if info['scale'] / self.zoomScale >= 1.0 if (pos - Point2(*info['pos'])).length() <= info['scale'] ]
            if not validInfo:
                info = mapInfo[0]
            info = validInfo[0]
            for i in validInfo[1:]:
                if i['scale'] < info['scale']:
                    info = i

            if info['name'] == self.mapTexName:
                return
            else:
                self.mapTexName = info['name']
                self.mapPos = Point2(*info['pos'])
                self.mapScale = float(info['scale'])
                self.setMapTexture(self.mapTexName)
        else:
            self.mapTexName = 'blank'
            self.mapPos = Point2(0)
            self.mapScale = 1.0
            self.setMapTexture()

    def clearAreaModel(self):
        self.mapTexName = ''
        self.stopUpdateTask()
        self.geom.clearTexture()
        self.geom.setColorScale(Vec4(1, 1, 1, 0))

    def setMapTexture(self, mapTexName=None):
        if not mapTexName:
            tex = None
        else:
            tex = self.texModel.findTexture(mapTexName)
        if tex != None:
            tex.setBorderColor(Vec4(1, 1, 0, 0))
            tex.setWrapU(Texture.WMClamp)
            tex.setWrapV(Texture.WMClamp)
        else:
            if not self.blank:
                blank = PNMImage(1, 1, PNMImage.CTFourChannel)
                blank.setAlphaVal(0, 0, 0)
                self.blank = Texture('blank')
                self.blank.setCompression(Texture.CMOff)
                self.blank.load(blank)
            tex = self.blank
        self.geom.setTexture(tex)
        return

    def setZoomScale(self, zoomScale):
        self.zoomScale = float(zoomScale)
        self.setMap()

    def startUpdateTask(self):
        self.stopUpdateTask()
        taskMgr.doMethodLater(0.1, self.updateTask, 'radarBackgroundTask')

    def updateTask(self, task):
        self.setMap()
        self.updateMapRelativeTo(self.av)
        return task.again

    def stopUpdateTask(self):
        taskMgr.remove('radarBackgroundTask')

    def updateMapRelativeTo(self, av):
        pos = av.getPos(self.relNode)
        pos = Point2(pos[0], pos[1])
        rot = av.getH(self.relNode)
        self._updateMapPosScale(-pos, -rot, self.mapScale / self.zoomScale)

    def _updateMapPosScale(self, pos, rot, scl):
        originInUVSpace = Point2(0.5)
        uvOrigin = TransformState.makePos2d(originInUVSpace)
        uvOriginInv = uvOrigin.getInverse()
        pos = pos + self.mapPos
        pos = TransformState.makePos2d(pos)
        gScl = TransformState.makeScale2d(scl / (2.0 * self.mapScale))
        pos = gScl.compose(pos).compose(gScl.getInverse())
        pos = pos.compose(uvOrigin)
        rot = TransformState.makeRotate2d(rot)
        zScl = TransformState.makeScale2d(scl)
        final = uvOrigin.compose(rot).compose(uvOriginInv).compose(pos).compose(zScl).compose(uvOriginInv)
        self.geom.setTexTransform(TextureStage.getDefault(), final.getInverse())


class RadarUtil(DirectFrame):
    

    def __init__(self, *args, **kwargs):
        super(DirectFrame, self).__init__(*args, **kwargs)
        self.initialiseoptions(RadarUtil)
        self.visPanel = None
        self.ctrlPanel = None
        self.resPanel = None
        self.model = None
        self.pnm = None
        self.setupCamera()
        self.setupPictureFrame()
        self.setupControls()
        self.setupMouseTask()
        self.setTransparency(1)
        return

    def setupMouseTask(self):
        self.accept('mouse1', self.startMouseDrag)
        self.accept('mouse1-up', self.stopMouseDrag)
        self.accept('wheel_down', self.adjustFilmSize, extraArgs=[-5])
        self.accept('wheel_up', self.adjustFilmSize, extraArgs=[5])

    def startMouseDrag(self):
        taskMgr.add(self.mouseDragTask, 'mouseDrag')

    def mouseDragTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            if task.time == 0.0:
                task.startPt = Point2(base.mouseWatcherNode.getMouse())
                task.startCamPos = Point2(base.camera.getX(), base.camera.getY())
            mPt = Point2(base.mouseWatcherNode.getMouse())
            mDelta = mPt - task.startPt
            ts = TransformState.makeScale2d(base.camLens.getFilmSize() / 2.0)
            posDelta = ts.getMat3().xformPoint(mDelta)
            newPos = task.startCamPos - posDelta
            self.setCameraX(newPos[0])
            self.setCameraY(newPos[1])
        return task.cont

    def stopMouseDrag(self):
        taskMgr.remove('mouseDrag')

    def adjustFilmSize(self, amount):
        self.setFilmSize(base.camLens.getFilmSize()[0] + amount)

    def setupCamera(self):
        oLens = OrthographicLens()
        oLens.setFar(100000)
        oLens.setAspectRatio(base.camLens.getAspectRatio())
        oLens.setFilmSize(1280)
        base.cam.node().setLens(oLens)
        base.camLens = oLens
        base.disableMouse()
        base.camera.setPos(0, 0, 1500)
        base.camera.setHpr(0, -90, 0)

    def setupPictureFrame(self):
        self.picFrame = DirectFrame(parent=self, relief=None)
        DirectFrame(parent=self.picFrame, relief=DGG.FLAT, frameSize=(-2, -1, -1, 1), frameColor=(1,
                                                                                                  0,
                                                                                                  1,
                                                                                                  1))
        DirectFrame(parent=self.picFrame, relief=DGG.FLAT, frameSize=(1, 2, -1, 1), frameColor=(1,
                                                                                                0,
                                                                                                1,
                                                                                                1))
        return

    def setupControls(self):
        if self.visPanel:
            self.visPanel.destroy()
        if self.resPanel:
            self.resPanel.destroy()
        if self.ctrlPanel:
            self.ctrlPanel.destroy()
        self.resPanel = DirectFrame(parent=self, relief=None)
        self.resPanel.hide()
        self.ctrlPanel = DirectFrame(parent=self, relief=None)
        self.fileNameEntry = DirectEntry(parent=self.ctrlPanel, initialText='models/jungles/jungle_a', scale=0.05, width=25, pos=(-0.982, 0, 0.905))
        self.loadModelButton = DirectButton(parent=self.ctrlPanel, pos=(-1.17, 0, 0.908), scale=0.06, borderWidth=(0.1,
                                                                                                                   0.1), text='Load Model', command=self.loadModelFromEntry)
        self.sizeLabel = DirectLabel(parent=self.ctrlPanel, relief=None, pos=(-1.28,
                                                                              0,
                                                                              0.4), text='size', text_scale=0.05)
        self.sizeEntry = DirectEntry(parent=self.ctrlPanel, initialText=`(int(base.camLens.getFilmSize()[0]))`, scale=0.05, width=3, pos=(-1.187,
                                                                                                                                          0,
                                                                                                                                          0.4), command=self.handleSizeEntryUpdated)
        self.xLabel = DirectLabel(parent=self.ctrlPanel, relief=None, pos=(-1.277,
                                                                           0, 0.22), text='x', text_scale=0.05)
        self.xEntry = DirectEntry(parent=self.ctrlPanel, initialText=`(base.camera.getX())`, scale=0.05, width=3, pos=(-1.187,
                                                                                                                       0,
                                                                                                                       0.22), command=self.handleXEntryUpdated)
        self.yLabel = DirectLabel(parent=self.ctrlPanel, relief=None, pos=(-1.277,
                                                                           0, 0.1), text='y', text_scale=0.05)
        self.yEntry = DirectEntry(parent=self.ctrlPanel, initialText=`(base.camera.getY())`, scale=0.05, width=3, pos=(-1.187,
                                                                                                                       0,
                                                                                                                       0.1), command=self.handleYEntryUpdated)
        self.gScaleLabel = DirectLabel(parent=self.resPanel, relief=None, scale=0.05, pos=(1.03, 0, -0.75), text='gScale = ' + `(int(base.camLens.getFilmSize()[0]))`, text_fg=Vec4(0, 0, 0, 1), text_bg=Vec4(1, 1, 1, 0), text_align=TextNode.ALeft, textMayChange=True)
        self.gPosLabel = DirectLabel(parent=self.resPanel, relief=None, scale=0.05, pos=(1.03, 0, -0.85), text='gPos = (0,0)', text_fg=Vec4(0, 0, 0, 1), text_bg=Vec4(1, 1, 1, 0), text_align=TextNode.ALeft, textMayChange=True)
        self.saveScreenButton = DirectButton(parent=self.ctrlPanel, pos=(-1.16719, 0, -0.75), scale=0.06, borderWidth=(0.1,
                                                                                                                       0.1), text='Save Screen', frameColor=(0,
                                                                                                                                                             1,
                                                                                                                                                             0,
                                                                                                                                                             1), command=self.saveScreenShot)
        return

    def handleSizeEntryUpdated(self, val):
        self.setFilmSize(float(val))

    def handleXEntryUpdated(self, val):
        self.setCameraX(float(val))

    def handleYEntryUpdated(self, val):
        self.setCameraY(float(val))

    def setFilmSize(self, size):
        base.camLens.setFilmSize(size)
        self.sizeEntry.enterText(`size`)
        self.gScaleLabel['text'] = 'scale: ' + `(self.getGlobalScale())`

    def setCameraX(self, x):
        base.camera.setX(x)
        self.xEntry.set('%3.1f' % -x)
        y = base.camera.getY()
        self.gPosLabel['text'] = 'x: %3.1f\ny: %3.1f' % (x, y)

    def setCameraY(self, y):
        base.camera.setY(y)
        self.yEntry.set('%3.1f' % -y)
        x = base.camera.getX()
        self.gPosLabel['text'] = 'x: %3.1f\ny: %3.1f' % (x, y)

    def loadModel(self, modelName):
        model = loader.loadModel(modelName)
        if model:
            if self.model:
                self.model.removeNode()
            self.model = model
            self.model.reparentTo(render)
            print modelName, ' loaded'
        else:
            print modelName, ' not loaded'

    def stashNamedNodes(self, names=[]):
        for name in names:
            self.model.findAllMatches('**/' + name).stash()

    def stashAllBut(self, nodepath):
        self.model.findAllMatches('**/*').stash()
        nodepath.findAllMatches('**/*;+s').unstash()
        while nodepath != nodepath.getTop():
            nodepath.unstash()
            nodepath = nodepath.getParent()

    def getGlobalScale(self):
        return int(base.camLens.getFilmSize()[1] / 2)

    def loadModelFromEntry(self):
        self.loadModel(self.fileNameEntry.get())

    def saveScreenShot(self):
        self.ctrlPanel.hide()
        self.resPanel.show()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        if not self.pnm:
            self.pnm = PNMImage(base.win.getXSize(), base.win.getYSize())
        if not base.win.getScreenshot(self.pnm):
            print 'Error: Screenshot not taken'
            return
        filepath = Filename(self.fileNameEntry.get().replace('/', '_') + '.tif')
        if not filepath.touch():
            print 'Error: invalid filepath: ' + `filepath`
        if not self.pnm.write(filepath):
            print 'Error: Screenshot taken but not saved'
            return
        filepath.resolveFilename(DSearchPath('.'))
        print 'Screenshot saved to ' + `filepath`
        self.ctrlPanel.show()
        self.resPanel.hide()


if __name__ == '__main__':
    from direct.showbase.PythonUtil import *
    from direct.gui.DirectGui import DGG
    base.camLens.setFar(100000)
    av = loader.loadModel('models/misc/smiley')
    av.setScale(10)
    av.reparentTo(render)
    av.setBin('fixed', 1)
    av.setDepthTest(0)
    axis = loader.loadModel('models/misc/xyzAxis')
    axis.reparentTo(av)
    carrot = NodePath('carrot')
    carrot.reparentTo(av)
    carrot.setY(0.03333 / 2)
    m = RadarMap(av, relief=None, pos=(4.0 / 3 - 0.5, 0, 0.5), scale=1)
    m.setTransparency(1)
    m.setZoomScale(1000)
    center = DirectFrame(parent=m, relief=DGG.FLAT, frameSize=(-0.5, 0.5, -0.5, 0.5), frameColor=(1, 0, 0, 1), scale=0.025)
    area = loader.loadModel('models/islands/port_royal_zero')
    area.reparentTo(render)
    m.setAreaModel(area)

    def updateMap(t):
        m.updateMapRelativeTo(av)
        av.setPos(render, carrot.getPos(render))
        par = Sequence(Func(av.setPos, render, Vec3(-250, 80, 0)), Parallel(av.hprInterval(30, Vec3(360, 0, 0), Vec3(0, 0, 0)), LerpFunc(updateMap, 30)))
        par.loop()


    base.mouseInterfaceNode.setPos(0, 1500, 0)
    base.mouseInterfaceNode.setHpr(0, 90, 0)
    run()
# okay decompiling .\pirates\piratesgui\RadarMap.pyc
