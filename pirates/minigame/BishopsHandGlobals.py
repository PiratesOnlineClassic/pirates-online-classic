# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.minigame.BishopsHandGlobals
from direct.showbase import PythonUtil
from pandac.PandaModules import *

TARGET_POS = {4: Vec3(0.85, 0, 0.0), 3: Vec3(0.6, 0, 0.42), 2: Vec3(0.27, 0, 0.6), 1: Vec3(-0.08, 0, 0.63), 0: Vec3(-0.59, 0, 0.29)}
FACES = PythonUtil.Enum('DEALER,ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN')
FACE_SPOT_POS = {FACES.DEALER: (-1.0, 0, 0.6), FACES.ONE: (-1.15, 0, -0.3), FACES.TWO: (-0.96, 0, -0.61), FACES.THREE: (-0.65, 0, -0.8), FACES.FOUR: (0.65, 0, -0.8), FACES.FIVE: (0.96, 0, -0.61), FACES.SIX: (1.15, 0, -0.3)}
FINGER_RANGES = [
 [
  -26, -16], [-3, 8], [23, 32], [52, 60]]
PLAYER_ACTIONS = PythonUtil.Enum('JoinGame,UnjoinGame,RejoinGame,Resign,Leave,Continue,Progress')
GAME_ACTIONS = PythonUtil.Enum('AskForContinue,NotifyOfWin,NotifyOfLoss')
CONTINUE_OPTIONS = PythonUtil.Enum('Resign,Continue,Rejoin,Leave')
GameTimeDelay = 5
RoundTimeDelay = 5
RoundTimeLimit = 90
RoundContinueWait = 10
# okay decompiling .\pirates\minigame\BishopsHandGlobals.pyc
