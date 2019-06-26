from panda3d.core import *

import math

class SeaPatchNode(CallbackNode):

    def __init__(self, name, patch):
        CallbackNode.__init__(self, name)

        self.patch = patch

        self.wantReflect = False
        self.wantColor = False
        self.wantNormal = False
        self.wantUv = False

        self.setCullCallback(PythonCallbackObject(self._cullCallback))

    def _cullCallback(self, callbackData):
        
        data = callbackData.getData()
        trav = callbackData.getTrav()
        node = data.node()
        netTransMat = node.getTransform().getMat()

        if self.patch.isEnabled():
            self._recurseChildren(node, netTransMat)

        callbackData.upcall()

    def _recurseChildren(self, node, netTransMat):
        
        if isinstance(node, GeomNode):
            numGeoms = len(node.getGeoms())
            for j in range(0, numGeoms):
                geom = node.modifyGeom(j)
                self._doWave(geom, netTransMat)

        numChildren = node.getNumChildren()
        for i in range(0, numChildren):
            self._recurseChildren(node.getChild(i), netTransMat)

    def _doWave(self, geom, netTransMat):
        
        vData = geom.modifyVertexData()
        vWriter = GeomVertexWriter(vData, InternalName.make('vertex'))
        nWriter = GeomVertexWriter(vData, InternalName.make('normal'))
        cWriter = GeomVertexWriter(vData, InternalName.make('color'))
        texWriter = GeomVertexWriter(vData, InternalName.make('texcoord'))
        vReader = GeomVertexReader(vData, InternalName.make('vertex'))
        nReader = GeomVertexReader(vData, InternalName.make('normal'))
        texReader = GeomVertexReader(vData, InternalName.make('texcoord'))

        while not vReader.isAtEnd():
            v = LVecBase3f(vReader.getData3f()) # Multiply with net transform
            newCenter = self.patch.center.getPos()

            x = v.getX()
            y = v.getY()

            cx = newCenter.getX()
            cy = newCenter.getY()

            # Calculate distance for fading out waves
            dist = float(math.sqrt(math.pow(x - cx, 2) + math.pow(y - cy,2)))

            heightChange = self.patch.calcHeight(x, y, dist)
            v.setZ(heightChange)
            vWriter.setData3f(v)

            if self.wantNormal:
                nWriter.setData3f(self.patch.calcNormal(x, y, dist))

            if self.wantColor:
                color = 1
                cWriter.setData4f(self.patch.calcColor(color, heightChange, x, y))

    def setWantReflect(self, wantReflect):
        self.wantReflect = wantReflect

    def getWantReflect(self):
        return self.wantReflect

    def setWantColor(self, wantColor):
        self.wantColor = wantColor

    def getWantColor(self):
        return self.wantColor

    def setWantNormal(self, wantNormal):
        self.wantNormal = wantNormal

    def getWantNormal(self):
        return self.wantNormal

    def setWantUv(self, wantUv):
        self.wantUv = wantUv

    def getWantUv(self):
        return self.wantUv

    def collectGeometry(self):
        pass
