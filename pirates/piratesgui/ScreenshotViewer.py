import os

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.PDialog import PDialog


class ScreenshotViewer:
    

    def __init__(self):
        self.resetImages()
        imageFrame = PDialog(aspect2d, pos=(0, 0, 0.1))
        imageFrame['image_scale'] = (1.3 * 4 / 3.0, 1, 1.3)
        imageFrame['fadeScreen'] = 0.85
        imageFrame.setScale(1.1)
        imageFrame.hide()
        imX = 0.85
        imY = imX * 3 / 4.0
        self.imageObj = OnscreenImage(image=self.screens[0], scale=(imX, 1, imY), pos=(0, 0, -0.025))
        self.imageObj.reparentTo(imageFrame)
        self.imageLabel = DirectLabel(imageFrame, relief=None, state=DGG.DISABLED, pos=(0,
                                                                                        0,
                                                                                        -0.75), textMayChange=1)
        self.imageLabel['text_fg'] = (0.6, 0.6, 0.6, 1)
        self.imageLabel['text_scale'] = 0.04
        self.imageLabel.hide()
        topGui = loader.loadModel('models/gui/toplevel_gui')
        arrow = topGui.find('**/generic_arrow')
        buttons = loader.loadModel('models/gui/lookout_gui')
        closeButton = (buttons.find('**/lookout_close_window'), buttons.find('**/lookout_close_window_down'), buttons.find('**/lookout_close_window_over'))
        xs = 1.2
        self.nextButton = DirectButton(imageFrame, relief=None, command=self.next, pos=(0.7,
                                                                                        0,
                                                                                        0), image=arrow, image_scale=(-xs, xs, xs), sortOrder=-5)
        self.prevButton = DirectButton(imageFrame, relief=None, command=self.prev, pos=(-0.7,
                                                                                        0,
                                                                                        0), image=arrow, image_scale=xs, sortOrder=-5)
        self.closeButton = DirectButton(imageFrame, relief=None, command=self.close, pos=(0.78,
                                                                                          0,
                                                                                          -0.5), image=closeButton, image_scale=0.3, text='close', text_fg=PiratesGuiGlobals.TextFG1, text_scale=0.05, text_pos=(0,
                                                                                                                                                                                                                 -0.1), sortOrder=-5)
        self.showIval = Sequence(Func(imageFrame.show), Wait(1), Parallel(LerpPosInterval(self.closeButton, 0.2, Vec3(0.78, 0, -0.8), Vec3(0.78, 0, -0.5)), LerpPosInterval(self.nextButton, 0.2, Vec3(1, 0, 0), Vec3(0.7, 0, 0)), LerpPosInterval(self.prevButton, 0.2, Vec3(-1, 0, 0), Vec3(-0.7, 0, 0))), Func(self.imageLabel.show))
        self.imageFrame = imageFrame
        return

    def destroy(self):
        self.imageFrame.destroy()

    def resetImages(self):
        filenames = os.listdir(os.curdir)
        self.screens = []
        for f in filenames:
            if 'jpg' in f:
                self.screens.append(f)

        self.currentIndex = 0

    def resetButtons(self):
        self.closeButton.setPos(Vec3(0.78, 0, -0.5))
        self.nextButton.setPos(Vec3(0.7, 0, 0))
        self.prevButton.setPos(Vec3(-0.7, 0, 0))

    def showImage(self, index):
        if index >= 0 and index < len(self.screens):
            self.imageFrame.show()
            self.imageObj.setImage(self.screens[index])
            self.imageLabel['text'] = '[%s/%s] %s' % (index + 1, len(self.screens), self.screens[index])
            self.imageLabel['text_fg'] = (0.6, 0.6, 0.6, 1)
            self.imageLabel['text_scale'] = 0.04
        if len(self.screens) == 1:
            self.prevButton['state'] = DGG.DISABLED
            self.prevButton['state'] = DGG.DISABLED

    def next(self):
        self.currentIndex = (self.currentIndex + 1) % len(self.screens)
        try:
            self.showImage(self.currentIndex)
        except:
            print 'badImage'

    def prev(self):
        self.currentIndex = (self.currentIndex - 1) % len(self.screens)
        try:
            self.showImage(self.currentIndex)
        except:
            print 'badImage'

    def close(self):
        self.imageFrame.hide()

    def show(self):
        self.resetImages()
        self.resetButtons()
        self.showImage(0)
        self.showIval.start()

    def toggleShow(self):
        if self.imageFrame.isHidden():
            self.show()
        else:
            self.close()
