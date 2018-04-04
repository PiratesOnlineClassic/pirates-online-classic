# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.GameOptionsGui
from direct.directnotify import DirectNotifyGlobal
from direct.gui import DirectGuiGlobals as DGG
from otp.otpgui import OTPDialog
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PDialog, PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import *
from pirates.piratesgui.CheckButton import *
from pirates.piratesgui.DialogButton import DialogButton
from pirates.piratesgui.GuiButton import *
from pirates.piratesgui.OptionMenu import *
from pirates.piratesgui.RadioButton import *
from pirates.seapatch.Water import Water

try:
    import embedded
except:
    pass

class GameOptionsGui(DirectFrame):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('GameOptions')
    debug = False
    resolution_table = [(800, 600), (1024, 768), (1280, 1024), (1600, 1200)]
    widescreen_resolution_table = [(1280, 720), (1920, 1080)]
    MinimumHorizontalResolution = 800
    MinimumVerticalResolution = 600
    texture_low = 256
    texture_medium = 512
    texture_high = 1024
    texture_maximum = -1
    texture_scale_low = 0.25
    texture_scale_medium = 0.5
    texture_scale_high = 1.0
    texture_scale_maximum = 1.0
    textureScaleOptionList = [
     texture_scale_low, texture_scale_medium, texture_scale_high, texture_scale_maximum]
    textureOptionList = [texture_low, texture_medium, texture_high, texture_maximum]

    def __init__(self, gameOptions, title, x, y, width, height, options=None, file_path=None, pipe=None, chooser=0, keyMappings=None):
        self.width = width
        self.height = height
        self.gameOptions = gameOptions
        DirectFrame.__init__(self, 
            relief=None, 
            image=loader.loadModel('models/misc/fade'), 
            image_scale=(5, 2, 2), 
            image_color=(0, 0,0, 0.8), 
            image_pos=(0.5, 0,0.8), 
            state=DGG.NORMAL,
            pos=(x, 0.0, y), 
            sortOrder=20)
        self.initialiseoptions(GameOptionsGui)
        self.setBin('gui-fixed', 5)
        self.setupUpperFrame()
        self.setupLowerFrame()
        self.setupAudioFrame()
        self.setupVideoFrame()
        self.setupGraphicsFrame()
        self.setupDisplayFrame()
        if self.gameOptions:
            self.gameOptions.display_identifier = -1
        self.set_options(False)
        self.updateUI('graphics')
        self.updateUI()
        self.defaultDialog = None
        self.restoreDialog = None
        return

    def setupUpperFrame(self):
        gui_main = loader.loadModel('models/gui/gui_main')
        topImage = gui_main.find('**/game_options_panel/top')
        topImage.setPos(0.52, 0, -0.15)
        gui_main.removeNode()
        x = 0.3
        self.upperFrame = DirectFrame(parent=self, relief=None, image=topImage, image_scale=0.3, pos=(x, 0, self.height - 0.26 - PiratesGuiGlobals.TextScaleLarge * 7))
        self.upperFrame.setBin('gui-fixed', 15)
        DirectLabel(parent=self.upperFrame, relief=None, text=PLocalizer.GameOptionsTitle, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_pos=(0.51,
                                                                                                                                                                                    0.46), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceOutlineFont(), textMayChange=1)
        x += -0.08
        y = 1.3
        self.videoButton = GuiButton(parent=self, text=PLocalizer.GameOptionsVideo, pos=(x, 0, y), command=self.updateUI, extraArgs=['video'])
        self.videoButton.setBin('gui-fixed', 20)
        y -= 0.08
        self.audioButton = GuiButton(parent=self, text=PLocalizer.GameOptionsAudio, pos=(x, 0, y), command=self.updateUI, extraArgs=['audio'])
        self.audioButton.setBin('gui-fixed', 10)
        parent = self.upperFrame
        x = 0.175
        y = 0
        ox = 0.23
        text = PLocalizer.GameOptionsDefault
        self.defaultButton = GuiButton(parent=parent, text=text, pos=(x, 0, y), command=self.defaultButtonCB)
        x += ox
        text = PLocalizer.GameOptionsRestore
        self.restoreButton = GuiButton(parent=parent, text=text, pos=(x, 0, y), command=self.restoreButtonCB)
        x += ox
        text = PLocalizer.GameOptionsSave
        if self.gameOptions:
            command = self.gameOptions.save_button_function
        else:
            command = None
        button = GuiButton(parent=parent, text=text, pos=(x, 0, y), command=command)
        x += ox
        text = PLocalizer.GameOptionsLogout
        if self.gameOptions:
            command = self.gameOptions.logout_button_function
        else:
            command = None
        button = GuiButton(parent=parent, text=text, pos=(x, 0, y), command=command)
        if self.gameOptions and self.gameOptions.play == False:
            self.disableButton(button)
        toplevel_gui = loader.loadModel('models/gui/toplevel_gui')
        generic_x = toplevel_gui.find('**/generic_x')
        generic_question = toplevel_gui.find('**/generic_question*')
        generic_question.setColor(0.6, 0.6, 0.6, 1)
        generic_box = toplevel_gui.find('**/generic_box')
        generic_box_over = toplevel_gui.find('**/generic_box_over')
        toplevel_gui.removeNode()
        x += 0.045
        y = 0.39
        button = DirectButton(parent=parent, relief=None, pos=(x, 0, y), scale=0.28, geom=generic_question, image=(generic_box, generic_box, generic_box_over, generic_box), image_scale=0.7, text='', textMayChange=1, command=self.__loadFeedbackPanel)
        x += 0.055
        button = DirectButton(parent=parent, relief=None, pos=(x, 0, y), scale=0.28, geom=generic_x, image=(generic_box, generic_box, generic_box_over, generic_box), image_scale=0.7, text='', textMayChange=1, command=self.close)
        return

    def setupVideoFrame(self):
        self.videoFrame = DirectFrame(parent=self.upperFrame, relief=None)
        self.videoVar = [
         0]
        x = 0.18
        y = 0.2
        sx = 0.24
        oy = 0.04
        self.videoRadios = self.createRadioButtonGroup(self.videoFrame, x, y, sx, oy, self.videoVar, 0.15, [
         PLocalizer.GameOptionsLow, PLocalizer.GameOptionsMedium, PLocalizer.GameOptionsHigh, PLocalizer.GameOptionsCustom], 1.4, self.videoRadioButtonCB)
        return

    def setupAudioFrame(self):
        self.audioFrame = DirectFrame(parent=self.upperFrame, relief=None)
        parent = self.audioFrame
        x = 0.1
        y = 0.3
        text = PLocalizer.GameOptionsSoundEffects
        self.create_label(x, y, text, parent, 1.2)
        x += 0.335
        self.soundEffectCheck = CheckButton(parent=parent, relief=None, scale=0.4, pos=(x, 0, y + 0.015), command=self.soundEffectCheckCB)
        x = 0.25
        y -= 0.05
        text = PLocalizer.GameOptionsVolume
        self.create_label(x, y, text, parent)
        x += 0.43

        def sound_volume_update_function(value):
            if self.gameOptions:
                self.gameOptions.options.sound_volume = value
            if base.sfxManagerList:
                index = 0
                length = len(base.sfxManagerList)
                while index < length:
                    sfx_manager = base.sfxManagerList[index]
                    sfx_manager.setVolume(value)
                    index += 1

        text = PLocalizer.GameOptionsSoundEffectsVolume
        default_value = 0.5
        resolution = 0.01
        if self.gameOptions:
            self.sound_volume_slider = self.create_slider(sound_volume_update_function, self.gameOptions.options.sound_volume, x, y, resolution, text, parent)
        else:
            self.sound_volume_slider = self.create_slider(sound_volume_update_function, default_value, x, y, resolution, text, parent)
        x = 0.1
        y -= 0.1
        text = PLocalizer.GameOptionsMusic
        self.create_label(x, y, text, parent, 1.2)
        x += 0.18
        self.musicCheck = CheckButton(parent=parent, relief=None, scale=0.4, pos=(x, 0, y + 0.015), command=self.musicCheckCB)
        x = 0.25
        y -= 0.05
        text = PLocalizer.GameOptionsVolume
        self.create_label(x, y, text, parent)
        x += 0.43

        def music_volume_update_function(value):
            if self.gameOptions:
                self.gameOptions.options.music_volume = value
            if base.musicManager:
                base.musicManager.setVolume(value)

        text = PLocalizer.GameOptionsSoundEffectsVolume
        default_value = 0.5
        resolution = 0.01
        if self.gameOptions:
            self.music_volume_slider = self.create_slider(music_volume_update_function, self.gameOptions.options.music_volume, x, y, resolution, text, parent)
        else:
            self.music_volume_slider = self.create_slider(music_volume_update_function, default_value, x, y, resolution, text, parent)
        return

    def setupLowerFrame(self):
        self.lowerFrame = DirectFrame(parent=self, relief=None, pos=(0.3, 0, self.height - 0.91 - PiratesGuiGlobals.TextScaleLarge * 17))
        gui_main = loader.loadModel('models/gui/gui_main')
        bottomImage = gui_main.find('**/game_options_panel/bottom')
        bottomImage.setPos(0.52, 0, 0.9)
        gui_main.removeNode()
        self.customFrame = DirectFrame(parent=self.lowerFrame, relief=None, image=bottomImage, image_scale=0.3, frameSize=(0, self.width, 0, PiratesGuiGlobals.TextScaleLarge * 22), pos=(0,
                                                                                                                                                                                          0,
                                                                                                                                                                                          0))
        self.customFrame.setBin('gui-fixed', 15)
        x = -0.08
        y = 0.8
        self.graphicsButton = GuiButton(parent=self.lowerFrame, text=PLocalizer.GameOptionsGraphics, pos=(x, 0, y), command=self.updateUI, extraArgs=['graphics'])
        self.graphicsButton.setBin('gui-fixed', 20)
        y -= 0.08
        self.displayButton = GuiButton(parent=self.lowerFrame, text=PLocalizer.GameOptionDisplay, pos=(x, 0, y), command=self.updateUI, extraArgs=['display'])
        self.displayButton.setBin('gui-fixed', 10)
        return

    def setupGraphicsFrame(self):
        self.graphicsFrame = DirectFrame(parent=self.customFrame, relief=None)
        x = 0.07
        y = 0.8
        oy = -0.08
        parent = self.graphicsFrame
        sl = 1
        sc = 0.35
        text = PLocalizer.GameOptionsCharacterDetailLevel
        self.create_label(x, y, text, parent, sl)
        rx = 0.54
        sx = 0.2
        self.characterDetailVar = [0]
        self.characterDetailRadios = self.createRadioButtonGroup(parent, rx, y, sx, 0.03, self.characterDetailVar, 0.15, [
         PLocalizer.GameOptionsLow, PLocalizer.GameOptionsMedium, PLocalizer.GameOptionsHigh], 0.8, self.characterDetailRadiosCB)
        y += oy
        text = PLocalizer.GameOptionsTerrainDetailLevel
        self.create_label(x, y, text, parent, sl)
        self.terrainDetailVar = [
         0]
        self.terrainDetailRadios = self.createRadioButtonGroup(parent, rx, y, sx, 0.03, self.terrainDetailVar, 0.15, [
         PLocalizer.GameOptionsLow, PLocalizer.GameOptionsMedium, PLocalizer.GameOptionsHigh], 0.8, self.terrainDetailRadiosCB)
        y += oy
        text = PLocalizer.GameOptionsReflections
        self.create_label(x, y, text, parent, sl)
        self.reflectionsVar = [
         0]
        self.reflectionRadios = self.createRadioButtonGroup(parent, rx, y, sx, 0.03, self.reflectionsVar, 0.15, [
         PLocalizer.GameOptionsOff, PLocalizer.GameOptionsSkyOnly, PLocalizer.GameOptionsOn], 0.8, self.reflectionRadiosCB)
        y += oy
        text = PLocalizer.GameOptionsSpecialEffectsLevel
        self.create_label(x, y, text, parent, sl)
        self.specialEffectsVar = [
         0]
        self.specialEffectsRadios = self.createRadioButtonGroup(parent, rx, y, sx, 0.03, self.specialEffectsVar, 0.15, [
         PLocalizer.GameOptionsLow, PLocalizer.GameOptionsMedium, PLocalizer.GameOptionsHigh], 0.8, self.specialEffectsRadiosCB)
        y += oy
        text = PLocalizer.GameOptionsTextureDetailLevel
        self.create_label(x, y, text, parent, sl)
        self.textureDetailVar = [
         0]
        if self.gameOptions and self.gameOptions.options.texture_scale_mode == False:
            sx = 0.13
            self.textureDetailRadios = self.createRadioButtonGroup(parent, rx, y, sx, 0.03, self.textureDetailVar, 0.15, [
             PLocalizer.GameOptionsLow, PLocalizer.GameOptionsMedium, PLocalizer.GameOptionsHigh, PLocalizer.GameOptionsMaximum], 0.8, self.textureDetailRadiosCB)
        else:
            self.textureDetailRadios = self.createRadioButtonGroup(parent, rx, y, sx, 0.03, self.textureDetailVar, 0.15, [
             PLocalizer.GameOptionsLow, PLocalizer.GameOptionsMedium, PLocalizer.GameOptionsHigh], 0.8, self.textureDetailRadiosCB)
        y += oy
        text = PLocalizer.GameOptionsTextureCompressed + ' *'
        self.create_label(x, y, text, parent, sl)
        self.compressedTextureCheck = CheckButton(parent=parent, relief=None, scale=sc, pos=(x + 0.42, 0, y + 0.015), command=self.compressedTextureCheckCB)
        y += oy
        if self.gameOptions and self.gameOptions.shader_support:
            text = PLocalizer.GameOptionsShaderLevel + ' ' + self.gameOptions.shader_model.__repr__() + ' *'
            self.create_label(x, y, text, parent, sl)
            self.shaderLevelCheck = CheckButton(parent=parent, relief=None, scale=sc, pos=(x + 0.315, 0, y + 0.015), command=self.shaderLevelCheckCB)
        else:
            text = PLocalizer.GameOptionsNoShader
            self.create_label(x, y, text, parent, sl * 0.9)
            self.shaderLevelCheck = None
        y += oy
        text = PLocalizer.GameOptionsRenderedShadows
        self.create_label(x, y, text, parent, sl)
        self.renderedShadowsCheck = CheckButton(parent=parent, relief=None, scale=sc, pos=(x + 0.38, 0, y + 0.015), command=self.renderedShadowsCheckCB)
        y += oy
        text = PLocalizer.GameOptionsAggressiveMemory
        self.create_label(x, y, text, parent, sl)
        self.aggressiveMemoryCheck = CheckButton(parent=parent, relief=None, scale=sc, pos=(x + 0.62, 0, y + 0.015), command=self.aggressiveMemoryCheckCB)
        text = PLocalizer.GameOptionsRestartRequired
        y += oy
        self.create_label(x, y, text, parent, 0.9, color=(0.7, 0.7, 0.7, 1))
        return

    def setupDisplayFrame(self):
        self.displayFrame = DirectFrame(parent=self.customFrame, relief=None)
        x = 0.07
        y = 0.8
        oy = -0.08
        parent = self.displayFrame
        sl = 1.0
        sc = 0.35
        ox = 0.6
        text = PLocalizer.GameOptionsFullscreen
        self.create_label(x, y, text, parent, sl)
        self.fullScreenCheck = CheckButton(parent=parent, relief=None, scale=sc, pos=(x + 0.23, 0, y + 0.015), command=self.fullScreenCheckCB)
        if self.gameOptions and self.gameOptions.freeLock:
            self.fullScreenCheck['command'] = self.callShowUpsell
            subCard = loader.loadModel('models/gui/toplevel_gui')
            appendMe = DirectFrame(parent=self.fullScreenCheck, relief=None, state=DGG.DISABLED, geom=subCard.find('**/subscribers_lock'), geom_scale=0.3, geom_pos=(0.06,
                                                                                                                                                                     0,
                                                                                                                                                                     0.06))
            appendMe.setAlphaScale(1.0, 2)
            subCard.removeNode()
        y += oy
        text = PLocalizer.GameOptionsWindowedResolutions
        self.create_label(x, y, text, parent, sl)
        self.windowed_resolutions = []
        if hasattr(base, 'windowed_resolution_table'):
            resolution_table = base.windowed_resolution_table
        else:
            resolution_table = self.resolution_table
        for windowed_resolution in resolution_table:
            self.windowed_resolutions.append(windowed_resolution[0].__repr__() + 'x' + windowed_resolution[1].__repr__())

        self.windowedResolutionMenu = OptionMenu(parent=parent, scale=0.05, pos=(x + 0.64, 0, y), items=self.windowed_resolutions, command=self.windowedResolutionMenuCB)
        y += oy
        text = PLocalizer.GameOptionsFullscreenResolutions
        self.create_label(x, y, text, parent, sl)
        fullscreen_resolutions = []
        if hasattr(base, 'fullscreen_resolution_table'):
            resolution_table = base.fullscreen_resolution_table
        else:
            resolution_table = self.resolution_table
        for fullscreen_resolution in resolution_table:
            fullscreen_resolutions.append(fullscreen_resolution[0].__repr__() + 'x' + fullscreen_resolution[1].__repr__())

        self.fullscreenResolutionMenu = OptionMenu(parent=parent, scale=0.05, pos=(x + 0.64, 0, y), items=fullscreen_resolutions, command=self.fullscreenResolutionMenuCB)
        y += oy
        text = PLocalizer.GameOptionsInvertMouseLook
        self.create_label(x, y, text, parent, sl)
        self.invertMouseCheck = CheckButton(parent=parent, relief=None, scale=sc, pos=(x + 0.36, 0, y + 0.015), command=self.invertMouseCheckCB)
        y += oy
        text = PLocalizer.GameOptionsGUIScale
        self.create_label(x, y, text, parent, sl)

        def gui_scale_update_function(value):
            if self.gameOptions:
                self.gameOptions.options.gui_scale = value
            try:
                gui_manager = localAvatar.guiMgr
            except:
                gui_manager = None
            else:
                if gui_manager:
                    gui_manager.setUIScale(value * 0.6 + 0.7)

            return

        resolution = 0.01
        if self.gameOptions:
            self.gui_scale_slider = self.create_slider(gui_scale_update_function, self.gameOptions.options.gui_scale, x + ox, y, resolution, text, parent)
        else:
            self.gui_scale_slider = self.create_slider(gui_scale_update_function, 1.0, x + ox, y, resolution, text, parent)
        y += oy
        text = PLocalizer.GameOptionsHardwareGamma
        self.create_label(x, y, text, parent, sl)
        self.hardwareGammaCheck = CheckButton(parent=parent, relief=None, scale=sc, pos=(x + 0.36, 0, y + 0.015), command=self.hardwareGammaCheckCB)
        y += oy * 0.8
        text = PLocalizer.GameOptionsIntensity
        self.create_label(x + 0.2, y, text, parent, sl * 0.8)

        def gamma_update_function(value):
            if self.gameOptions:
                self.gameOptions.options.gamma = value
            if base.win and base.win.getGsg():
                if self.gameOptions and self.gameOptions.options.gamma_enable:
                    base.win.getGsg().setGamma(self.gameOptions.options.optionsGammaToGamma(self.gameOptions.options.gamma))

        resolution = 0.02
        if self.gameOptions:
            self.gamma_slider = self.create_slider(gamma_update_function, self.gameOptions.options.gamma, x + ox, y, resolution, text, parent)
        else:
            self.gamma_slider = self.create_slider(gamma_update_function, 1.0, x + ox, y, resolution, text, parent)
        if self.gameOptions.enable_hdr:
            y += oy
            text = PLocalizer.GameOptionsHdr
            self.create_label(x, y, text, parent, sl)
            self.hdrCheck = CheckButton(parent=parent, relief=None, scale=sc, pos=(x + 0.8, 0, y + 0.015), command=self.hdrCheckCB)
            y += oy * 0.8
            text = PLocalizer.GameOptionsIntensity
            self.create_label(x + 0.2, y, text, parent, sl * 0.8)

            def hdr_update_function(value):
                if self.gameOptions:
                    self.gameOptions.options.hdr_factor = value
                if hasattr(base, 'hdr') and base.hdr:
                    if self.gameOptions and self.gameOptions.options.hdr:
                        base.hdr.updateHdrFactor(value)

            resolution = 0.02
            if self.gameOptions:
                self.hdr_factor_slider = self.create_slider(hdr_update_function, self.gameOptions.options.hdr_factor, x + ox, y, resolution, text, parent)
            else:
                self.hdr_factor_slider = self.create_slider(hdr_update_function, 1.0, x + ox, y, resolution, text, parent)
            text = PLocalizer.GameOptionsRestartRequired
            y += oy
            self.create_label(x, y, text, parent, 0.9, color=(0.7, 0.7, 0.7, 1))
        if base.config.GetBool('want-cpu-frequency-warning', 0):
            y += oy
            text = PLocalizer.GameOptionsCpuFrequencyWarning
            self.create_label(x, y, text, parent, sl)
            self.cpuFrequencyWarningCheck = CheckButton(parent=parent, relief=None, scale=sc, pos=(x + 0.45, 0, y + 0.015), command=self.cpuFrequencyWarningCheckCB)
        else:
            self.cpuFrequencyWarningCheck = None
        return

    def createRadioButtonGroup(self, parent, x, y, sx, oy, variable, scale, labels, textScale, cmd=None):
        i = 0
        radioButtons = []
        for label in labels:
            radioButton = RadioButton(parent=parent, variable=variable, value=[i], scale=scale, relief=None, pos=(x + i * sx, 0, y), command=cmd)
            radioButtons.append(radioButton)
            i += 1

        for radio in radioButtons:
            radio.setOthers(radioButtons)

        y += oy
        i = 0
        for label in labels:
            self.create_label(x + i * sx, y, label, parent, textScale, TextNode.ACenter)
            i += 1

        return radioButtons

    def create_label(self, x, y, title, parent, scale=1, text_align=TextNode.ALeft, color=PiratesGuiGlobals.TextFG1):
        label = DirectLabel(parent=parent, relief=None, text=title, text_align=text_align, text_scale=PiratesGuiGlobals.TextScaleLarge * scale, text_pos=(x, y), text_fg=color, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceOutlineFont(), textMayChange=1)
        return

    def create_slider(self, update_function, default_value, x, y, resolution, label, parent):

        def update_slider(slider, update_function):
            update_function(slider['value'])

        charGui = loader.loadModel('models/gui/char_gui')
        slider = DirectSlider(parent=parent, relief=None, command=update_slider, image=charGui.find('**/chargui_slider_small'), image_scale=(2.15,
                                                                                                                                             2.15,
                                                                                                                                             1.5), thumb_relief=None, thumb_image=(charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), pos=(x, 0.0, y + 0.01), text_align=TextNode.ACenter, text_scale=(0.1,
                                                                                                                                                                                                                                                                                                                                                                                       0.1), text_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                                                                       0.1), text_fg=PiratesGuiGlobals.TextFG1, scale=0.28, pageSize=resolution, text=None, value=default_value)
        charGui.removeNode()
        slider.label = label
        slider['extraArgs'] = [slider, update_function]
        return slider

    def updateUI(self, name='video'):
        if name == 'video':
            self.videoButton.setBin('gui-fixed', 20)
            self.audioButton.setBin('gui-fixed', 10)
            self.highlightButton(self.videoButton)
            self.fadeButton(self.audioButton)
            self.audioFrame.hide()
            self.videoFrame.show()
            if self.videoVar[0] == 3:
                self.lowerFrame.show()
            else:
                self.lowerFrame.hide()
        else:
            if name == 'audio':
                self.videoButton.setBin('gui-fixed', 10)
                self.audioButton.setBin('gui-fixed', 20)
                self.highlightButton(self.audioButton)
                self.fadeButton(self.videoButton)
                self.audioFrame.show()
                self.videoFrame.hide()
                self.lowerFrame.hide()
            else:
                if name == 'graphics':
                    self.graphicsButton.setBin('gui-fixed', 20)
                    self.displayButton.setBin('gui-fixed', 10)
                    self.highlightButton(self.graphicsButton)
                    self.fadeButton(self.displayButton)
                    self.graphicsFrame.show()
                    self.displayFrame.hide()
                else:
                    if name == 'display':
                        self.graphicsButton.setBin('gui-fixed', 10)
                        self.displayButton.setBin('gui-fixed', 20)
                        self.highlightButton(self.displayButton)
                        self.fadeButton(self.graphicsButton)
                        self.graphicsFrame.hide()
                        self.displayFrame.show()

    def disableButton(self, button):
        c = 0.5
        button['state'] = DGG.DISABLED
        button['text_fg'] = (c, c, c, 1.0)

    def fadeButton(self, button):
        if button:
            button['text_fg'] = (1.0, 1.0, 1.0, 1.0)
            button['selected'] = False

    def highlightButton(self, button):
        if button:
            button['text_fg'] = (0.2, 0.8, 0.6, 1.0)
            button['selected'] = True

    def close(self):
        if self.gameOptions:
            self.gameOptions.hide()
        else:
            self.hide()

    def __loadFeedbackPanel(self):
        from pirates.piratesgui import FeedbackPanel
        self.close()
        if self.gameOptions:
            FeedbackPanel.FeedbackPanel()

    def initResolutionSettings(self):
        if self.gameOptions is None:
            return
        if base.inAdFrame:
            self.fullscreenResolutionMenu.updateState(DGG.DISABLED)
            if len(self.windowed_resolutions) > 2:
                self.windowedResolutionMenu['items'] = self.windowed_resolutions[:2]
                self.windowedResolutionMenu.setItems()
            total_modes = embedded.getCountWindowModes()
            current_mode = embedded.getCurrentWindowModeDef()
            for button_index in range(total_modes):
                m = embedded.getAtWindowModeDef(button_index)
                if current_mode['want_size_x'] == m['want_size_x'] and current_mode['want_size_y'] == m['want_size_y']:
                    self.windowedResolutionMenu.set(button_index, False)

        else:
            self.fullscreenResolutionMenu.updateState(DGG.NORMAL)
            self.windowedResolutionMenu['items'] = self.windowed_resolutions
            self.windowedResolutionMenu.setItems()
            self.windowedResolutionMenu.setByValue('%dx%d' % (self.gameOptions.options.window_width, self.gameOptions.options.window_height), False)
            self.fullscreenResolutionMenu.setByValue('%dx%d' % (self.gameOptions.options.fullscreen_width, self.gameOptions.options.fullscreen_height), False)
        self.videoRadios[self.gameOptions.options.simple_display_option].check()
        return

    def update(self):
        if self.gameOptions is None:
            return
        self.gameOptions.options.options_to_config()
        return

    def set_options(self, change_display):
        if self.gameOptions is None:
            return
        if change_display:
            self.gameOptions.set_display(self.gameOptions.options, base.pipe, self.gameOptions.options.getWidth(), self.gameOptions.options.getHeight())
        self.fullScreenCheck.setQuiet(self.gameOptions.options.fullscreen)
        self.initResolutionSettings()
        self.reflectionRadios[self.gameOptions.options.reflection].check()
        if self.shaderLevelCheck:
            self.shaderLevelCheck['value'] = self.gameOptions.options.shader
        self.renderedShadowsCheck['value'] = self.gameOptions.options.shadow
        self.specialEffectsRadios[self.gameOptions.options.special_effects].check()
        if self.gameOptions.options.texture_scale_mode:
            if self.gameOptions.options.texture_scale in self.textureScaleOptionList:
                self.textureDetailRadios[self.textureScaleOptionList.index(self.gameOptions.options.texture_scale)].check()
        else:
            if self.gameOptions.options.texture in self.textureOptionList:
                self.textureDetailRadios[self.textureOptionList.index(self.gameOptions.options.texture)].check()
        self.compressedTextureCheck.setQuiet(self.gameOptions.options.textureCompression)
        self.characterDetailRadios[self.gameOptions.options.reflection].check()
        self.terrainDetailRadios[self.gameOptions.options.terrain_detail_level].check()
        self.aggressiveMemoryCheck['value'] = self.gameOptions.options.memory
        self.soundEffectCheck['value'] = self.gameOptions.options.sound
        self.sound_volume_slider['value'] = self.gameOptions.options.sound_volume
        self.musicCheck['value'] = self.gameOptions.options.music
        self.music_volume_slider['value'] = self.gameOptions.options.music_volume
        self.invertMouseCheck['value'] = self.gameOptions.options.mouse_look
        self.gui_scale_slider['value'] = self.gameOptions.options.gui_scale
        if self.cpuFrequencyWarningCheck:
            self.cpuFrequencyWarningCheck['value'] = self.gameOptions.options.cpu_frequency_warning
        self.hardwareGammaCheck['value'] = self.gameOptions.options.gamma_enable
        self.gamma_slider['value'] = self.gameOptions.options.gamma
        if self.gameOptions.enable_hdr:
            self.hdrCheck['value'] = self.gameOptions.options.hdr
        self.update()
        return

    def callShowUpsell(self, val):
        self.fullScreenCheck.setQuiet(False)
        self.gameOptions.showUpsell()

    def fullScreenCheckCB(self, val):
        if self.gameOptions is None:
            return
        if self.gameOptions.velvet:
            self.gameOptions.options.fullscreen = 0
            self.fullScreenCheck.setQuiet(False)
        else:
            self.gameOptions.options.fullscreen = val
            self.gameOptions.options.fullscreen_runtime = val
            if val:
                self.gameOptions.set_display(self.gameOptions.options, base.pipe, self.gameOptions.options.fullscreen_width, self.gameOptions.options.fullscreen_height)
            else:
                self.gameOptions.set_display(self.gameOptions.options, base.pipe, self.gameOptions.options.window_width, self.gameOptions.options.window_height)
        self.set_options(False)
        return

    def windowedResolutionMenuCB(self, val, index):
        if self.gameOptions is None:
            return
        if base.inAdFrame:
            self.gameOptions.display_identifier = index
            self.gameOptions.set_display(self.gameOptions.options, base.pipe, base.windowed_resolution_table[index][0], base.windowed_resolution_table[index][1])
            if base.hasEmbedded:
                self.gameOptions.options.resolution = index
        else:
            if not self.gameOptions.options.fullscreen_runtime:
                self.gameOptions.set_display(self.gameOptions.options, base.pipe, base.windowed_resolution_table[index][0], base.windowed_resolution_table[index][1])
            self.gameOptions.options.window_width = base.windowed_resolution_table[index][0]
            self.gameOptions.options.window_height = base.windowed_resolution_table[index][1]
        return

    def fullscreenResolutionMenuCB(self, val, index):
        if self.gameOptions is None:
            return
        if base.inAdFrame:
            pass
        else:
            if self.gameOptions.options.fullscreen_runtime:
                self.gameOptions.set_display(self.gameOptions.options, base.pipe, base.fullscreen_resolution_table[index][0], base.fullscreen_resolution_table[index][1])
            self.gameOptions.options.fullscreen_width = base.fullscreen_resolution_table[index][0]
            self.gameOptions.options.fullscreen_height = base.fullscreen_resolution_table[index][1]
        return

    def shaderLevelCheckCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.shader = val
        if self.gameOptions.options.shader != val:
            self.gameOptions.display_restart_dialog()
        return

    def renderedShadowsCheckCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.shadow = val
        try:
            time_of_day_manager = base.cr.timeOfDayManager
        except:
            time_of_day_manager = None
        else:
            if time_of_day_manager:
                if val:
                    time_of_day_manager.enableAvatarShadows()
                else:
                    time_of_day_manager.disableAvatarShadows()

        return

    def reflectionRadiosCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.reflection = val[0]
        funcList = [Water.all_reflections_off, Water.all_reflecttions_show_through_only, Water.all_reflections_on]
        funcList[val[0]]()
        self.update()
        return

    def specialEffectsRadiosCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.special_effects = val[0]
        self.gameOptions.options.setRuntimeSpecialEffects()
        return

    def textureDetailRadiosCB(self, val):
        if self.gameOptions is None:
            return
        if self.gameOptions.options.texture_scale_mode:
            if self.gameOptions.options.texture_scale != self.textureScaleOptionList[val[0]]:
                self.gameOptions.display_restart_dialog()
            self.gameOptions.options.texture_scale = self.textureScaleOptionList[val[0]]
        else:
            self.gameOptions.options.texture = self.textureOptionList[val]
        return

    def compressedTextureCheckCB(self, val):
        if self.gameOptions is None:
            return
        if self.gameOptions.options.textureCompression != val:
            self.gameOptions.display_restart_dialog()
        self.gameOptions.options.textureCompression = val
        return

    def characterDetailRadiosCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.character_detail_level = val[0]
        self.gameOptions.options.setRuntimeAvatarDetailLevel(val[0])
        return

    def terrainDetailRadiosCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.terrain_detail_level = val[0]
        self.gameOptions.options.setRuntimeGridDetailLevel(val[0])
        return

    def aggressiveMemoryCheckCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.memory = val
        try:
            base.setLowMemory(self.gameOptions.options.memory)
        except:
            pass

        return

    def soundEffectCheckCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.sound = val
        base.enableSoundEffects(val)
        self.update()
        return

    def musicCheckCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.music = val
        base.enableMusic(val)
        self.update()
        return

    def invertMouseCheckCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.mouse_look = val
        self.update()
        return

    def cpuFrequencyWarningCheckCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.cpu_frequency_warning = val
        self.update()
        return

    def hardwareGammaCheckCB(self, val):
        if self.gameOptions is None:
            return
        self.gameOptions.options.gamma_enable = val
        if base.win and base.win.getGsg():
            if self.gameOptions.options.gamma_enable:
                base.win.getGsg().setGamma(self.gameOptions.options.optionsGammaToGamma(self.gameOptions.options.gamma))
            else:
                base.win.getGsg().restoreGamma()
        self.update()
        return

    def hdrCheckCB(self, val):
        if self.gameOptions is None:
            return
        if self.gameOptions.options.hdr != val:
            self.gameOptions.display_restart_dialog()
        self.gameOptions.options.hdr = val
        self.update()
        return

    def defaultButtonCB(self):
        if self.gameOptions is None:
            return
        if self.defaultDialog:
            self.defaultDialog.destroy()
        self.defaultDialog = PDialog.PDialog(text=PLocalizer.GameOptionsDefaultConfirm, style=OTPDialog.YesNo, giveMouse=False, command=self.defaultDialogCB)
        self.defaultDialog.setBin('gui-fixed', 20, 20)
        return

    def defaultDialogCB(self, val):
        self.defaultDialog.destroy()
        del self.defaultDialog
        self.defaultDialog = None
        if val == 1:
            self.gameOptions.default_button_function()
            self.videoRadios[3].check()
        return

    def restoreButtonCB(self):
        if self.gameOptions is None:
            return
        if self.restoreDialog:
            self.restoreDialog.destroy()
        self.restoreDialog = PDialog.PDialog(text=PLocalizer.GameOptionsRestoreConfirm, style=OTPDialog.YesNo, giveMouse=False, command=self.restoreDialogCB)
        self.restoreDialog.setBin('gui-fixed', 20, 20)
        return

    def restoreDialogCB(self, val):
        self.restoreDialog.destroy()
        del self.restoreDialog
        self.restoreDialog = None
        if val == 1:
            self.gameOptions.restore_button_function()
            self.videoRadios[self.gameOptions.options.simple_display_option].check()
        return

    def videoRadioButtonCB(self, var):
        self.updateUI()
        if self.gameOptions is None:
            return

        def handleAggressiveMemoryCheck():
            block_size = 1024 * 1024 * 256
            physical_memory = self.gameOptions.options.getPhysicalMemory(base.pipe)
            if physical_memory > 0:
                blocks = (physical_memory + block_size / 2) / block_size
                if blocks <= 2:
                    self.aggressiveMemoryCheck['value'] = True
                else:
                    self.aggressiveMemoryCheck['value'] = False
            else:
                self.aggressiveMemoryCheck['value'] = False

        self.gameOptions.options.simple_display_option = self.videoVar[0]
        if self.videoVar[0] == 0:
            self.characterDetailRadios[0].check()
            self.terrainDetailRadios[0].check()
            self.reflectionRadios[0].check()
            self.specialEffectsRadios[0].check()
            self.textureDetailRadios[0].check()
            self.compressedTextureCheck['value'] = True
            if self.shaderLevelCheck:
                self.shaderLevelCheck['value'] = False
            self.renderedShadowsCheck['value'] = False
            handleAggressiveMemoryCheck()
        else:
            if self.videoVar[0] == 1:
                self.characterDetailRadios[1].check()
                self.terrainDetailRadios[1].check()
                self.reflectionRadios[1].check()
                self.specialEffectsRadios[1].check()
                self.textureDetailRadios[1].check()
                self.compressedTextureCheck['value'] = True
                if self.shaderLevelCheck:
                    self.shaderLevelCheck['value'] = True
                self.renderedShadowsCheck['value'] = False
                handleAggressiveMemoryCheck()
            else:
                if self.videoVar[0] == 2:
                    self.characterDetailRadios[2].check()
                    self.terrainDetailRadios[2].check()
                    self.reflectionRadios[2].check()
                    self.specialEffectsRadios[2].check()
                    self.textureDetailRadios[2].check()
                    self.compressedTextureCheck['value'] = True
                    if self.shaderLevelCheck:
                        self.shaderLevelCheck['value'] = True
                    self.renderedShadowsCheck['value'] = True
                    handleAggressiveMemoryCheck()
        return
# okay decompiling .\pirates\piratesgui\GameOptionsGui.pyc
