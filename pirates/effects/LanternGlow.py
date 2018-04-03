# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.LanternGlow
Instruction context:
-> 
 100      48  LOAD_DEREF            0  'self'
             51  LOAD_ATTR             2  'isEmpty'
             54  CALL_FUNCTION_0       0  None
             57  UNARY_NOT        
             58  JUMP_IF_FALSE       138  'to 199'
             61  POP_TOP          
             62  LOAD_GLOBAL           4  'hasattr'
             65  LOAD_DEREF            0  'self'
             68  LOAD_CONST            2  'glow'
             71  CALL_FUNCTION_2       2  None
             74  JUMP_IF_FALSE       122  'to 199'
           77_0  THEN                     200
             77  POP_TOP          
Instruction context:
-> 
 130      70  LOAD_GLOBAL           7  'hasattr'
             73  LOAD_FAST             0  'self'
             76  LOAD_CONST            2  'shaderNp'
             79  CALL_FUNCTION_2       2  None
             82  JUMP_IF_FALSE        79  'to 164'
           85_0  THEN                     165
             85  POP_TOP          
from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from EffectController import EffectController
import random

class LanternGlow(DirectObject, EffectController, NodePath):
    __module__ = __name__

    def __init__(self, newParent=render, billboardOffset=1.0):
        NodePath.__init__(self, 'LanternGlow')
        EffectController.__init__(self)
        self.newParent = newParent
        self.setColorScaleOff()
        self.setBillboardPointEye(billboardOffset)
        self.glow = NodePath(SequenceNode('lanternGlow'))
        glowCard = loader.loadModel('models/effects/lanternGlow').getChild(0)
        self.glowCards = []
        level = [
         15, 15.5, 16, 16.5, 17, 17.5, 18, 17.5, 17, 16.5, 16, 15.5, 15]
        index = random.randint(0, len(level))
        level = level[index:-1] + level[0:index]
        for i in level:
            for j in xrange(random.choice([1, 2, 3, 4])):
                newGlow = glowCard.copyTo(self.glow)
                newGlow.setScale(i)
                self.glowCards.append(newGlow)

        self.glow.node().setFrameRate(len(self.glowCards * 2) * random.choice([0.8, 0.9, 1, 1.1, 1.2]))
        self.glow.node().setPlayRate(1)
        self.glow.node().loop(1)
        self.glow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.glow.setDepthWrite(0)
        self.glow.setFogOff()
        self.glow.setLightOff()
        self.glow.setBin('fixed', 120)
        self.glow.setColorScale(0.5, 0.5, 0.5, 1)
        self.glow.reparentTo(self)
        self.startScale = 15
        self.endScale = 18
        self.period = 0.2
        self.glow.node().setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CRed | ColorWriteAttrib.CGreen | ColorWriteAttrib.CBlue))

    def createTrack(self, lod=None):
        randomness = random.random() / 20
        scaleUp = self.glow.scaleInterval(self.period + randomness, self.endScale, startScale=self.startScale, blendType='easeInOut', other=render)
        scaleDown = self.glow.scaleInterval(self.period + randomness, self.startScale, startScale=self.endScale, blendType='easeInOut', other=render)
        self.startEffect = Sequence(scaleUp, scaleDown)
        self.endEffect = None
        self.track = self.startEffect
        self.accept('toggleGlows', self.toggleGlows)
        return

    def destroy(self):
        self.ignore('toggleGlows')
        if self.glow:
            self.glow.removeNode()
            self.glow = None
        self.glowCards = None
        EffectController.destroy(self)
        return

    def toggleGlows(self):
        if self.glow.isStashed():
            self.glow.unstash()
        else:
            self.glow.stash()

    def setupShaders(self):
        LanternGlow.shaders = {'lantern': loader.loadShader('models/misc/ship_lantern.cg')}

    def enableShaders--- This code section failed: ---

  97       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             1  'glow'
           6  JUMP_IF_FALSE        34  'to 43'
           9  POP_TOP          
          10  LOAD_DEREF            0  'self'
          13  LOAD_ATTR             1  'glow'
          16  LOAD_ATTR             2  'isEmpty'
          19  CALL_FUNCTION_0       0  None
          22  UNARY_NOT        
          23  JUMP_IF_FALSE        17  'to 43'
          26  POP_TOP          

  98      27  LOAD_DEREF            0  'self'
          30  LOAD_ATTR             1  'glow'
          33  LOAD_ATTR             3  'setShaderOff'
          36  CALL_FUNCTION_0       0  None
          39  POP_TOP          
          40  JUMP_ABSOLUTE       200  'to 200'
        43_0  COME_FROM            23  '23'
        43_1  COME_FROM             6  '6'
          43  POP_TOP          
          44  JUMP_FORWARD        153  'to 200'
          47  POP_TOP          

 100      48  LOAD_DEREF            0  'self'
          51  LOAD_ATTR             2  'isEmpty'
          54  CALL_FUNCTION_0       0  None
          57  UNARY_NOT        
          58  JUMP_IF_FALSE       138  'to 199'
          61  POP_TOP          
          62  LOAD_GLOBAL           4  'hasattr'
          65  LOAD_DEREF            0  'self'
          68  LOAD_CONST            2  'glow'
          71  CALL_FUNCTION_2       2  None
          74  JUMP_IF_FALSE       122  'to 199'
        77_0  THEN                     200
          77  POP_TOP          

 101      78  LOAD_GLOBAL           5  'LanternGlow'
          81  LOAD_ATTR             6  'setupShaders'
          84  LOAD_DEREF            0  'self'
          87  CALL_FUNCTION_1       1  None
          90  POP_TOP          

 103      91  LOAD_DEREF            0  'self'
          94  LOAD_ATTR             1  'glow'
          97  LOAD_DEREF            0  'self'
         100  STORE_ATTR            7  'shaderNp'

 105     103  LOAD_GLOBAL           8  'taskMgr'
         106  LOAD_ATTR             9  'hasTaskNamed'
         109  LOAD_CONST            3  'LanternColorScale'
         112  CALL_FUNCTION_1       1  None
         115  JUMP_IF_TRUE         43  'to 161'
       118_0  THEN                     162
         118  POP_TOP          

 106     119  LOAD_CLOSURE          0  'self'
         122  LOAD_CONST               '<code_object lanternColorScaleTask>'
         125  MAKE_CLOSURE_0        0  None
         128  STORE_FAST            2  'lanternColorScaleTask'

 116     131  LOAD_GLOBAL           8  'taskMgr'
         134  LOAD_ATTR            11  'add'
         137  LOAD_FAST             2  'lanternColorScaleTask'
         140  LOAD_CONST            3  'LanternColorScale'
         143  CALL_FUNCTION_2       2  None
         146  STORE_FAST            1  't'

 117     149  LOAD_CONST            5  0
         152  LOAD_FAST             1  't'
         155  STORE_ATTR           13  'shaderCount'
         158  JUMP_FORWARD          1  'to 162'
       161_0  COME_FROM           115  '115'
         161  POP_TOP          
       162_0  COME_FROM           158  '158'

 119     162  LOAD_GLOBAL           8  'taskMgr'
         165  LOAD_ATTR            14  'getTasksNamed'
         168  LOAD_CONST            3  'LanternColorScale'
         171  CALL_FUNCTION_1       1  None
         174  STORE_FAST            3  'tList'

 121     177  LOAD_FAST             3  'tList'
         180  LOAD_CONST            5  0
         183  BINARY_SUBSCR    
         184  DUP_TOP          
         185  LOAD_ATTR            13  'shaderCount'
         188  LOAD_CONST            1  1
         191  INPLACE_ADD      
         192  ROT_TWO          
         193  STORE_ATTR           13  'shaderCount'
         196  JUMP_FORWARD          1  'to 200'
       199_0  COME_FROM            74  '74'
       199_1  COME_FROM            58  '58'
         199  POP_TOP          
       200_0  COME_FROM           196  '196'
       200_1  COME_FROM            44  '44'

Parse error at or near `LOAD_DEREF' instruction at offset 48

    def disableShaders--- This code section failed: ---

 126       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             1  'glow'
           6  JUMP_IF_FALSE        56  'to 65'
           9  POP_TOP          
          10  LOAD_FAST             0  'self'
          13  LOAD_ATTR             1  'glow'
          16  LOAD_ATTR             2  'isEmpty'
          19  CALL_FUNCTION_0       0  None
          22  UNARY_NOT        
          23  JUMP_IF_FALSE        39  'to 65'
          26  POP_TOP          

 127      27  LOAD_FAST             0  'self'
          30  LOAD_ATTR             1  'glow'
          33  LOAD_ATTR             3  'clearShader'
          36  CALL_FUNCTION_0       0  None
          39  POP_TOP          

 128      40  LOAD_FAST             0  'self'
          43  LOAD_ATTR             1  'glow'
          46  LOAD_ATTR             4  'clearAttrib'
          49  LOAD_GLOBAL           5  'ShaderAttrib'
          52  LOAD_ATTR             6  'getClassType'
          55  CALL_FUNCTION_0       0  None
          58  CALL_FUNCTION_1       1  None
          61  POP_TOP          
          62  JUMP_ABSOLUTE       165  'to 165'
        65_0  COME_FROM            23  '23'
        65_1  COME_FROM             6  '6'
          65  POP_TOP          
          66  JUMP_FORWARD         96  'to 165'
          69  POP_TOP          

 130      70  LOAD_GLOBAL           7  'hasattr'
          73  LOAD_FAST             0  'self'
          76  LOAD_CONST            2  'shaderNp'
          79  CALL_FUNCTION_2       2  None
          82  JUMP_IF_FALSE        79  'to 164'
        85_0  THEN                     165
          85  POP_TOP          

 131      86  LOAD_FAST             0  'self'
          89  LOAD_ATTR             8  'shaderNp'
          92  LOAD_ATTR             3  'clearShader'
          95  CALL_FUNCTION_0       0  None
          98  POP_TOP          

 132      99  LOAD_FAST             0  'self'
         102  LOAD_ATTR             8  'shaderNp'
         105  LOAD_ATTR             4  'clearAttrib'
         108  LOAD_GLOBAL           5  'ShaderAttrib'
         111  LOAD_ATTR             6  'getClassType'
         114  CALL_FUNCTION_0       0  None
         117  CALL_FUNCTION_1       1  None
         120  POP_TOP          

 134     121  LOAD_GLOBAL           9  'taskMgr'
         124  LOAD_ATTR            10  'getTasksNamed'
         127  LOAD_CONST            3  'LanternColorScale'
         130  CALL_FUNCTION_1       1  None
         133  STORE_FAST            1  'tList'

 136     136  LOAD_FAST             1  'tList'
         139  LOAD_CONST            4  0
         142  BINARY_SUBSCR    
         143  DUP_TOP          
         144  LOAD_ATTR            12  'shaderCount'
         147  LOAD_CONST            1  1
         150  INPLACE_SUBTRACT 
         151  ROT_TWO          
         152  STORE_ATTR           12  'shaderCount'

 138     155  LOAD_FAST             0  'self'
         158  DELETE_ATTR           8  'shaderNp'
         161  JUMP_FORWARD          1  'to 165'
       164_0  COME_FROM            82  '82'
         164  POP_TOP          
       165_0  COME_FROM           161  '161'
       165_1  COME_FROM            66  '66'

Parse error at or near `LOAD_GLOBAL' instruction at offset 70
