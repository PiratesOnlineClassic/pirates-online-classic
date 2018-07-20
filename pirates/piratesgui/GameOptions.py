import copy
import datetime
import os
import string
import sys

from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.motiontrail.MotionTrail import MotionTrail
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from panda3d.core import *
from pirates.piratesbase import Freebooter, PiratesGlobals, PLocalizer
from pirates.piratesgui import GameOptionsMatrix, PDialog, PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.DialogButton import DialogButton
from pirates.piratesgui.GameOptionsGui import *
from pirates.piratesgui.GuiButton import GuiButton
from pirates.seapatch.Water import Water
from otp.nametag import NametagGlobals

try:
    import embedded
except:
    pass


class OptionSpace:

    notify = DirectNotifyGlobal.directNotify.newCategory('OptionSpace')

    def __init__(self):
        pass

    def read_integer(self, input_file):
        s = string.strip(input_file.readline())
        if self.debug:
            print s
        return string.atoi(s)

    def read_float(self, input_file):
        s = string.strip(input_file.readline())
        if self.debug:
            print s
        return string.atof(s)

    def read_string(self, input_file):
        return string.strip(input_file.readline())

    def write_integer(self, output_file, value):
        if output_file:
            output_file.write(value.__repr__())
            output_file.write('\n')

    def write_float(self, output_file, value):
        if output_file:
            output_file.write(value.__repr__())
            output_file.write('\n')

    def write_text(self, output_file, string):
        if output_file:
            output_file.write(string)

    def write_string(self, output_file, string):
        if output_file:
            output_file.write(string)
            output_file.write('\n')


class Options(OptionSpace):

    notify = DirectNotifyGlobal.directNotify.newCategory('Options')
    debug = False
    options_version = 16
    DEFAULT_API_FILE_PATH = 'game_api.txt'
    DEFAULT_FILE_PATH = 'game_options.txt'
    WORKING_FILE_PATH = 'last_working_options.txt'
    POSSIBLE_WORKING_FILE_PATH = 'p_working_options.txt'
    DEFAULT_STATE = 'default'
    CONFIG_STATE = 'config'
    NEW_STATE = 'new'
    ATTEMPT_STATE = 'attempt'
    WORKING_STATE = 'working'
    ATTEMPT_WORKING_STATE = 'attempt_working'
    option_low = 0
    option_medium = 1
    option_high = 2
    option_custom = 3
    texture_low = 256
    texture_medium = 512
    texture_high = 1024
    texture_maximum = -1
    default_max_texture_dimension = -1
    texture_scale_low = 0.25
    texture_scale_medium = 0.5
    texture_scale_high = 1.0
    texture_scale_maximum = 1.0
    gamma_save_offset = 0.25
    SpecialEffectsHigh = 2
    SpecialEffectsMedium = 1
    SpecialEffectsLow = 0
    desiredApi = 'default'

    def __init__(self):
        self.default()
        self.texture_scale_mode = True
        self.recommendOptionsBasedOnData = base.config.GetBool(
            'use-statistical-gameoptions-recommendation', 1)

    def save(self, file_path, state_string=None):
        state = False

        if os.path.exists(file_path):
            with open(file_path, 'w') as output_file:
                self.write_string(output_file, 'version ')
                self.write_integer(output_file, self.version)
                self.write_string(output_file, 'state ')
                if state_string == None:
                    self.write_string(output_file, self.state)
                else:
                    self.write_string(output_file, state_string)

                self.write_string(output_file, 'api ')
                self.write_string(output_file, self.api)
                self.write_string(output_file, 'window_width ')
                self.write_integer(output_file, self.window_width)
                self.write_string(output_file, 'window_height ')
                self.write_integer(output_file, self.window_height)
                self.write_string(output_file, 'fullscreen_width ')
                self.write_integer(output_file, self.fullscreen_width)
                self.write_string(output_file, 'fullscreen_height ')
                self.write_integer(output_file, self.fullscreen_height)
                self.write_string(output_file, 'resolution ')
                self.write_integer(output_file, self.resolution)
                self.write_string(output_file, 'fullscreen ')
                self.write_integer(output_file, self.fullscreen)
                self.write_string(output_file, 'widescreen ')
                self.write_integer(output_file, self.widescreen)
                self.write_string(output_file, 'widescreen_resolution ')
                self.write_integer(output_file, self.widescreen_resolution)
                self.write_string(output_file, 'widescreen_fullscreen ')
                self.write_integer(output_file, self.widescreen_fullscreen)
                self.write_string(output_file, 'reflection ')
                self.write_integer(output_file, self.reflection)
                self.write_string(output_file, 'shader ')
                self.write_integer(output_file, self.shader)
                self.write_string(output_file, 'shadow ')
                self.write_integer(output_file, self.shadow)
                self.write_string(output_file, 'texture ')
                self.write_integer(output_file, self.texture)
                self.write_string(output_file, 'texture_compression ')
                self.write_integer(output_file, self.textureCompression)
                self.write_string(output_file, 'sound ')
                self.write_integer(output_file, self.sound)
                self.write_string(output_file, 'sound_volume ')
                self.write_float(output_file, self.sound_volume)
                self.write_string(output_file, 'music ')
                self.write_integer(output_file, self.music)
                self.write_string(output_file, 'music_volume ')
                self.write_float(output_file, self.music_volume)
                self.write_string(output_file, 'gui_scale ')
                self.write_float(output_file, self.gui_scale)
                self.write_string(output_file, 'special_effects ')
                self.write_integer(output_file, self.special_effects)
                self.write_string(output_file, 'texture_scale ')
                self.write_string(output_file, 'frame_rate ')
                self.write_integer(output_file, self.frame_rate)
                if self.texture_scale <= 0.0:
                    self.texture_scale = 1.0

                self.write_float(output_file, self.texture_scale)
                self.write_string(output_file, 'character_detail_level ')
                self.write_integer(output_file, self.character_detail_level)
                self.write_string(output_file, 'terrain_detail_level ')
                self.write_integer(output_file, self.terrain_detail_level)
                self.write_string(output_file, 'memory ')
                self.write_integer(output_file, self.memory)
                self.write_string(output_file, 'mouse_look ')
                self.write_integer(output_file, self.mouse_look)
                self.write_string(output_file, 'gamma ')
                self.write_float(output_file, self.gamma - self.gamma_save_offset)
                self.write_string(output_file, 'gamma_enable ')
                self.write_integer(output_file, self.gamma_enable)
                self.write_string(output_file, 'cpu_frequency_warning ')
                if self.cpu_frequency_warning:
                    cpu_frequency_warning = 0
                else:
                    cpu_frequency_warning = 1

                self.write_integer(output_file, cpu_frequency_warning)
                self.write_string(output_file, 'hdr ')
                self.write_integer(output_file, self.hdr)
                self.write_string(output_file, 'hdr_factor ')
                self.write_integer(output_file, self.hdr_factor)
                self.write_string(output_file, 'ocean_visibility ')
                self.write_integer(output_file, self.ocean_visibility)
                self.write_string(output_file, 'simple_display_option ')
                self.write_integer(output_file, self.simple_display_option)
                state = True
                output_file.close()

        return state

    def saveWorking(self):
        options = Options()
        options_loaded = options.load(Options.POSSIBLE_WORKING_FILE_PATH)
        if options_loaded:
            options.save(Options.WORKING_FILE_PATH, Options.WORKING_STATE)
        options = Options()
        options_loaded = options.load(Options.DEFAULT_FILE_PATH)
        if options_loaded:
            options.save(Options.DEFAULT_FILE_PATH, Options.WORKING_STATE)

    def savePossibleWorking(self, options):
        options.save(Options.POSSIBLE_WORKING_FILE_PATH, Options.WORKING_STATE)

    def validate(self, dataType, dataName, default, acceptableValues=[]):
        try:
            data = self.tokenDict.get(dataName, default)
            if data == default:
                return default
            if isinstance(dataType, type):
                castValue = dataType(data)
                if acceptableValues:
                    if castValue in acceptableValues:
                        return castValue
                    else:
                        return default
                return castValue
            else:
                return default
        except:
            return default

    def load(self, file_path):
        state = False

        if os.path.exists(Options.DEFAULT_API_FILE_PATH):
            with open(Options.DEFAULT_API_FILE_PATH, 'r') as input_file:
                file_data = [x.strip() for x in input_file.read().split('\n')]
                self.desiredApi = file_data[0]
                input_file.close()

        if os.path.exists(file_path):
            with open(file_path, 'r') as input_file:
                file_data = [x.strip() for x in input_file.read().split('\n')]
                self.tokenDict = dict([
                    x for x in zip(file_data[:-1], file_data[1:])
                    if x[0][0].isalpha() or x[0].isalnum()
                ])
                self.version = self.validate(int, 'version', 0)
                self.state = self.validate(
                    str, 'state', 'default',
                    ['new', 'attempt', 'default', 'working'])

                self.api = self.validate(
                    str, 'api', 'default',
                    ['default', 'pandagl', 'pandadx7', 'pandadx8', 'pandadx9'])

                self.window_width = self.validate(int, 'window_width', 0)
                self.window_height = self.validate(int, 'window_height', 0)
                if (self.window_width, self.window_height
                   ) not in base.windowed_resolution_table:
                    self.window_width, self.window_height = base.windowed_resolution_table[
                        0]

                self.fullscreen_width = self.validate(int, 'fullscreen_width',
                                                      0)
                self.fullscreen_height = self.validate(int, 'fullscreen_height',
                                                       0)
                if (self.fullscreen_width, self.fullscreen_height
                   ) not in base.fullscreen_resolution_table:
                    self.fullscreen_width, self.fullscreen_height = base.fullscreen_resolution_table[
                        0]

                self.resolution = self.validate(int, 'resolution', 0, [0, 1])
                self.fullscreen = self.validate(int, 'fullscreen', 0, [0, 1])
                self.widescreen = self.validate(int, 'widescreen', 0)
                self.widescreen_resolution = self.validate(
                    int, 'widescreen_resolution', 0)
                self.widescreen_fullscreen = self.validate(
                    int, 'widescreen_fullscreen', 0)
                self.reflection = self.validate(int, 'reflection', 0)
                self.shader = self.validate(int, 'shader', 0)
                self.shadow = self.validate(int, 'shadow', 0)
                self.texture = self.validate(int, 'texture', -1,
                                             [-1, 256, 512, 1024])
                self.textureCompression = self.validate(
                    int, 'texture_compression', 1)
                self.sound = self.validate(int, 'sound', 1)
                self.sound_volume = self.validate(float, 'sound_volume', 1.0)
                self.music = self.validate(int, 'music', 1)
                self.music_volume = self.validate(float, 'music_volume', 1.0)
                self.gui_scale = self.validate(float, 'gui_scale', 0.5)
                self.special_effects = self.validate(int, 'special_effects', 2)
                self.texture_scale = self.validate(float, 'texture_scale', 1.0)
                if self.texture_scale <= 0.0:
                    self.texture_scale = 1.0

                self.character_detail_level = self.validate(
                    int, 'character_detail_level', 2)
                self.terrain_detail_level = self.validate(
                    int, 'terrain_detail_level', 2)
                self.memory = self.validate(int, 'memory', 0)
                self.mouse_look = self.validate(int, 'mouse_look', 0, [0, 1])
                self.frame_rate = self.validate(int, 'frame_rate', 0, [0, 1])
                self.gamma = self.validate(float, 'gamma', 0.0)
                self.gamma += self.gamma_save_offset
                self.gamma_enable = self.validate(int, 'gamma_enable', 0,
                                                  [0, 1])
                token = self.read_string(input_file)
                cpu_frequency_warning = self.validate(
                    int, 'cpu_frequency_warning', 0)
                if cpu_frequency_warning:
                    self.cpu_frequency_warning = 0
                else:
                    self.cpu_frequency_warning = 1

                self.hdr = self.validate(int, 'hdr', 0)
                self.hdr_factor = self.validate(float, 'hdr_factor', 1.0)
                if base.config.GetInt('want-game-options-ship-visibility', 0):
                    self.ocean_visibility = self.validate(
                        int, 'ocean_visibility', 1, [0, 1, 2])

                self.ocean_visibility = 0
                self.simple_display_option = self.validate(
                    int, 'simple_display_option', 3, [0, 1, 2, 3])
                state = True
                input_file.close()

        self.runtime()
        return state

    def config_resolution(self):
        self.resolution = base.width_to_resolution_id(
            base.config.GetInt('win-size', 800))
        horizontal_resolution = win_size.getIntWord(0)
        vertical_resolution = win_size.getIntWord(1)
        self.widescreen = 0
        if horizontal_resolution == 1280 and vertical_resolution == 720:
            self.widescreen = 1
            self.widescreen_resolution = 0
        if horizontal_resolution == 1920 and vertical_resolution == 1080:
            self.widescreen = 1
            self.widescreen_resolution = 1
        self.window_width = horizontal_resolution
        self.window_height = vertical_resolution
        self.fullscreen_width = horizontal_resolution
        self.fullscreen_height = vertical_resolution

    def config_to_options(self):
        self.default()
        win_size = ConfigVariableInt('win-size')
        self.resolution = GameOptions.width_to_resolution_id(
            base.config.GetInt('win-size', 800))
        horizontal_resolution = int(win_size.getValue())
        vertical_resolution = int(win_size.getValue())
        self.widescreen = 0
        if horizontal_resolution == 1280 and vertical_resolution == 720:
            self.widescreen = 1
            self.widescreen_resolution = 0
        if horizontal_resolution == 1920 and vertical_resolution == 1080:
            self.widescreen = 1
            self.widescreen_resolution = 1
        self.fullscreen = base.config.GetBool('fullscreen', 1)
        if base.config.GetBool('want-water-reflection', 1):
            self.reflection = 2
            if base.config.GetBool('want-water-reflection-show-through-only',
                                   1):
                self.reflection = 1
        else:
            self.reflection = 0
        if base.config.GetBool('want-water-reflect-all', 0):
            self.reflection = 3
        self.window_width = horizontal_resolution
        self.window_height = vertical_resolution
        self.fullscreen_width = horizontal_resolution
        self.fullscreen_height = vertical_resolution
        self.shader = base.config.GetBool('want-shaders', 1)
        self.shadow = base.config.GetBool('want-avatar-shadows', 0)
        self.texture = base.config.GetInt('max-texture-dimension',
                                          Options.default_max_texture_dimension)
        self.textureCompression = base.config.GetBool('compressed-textures', 0)
        self.texture_scale = base.config.GetFloat('texture-scale', 1.0)
        self.sound = base.config.GetBool('audio-sfx-active', 1)
        self.sound_volume = base.config.GetFloat('audio-sfx-volume', 1.0)
        self.music = base.config.GetBool('audio-music-active', 1)
        self.music_volume = base.config.GetFloat('audio-music-volume', 1.0)
        self.ocean_visibility = base.config.GetInt('ocean-visibility', 0)
        self.runtime()

    def options_to_config(self):
        config_variable = ConfigVariableBool('want-widescreen', 0)
        config_variable.setValue(self.widescreen)
        config_variable = ConfigVariableBool('want-water-reflection', 1)
        if self.reflection == 0:
            config_variable.setValue(0)
        else:
            config_variable.setValue(1)
        config_variable = ConfigVariableBool(
            'want-water-reflection-show-through-only', 1)
        if self.reflection == 1:
            config_variable.setValue(1)
        if self.reflection == 2:
            config_variable.setValue(0)
        if self.reflection == 3:
            config_variable.setValue(0)
        config_variable = ConfigVariableBool('want-water-reflect-all', 0)
        if self.reflection == 3:
            config_variable.setValue(1)
        else:
            config_variable.setValue(0)
        config_variable = ConfigVariableBool('want-shaders', 0)
        config_variable.setValue(self.shader_runtime)
        config_variable = ConfigVariableBool('want-avatar-shadows', 0)
        config_variable.setValue(self.shadow)
        config_variable = ConfigVariableBool('compressed-textures', 0)
        config_variable.setValue(self.textureCompressionRuntime)

    def getWidth(self):
        if self.fullscreen_runtime:
            return self.fullscreen_width
        else:
            return self.window_width

    def getHeight(self):
        if self.fullscreen_runtime:
            return self.fullscreen_height
        else:
            return self.window_height

    def getFullscreen(self):
        return self.fullscreen_runtime

    def pipeOptionsToPrcData(self):
        string = None
        if self.api == 'pandagl' or self.api == 'pandadx9' or self.api == 'pandadx8':
            string = '*********************'
            string = string + 'load-display ' + self.api + string
            print string
        return string

    def optionsToPrcData(self):
        string = ''
        string = string + 'win-size ' + self.getWidth().__repr__(
        ) + ' ' + self.getHeight().__repr__() + '\n'
        string = string + 'fullscreen ' + self.getFullscreen().__repr__() + '\n'
        if self.textureCompressionRuntime:
            string = string + 'compressed-textures 1\n'
        else:
            string = string + 'compressed-textures 0\n'
        if self.debug:
            print string
        return string

    def setRuntimeOptions(self):
        base.enableSoundEffects(self.sound)
        base.enableMusic(self.music)
        base.setFrameRateMeter(self.frame_rate)
        if base.sfxManagerList:
            index = 0
            length = len(base.sfxManagerList)
            while index < length:
                sfx_manager = base.sfxManagerList[index]
                sfx_manager.setVolume(self.sound_volume)
                index += 1

        if base.musicManager:
            base.musicManager.setVolume(self.music_volume)
        self.setRuntimeSpecialEffects()
        self.setRuntimeGridDetailLevel(self.terrain_detail_level)
        self.setRuntimeAvatarDetailLevel(self.character_detail_level)
        try:
            base.setLowMemory(self.memory)
        except:
            pass

        if base.win and base.win.getGsg():
            if self.gamma_enable:
                base.win.getGsg().setGamma(self.optionsGammaToGamma(self.gamma))
        self.setTextureScale()

    def setTextureScale(self):
        config_variable = ConfigVariableDouble('texture-scale', 1.0)
        value = self.texture_scale
        if value <= 0.0:
            value = 1.0
        if value >= 1.0:
            value = 1.0
        config_variable.setValue(value)

    def getGUIScale(self):
        return self.gui_scale * 0.6 + 0.7

    def default(self):
        self.version = self.options_version
        self.state = 'default'
        self.api = 'default'
        self.window_width = 800
        self.window_height = 600
        self.fullscreen_width = 800
        self.fullscreen_height = 600
        self.resolution = 1
        self.fullscreen = 0
        self.widescreen = 0
        self.widescreen_resolution = 0
        self.widescreen_fullscreen = 0
        self.reflection = 1
        self.shader = 0
        self.shadow = 0
        self.texture = Options.default_max_texture_dimension
        self.textureCompression = 0
        self.sound = 1
        self.sound_volume = 1.0
        self.music = 1
        self.music_volume = 1.0
        self.gui_scale = 0.5
        self.special_effects = self.SpecialEffectsHigh
        self.texture_scale = 0.0
        self.character_detail_level = Options.option_high
        self.terrain_detail_level = Options.option_high
        self.memory = 0
        self.mouse_look = 0
        self.frame_rate = 0
        self.gamma = self.gamma_save_offset
        self.gamma_enable = 0
        self.cpu_frequency_warning = 1
        self.reserved10 = 0
        self.ocean_visibility = 0
        self.hdr = 0
        self.hdr_factor = 1.0
        self.simple_display_option = Options.option_custom
        self.runtime()

    def runtime(self):
        self.fullscreen_runtime = self.fullscreen
        self.widescreen_runtime = self.widescreen
        self.shader_runtime = self.shader
        self.texture_runtime = self.texture
        self.textureCompressionRuntime = self.textureCompression

    def totalDisplayResolutions(self, pipe):
        total = 0
        if pipe:
            di = pipe.getDisplayInformation()
            total = di.getTotalDisplayModes()
        return total

    def findResolution(self, width, height, bits_per_pixel, pipe):
        found = False
        if pipe:
            di = pipe.getDisplayInformation()
            index = 0
            total_display_modes = di.getTotalDisplayModes()
            while index < total_display_modes:
                if di.getDisplayModeBitsPerPixel(index) == bits_per_pixel:
                    if width == di.getDisplayModeWidth(
                            index) and height == di.getDisplayModeHeight(index):
                        found = True
                        break
                index += 1

        return found

    def verifyOptions(self, pipe, overwrite=False):
        state = False
        bits_per_pixel = 32
        if pipe:
            state = True
            di = pipe.getDisplayInformation()
            if self.window_width <= di.getMaximumWindowWidth(
            ) and self.window_height <= di.getMaximumWindowHeight():
                state = state and True
            else:
                state = False
                if di.getMaximumWindowWidth() > 0 and di.getMaximumWindowHeight(
                ) > 0 and self.findResolution(di.getMaximumWindowWidth(),
                                              di.getMaximumWindowHeight(),
                                              bits_per_pixel, pipe):
                    if overwrite:
                        self.window_width = di.getMaximumWindowWidth()
                        self.window_height = di.getMaximumWindowHeight()
                else:
                    index = 0
                    total_display_modes = di.getTotalDisplayModes()
                    while index < total_display_modes:
                        if di.getDisplayModeBitsPerPixel(
                                index) == bits_per_pixel:
                            if di.getDisplayModeWidth(
                                    index
                            ) >= GameOptions.MinimumHorizontalResolution and di.getDisplayModeHeight(
                                    index
                            ) >= GameOptions.MinimumVerticalResolution:
                                if overwrite:
                                    self.window_width = di.getDisplayModeWidth(
                                        index)
                                    self.window_height = di.getDisplayModeHeight(
                                        index)
                                break
                        index += 1

            if self.findResolution(self.fullscreen_width,
                                   self.fullscreen_height, bits_per_pixel,
                                   pipe):
                state = state and True
            else:
                state = False
                if di.getMaximumWindowWidth() > 0 and di.getMaximumWindowHeight(
                ) > 0 and self.findResolution(di.getMaximumWindowWidth(),
                                              di.getMaximumWindowHeight(),
                                              bits_per_pixel, pipe):
                    if overwrite:
                        self.fullscreen_width = di.getMaximumWindowWidth()
                        self.fullscreen_height = di.getMaximumWindowHeight()
                else:
                    index = 0
                    total_display_modes = di.getTotalDisplayModes()
                    while index < total_display_modes:
                        if di.getDisplayModeBitsPerPixel(
                                index) == bits_per_pixel:
                            if di.getDisplayModeWidth(
                                    index
                            ) >= GameOptions.MinimumHorizontalResolution and di.getDisplayModeHeight(
                                    index
                            ) >= GameOptions.MinimumVerticalResolution:
                                if overwrite:
                                    self.fullscreen_width = di.getDisplayModeWidth(
                                        index)
                                    self.fullscreen_height = di.getDisplayModeHeight(
                                        index)
                                break
                        index += 1

        return state

    def physicalMemoryToGeomCacheSize(self, pipe):
        size = 100
        di = pipe.getDisplayInformation()
        if di.getDisplayState() == DisplayInformation.DSSuccess:
            block_size = 1024 * 1024 * 256
            physical_memory = di.getPhysicalMemory()
            if physical_memory > 0:
                blocks = (physical_memory + block_size / 2) / block_size
                if blocks <= 1:
                    size = 100
                elif blocks == 2:
                    size = 100
                elif blocks == 3:
                    size = 300
                elif blocks == 4:
                    size = 500
                elif blocks == 5:
                    size = 1000
                elif blocks == 6:
                    size = 2000
                elif blocks == 7:
                    size = 3000
                else:
                    size = 3000
        return size

    def setPrc(self, string):
        loadPrcFileData('game_options', string)

    def setRuntimeGeomCacheSize(self, size):
        if size > 0:
            string = 'geom-cache-size ' + size.__repr__() + '\n'
            self.setPrc(string)

    def getTextureScaleString(self):
        level = self.texture_scale
        if level == Options.texture_scale_low:
            string = 'low'
        else:
            if level == Options.texture_scale_medium:
                string = 'medium'
            else:
                if level == Options.texture_scale_high:
                    string = 'high'
        return string

    def getGameOptionString(self, level):
        if level == Options.option_low:
            string = 'low'
        else:
            if level == Options.option_medium:
                string = 'med'
            else:
                string = 'high'
        return string

    def setRuntimeGridDetailLevel(self, level):
        string = 'grid-detail %s\n' % self.getGameOptionString(level)
        self.setPrc(string)
        try:
            base.positionFarCull()
        except:
            pass

    def setRuntimeAvatarDetailLevel(self, level):
        string = 'avatar-detail %s\n' % self.getGameOptionString(level)
        self.setPrc(string)

    def setGeomCacheSize(self, pipe):
        return
        if base.config.GetInt('ignore-game-options', 0) == 0:
            size = self.physicalMemoryToGeomCacheSize(pipe)
            if size > 0:
                string = 'geom-cache-size ' + size.__repr__() + '\n'
                if self.debug:
                    print string
                self.setPrc(string)

    def getPhysicalMemory(self, pipe):
        physical_memory = 0
        di = pipe.getDisplayInformation()
        if di.getDisplayState() == DisplayInformation.DSSuccess:
            physical_memory = di.getPhysicalMemory()
        return physical_memory

    def optionsGammaToGamma(self, gamma):
        return gamma * 2.0 + 0.5

    def automaticGrapghicsApiSelection(self, pipe):
        di = pipe.getDisplayInformation()
        if di.getDisplayState(
        ) == DisplayInformation.DSSuccess and base.config.GetBool(
                'use-graphics-api-auto-select', 1):
            state = False
            api = 'default'
            api2 = 'default'
            vendor_id = di.getVendorId()
            device_id = di.getDeviceId()
            if vendor_id == 4153:
                sis_device_list = [[25381, 'SiS 650']]
                length = len(sis_device_list)
                for i in range(length):
                    entry = sis_device_list[i]
                    if entry[0] == device_id:
                        pass

                api = 'pandadx9'
                api2 = 'pandadx8'
                state = True
            if state:
                print 'self.api =', self.api, 'api =', api
                if self.api == api or self.api == api2:
                    pass
                else:
                    base.makeAllPipes()
                    for pipe in base.pipeList:
                        if api == 'pandadx9' and pipe.getInterfaceName(
                        ) == 'DirectX9':
                            base.pipe = pipe
                            break
                        if api2 == 'pandadx8' and pipe.getInterfaceName(
                        ) == 'DirectX8':
                            base.pipe = pipe
                            break

    def recommendedOptions(self, pipe, realtime):
        di = pipe.getDisplayInformation()
        if di.getDisplayState() == DisplayInformation.DSSuccess:
            vendor_id = di.getVendorId()
            device_id = di.getDeviceId()
            driver_year = di.getDriverDateYear()
            driver_month = di.getDriverDateMonth()
            driver_day = di.getDriverDateDay()
            driver_product = di.getDriverProduct()
            driver_version = di.getDriverVersion()
            driver_sub_version = di.getDriverSubVersion()
            driver_build = di.getDriverBuild()
            days = 0.0
            if driver_year > 0 and driver_month > 0 and driver_day > 0:
                today = datetime.date.today()
                days = self.compareDates(today.year, today.month, today.day,
                                         driver_year, driver_month, driver_day)
            if driver_product or driver_version or driver_sub_version or driver_build:
                product = 0
                version = 0
                sub_version = 0
                build = 0
                state = self.compareNumbers(
                    product, version, sub_version, build, driver_product,
                    driver_version, driver_sub_version, driver_build)
            low_end_card = 0
            self.shader = 0
            self.output('vendor_id ', vendor_id)
            self.output('device_id ', device_id)
            if vendor_id == 4098:
                ati_device_list = [
                    [0, 'Rage 128 Pro',
                     20550], [0, 'RV100 Radeon 7000 / Radeon VE', 20825], [
                         0, 'Rage 128 PRO ULTRA Video Controller', 21574
                     ], ['AMD Stream Processor',
                         29262], ['AMD Stream Processor Secondary', 29294],
                    ['Fire PRO Professional Graphics ASIC',
                     38348], ['FireStream 9170',
                              38169], ['ATI FireGL T2', 16724], [
                                  'ATI FireGL T2 Secondary', 16756
                              ], ['ATI FireGL V3100', 23396], [
                                  'ATI FireGL V3100 Secondary', 23412
                              ], ['ATI FireGL V3200', 15956], [
                                  'ATI FireGL V3200 Secondary', 15988
                              ], ['ATI FireGL V3300', 29010], [
                                  'ATI FireGL V3300 Secondary', 29042
                              ], ['ATI FireGL V3350', 29011], [
                                  'ATI FireGL V3350 Secondary', 29043
                              ], ['ATI FireGL V3400', 29138], [
                                  'ATI FireGL V3400 Secondary', 29170
                              ], ['ATI FireGL V5000', 24136], [
                                  'ATI FireGL V5000 Secondary', 24168
                              ], ['ATI FireGL V5100', 21841], [
                                  'ATI FireGL V5100  Secondary', 21873
                              ], ['ATI FireGL V5200', 29146], [
                                  'ATI FireGL V5200 Secondary', 29178
                              ], ['ATI FireGL V5300', 28933], [
                                  'ATI FireGL V5300 Secondary', 28965
                              ], ['ATI FireGL V7100', 21840], [
                                  'ATI FireGL V7100 Secondary', 21872
                              ], ['ATI FireGL V7200', 23888], [
                                  'ATI FireGL V7200 ', 28932
                              ], ['ATI FireGL V7200 Secondary', 23920], [
                                  'ATI FireGL V7200 Secondary ', 28964
                              ], ['ATI FireGL V7300', 28942], [
                                  'ATI FireGL V7300 Secondary', 28974
                              ], ['ATI FireGL V7350', 28943], [
                                  'ATI FireGL V7350 Secondary', 28975
                              ], ['ATI FireGL V7600', 37903], [
                                  'ATI FireGL V7700', 38161
                              ], ['ATI FireGL V8600', 37899], [
                                  'ATI FireGL V8650',
                                  37898
                              ], ['ATI FireGL X1', 20039], [
                                  'ATI FireGL X1 Secondary', 20071
                              ], ['ATI FireGL X2-256/X2-256t', 20043], [
                                  'ATI FireGL X2-256/X2-256t Secondary', 20075
                              ], ['ATI FireGL X3-256', 19021], [
                                  'ATI FireGL X3-256 Secondary', 19053
                              ], ['ATI FireGL Z1', 16711], [
                                  'ATI FireGL Z1 Secondary', 16743
                              ], ['ATI FireMV 2200', 23397], [
                                  'ATI FireMV 2200 Secondary', 23413
                              ], ['ATI FireMV 2250', 29083], [
                                  'ATI FireMV 2250 Secondary', 29115
                              ], ['ATI FireMV 2260', 38350], [
                                  'ATI FireMV 2260',
                                  38351
                              ], ['ATI FireMV 2400', 12625],
                    ['ATI FireMV 2400 Secondary', 12657], [
                        'ATI FireMV 2450',
                        38349
                    ], ['ATI FireStream 2U',
                        29262], ['ATI FireStream 2U Secondary', 29294], [
                            'ATI MOBILITY FIRE GL 7800', 19544
                        ], ['ATI MOBILITY FIRE GL T2/T2e',
                            20052], ['ATI MOBILITY FireGL V3100', 21604], [
                                'ATI MOBILITY FireGL V3200', 12628
                            ], ['ATI MOBILITY FireGL V5000', 22090], [
                                'ATI MOBILITY FireGL V5000 ', 22091
                            ], ['ATI MOBILITY FireGL V5100', 23881], [
                                'ATI MOBILITY FireGL V5200', 29124
                            ], ['ATI MOBILITY FireGL V5250', 29140], [
                                'ATI MOBILITY FireGL V7100', 28934
                            ], ['ATI MOBILITY FireGL V7200', 28931], [
                                'ATI MOBILITY RADEON', 19545
                            ], ['ATI MOBILITY RADEON 7500', 19543], [
                                'ATI MOBILITY RADEON 9500', 20050
                            ], ['ATI MOBILITY RADEON 9550', 20054], [
                                'ATI MOBILITY RADEON 9600/9700 Series', 20048
                            ], ['ATI MOBILITY RADEON 9800', 19022], [
                                'ATI Mobility Radeon HD 2300', 29200
                            ], ['ATI Mobility Radeon HD 2300 ', 29201], [
                                'ATI Mobility Radeon HD 2400', 38089
                            ], ['ATI Mobility Radeon HD 2400 XT', 38088], [
                                1, 'ATI Mobility Radeon HD 2600', 38273
                            ], [1, 'ATI Mobility Radeon HD 2600 XT', 38275], [
                                1, 'ATI Mobility Radeon HD 3400 Series', 38340
                            ], [1, 'ATI Mobility Radeon HD 3430', 38338], [
                                1, 'ATI Mobility Radeon HD 3650', 38289
                            ], [1, 'ATI Mobility Radeon HD 3670', 38291], [
                                1, 'ATI Mobility Radeon HD 3850', 38148
                            ], [1, 'ATI Mobility Radeon HD 3850 X2', 38150], [
                                1, 'ATI Mobility Radeon HD 3870', 38152
                            ], [1, 'ATI Mobility Radeon HD 3870 X2',
                                38153], ['ATI Mobility Radeon X1300', 29002], [
                                    'ATI Mobility Radeon X1300 ', 29001
                                ], ['ATI Mobility Radeon X1300  ', 29003], [
                                    'ATI Mobility Radeon X1300   ', 29004
                                ], ['ATI Mobility Radeon X1350', 29067], [
                                    'ATI Mobility Radeon X1350 ', 29068
                                ], ['ATI Mobility Radeon X1350  ', 29078], [
                                    'ATI Mobility Radeon X1400', 28997
                                ], ['ATI Mobility Radeon X1450', 29062], [
                                    'ATI Mobility Radeon X1450 ', 29069
                                ], ['ATI Mobility Radeon X1600', 29125], [
                                    'ATI Mobility Radeon X1700', 29141
                                ], ['ATI Mobility Radeon X1700 ', 29150], [
                                    'ATI Mobility Radeon X1700 XT', 29142
                                ], [1, 'ATI Mobility Radeon X1800', 28930], [
                                    1, 'ATI Mobility Radeon X1800 XT', 28929
                                ], [1, 'ATI Mobility Radeon X1900', 29316], [
                                    1, 'ATI Mobility Radeon X2300', 29066
                                ], [1, 'ATI Mobility Radeon X2300 ',
                                    29064], ['ATI MOBILITY RADEON X300', 21601],
                    ['ATI MOBILITY RADEON X300 ',
                     21600], ['ATI MOBILITY RADEON X300  ', 12626], [
                         'ATI MOBILITY RADEON X600', 12624
                     ], ['ATI MOBILITY RADEON X600 SE', 21602], [
                         'ATI MOBILITY RADEON X700', 22098
                     ], ['ATI MOBILITY RADEON X700 ', 22099], [
                         'ATI MOBILITY RADEON X700 Secondary', 22131
                     ], [1, 'ATI MOBILITY RADEON X800', 23882], [
                         1, 'ATI MOBILITY RADEON X800  XT', 23880
                     ], [1, 'ATI Mobility Radeon HD 2600 XT Gemini', 38283], [
                         1, 'ATI Radeon 2100', 31086
                     ], [1, 'ATI Radeon 3100 Graphics', 38417], [
                         1, 'ATI Radeon 3100 Graphics', 38419
                     ], ['ATI Radeon 9550/X1050 Series', 16723], [
                         'ATI Radeon 9550/X1050 Series Secondary', 16755
                     ], ['ATI RADEON 9600 Series', 16720], [
                         'ATI RADEON 9600 Series ', 20049
                     ], ['ATI RADEON 9600 Series  ', 16721], [
                         'ATI RADEON 9600 Series   ', 16725
                     ], ['ATI RADEON 9600 Series    ', 16722], [
                         'ATI RADEON 9600 Series Secondary', 20081
                     ], ['ATI RADEON 9600 Series Secondary ', 16753], [
                         'ATI RADEON 9600 Series Secondary  ', 16752
                     ], ['ATI RADEON 9600 Series Secondary   ', 16757], [
                         'ATI RADEON 9600 Series Secondary    ', 16754
                     ], ['ATI Radeon E2400', 38091], [
                         'ATI Radeon HD 2350', 38087
                     ], ['ATI Radeon HD 2400', 38092], [
                         'ATI Radeon HD 2400 LE', 38085
                     ], ['ATI Radeon HD 2400 PRO', 38083], [
                         'ATI Radeon HD 2400 PRO AGP', 38084
                     ], ['ATI Radeon HD 2400 XT', 38081], [
                         1, 'ATI Radeon HD 2600 LE', 38286
                     ], [1, 'ATI Radeon HD 2600 Pro', 38281], [
                         1, 'ATI Radeon HD 2600 Pro AGP', 38279
                     ], [1, 'ATI Radeon HD 2600 XT', 38280], [
                         1, 'ATI Radeon HD 2600 XT AGP', 38278
                     ], [1, 'ATI Radeon HD 2900 GT', 9405], [
                         1, 'ATI Radeon HD 2900 PRO', 37891
                     ], [1, 'ATI Radeon HD 2900 XT', 37888], [
                         1, 'ATI Radeon HD 2900 XT ', 37889
                     ], [1, 'ATI Radeon HD 2900 XT  ', 37890], [
                         1, 'ATI Radeon HD 3200 Graphics', 38416
                     ], [1, 'ATI Radeon HD 3200 Graphics', 38418], [
                         1, 'ATI Radeon HD 3300 Graphics', 38420
                     ], [1, 'ATI Radeon HD 3430', 38343], [
                         1, 'ATI Radeon HD 3450', 38341
                     ], [1, 'ATI Radeon HD 3470', 38336], [
                         1, 'ATI Radeon HD 3600 Series', 38288
                     ], [1, 'ATI Radeon HD 3600 Series', 38295], [
                         1, 'ATI Radeon HD 3600 Series', 38296
                     ], [1, 'ATI Radeon HD 3600 Series', 38297], [
                         1, 'ATI Radeon HD 3650 AGP', 38294
                     ], [1, 'ATI Radeon HD 3830', 38151], [
                         1, 'ATI Radeon HD 3850', 38149
                     ], [1, 'ATI Radeon HD 3850 AGP', 38165], [
                         1, 'ATI Radeon HD 3850 X2', 38163
                     ], [1, 'ATI Radeon HD 3870', 38145], [
                         1, 'ATI Radeon HD 3870 X2', 38159
                     ], ['ATI Radeon X1200 Series', 31006], [
                         'ATI Radeon X1200 Series ', 31007
                     ], [1, 'Radeon X1950 XTX Uber - Limited Edition', 29256], [
                         1, 'Radeon X1950 XTX Uber - Limited Edition Secondary',
                         29288
                     ], [1, 'ATI Radeon X1950 GT',
                         29320], [1, 'ATI Radeon X1950 GT Secondary', 29352], [
                             1, 'ATI Radeon X800 GT', 23886
                         ], [1, 'ATI RADEON X800 GT', 21838], [
                             1, 'ATI Radeon X800 GT Secondary', 23918
                         ], [1, 'ATI RADEON X800 GT Secondary', 21870], [
                             1, 'ATI RADEON X800 XL', 21837
                         ], [1, 'ATI RADEON X800 XL Secondary', 21869], [
                             1, 'ATI RADEON X850 PRO', 19275
                         ], [1, 'ATI RADEON X850 PRO Secondary', 19307], [
                             1, 'ATI RADEON X850 SE', 19274
                         ], [1, 'ATI RADEON X850 SE Secondary', 19306], [
                             1, 'ATI RADEON X850 XT', 19273
                         ], [1, 'ATI RADEON X850 XT Platinum Edition', 19276], [
                             1, 'ATI RADEON X850 XT Platinum Edition Secondary',
                             19308
                         ], [1, 'Radeon X800 CrossFire Edition', 21837], [
                             1, 'Radeon X800 CrossFire Edition Secondary', 21869
                         ], [1, 'Radeon X850 CrossFire Edition', 23890], [
                             1, 'Radeon X850 CrossFire Edition Secondary', 23922
                         ], ['Radeon X550/X700 Series', 22095], [
                             'ATI Radeon X700 Series Secondary', 22127
                         ], [1, 'ATI RADEON X850 XT Secondary', 19305], [
                             'ATI Radeon Xpress 1200 Series', 31039
                         ], ['ATI Radeon Xpress 1200 Series ', 31041], [
                             'ATI Radeon Xpress 1200 Series  ', 31042
                         ], [0, 'ATI Radeon Xpress Series', 23137], [
                             0, 'ATI Radeon Xpress Series ', 23139
                         ], [0, 'ATI Radeon Xpress Series  ', 23138], [
                             0, 'ATI Radeon Xpress Series   ', 23105
                         ], [0, 'ATI Radeon Xpress Series    ', 23107], [
                             0, 'ATI Radeon Xpress Series     ', 23106
                         ], [0, 'ATI Radeon Xpress Series      ', 22868], [
                             0, 'ATI Radeon Xpress Series       ', 22612
                         ], [0, 'ATI Radeon Xpress Series        ', 22869], [
                             0, 'ATI Radeon Xpress Series         ', 22900
                         ], [0, 'ATI Radeon Xpress Series          ', 22644], [
                             0, 'ATI Radeon Xpress Series           ', 22901
                         ], ['Radeon 9500', 16708], ['Radeon 9500 ', 16713], [
                             'Radeon 9500 PRO / 9700', 20037
                         ], ['Radeon 9500 PRO / 9700 Secondary',
                             20069], ['Radeon 9500 Secondary', 16740], [
                                 'Radeon 9500 Secondary ', 16745
                             ], ['Radeon 9600 TX',
                                 20038], ['Radeon 9600 TX Secondary',
                                          20070], ['Radeon 9600TX', 16710],
                    ['Radeon 9600TX Secondary',
                     16742], ['Radeon 9700 PRO', 20036], [
                         'Radeon 9700 PRO Secondary', 20068
                     ], ['Radeon 9800', 20041], ['Radeon 9800 PRO', 20040], [
                         'Radeon 9800 PRO Secondary', 20072
                     ], ['Radeon 9800 SE', 16712], [
                         'Radeon 9800 SE Secondary', 16744
                     ], ['Radeon 9800 Secondary', 20073], [
                         'Radeon 9800 XT', 20042
                     ], ['Radeon 9800 XT Secondary', 20074], [
                         'Radeon X1300 / X1550 Series', 28998
                     ], ['Radeon X1300 / X1550 Series Secondary', 29030], [
                         'Radeon X1300 Series', 29006
                     ], ['Radeon X1300 Series ', 29022], [
                         'Radeon X1300 Series  ', 29005
                     ], ['Radeon X1300 Series   ', 29123], [
                         'Radeon X1300 Series    ', 29071
                     ], ['Radeon X1300 Series Secondary', 29038], [
                         'Radeon X1300 Series Secondary ', 29054
                     ], ['Radeon X1300 Series Secondary  ', 29037], [
                         'Radeon X1300 Series Secondary   ', 29155
                     ], ['Radeon X1300 Series Secondary    ', 29103], [
                         'Radeon X1300/X1550 Series', 28994
                     ], ['Radeon X1300/X1550 Series ', 29056], [
                         'Radeon X1300/X1550 Series  ', 29059
                     ], ['Radeon X1300/X1550 Series   ', 29063], [
                         'Radeon X1300/X1550 Series Secondary', 29026
                     ], ['Radeon X1300/X1550 Series Secondary ', 29088], [
                         'Radeon X1300/X1550 Series Secondary  ', 29091
                     ], ['Radeon X1300/X1550 Series Secondary   ', 29095], [
                         'Radeon X1550 64-bit', 28999
                     ], ['Radeon X1550 64-bit ', 29023], [
                         'Radeon X1550 64-bit  ', 29087
                     ], ['Radeon X1550 64-bit Secondary', 29031], [
                         'Radeon X1550 64-bit Secondary ', 29055
                     ], ['Radeon X1550 Series', 28995], [
                         'Radeon X1550 Series ', 29075
                     ], ['Radeon X1550 Series Secondary', 29027], [
                         'Radeon X1550 Series Secondary ', 29107
                     ], ['Radeon X1600 Pro / Radeon X1300 XT', 29134], [
                         'Radeon X1600 Pro / Radeon X1300 XT Secondary', 29166
                     ], ['Radeon X1600 Series',
                         28992], ['Radeon X1600 Series ', 29120], [
                             'Radeon X1600 Series  ', 29122
                         ], ['Radeon X1600 Series   ', 29126], [
                             'Radeon X1600 Series    ', 29057
                         ], ['Radeon X1600 Series     ', 29133], [
                             'Radeon X1600 Series Secondary', 29024
                         ], ['Radeon X1600 Series Secondary ', 29154], [
                             'Radeon X1600 Series Secondary  ', 29158
                         ], ['Radeon X1600 Series Secondary   ', 29089], [
                             'Radeon X1600 Series Secondary    ', 29165
                         ], ['Radeon X1600 Series Secondary     ',
                             29152], ['Radeon X1650 Series', 29121], [
                                 'Radeon X1650 Series ', 29331
                             ], ['Radeon X1650 Series  ', 29329], [
                                 'Radeon X1650 Series   ', 29127
                             ], ['Radeon X1650 Series Secondary', 29153], [
                                 'Radeon X1650 Series Secondary ', 29363
                             ], ['Radeon X1650 Series Secondary  ', 29361], [
                                 'Radeon X1650 Series Secondary   ', 29159
                             ], [1, 'Radeon X1800 Series',
                                 28928], [1, 'Radeon X1800 Series ', 28936], [
                                     1, 'Radeon X1800 CrossFire Edition', 28937
                                 ], [1, 'Radeon X1800 Series   ', 28938], [
                                     1, 'Radeon X1800 Series    ', 28939
                                 ], [1, 'Radeon X1800 Series     ', 28940],
                    [1, 'Radeon X1800 Series Secondary', 28960], [
                        1, 'Radeon X1800 Series Secondary ', 28968
                    ], [1, 'Radeon X1800 CrossFire Edition Secondary', 28969], [
                        1, 'Radeon X1800 Series Secondary   ', 28970
                    ], [1, 'Radeon X1800 Series Secondary    ', 28971], [
                        1, 'Radeon X1800 Series Secondary     ', 28972
                    ], [1, 'Radeon X1900 Series', 29251], [
                        1, 'Radeon X1900 Series ', 29253
                    ], [1, 'Radeon X1900 Series  ', 29254], [
                        1, 'Radeon X1900 Series   ', 29255
                    ], [1, 'Radeon X1900 CrossFire Edition', 29257], [
                        1, 'Radeon X1900 Series      ', 29258
                    ], [1, 'Radeon X1900 Series       ', 29259], [
                        1, 'Radeon X1900 Series        ', 29260
                    ], [1, 'Radeon X1900 Series         ', 29261], [
                        1, 'Radeon X1900 Series          ', 29263
                    ], [1, 'Radeon X1900 Series Secondary', 29283], [
                        1, 'Radeon X1900 Series Secondary ', 29285
                    ], [1, 'Radeon X1900 Series Secondary  ', 29286], [
                        1, 'Radeon X1900 Series Secondary   ', 29287
                    ], [1, 'Radeon X1900 CrossFire Edition Secondary', 29289], [
                        1, 'Radeon X1900 Series Secondary      ', 29290
                    ], [1, 'Radeon X1900 Series Secondary       ', 29291], [
                        1, 'Radeon X1900 Series Secondary        ', 29292
                    ], [1, 'Radeon X1900 Series Secondary         ', 29293], [
                        1, 'Radeon X1900 Series Secondary          ', 29295
                    ], [1, 'Radeon X1950 Series', 29312], [
                        1, 'Radeon X1950 CrossFire Edition', 29248
                    ], [1, 'Radeon X1950 Series  ', 29252], [
                        1, 'Radeon X1950 Series Secondary', 29344
                    ], [1, 'Radeon X1950 CrossFire Edition Secondary', 29280], [
                        1, 'Radeon X1950 Series Secondary  ', 29284
                    ], ['Radeon X300/X550/X1050 Series', 23392], [
                        'Radeon X300/X550/X1050 Series ', 23395
                    ], ['Radeon X300/X550/X1050 Series Secondary', 23411], [
                        'Radeon X300/X550/X1050 Series Secondary ', 23408
                    ], ['Radeon X550/X700 Series ', 22103], [
                        'Radeon X550/X700 Series Secondary', 22135
                    ], ['Radeon X600 Series', 23394], [
                        'Radeon X600 Series Secondary', 23410
                    ], ['Radeon X600/X550 Series', 15952], [
                        'Radeon X600/X550 Series Secondary', 15984
                    ], ['Radeon X700', 24141], ['Radeon X700 PRO', 24139], [
                        'Radeon X700 PRO Secondary', 24171
                    ], ['Radeon X700 SE', 24140], [
                        'Radeon X700 SE Secondary', 24172
                    ], ['Radeon X700 Secondary', 24173], [
                        'Radeon X700 XT', 24138
                    ], ['Radeon X700 XT Secondary', 24170], [
                        'Radeon X700/X550 Series', 24143
                    ], ['Radeon X700/X550 Series Secondary', 24175], [
                        1, 'Radeon X800 GT', 21835
                    ], [1, 'Radeon X800 GT Secondary', 21867], [
                        1, 'Radeon X800 GTO', 21833
                    ], [1, 'Radeon X800 GTO ', 21839], [
                        1, 'Radeon X800 GTO  ', 23887
                    ], [1, 'Radeon X800 GTO Secondary', 21865], [
                        1, 'Radeon X800 GTO Secondary ', 21871
                    ], [1, 'Radeon X800 GTO Secondary  ', 23919], [
                        1, 'Radeon X800 PRO', 19017
                    ], [1, 'Radeon X800 PRO Secondary', 19049], [
                        1, 'Radeon X800 SE', 19023
                    ], [1, 'Radeon X800 SE Secondary', 19055], [
                        1, 'Radeon X800 Series', 19016
                    ], [1, 'Radeon X800 Series ', 19018], [
                        1, 'Radeon X800 Series  ', 19020
                    ], [1, 'Radeon X800 Series   ', 21832], [
                        1, 'Radeon X800 Series Secondary', 19048
                    ], [1, 'Radeon X800 Series Secondary ', 19050], [
                        1, 'Radeon X800 Series Secondary  ', 19052
                    ], [1, 'Radeon X800 Series Secondary   ', 21864], [
                        1, 'Radeon X800 VE', 19028
                    ], [1, 'Radeon X800 VE Secondary', 19060], [
                        1, 'Radeon X800 XT', 19019
                    ], [1, 'Radeon X800 XT ', 23895], [
                        1, 'Radeon X800 XT Platinum Edition', 19024
                    ], [1, 'Radeon X800 XT Platinum Edition ', 21834], [
                        1, 'Radeon X800 XT Platinum Edition Secondary', 19056
                    ], [1, 'Radeon X800 XT Platinum Edition Secondary ',
                        21866], [1, 'Radeon X800 XT Secondary', 19051], [
                            1, 'Radeon X800 XT Secondary ', 23927
                        ], [1, 'Radeon X850 XT', 23890], [
                            1, 'Radeon X850 XT Platinum Edition', 23885
                        ], [
                            1, 'Radeon X850 XT Platinum Edition Secondary',
                            23917
                        ], [1, 'Radeon X850 XT Secondary', 23922]
                ]
                length = len(ati_device_list)
                for i in range(length):
                    entry = ati_device_list[i]
                    if entry[0] == 1:
                        if device_id == entry[2]:
                            self.shader = 1
                            self.output('device_name* ', entry[1])
                            break
                    else:
                        if entry[0] == 0:
                            if device_id == entry[2]:
                                low_end_card = 1
                                self.output('device_name* ', entry[1])
                                break
                        else:
                            if device_id == entry[1]:
                                self.output('device_name ', entry[0])
                                break

            if vendor_id == 4318:
                nvidia_device_list = [[
                    0, 45, 'NV5 TNT2 Model 64 / TNT2 Model 64 Pro'
                ], [0, 272, 'GeForce2 MX/MX 400'], [0, 273, 'GeForce2 MX200'], [
                    0, 272, 'GeForce2 MX/MX 400'
                ], [0, 370,
                    'GeForce4 MX 420'], [0, 373, 'NV17M GeForce4 420 Go'], [
                        0, 978, 'NVIDIA GeForce 6100 nForce 400'
                    ], [0, 977, 'NVIDIA GeForce 6100 nForce 405'], [
                        0, 976, 'NVIDIA GeForce 6100 nForce 430'
                    ], [0, 578, 'NVIDIA GeForce 6100'], [
                        0, 576, 'GeForce 6150'
                    ], [0, 577, 'NVIDIA GeForce 6150 LE'], [
                        0, 581, 'NVIDIA Quadro NVS 210S / NVIDIA GeForce 6150LE'
                    ], [335, 'GeForce 6200'], [243, 'GeForce 6200'], [
                        545, 'GeForce 6200  '
                    ], [546, 'GeForce 6200 A-LE'], [355, 'GeForce 6200 LE'], [
                        354, 'GeForce 6200SE TurboCache(TM)'
                    ], [353,
                        'GeForce 6200 TurboCache(TM)'], [361, 'GeForce 6250'], [
                            352, 'GeForce 6500'
                        ], [1, 321, 'GeForce 6600'], [1, 242, 'GeForce 6600'], [
                            1, 320, 'GeForce 6600 GT'
                        ], [1, 241, 'GeForce 6600 GT'], [
                            1, 322, 'GeForce 6600 LE'
                        ], [1, 244, 'GeForce 6600 LE'], [
                            1, 323, 'GeForce 6600 VE'
                        ], [1, 325, 'GeForce 6610 XL'], [
                            1, 327, 'GeForce 6700 XL'
                        ], [1, 65, 'GeForce 6800'], [1, 193, 'GeForce 6800 '], [
                            1, 529, 'GeForce 6800  '
                        ], [1, 71, 'GeForce 6800 GS'], [
                            1, 246, 'GeForce 6800 GS'
                        ], [1, 192, 'GeForce 6800 GS'], [
                            1, 69, 'GeForce 6800 GT'
                        ], [1, 70, 'GeForce 6800 GT '], [
                            1, 533, 'GeForce 6800 GT  '
                        ], [1, 249, 'GeForce 6800 Series GPU'], [
                            1, 66, 'GeForce 6800 LE'
                        ], [1, 194, 'GeForce 6800 LE '], [
                            1, 530, 'GeForce 6800 LE  '
                        ], [1, 64, 'GeForce 6800 Ultra'], [
                            1, 249, 'GeForce 6800 Series GPU'
                        ], [1, 67, 'GeForce 6800 XE'], [
                            1, 68, 'GeForce 6800 XT'
                        ], [1, 72, 'GeForce 6800 XT'], [
                            1, 195, 'GeForce 6800 XT  '
                        ], [1, 536, 'GeForce 6800 XT   '], [
                            1338, 'GeForce 7050 PV / NVIDIA nForce 630a'
                        ], [1339, 'GeForce 7050 PV / NVIDIA nForce 630a '], [
                            1342, 'GeForce 7025 / NVIDIA nForce 630a'
                        ], [2016, 'GeForce 7150 / NVIDIA nForce 630i'], [
                            2017, 'GeForce 7100 / NVIDIA nForce 630i'
                        ], [2018, 'GeForce 7050 / NVIDIA nForce 630i'], [
                            2019, 'GeForce 7050 / NVIDIA nForce 610i'
                        ], [2021, 'GeForce 7050 / NVIDIA nForce 620i'], [
                            362, 'GeForce 7100 GS'
                        ], [
                            479, 'GeForce 7300 GS'
                        ], [915, 'GeForce 7300 GT '], [
                            917, 'GeForce 7300 GT  '
                        ], [738, 'GeForce 7300 GT'], [465, 'GeForce 7300 LE'], [
                            467, 'GeForce 7300 SE/7200 GS'
                        ], [464, 'GeForce 7350 LE'], [477, 'GeForce 7500 LE'], [
                            1, 914, 'GeForce 7600 GS '
                        ], [1, 737, 'GeForce 7600 GS'], [
                            1, 913, 'GeForce 7600 GT'
                        ], [1, 736, 'GeForce 7600 GT'], [
                            1, 916, 'GeForce 7600 LE'
                        ], [1, 912, 'GeForce 7650 GS'], [
                            1, 245, 'GeForce 7800 GS'
                        ], [1, 147, 'GeForce 7800 GS '], [
                            1, 146, 'GeForce 7800 GT'
                        ], [1, 144, 'GeForce 7800 GTX'], [
                            1, 145, 'GeForce 7800 GTX'
                        ], [1, 149, 'GeForce 7800 SLI'], [
                            1, 739, 'GeForce 7900 GS'
                        ], [1, 658, 'GeForce 7900 GS '], [
                            1, 657, 'GeForce 7900 GT/GTO'
                        ], [1, 656, 'GeForce 7900 GTX'], [
                            1, 659, 'GeForce 7900 GX2'
                        ], [1, 740, 'GeForce 7950 GT'], [
                            1, 660, 'GeForce 7950 GX2 '
                        ], [1, 661, 'NVIDIA GeForce 7950 GT '], [
                            2121, 'GeForce 8200'
                        ], [2123, 'GeForce 8200 '], [2120, 'GeForce 8300'], [
                            1059, 'NVIDIA GeForce 8300 GS'
                        ], [1762, 'GeForce 8400'], [1056, 'GeForce 8400 SE'], [
                            1028, 'GeForce 8400 GS'
                        ], [1058, 'NVIDIA GeForce 8400 GS '], [
                            1060, 'GeForce 8400 GS  '
                        ], [1764, 'GeForce 8400 GS   '], [
                            1057, 'NVIDIA GeForce 8500 GT'
                        ], [1, 1024, 'NVIDIA GeForce 8600 GTS'], [
                            1, 1025, 'GeForce 8600 GT'
                        ], [1, 1026, 'NVIDIA GeForce 8600 GT'], [
                            1, 1027, 'GeForce 8600GS'
                        ], [1, 401, 'NVIDIA GeForce 8800 GTX'], [
                            1, 403, 'NVIDIA GeForce 8800 GTS'
                        ], [1, 404, 'GeForce 8800 Ultra'], [
                            1, 1536, 'GeForce 8800 GTS 512'
                        ], [1, 1538, 'GeForce 8800 GT'], [
                            1, 1553, 'GeForce 8800 GT '
                        ], [1, 1542, 'GeForce 8800 GS'], [
                            1, 1552, 'GeForce 9600 GSO'
                        ], [1, 1570, 'GeForce 9600 GT'], [
                            1, 1540, 'GeForce 9800 GX2'
                        ], [1, 1554, 'GeForce 9800 GTX'], [
                            2127, 'GeForce 8100 / nForce 720a'
                        ], [2122, 'nForce 730a'], [2125, 'nForce 750a SLI'], [
                            2124, 'nForce 780a SLI'
                        ], [802, 'GeForce FX 5200'], [
                            801, 'GeForce FX 5200 Ultra'
                        ], [803, 'GeForce FX 5200LE'], [
                            806, 'GeForce FX 5500'
                        ], [806, 'GeForce FX 5500'], [786, 'GeForce FX 5600'], [
                            785, 'GeForce FX 5600 Ultra'
                        ], [788, 'GeForce FX 5600XT'], [
                            834, 'GeForce FX 5700'
                        ], [833, 'GeForce FX 5700 Ultra'], [
                            835, 'GeForce FX 5700LE'
                        ], [836, 'GeForce FX 5700VE'], [
                            770, 'GeForce FX 5800'
                        ], [769, 'GeForce FX 5800 Ultra'], [
                            817, 'GeForce FX 5900'
                        ], [816, 'GeForce FX 5900 Ultra'], [
                            819, 'GeForce FX 5950 Ultra'
                        ], [804, 'GeForce FX Go5200 64M'], [
                            794, 'GeForce FX Go5600'
                        ], [839, 'GeForce FX Go5700'], [
                            359, 'GeForce Go 6200/6400'
                        ], [360, 'GeForce Go 6200/6400'], [
                            1, 328, 'GeForce Go 6600'
                        ], [1, 200, 'GeForce Go 6800'], [
                            1, 201, 'GeForce Go 6800 Ultra'
                        ], [1, 152, 'GeForce Go 7800'], [
                            1, 153, 'GeForce Go 7800 GTX'
                        ], [1, 664, 'GeForce Go 7900 GS'], [
                            1, 665, 'GeForce Go 7900 GTX'
                        ], [389, 'GeForce MX 4000'], [
                            250, 'GeForce PCX 5750'
                        ], [251, 'GeForce PCX 5900'], [512, 'GeForce3'], [
                            513, 'GeForce3 Ti200'
                        ], [514, 'GeForce3 Ti500'], [369, 'GeForce4 MX 440'], [
                            385, 'GeForce4 MX 440 with AGP8X'
                        ], [371, 'GeForce4 MX 440-SE'], [
                            368, 'GeForce4 MX 460'
                        ], [595, 'GeForce4 Ti 4200'], [
                            641, 'GeForce4 Ti 4200 with AGP8X'
                        ], [593, 'GeForce4 Ti 4400'], [
                            592, 'GeForce4 Ti 4600'
                        ], [640, 'GeForce4 Ti 4800'], [
                            642, 'GeForce4 Ti 4800SE'
                        ], [515, 'Quadro DCC'], [777, 'Quadro FX 1000'], [
                            846, 'Quadro FX 1100'
                        ], [254, 'Quadro FX 1300'], [206, 'Quadro FX 1400'], [
                            670, 'Quadro FX 1500'
                        ], [1039, 'Quadro FX 1700'], [776, 'Quadro FX 2000'], [
                            824, 'Quadro FX 3000'
                        ], [253, 'Quadro PCI-E Series'], [
                            1, 248, 'Quadro FX 3400/4400'
                        ], [1, 205, 'Quadro FX 3450/4000 SDI'], [
                            1, 669, 'Quadro FX 3500'
                        ], [1, 1562, 'Quadro FX 3700'], [
                            1, 78, 'Quadro FX 4000'
                        ], [1, 157, 'Quadro FX 4500'], [
                            1, 671, 'Quadro FX 4500 X2'
                        ], [1, 414, 'Quadro FX 4600'], [
                            1, 668, 'NVIDIA Quadro FX 5500'
                        ], [1, 413, 'Quadro FX 5600'], [478, 'Quadro FX 350'], [
                            1034, 'Quadro FX 370'
                        ], [811, 'Quadro FX 500/FX 600'], [
                            334, 'Quadro FX 540'
                        ], [332, 'Quadro FX 540 MXM'], [
                            811, 'Quadro FX 500/FX 600'
                        ], [333, 'Quadro FX 550'], [926, 'Quadro FX 560'], [
                            1038, 'Quadro FX 570'
                        ], [831, 'Quadro FX 700'], [844, 'Quadro FX Go1000'], [
                            204, 'Quadro FX Go1400'
                        ], [796, 'Quadro FX Go700'], [
                            394, 'Quadro NVS with AGP8X'
                        ], [810, 'Quadro NVS 280 PCI'], [
                            253, 'Quadro PCI-E Series'
                        ], [357, 'Quadro NVS 285'], [1071, 'Quadro NVS 290'], [
                            330, 'Quadro NVS 440'
                        ], [
                            378, 'Quadro NVS'
                        ], [394, 'Quadro NVS with AGP8X'], [
                            275, 'Quadro2 MXR/EX'
                        ], [378, 'Quadro NVS'], [395, 'Quadro4 380 XGL'], [
                            376, 'Quadro4 550 XGL'
                        ], [392, 'Quadro4 580 XGL'], [603, 'Quadro4 700 XGL'], [
                            601, 'Quadro4 750 XGL'
                        ], [600, 'Quadro4 900 XGL'], [648, 'Quadro4 980 XGL'],
                                      [652, 'Quadro4 Go700']]
                length = len(nvidia_device_list)
                for i in range(length):
                    entry = nvidia_device_list[i]
                    if entry[0] == 1:
                        if device_id == entry[1]:
                            self.shader = 1
                            self.output('device_name* ', entry[2])
                            break
                    else:
                        if entry[0] == 0:
                            if device_id == entry[1]:
                                low_end_card = 1
                                self.output('device_name* ', entry[2])
                                break
                        else:
                            if device_id == entry[1]:
                                self.output('device_name ', entry[1])
                                break

            if vendor_id == 32902:
                intel_device_list = [['Q35 Device 0 / X3000', 10674], [
                    'Q35 Device 1 / X3000', 10675
                ], ['G33/G31 Device 0 / 3000',
                    10690], ['G33/G31 Device 1 / 3000', 10691], [
                        'Q33 Device 0', 10706
                    ], ['Q33 Device 1', 10707], ['Q965/Q963 Device 0', 10642], [
                        'Q965/Q963 Device 1', 10643
                    ], ['GM965 Device 0 / X3100', 10754], [
                        'GM965 Device 1 / X3100', 10755
                    ], ['G965 Device 0 / X3000', 10658], [
                        'G965 Device 1 / X3000', 10659
                    ], ['946GZ Device 0', 10610], ['946GZ Device 1', 10611], [
                        '945GM Device 0', 10146
                    ], ['945GM Device 1', 10150], ['945G Device 0', 10098], [
                        '945G Device 1', 10102
                    ], ['915GM Device 0', 9618], ['915GM Device 1', 10130], [
                        '915G Device 0', 9602
                    ], ['915G Device 1', 10114], ['865G', 9586],
                                     ['855GM', 13698], ['845G',
                                                        9570], ['830M', 13687]]
                if device_id in intel_device_list:
                    pass
                low_end_card = 1
            if vendor_id == 21299:
                low_end_card = 1
            if vendor_id == 4153:
                low_end_card = 1
            if vendor_id == 4358:
                low_end_card = 1
            size = di.getVideoMemory()
            if size == 0:
                size = di.getTextureMemory()
            mb = 1024 * 1024
            if self.debug:
                size = 32 * mb
            test_size = base.config.GetInt('test-video-memory', 0)
            if test_size > 0:
                size = test_size * mb
            self.textureCompression = 1
            self.texture = Options.texture_maximum
            if size <= 0:
                self.texture = Options.texture_low
            elif size <= 32 * mb:
                self.texture = Options.texture_low
            elif size <= 64 * mb:
                self.texture = Options.texture_medium
            elif size <= 96 * mb:
                self.texture = Options.texture_medium
            elif size <= 128 * mb:
                self.texture = Options.texture_high
            elif size <= 256 * mb:
                pass
            elif size <= 512 * mb:
                pass
            elif size <= 768 * mb:
                pass
            elif size <= 1024 * mb:
                pass
            elif size > 1024 * mb:
                pass
            scale = Options.texture_scale_low
            block_size = 1024 * 1024 * 256
            physical_memory = di.getPhysicalMemory()
            if physical_memory > 0:
                blocks = (physical_memory + block_size / 2) / block_size
                if blocks <= 1:
                    scale = Options.texture_scale_low
                    self.special_effects = Options.SpecialEffectsLow
                    self.character_detail_level = Options.option_low
                    self.terrain_detail_level = Options.option_low
                    self.memory = 1
                elif blocks == 2:
                    scale = Options.texture_scale_low
                    self.special_effects = Options.SpecialEffectsLow
                    self.character_detail_level = Options.option_low
                    self.terrain_detail_level = Options.option_low
                    self.memory = 1
                elif blocks == 3:
                    scale = Options.texture_scale_medium
                    self.special_effects = Options.SpecialEffectsMedium
                    self.character_detail_level = Options.option_medium
                    self.terrain_detail_level = Options.option_medium
                elif blocks == 4:
                    if self.shader:
                        scale = Options.texture_scale_medium
                        self.special_effects = Options.SpecialEffectsMedium
                        self.character_detail_level = Options.option_high
                        self.terrain_detail_level = Options.option_high
                    else:
                        scale = Options.texture_scale_medium
                        self.special_effects = Options.SpecialEffectsMedium
                        self.character_detail_level = Options.option_medium
                        self.terrain_detail_level = Options.option_medium
                elif blocks == 5:
                    if self.shader:
                        scale = Options.texture_scale_high
                        self.special_effects = Options.SpecialEffectsHigh
                        self.character_detail_level = Options.option_high
                        self.terrain_detail_level = Options.option_high
                    else:
                        scale = Options.texture_scale_medium
                        self.special_effects = Options.SpecialEffectsMedium
                        self.character_detail_level = Options.option_medium
                        self.terrain_detail_level = Options.option_medium
                else:
                    if self.shader:
                        scale = Options.texture_scale_high
                        self.special_effects = Options.SpecialEffectsHigh
                        self.character_detail_level = Options.option_high
                        self.terrain_detail_level = Options.option_high
                    else:
                        scale = Options.texture_scale_medium
                        self.special_effects = Options.SpecialEffectsMedium
                        self.character_detail_level = Options.option_medium
                        self.terrain_detail_level = Options.option_medium
            low_end_card = base.config.GetInt('low-end-card', low_end_card)
            if low_end_card:
                self.output('info ', 'test-low-end card')
                scale = Options.texture_scale_low
                self.special_effects = Options.SpecialEffectsLow
                self.character_detail_level = Options.option_low
                self.terrain_detail_level = Options.option_low
                self.memory = 1
            self.texture_scale = scale
            high_end_card = base.config.GetInt('test-high-end-card',
                                               self.shader)
            if high_end_card:
                width = 1024
                height = 768
                bits_per_pixel = 32
                supported = False
                total_display_modes = di.getTotalDisplayModes()
                if total_display_modes > 0:
                    index = 0
                    while index < total_display_modes:
                        if di.getDisplayModeBitsPerPixel(
                                index) == bits_per_pixel:
                            if width == di.getDisplayModeWidth(
                                    index
                            ) and height == di.getDisplayModeHeight(index):
                                supported = True
                                break
                        index += 1

                if supported:
                    if width <= di.getMaximumWindowWidth(
                    ) and height <= di.getMaximumWindowHeight():
                        self.window_width = width
                        self.window_height = height
                    self.fullscreen_width = width
                    self.fullscreen_height = height
            if self.recommendOptionsBasedOnData:

                def validate_gameOptions(options):
                    if len(options) != 18:
                        return False
                    if int(options[1:2]) not in [0, 1, 2]:
                        return False
                    if int(options[3:4]) not in [0, 1]:
                        return False
                    if int(options[5:6]) not in [0, 1]:
                        return False
                    if int(options[7:8]) not in [1, 2, 4]:
                        return False
                    if int(options[9:10]) not in [0, 1]:
                        return False
                    if int(options[11:12]) not in [0, 1, 2]:
                        return False
                    if int(options[13:14]) not in [0, 1, 2]:
                        return False
                    if int(options[15:16]) not in [0, 1, 2]:
                        return False
                    if int(options[17:18]) not in [0, 1]:
                        return False
                    return True

                system_key = ('0x%04x' % di.getVendorId(),
                              '0x%04x' % di.getDeviceId(),
                              '%s.%d.%d.%d' % (os.name, di.getOsPlatformId(),
                                               di.getOsVersionMajor(),
                                               di.getOsVersionMinor()))
                if GameOptionsMatrix.GameOptionsMatrix.has_key(system_key):
                    options_from_data = GameOptionsMatrix.GameOptionsMatrix[
                        system_key][0]
                    if validate_gameOptions(options_from_data):
                        self.reflection = int(options_from_data[1:2])
                        self.shader = int(options_from_data[3:4])
                        self.shadow = int(options_from_data[5:6])
                        self.texture_scale = 1.0 / int(options_from_data[7:8])
                        self.textureCompression = int(options_from_data[9:10])
                        self.special_effects = int(options_from_data[11:12])
                        self.character_detail_level = int(
                            options_from_data[13:14])
                        self.terrain_detail_level = int(
                            options_from_data[15:16])
                        self.memory = int(options_from_data[17:18])
        else:
            self.textureCompression = 1
            self.texture = Options.texture_medium
        if not realtime:
            self.runtime()
        return

    def getSpecialEffectsSetting(self):
        return self.special_effects

    def setRuntimeSpecialEffects(self):
        if hasattr(base,
                   'localAvatar') and localAvatar and not localAvatar.ship:
            gamearea = localAvatar.getParentObj()
            if hasattr(gamearea, 'envEffects') and gamearea.envEffects:
                gamearea.envEffects.unloadEffects()
                gamearea.envEffects.loadEffects()
        if self.special_effects == Options.SpecialEffectsLow:
            MotionTrail.setGlobalEnable(False)
        if self.special_effects == Options.SpecialEffectsMedium:
            MotionTrail.setGlobalEnable(True)
        if self.special_effects == Options.SpecialEffectsHigh:
            MotionTrail.setGlobalEnable(True)

    def output(self, token, value):
        self.notify.info(token + '= ' + value.__repr__())

    def log(self, message=None):
        if message:
            self.notify.info(message)
        self.output('version ', self.version)
        self.output('state ', self.state)
        self.output('api ', self.api)
        self.output('window_width ', self.window_width)
        self.output('window_height ', self.window_height)
        self.output('fullscreen_width ', self.fullscreen_width)
        self.output('fullscreen_height ', self.fullscreen_height)
        self.output('resolution ', self.resolution)
        self.output('fullscreen ', self.fullscreen)
        self.output('widescreen ', self.widescreen)
        self.output('widescreen_resolution ', self.widescreen_resolution)
        self.output('widescreen_fullscreen ', self.widescreen_fullscreen)
        self.output('reflection ', self.reflection)
        self.output('shader ', self.shader)
        self.output('shadow ', self.shadow)
        self.output('texture ', self.texture)
        self.output('texture_compression ', self.textureCompression)
        self.output('sound ', self.sound)
        self.output('sound_volume ', self.sound_volume)
        self.output('music ', self.music)
        self.output('music_volume ', self.music_volume)
        self.output('gui_scale ', self.gui_scale)
        self.output('special_effects ', self.special_effects)
        self.output('texture_scale ', self.texture_scale)
        self.output('character_detail_level ', self.character_detail_level)
        self.output('terrain_detail_level ', self.terrain_detail_level)
        self.output('memory ', self.memory)
        self.output('mouse_look ', self.mouse_look)
        self.output('frame_rate', self.frame_rate)
        self.output('gamma ', self.gamma - self.gamma_save_offset)
        self.output('gamma_enable ', self.gamma_enable)
        self.output('cpu_frequency_warning ', self.cpu_frequency_warning)
        self.output('hdr ', self.hdr)
        self.output('hdr_factor ', self.hdr_factor)
        self.output('ship_visibility_from_islands ', self.ocean_visibility)
        self.output('simple_display_option', self.simple_display_option)
        scale = self.texture_scale
        if scale <= 0.0:
            scale = 1.0
        scale = 1.0 / scale
        gameOptionsCode = 'r%ds%ds%dt%dc%de%dc%dt%dm%d' % (
            self.reflection, self.shader, self.shadow, scale,
            self.textureCompression, self.special_effects,
            self.character_detail_level, self.terrain_detail_level, self.memory)
        base.gameOptionsCode = gameOptionsCode

    def compareNumbers(self, x1, y1, z1, w1, x2, y2, z2, w2):
        axis = 0
        delta = 0
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        dw = w1 - w2
        if dx == 0:
            if dy == 0:
                if dz == 0:
                    if dw == 0:
                        axis = 0
                        delta = 0
                    else:
                        axis = 4
                        delta = dw
                else:
                    axis = 3
                    delta = dz
            else:
                axis = 2
                delta = dy
        else:
            axis = 1
            delta = dx
        return [delta, axis, dx, dy, dz, dw]

    def compareDates(self, year1, month1, day1, year2, month2, day2):
        delta_days = 0.0
        state = self.compareNumbers(year1, month1, day1, 0, year2, month2, day2,
                                    0)
        if state[0] == 0:
            pass
        else:
            delta_days = state[2] * 365.25 + state[3] * 30.4375 + state[4]
        return delta_days


class KeyMappings(OptionSpace):

    notify = DirectNotifyGlobal.directNotify.newCategory('KeyMappings')

    def __init__(self):
        self.startWatcher()

    def startWatcher(self):
        self.notify.debug('Starting key watcher')
        base.buttonThrowers[0].node().setButtonDownEvent(
            'GameOptions-buttonWatcher')

    def destroy(self):
        self.notify.debug('Stopping key watcher')
        base.buttonThrowers[0].node().setButtonDownEvent('')


class GameOptions(BorderFrame):

    notify = DirectNotifyGlobal.directNotify.newCategory('GameOptions')
    debug = False
    resolution_table = [(800, 600), (1024, 768), (1280, 1024), (1600, 1200)]
    widescreen_resolution_table = [(1280, 720), (1920, 1080)]
    MinimumHorizontalResolution = 800
    MinimumVerticalResolution = 600

    def __init__(self,
                 title,
                 x,
                 y,
                 width,
                 height,
                 options=None,
                 file_path=None,
                 pipe=None,
                 chooser=0,
                 keyMappings=None):
        self.inAdFrame = False
        self.width = width
        self.height = height
        self.chooser = chooser
        self.enable_hdr = base.config.GetInt('want-game-options-hdr', 0)
        self.enable_ship_visibility = base.config.GetInt(
            'want-game-options-ship-visibility', 0)
        if file_path:
            self.file_path = file_path
        else:
            self.file_path = Options.DEFAULT_FILE_PATH
        if base.config.GetBool('want-test-gameoptions', 0):
            self.velvet = False
            base.gameoptions = self
        else:
            if base.hasEmbedded:
                self.velvet = embedded.isMainWindowVisible() or base.cr.isPaid(
                ) == OTPGlobals.AccessVelvetRope
            else:
                self.velvet = False
        if os.getenv(
                'GAME_SHOW_ADDS'
        ) == 'NO' or sys.platform == 'darwin' or sys.platform == 'linux2':
            self.velvet = False
        self.restartDialog = None
        self.savedDialog = None
        self.logoutDialog = None
        self.restore_options = None
        self.current_options = None
        self.restore_failed = False
        if options:
            self.options = options
        else:
            self.options = Options()
            if self.options.load(self.file_path):
                pass
            else:
                self.options = Options()
                self.options.config_to_options()
                self.options.recommendedOptions(base.pipe, True)
        if keyMappings:
            self.keyMappings = keyMappings
        else:
            self.keyMappings = KeyMappings()
        self.options.options_to_config()
        self.current_options = copy.copy(self.options)
        self.shader_support = False
        self.shader_model = GraphicsStateGuardian.SM00
        if base.win and base.win.getGsg():
            self.shader_model = base.win.getGsg().getShaderModel()
            if self.shader_model >= GraphicsStateGuardian.SM11:
                self.shader_support = True
        self.play = False
        try:
            if base.cr.gameFSM.getCurrentState().getName() == 'playGame':
                self.play = True
        except:
            pass
        self.freeLock = False
        BorderFrame.__init__(
            self,
            relief=None,
            state=DGG.NORMAL,
            frameColor=PiratesGuiGlobals.FrameColor,
            borderWidth=PiratesGuiGlobals.BorderWidth,
            pos=(x, 0.0, y),
            frameSize=(0, width, 0, height),
            sortOrder=20)
        self.initialiseoptions(GameOptions)
        if not base.config.GetBool('use-simple-gameoptions-gui', 0):
            BorderFrame.hide(self)
            self.gui = GameOptionsGui(self, title, x, y, width, height, options,
                                      file_path, pipe, chooser, keyMappings)
            return
        else:
            self.gui = None
        self.hide(False)
        self.setBin('gui-popup', -10)
        self.titleFrame = BorderFrame(
            parent=self,
            relief=None,
            frameSize=(0, width - 0.15, 0,
                       PiratesGuiGlobals.TextScaleLarge * 2.5),
            pos=(0.075, 0, height - 0.11 - PiratesGuiGlobals.TextScaleLarge))
        self.titleLabel = DirectLabel(
            parent=self.titleFrame,
            relief=None,
            text=title,
            text_align=TextNode.ALeft,
            text_scale=PiratesGuiGlobals.TextScaleLarge,
            text_pos=(0.03, 0.04),
            text_fg=PiratesGuiGlobals.TextFG1,
            text_shadow=PiratesGuiGlobals.TextShadow,
            text_font=PiratesGlobals.getInterfaceOutlineFont(),
            textMayChange=1)
        parent = self
        y_section_increment = 0.15
        y_section_increment2 = 0.12
        y_section_offset = 0.3
        x = 0.1
        y = 0.15
        if base.config.GetBool('want-custom-keys', 0):
            x_increment = 0.133
        else:
            x_increment = 0.15
        y_increment = 0.0
        text = PLocalizer.GameOptionDisplay
        button = GuiButton(parent=parent, command=self.display_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.display_button = button
        text = PLocalizer.GameOptionsGraphics
        button = GuiButton(parent=parent, command=self.graphics_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.graphics_button = button
        text = PLocalizer.GameOptionsGeometry
        button = GuiButton(parent=parent, command=self.geometry_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.geometry_button = button
        text = PLocalizer.GameOptionsAudio
        button = GuiButton(parent=parent, command=self.audio_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.audio_button = button
        text = PLocalizer.GameOptionsInterface
        button = GuiButton(parent=parent, command=self.controls_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.controls_button = button
        text = PLocalizer.GameOptionsImage
        button = GuiButton(parent=parent, command=self.gamma_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.gamma_button = button
        if base.config.GetBool('want-custom-keys', 0):
            text = PLocalizer.GameOptionsKeys
            button = GuiButton(parent=parent, command=self.keys_button_function)
            self.set_button_settings(button, x, y, text)
            x += x_increment
            y += y_increment
            self.keys_button = button
        label_x_offset = -0.07
        label_y_offset = -0.05
        increment1 = 0
        increment2 = 0
        self.display_page = DirectFrame(parent=self)
        parent = self.display_page
        start_x = 0.1
        x = start_x
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.15
        y_increment = 0.0
        text = PLocalizer.GameOptionsFullscreenOnOff
        self.fullscreen_label = self.create_label(
            x + label_x_offset, y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsFullscreen
        button = GuiButton(
            parent=parent, command=self.fullscreen_button_function2)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        if self.freeLock:
            button['command'] = self.showUpsell
            subCard = loader.loadModel('models/gui/toplevel_gui')
            appendMe = DirectFrame(
                parent=button,
                relief=None,
                pos=(-0.165, 0, -0.058),
                state=DGG.DISABLED,
                geom=subCard.find('**/subscribers_lock'),
                geom_scale=0.15,
                geom_pos=(0.06, 0, 0.06))
            appendMe.setAlphaScale(1.0, 2)
            subCard.removeNode()
        self.fullscreen_button2 = button
        increment1 += 1
        x = start_x
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.15
        y_increment = 0.0
        text = PLocalizer.GameOptionsWindowedResolutions
        self.windowed_resolutions_label = self.create_label(
            x + label_x_offset, y + label_y_offset, text, parent)
        by_text = 'x'
        buttons_per_row = 6
        maximum_rows = 3
        maximum_buttons = buttons_per_row * maximum_rows
        total_windowed_resolutions = len(base.windowed_resolution_table)
        if total_windowed_resolutions > maximum_buttons:
            base.windowed_resolution_table[0:(
                total_windowed_resolutions - maximum_buttons)] = []
        self.windowed_resolutions_button_array = []
        total_windowed_resolutions = len(base.windowed_resolution_table)
        if total_windowed_resolutions > 0:
            index = 0
            while index < total_windowed_resolutions:
                text = base.windowed_resolution_table[index][0].__repr__(
                ) + by_text + base.windowed_resolution_table[index][1].__repr__(
                )
                button = GuiButton(
                    parent=parent,
                    command=self.windowed_resolution_button_function)
                button['extraArgs'] = [button]
                button.identifier = index
                self.set_button_settings(button, x, y, text)
                x += x_increment
                y += y_increment
                if (index + 1) % buttons_per_row == 0:
                    next_row_y_increment = 0.0575
                    x = start_x
                    y += next_row_y_increment
                self.windowed_resolutions_button_array = self.windowed_resolutions_button_array + [
                    button
                ]
                index += 1

        increment1 += 2
        x = start_x
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset - 0.07
        x_increment = 0.15
        y_increment = 0.0
        text = PLocalizer.GameOptionsFullscreenResolutions
        self.fullscreen_resolutions_label = self.create_label(
            x + label_x_offset, y + label_y_offset, text, parent)
        total_fullscreen_resolutions = len(base.fullscreen_resolution_table)
        if total_fullscreen_resolutions > maximum_buttons:
            base.fullscreen_resolution_table[0:(
                total_fullscreen_resolutions - maximum_buttons)] = []
        self.fullscreen_resolutions_button_array = []
        total_fullscreen_resolutions = len(base.fullscreen_resolution_table)
        if total_fullscreen_resolutions > 0:
            index = 0
            while index < total_fullscreen_resolutions:
                text = base.fullscreen_resolution_table[index][0].__repr__(
                ) + by_text + base.fullscreen_resolution_table[index][1].__repr__(
                )
                button = GuiButton(
                    parent=parent,
                    command=self.fullscreen_resolution_button_function)
                button['extraArgs'] = [button]
                button.identifier = index
                self.set_button_settings(button, x, y, text)
                x += x_increment
                y += y_increment
                if (index + 1) % buttons_per_row == 0:
                    next_row_y_increment = 0.0575
                    x = start_x
                    y += next_row_y_increment
                self.fullscreen_resolutions_button_array = self.fullscreen_resolutions_button_array + [
                    button
                ]
                index += 1

        increment1 = 0
        increment2 = 0
        self.graphics_page = DirectFrame(parent=self)
        parent = self.graphics_page
        y_offset = 0.1
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        text = PLocalizer.GameOptionsReflections
        self.reflection_label = self.create_label(
            x + label_x_offset, y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsOff
        button = GuiButton(
            parent=parent, command=self.reflection_off_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.reflection_off_button = button
        text = PLocalizer.GameOptionsSkyOnly
        button = GuiButton(
            parent=parent, command=self.reflection_sky_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.reflection_sky_button = button
        text = PLocalizer.GameOptionsOn
        button = GuiButton(
            parent=parent, command=self.reflection_default_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.reflection_default_button = button
        text = PLocalizer.GameOptionsAll
        button = GuiButton(
            parent=parent, command=self.reflection_all_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.reflection_all_button = button
        if True:
            self.reflection_all_button.hide()
        increment2 += 1
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        self.shader_off_button = None
        self.shader_on_button = None
        if self.shader_support:
            text = PLocalizer.GameOptionsShaderLevel + ' ' + self.shader_model.__repr__(
            ) + ' *'
        else:
            text = PLocalizer.GameOptionsNoShader
        self.shader_label = self.create_label(x + label_x_offset,
                                              y + label_y_offset, text, parent)
        if self.shader_support:
            text = PLocalizer.GameOptionsOff
            button = GuiButton(
                parent=parent, command=self.shader_off_button_function)
            self.set_button_settings(button, x, y, text)
            x += x_increment
            y += y_increment
            self.shader_off_button = button
            text = PLocalizer.GameOptionsOn
            button = GuiButton(
                parent=parent, command=self.shader_on_button_function)
            self.set_button_settings(button, x, y, text)
            x += x_increment
            y += y_increment
            self.shader_on_button = button
        increment2 += 1
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        text = PLocalizer.GameOptionsShadows
        self.shadow_label = self.create_label(x + label_x_offset,
                                              y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsSimple
        button = GuiButton(
            parent=parent, command=self.simple_shadow_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.simple_shadow_button = button
        text = PLocalizer.GameOptionsRendered
        button = GuiButton(parent=parent, command=self.shadow_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.shadow_button = button
        increment2 += 1
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        text = PLocalizer.GameOptionsSpecialEffectsLevel
        self.special_effects_label = self.create_label(
            x + label_x_offset, y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsLow
        button = GuiButton(
            parent=parent, command=self.special_effects_low_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.special_effects_low_button = button
        text = PLocalizer.GameOptionsMedium
        button = GuiButton(
            parent=parent, command=self.special_effects_medium_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.special_effects_medium_button = button
        text = PLocalizer.GameOptionsHigh
        button = GuiButton(
            parent=parent, command=self.special_effects_high_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.special_effects_high_button = button
        increment2 += 1
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        text = PLocalizer.GameOptionsTextureDetailLevel
        self.texture_label = self.create_label(x + label_x_offset,
                                               y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsLow
        button = GuiButton(
            parent=parent, command=self.texture_low_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.texture_low_button = button
        text = PLocalizer.GameOptionsMedium
        button = GuiButton(
            parent=parent, command=self.texture_medium_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.texture_medium_button = button
        text = PLocalizer.GameOptionsHigh
        button = GuiButton(
            parent=parent, command=self.texture_high_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.texture_high_button = button
        self.texture_maximum_button = None
        if self.options.texture_scale_mode == False:
            text = PLocalizer.GameOptionsMaximum
            button = GuiButton(
                parent=parent, command=self.texture_maximum_button_function)
            self.set_button_settings(button, x, y, text)
            x += x_increment
            y += y_increment
            self.texture_maximum_button = button
        text = PLocalizer.GameOptionsCompressed
        button = GuiButton(
            parent=parent, command=self.texture_compression_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.texture_compression_button = button
        x = 0.1
        y = y_section_increment * 1 + y_section_increment2 * 4 + y_section_offset - 0.0
        text = PLocalizer.GameOptionsRestartRequired
        self.restart_label = self.create_label(x + label_x_offset,
                                               y + label_y_offset, text, parent,
                                               (0.7, 0.7, 0.7, 1))
        increment1 = 0
        increment2 = 0
        self.geometry_page = DirectFrame(parent=self)
        parent = self.geometry_page
        y_offset = 0.1
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        text = PLocalizer.GameOptionsCharacterDetailLevel
        self.texture_label = self.create_label(x + label_x_offset,
                                               y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsLow
        button = GuiButton(
            parent=parent, command=self.character_low_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.character_low_button = button
        text = PLocalizer.GameOptionsMedium
        button = GuiButton(
            parent=parent, command=self.character_medium_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.character_medium_button = button
        text = PLocalizer.GameOptionsHigh
        button = GuiButton(
            parent=parent, command=self.character_high_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.character_high_button = button
        increment2 += 1
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        text = PLocalizer.GameOptionsTerrainDetailLevel
        self.texture_label = self.create_label(x + label_x_offset,
                                               y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsLow
        button = GuiButton(
            parent=parent, command=self.terrain_low_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.terrain_low_button = button
        text = PLocalizer.GameOptionsMedium
        button = GuiButton(
            parent=parent, command=self.terrain_medium_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.terrain_medium_button = button
        text = PLocalizer.GameOptionsHigh
        button = GuiButton(
            parent=parent, command=self.terrain_high_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.terrain_high_button = button
        increment2 += 1
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        text = PLocalizer.GameOptionsMemory
        self.texture_label = self.create_label(x + label_x_offset,
                                               y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsAggressive
        button = GuiButton(
            parent=parent, command=self.aggressive_memory_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.aggressive_memory_button = button
        text = PLocalizer.GameOptionsDefault
        button = GuiButton(
            parent=parent, command=self.default_memory_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.default_memory_button = button
        increment2 += 1
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        if self.enable_ship_visibility:
            text = PLocalizer.GameOptionsShipVis
            self.texture_label = self.create_label(
                x + label_x_offset, y + label_y_offset, text, parent)
            text = PLocalizer.GameOptionsShipVisOff
            button = GuiButton(
                parent=parent, command=self.off_ship_vis_button_function)
            self.set_button_settings(button, x, y, text)
            x += x_increment
            y += y_increment
            self.off_ship_vis_button = button
            text = PLocalizer.GameOptionsShipVisLow
            button = GuiButton(
                parent=parent, command=self.low_ship_vis_button_function)
            self.set_button_settings(button, x, y, text)
            x += x_increment
            y += y_increment
            self.low_ship_vis_button = button
            text = PLocalizer.GameOptionsShipVisHigh
            button = GuiButton(
                parent=parent, command=self.high_ship_vis_button_function)
            self.set_button_settings(button, x, y, text)
            x += x_increment
            y += y_increment
            self.high_ship_vis_button = button
        increment2 += 1
        increment1 = 0
        increment2 = 0
        self.audio_page = DirectFrame(parent=self)
        parent = self.audio_page
        slider_y_offset = 0.1
        x = 0.1
        y = y_section_increment * 0 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        text = PLocalizer.GameOptionsSoundEffects
        self.sound_effects_label = self.create_label(
            x + label_x_offset, y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsOff
        button = GuiButton(
            parent=parent, command=self.sound_off_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.sound_off_button = button
        text = PLocalizer.GameOptionsOn
        button = GuiButton(parent=parent, command=self.sound_on_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.sound_on_button = button

        def sound_volume_update_function(value):
            self.options.sound_volume = value
            if base.sfxManagerList:
                index = 0
                length = len(base.sfxManagerList)
                while index < length:
                    sfx_manager = base.sfxManagerList[index]
                    sfx_manager.setVolume(value)
                    index += 1

        y += slider_y_offset
        text = PLocalizer.GameOptionsSoundEffectsVolume
        default_value = 0.5
        resolution = 0.01
        self.sound_volume_slider = self.create_slider(
            sound_volume_update_function, self.options.sound_volume, x, y,
            resolution, text, parent)
        x = 0.1
        y = y_section_increment * 2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        text = PLocalizer.GameOptionsMusic
        self.music_label = self.create_label(x + label_x_offset,
                                             y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsOff
        button = GuiButton(
            parent=parent, command=self.music_off_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.music_off_button = button
        text = PLocalizer.GameOptionsOn
        button = GuiButton(parent=parent, command=self.music_on_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.music_on_button = button

        def music_volume_update_function(value):
            self.options.music_volume = value
            if base.musicManager:
                base.musicManager.setVolume(value)

        y += slider_y_offset
        text = PLocalizer.GameOptionsMusicVolume
        default_value = 0.5
        resolution = 0.01
        self.music_volume_slider = self.create_slider(
            music_volume_update_function, self.options.music_volume, x, y,
            resolution, text, parent)
        increment1 = 0
        increment2 = 0
        self.controls_page = DirectFrame(parent=self)
        parent = self.controls_page
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        text = PLocalizer.GameOptionsInvertMouseLook
        self.invert_mouse_look_label = self.create_label(
            x + label_x_offset, y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsOff
        button = GuiButton(
            parent=parent, command=self.mouse_look_off_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.mouse_look_off_button = button
        text = PLocalizer.GameOptionsOn
        button = GuiButton(
            parent=parent, command=self.mouse_look_on_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.mouse_look_on_button = button
        increment2 += 1.5
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset

        def gui_scale_update_function(value):
            self.options.gui_scale = value
            try:
                gui_manager = localAvatar.guiMgr
            except:
                gui_manager = None
            else:
                if gui_manager:
                    gui_manager.setUIScale(value * 0.6 + 0.7)
            return

        text = PLocalizer.GameOptionsGUIScale
        self.gui_scale_label = self.create_label(
            x + label_x_offset, y + label_y_offset, text, parent)
        x += x_increment * 2
        text = PLocalizer.GameOptionsGUIScale
        resolution = 0.01
        self.gui_scale_slider = self.create_slider(gui_scale_update_function,
                                                   self.options.gui_scale, x, y,
                                                   resolution, text, parent)
        increment2 += 1.5
        if base.config.GetBool('want-cpu-frequency-warning', 0):
            x = 0.1
            y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
            text = PLocalizer.GameOptionsCpuFrequencyWarning
            self.cpu_frequency_warning_label = self.create_label(
                x + label_x_offset, y + label_y_offset, text, parent)
            text = PLocalizer.GameOptionsOff
            button = GuiButton(
                parent=parent,
                command=self.cpu_frequency_warning_off_button_function)
            self.set_button_settings(button, x, y, text)
            x += x_increment
            y += y_increment
            self.cpu_frequency_warning_off_button = button
            text = PLocalizer.GameOptionsOn
            button = GuiButton(
                parent=parent,
                command=self.cpu_frequency_warning_on_button_function)
            self.set_button_settings(button, x, y, text)
            x += x_increment
            y += y_increment
            self.cpu_frequency_warning_on_button = button
            increment2 += 1.5
        increment1 = 0
        increment2 = 0
        delta_y = 1.0
        self.gamma_page = DirectFrame(parent=self)
        parent = self.gamma_page
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
        x_increment = 0.2
        y_increment = 0.0
        text = PLocalizer.GameOptionsEnableGamma
        self.enable_gamma_label = self.create_label(
            x + label_x_offset, y + label_y_offset, text, parent)
        text = PLocalizer.GameOptionsOff
        button = GuiButton(
            parent=parent, command=self.gamma_off_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.gamma_off_button = button
        text = PLocalizer.GameOptionsOn
        button = GuiButton(parent=parent, command=self.gamma_on_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        self.gamma_on_button = button
        increment2 += delta_y
        x = 0.1
        y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset

        def gamma_update_function(value):
            self.options.gamma = value
            if base.win and base.win.getGsg():
                if self.options.gamma_enable:
                    base.win.getGsg().setGamma(
                        self.options.optionsGammaToGamma(self.options.gamma))

        text = PLocalizer.GameOptionsGamma
        self.gamma_label = self.create_label(x + label_x_offset,
                                             y + label_y_offset, text, parent)
        x += x_increment * 2
        text = ''
        resolution = 0.02
        self.gamma_slider = self.create_slider2(gamma_update_function,
                                                self.options.gamma, x, y,
                                                resolution, text, parent)
        increment2 += delta_y
        if self.enable_hdr:
            x = 0.1
            y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset
            text = PLocalizer.GameOptionsHdr
            self.hdr_label = self.create_label(x + label_x_offset,
                                               y + label_y_offset, text, parent)
            text = PLocalizer.GameOptionsOff
            button = GuiButton(
                parent=parent, command=self.hdr_off_button_function)
            self.set_button_settings(button, x, y, text)
            x += x_increment
            y += y_increment
            self.hdr_off_button = button
            helpPos = (0.35, 0.0, 0.0)
            helpText = PLocalizer.GameOptionsOnLowerFrameRate
            text = PLocalizer.GameOptionsOn
            button = GuiButton(
                parent=parent,
                command=self.hdr_on_button_function,
                helpText=helpText,
                helpPos=helpPos,
                canReposition=True)
            self.set_button_settings(button, x, y, text)
            button.resetHelpWatcher()
            x += x_increment
            y += y_increment
            self.hdr_on_button = button
            increment2 += delta_y
            x = 0.1
            y = y_section_increment * increment1 + y_section_increment2 * increment2 + y_section_offset

            def hdr_update_function(value):
                self.options.hdr_factor = value
                if base.hdr:
                    if self.options.hdr:
                        base.hdr.updateHdrFactor(value)

            text = PLocalizer.GameOptionsHdrIntensity
            self.hdr_factor_label = self.create_label(
                x + label_x_offset, y + label_y_offset, text, parent)
            x += x_increment * 2
            text = ''
            resolution = 0.02
            self.hdr_factor_slider = self.create_slider(
                hdr_update_function, self.options.hdr_factor, x, y, resolution,
                text, parent)
            increment2 += delta_y
        x = 0.1
        y = y_section_increment * 1 + y_section_increment2 * 4 + y_section_offset - 0.0
        text = PLocalizer.GameOptionsRestartRequired
        self.restart_label = self.create_label(x + label_x_offset,
                                               y + label_y_offset, text, parent,
                                               (0.7, 0.7, 0.7, 1))
        if base.config.GetBool('want-custom-keys', 0):
            increment1 = 0
            increment2 = 0
            self.keys_page = DirectFrame(parent=self)
            parent = self.keys_page
        parent = self
        x = 0.1
        y = 0.95
        x_increment = 0.15
        y_increment = 0.0
        text = PLocalizer.GameOptionsLogout
        button = GuiButton(parent=parent, command=self.logout_button_function)
        self.set_button_settings(button, x, y, text)
        if self.play == False:
            self.disableButton(button)
        x += x_increment
        y += y_increment
        x += x_increment
        y += y_increment
        text = PLocalizer.GameOptionsDefault
        button = GuiButton(parent=parent, command=self.default_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        text = PLocalizer.GameOptionsRestore
        button = GuiButton(parent=parent, command=self.restore_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        text = PLocalizer.GameOptionsSave
        button = GuiButton(parent=parent, command=self.save_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        text = PLocalizer.GameOptionsClose
        button = DialogButton(
            parent=parent,
            buttonStyle=DialogButton.YES,
            command=self.close_button_function)
        self.set_button_settings(button, x, y, text)
        x += x_increment
        y += y_increment
        from pirates.piratesgui import FeedbackPanel
        guiQMark = loader.loadModel('models/gui/toplevel_gui')
        questionMark = guiQMark.find('**/generic_question*')
        button = DirectButton(
            parent=parent,
            relief=0,
            pos=(1.345, 0, -0.2),
            scale=3.2,
            geom=questionMark,
            geom_scale=0.18,
            geom_pos=(0.06, 0, 0.087),
            text='',
            textMayChange=1,
            command=self.__loadFeedbackPanel)
        button.setColor(0.8, 0.7, 0.5, 1)
        self.selected_color = 1.0
        self.not_selected_color = 0.5
        self.display_identifier = -1
        self.set_options(False)
        self.display_button_function()
        self.accept('access-changed', self.initDisplayButtons)
        return

    def destroy(self):
        if self.gui:
            self.gui.destroy()
        else:
            self.ignoreAll()
        self.delete_dialogs()
        BorderFrame.destroy(self)

    def get_pipe(self):
        return base.pipe

    def set_button_settings(self, button, x, y, text):
        button_x = self.x_to_gui_coordinate(x)
        button_y = self.y_to_gui_coordinate(y)
        button.configure(
            text=text,
            text_fg=(1.0, 1.0, 1.0, 1.0),
            text_scale=PiratesGuiGlobals.TextScaleLarge,
            text_wordwrap=0)
        button.setPos(button_x, 0, button_y)
        button.resetFrameSize()

    def create_label(self, x, y, title, parent,
                     color=PiratesGuiGlobals.TextFG1):
        label_x = self.x_to_gui_coordinate(x)
        label_y = self.y_to_gui_coordinate(y)
        label = DirectLabel(
            parent=parent,
            relief=None,
            text=title,
            text_align=TextNode.ALeft,
            text_scale=PiratesGuiGlobals.TextScaleLarge,
            text_pos=(label_x, label_y),
            text_fg=color,
            text_shadow=PiratesGuiGlobals.TextShadow,
            text_font=PiratesGlobals.getInterfaceOutlineFont(),
            textMayChange=1)
        return label

    def create_slider(self, update_function, default_value, x, y, resolution,
                      label, parent):
        slider_x = self.x_to_gui_coordinate(x)
        slider_y = self.y_to_gui_coordinate(y)

        def update_slider(slider, update_function):
            string = slider.label + '  (%.0f)' % (slider['value'] * 100.0)
            slider['text'] = string
            update_function(slider['value'])

        charGui = loader.loadModel('models/gui/char_gui')
        slider = DirectSlider(
            parent=parent,
            relief=None,
            command=update_slider,
            image=charGui.find('**/chargui_slider_small'),
            image_scale=(2.15, 2.15, 1.5),
            thumb_relief=None,
            thumb_image=(charGui.find('**/chargui_slider_node'),
                         charGui.find('**/chargui_slider_node_down'),
                         charGui.find('**/chargui_slider_node_over')),
            pos=(slider_x, 0.0, slider_y),
            text_align=TextNode.ACenter,
            text_scale=(0.1, 0.1),
            text_pos=(0.0, 0.1),
            text_fg=PiratesGuiGlobals.TextFG1,
            scale=0.43,
            pageSize=resolution,
            text='default',
            value=default_value)
        charGui.removeNode()
        slider.label = label
        slider['extraArgs'] = [slider, update_function]
        return slider

    def create_slider2(self, update_function, default_value, x, y, resolution,
                       label, parent):
        slider_x = self.x_to_gui_coordinate(x)
        slider_y = self.y_to_gui_coordinate(y)

        def update_slider(slider, update_function):
            string = slider.label + '  (%.2f)' % (slider['value'] * 2.0 + 0.5)
            slider['text'] = string
            update_function(slider['value'])

        charGui = loader.loadModel('models/gui/char_gui')
        slider = DirectSlider(
            parent=parent,
            relief=None,
            command=update_slider,
            image=charGui.find('**/chargui_slider_small'),
            image_scale=(2.15, 2.15, 1.5),
            thumb_relief=None,
            thumb_image=(charGui.find('**/chargui_slider_node'),
                         charGui.find('**/chargui_slider_node_down'),
                         charGui.find('**/chargui_slider_node_over')),
            pos=(slider_x, 0.0, slider_y),
            text_align=TextNode.ACenter,
            text_scale=(0.1, 0.1),
            text_pos=(0.0, 0.1),
            text_fg=PiratesGuiGlobals.TextFG1,
            scale=0.43,
            pageSize=resolution,
            text='default',
            value=default_value)
        charGui.removeNode()
        slider.label = label
        slider['extraArgs'] = [slider, update_function]
        return slider

    def fade_button(self, button):
        if button:
            button.setAlphaScale(self.not_selected_color)
            button['text_fg'] = (1.0, 1.0, 1.0, 1.0)
            button['selected'] = False

    def highlight_button(self, button):
        if button:
            button.setAlphaScale(self.selected_color)
            button['text_fg'] = (0.2, 0.8, 0.6, 1.0)
            button['selected'] = True

    def inactive_highlight_button(self, button):
        if button:
            button.setAlphaScale(self.selected_color)
            button['text_fg'] = (0.1, 0.4, 0.3, 1.0)

    def inactive_button(self, button):
        if button:
            button.setAlphaScale(self.selected_color)
            button['text_fg'] = (0.2, 0.2, 0.2, 1.0)

    def show_display_interface(self):
        self.highlight_button(self.display_button)
        self.display_page.show()

    def hide_display_interface(self):
        self.fade_button(self.display_button)
        self.display_page.hide()

    def show_graphics_interface(self):
        self.highlight_button(self.graphics_button)
        self.graphics_page.show()

    def hide_graphics_interface(self):
        self.fade_button(self.graphics_button)
        self.graphics_page.hide()

    def show_geometry_interface(self):
        self.highlight_button(self.geometry_button)
        self.geometry_page.show()

    def hide_geometry_interface(self):
        self.fade_button(self.geometry_button)
        self.geometry_page.hide()

    def show_audio_interface(self):
        self.highlight_button(self.audio_button)
        self.audio_page.show()

    def hide_audio_interface(self):
        self.fade_button(self.audio_button)
        self.audio_page.hide()

    def show_controls_interface(self):
        self.highlight_button(self.controls_button)
        self.controls_page.show()

    def hide_controls_interface(self):
        self.fade_button(self.controls_button)
        self.controls_page.hide()

    def show_gamma_interface(self):
        self.highlight_button(self.gamma_button)
        self.gamma_page.show()

    def hide_gamma_interface(self):
        self.fade_button(self.gamma_button)
        self.gamma_page.hide()

    def show_keys_interface(self):
        self.highlight_button(self.keys_button)
        self.keys_page.show()

    def hide_keys_interface(self):
        self.fade_button(self.keys_button)
        self.keys_page.hide()

    def display_button_function(self):
        self.show_display_interface()
        self.hide_graphics_interface()
        self.hide_geometry_interface()
        self.hide_audio_interface()
        self.hide_controls_interface()
        self.hide_gamma_interface()
        if base.config.GetBool('want-custom-keys', 0):
            self.hide_keys_interface()

    def graphics_button_function(self):
        self.hide_display_interface()
        self.show_graphics_interface()
        self.hide_geometry_interface()
        self.hide_audio_interface()
        self.hide_controls_interface()
        self.hide_gamma_interface()
        if base.config.GetBool('want-custom-keys', 0):
            self.hide_keys_interface()

    def geometry_button_function(self):
        self.hide_display_interface()
        self.hide_graphics_interface()
        self.show_geometry_interface()
        self.hide_audio_interface()
        self.hide_controls_interface()
        self.hide_gamma_interface()
        if base.config.GetBool('want-custom-keys', 0):
            self.hide_keys_interface()

    def audio_button_function(self):
        self.hide_display_interface()
        self.hide_graphics_interface()
        self.hide_geometry_interface()
        self.show_audio_interface()
        self.hide_controls_interface()
        self.hide_gamma_interface()
        if base.config.GetBool('want-custom-keys', 0):
            self.hide_keys_interface()

    def controls_button_function(self):
        self.hide_display_interface()
        self.hide_graphics_interface()
        self.hide_geometry_interface()
        self.hide_audio_interface()
        self.show_controls_interface()
        self.hide_gamma_interface()
        if base.config.GetBool('want-custom-keys', 0):
            self.hide_keys_interface()

    def gamma_button_function(self):
        self.hide_display_interface()
        self.hide_graphics_interface()
        self.hide_geometry_interface()
        self.hide_audio_interface()
        self.hide_controls_interface()
        self.show_gamma_interface()
        if base.config.GetBool('want-custom-keys', 0):
            self.hide_keys_interface()

    def keys_button_function(self):
        self.hide_display_interface()
        self.hide_graphics_interface()
        self.hide_geometry_interface()
        self.hide_audio_interface()
        self.hide_controls_interface()
        self.hide_gamma_interface()
        self.show_keys_interface()

    def logout_dialog_command(self, value):
        self.delete_dialogs()
        if value == 1:
            try:
                if base.cr.tutorialObject and base.cr.tutorialObject.map:
                    base.cr.tutorialObject.map.handleCancel()
                else:
                    if base.cr.gameFSM.getCurrentState().getName(
                    ) == 'playGame':
                        base.cr.gameFSM.request('closeShard',
                                                ['waitForAvatarList'])
            except:
                pass

    def logout_button_function(self):
        if self.logoutDialog:
            self.logoutDialog.destroy()
        self.logoutDialog = PDialog.PDialog(
            text=PLocalizer.GameOptionsLogoutConfirm,
            style=OTPDialog.YesNo,
            giveMouse=False,
            command=self.logout_dialog_command)
        self.logoutDialog.setBin('gui-popup', -5)

    def default_button_function(self):
        self.options = Options()
        self.options.recommendedOptions(self.get_pipe(), True)
        self.set_options(True)

    def restore_button_function(self):
        if self.restore_options:
            self.options = copy.copy(self.restore_options)
            self.set_options(True)

    def delete_dialogs(self):
        if self.restartDialog:
            self.restartDialog.destroy()
            del self.restartDialog
            self.restartDialog = None
        if self.savedDialog:
            self.savedDialog.destroy()
            del self.savedDialog
            self.savedDialog = None
        if self.logoutDialog:
            self.logoutDialog.destroy()
            del self.logoutDialog
            self.logoutDialog = None
        return

    def display_restart_dialog(self):
        self.delete_dialogs()
        self.restartDialog = PDialog.PDialog(
            text=PLocalizer.GameOptionsApplicationRestartMessage,
            style=OTPDialog.Acknowledge,
            giveMouse=False,
            command=self.default_dialog_command)
        self.restartDialog.setBin('gui-popup', -5)

    def save_button_function(self):
        self.delete_dialogs()
        if self.options.save(self.file_path, Options.NEW_STATE):
            self.options.log('User Saved Options')
            self.savedDialog = PDialog.PDialog(
                text=PLocalizer.GameOptionsSaved,
                style=OTPDialog.Acknowledge,
                giveMouse=False,
                command=self.default_dialog_command)
        else:
            self.savedDialog = PDialog.PDialog(
                text=PLocalizer.GameOptionsFailedToSaveOptions,
                style=OTPDialog.Acknowledge,
                giveMouse=False,
                command=self.default_dialog_command)
        self.savedDialog.setBin('gui-popup', -5)

    def default_dialog_command(self, value):
        self.delete_dialogs()

    def showUpsell(self):
        if self.chooser:
            self.chooser.popupFeatureBrowser(0, 0)
        else:
            base.localAvatar.guiMgr.showNonPayer(quest='Game_Options', focus=0)
        self.hide()

    def close_button_function(self):
        self.hide()

    def x_to_gui_coordinate(self, x):
        return x * self.width

    def y_to_gui_coordinate(self, y):
        return self.height - y * self.height

    def resetDisplayProperties(self, pipe, properties):
        if base.win:
            currentProperties = WindowProperties(base.win.getProperties())
            gsg = base.win.getGsg()
        else:
            currentProperties = WindowProperties.getDefault()
            gsg = None
        newProperties = WindowProperties(currentProperties)
        newProperties.addProperties(properties)
        if base.pipe != pipe:
            self.apiChanged = 1
            gsg = None
        if gsg == None or currentProperties.getFullscreen(
        ) != newProperties.getFullscreen():
            if self.debug:
                print 'window properties', properties, 'gsg', gsg
            base.pipe = pipe
            if not base.openMainWindow(
                    props=properties, gsg=gsg, keepCamera=True):
                if self.debug:
                    print 'OPEN MAIN WINDOW FAILED'
                return 0
            if self.debug:
                print 'OPEN MAIN WINDOW PASSED'
            NametagGlobals.setCamera(base.cam)
            NametagGlobals.setMouseWatcher(base.mouseWatcherNode)
            base.graphicsEngine.openWindows()
            if base.win.isClosed():
                print 'Window did not open, removing.'
                base.closeWindow(base.win)
                return 0
        else:
            if self.debug:
                print 'Adjusting properties'
            base.win.requestProperties(properties)
            base.graphicsEngine.renderFrame()
        return 1

    def restore_display_properties(self):
        if self.resetDisplayProperties(self.current_pipe,
                                       self.current_properties):
            self.options = self.current_options
            self.set_options(False, True)
        else:
            if self.current_properties.getFullscreen():
                self.current_options.fullscreen = 0
                self.current_properties.setFullscreen(0)
                if self.resetDisplayProperties(self.current_pipe,
                                               self.current_properties):
                    self.options = self.current_options
                    self.set_options(False, True)
                    return
            base.panda3dRenderError()
            self.restore_failed = True

    def set_fullscreen_button2(self, enable):
        if self.velvet:
            self.inactive_button(self.fullscreen_button2)
        else:
            if enable:
                if self.options.fullscreen_runtime:
                    self.highlight_button(self.fullscreen_button2)
                else:
                    self.inactive_highlight_button(self.fullscreen_button2)
            else:
                self.fade_button(self.fullscreen_button2)

    def fullscreen_button_function2(self):
        if self.velvet:
            self.options.fullscreen = 0
        else:
            if self.options.fullscreen == 1:
                self.options.fullscreen = 0
                self.options.fullscreen_runtime = 0
                self.set_display(self.options, base.pipe,
                                 self.options.window_width,
                                 self.options.window_height)
            else:
                self.options.fullscreen = 1
                self.options.fullscreen_runtime = 1
                self.set_display(self.options, base.pipe,
                                 self.options.fullscreen_width,
                                 self.options.fullscreen_height)
        self.set_fullscreen_button2(self.options.fullscreen)
        self.set_options(False, False)

    def reflection_off_button_function(self):
        self.options.reflection = 0
        Water.all_reflections_off()
        self.highlight_button(self.reflection_off_button)
        self.fade_button(self.reflection_sky_button)
        self.fade_button(self.reflection_default_button)
        self.fade_button(self.reflection_all_button)
        self.update()

    def reflection_sky_button_function(self):
        self.options.reflection = 1
        Water.all_reflecttions_show_through_only()
        self.fade_button(self.reflection_off_button)
        self.highlight_button(self.reflection_sky_button)
        self.fade_button(self.reflection_default_button)
        self.fade_button(self.reflection_all_button)
        self.update()

    def reflection_default_button_function(self):
        self.options.reflection = 2
        Water.all_reflections_on()
        self.fade_button(self.reflection_off_button)
        self.fade_button(self.reflection_sky_button)
        self.highlight_button(self.reflection_default_button)
        self.fade_button(self.reflection_all_button)
        self.update()

    def reflection_all_button_function(self):
        self.options.reflection = 3
        Water.all_reflections_on()
        self.fade_button(self.reflection_off_button)
        self.fade_button(self.reflection_sky_button)
        self.fade_button(self.reflection_default_button)
        self.highlight_button(self.reflection_all_button)
        self.update()

    def shader_off_button_function(self):
        if self.options.shader != 0:
            self.display_restart_dialog()
        self.options.shader = 0
        self.fade_button(self.shader_on_button)
        self.highlight_button(self.shader_off_button)
        self.update()

    def shader_on_button_function(self):
        if self.options.shader != 1:
            self.display_restart_dialog()
        self.options.shader = 1
        self.fade_button(self.shader_off_button)
        self.highlight_button(self.shader_on_button)
        self.update()

    def simple_shadow_button_function(self):
        try:
            time_of_day_manager = base.cr.timeOfDayManager
        except:
            time_of_day_manager = None
        else:
            if time_of_day_manager:
                time_of_day_manager.disableAvatarShadows()

        self.options.shadow = 0
        self.highlight_button(self.simple_shadow_button)
        self.fade_button(self.shadow_button)
        self.update()
        return

    def shadow_button_function(self):
        try:
            time_of_day_manager = base.cr.timeOfDayManager
        except:
            time_of_day_manager = None
        else:
            if time_of_day_manager:
                time_of_day_manager.enableAvatarShadows()

        self.options.shadow = 1
        self.fade_button(self.simple_shadow_button)
        self.highlight_button(self.shadow_button)
        self.update()
        return

    def special_effects_low_button_function(self):
        self.highlight_button(self.special_effects_low_button)
        self.fade_button(self.special_effects_medium_button)
        self.fade_button(self.special_effects_high_button)
        self.options.special_effects = Options.SpecialEffectsLow
        self.options.setRuntimeSpecialEffects()

    def special_effects_medium_button_function(self):
        self.fade_button(self.special_effects_low_button)
        self.highlight_button(self.special_effects_medium_button)
        self.fade_button(self.special_effects_high_button)
        self.options.special_effects = Options.SpecialEffectsMedium
        self.options.setRuntimeSpecialEffects()

    def special_effects_high_button_function(self):
        self.fade_button(self.special_effects_low_button)
        self.fade_button(self.special_effects_medium_button)
        self.highlight_button(self.special_effects_high_button)
        self.options.special_effects = Options.SpecialEffectsHigh
        self.options.setRuntimeSpecialEffects()

    def texture_low_button_function(self):
        self.highlight_button(self.texture_low_button)
        self.fade_button(self.texture_medium_button)
        self.fade_button(self.texture_high_button)
        self.fade_button(self.texture_maximum_button)
        if self.options.texture_scale_mode:
            if self.options.texture_scale != Options.texture_scale_low:
                self.display_restart_dialog()
            self.options.texture_scale = Options.texture_scale_low
            self.setTextureScale()
        else:
            self.options.texture = Options.texture_low

    def texture_medium_button_function(self):
        self.fade_button(self.texture_low_button)
        self.highlight_button(self.texture_medium_button)
        self.fade_button(self.texture_high_button)
        self.fade_button(self.texture_maximum_button)
        if self.options.texture_scale_mode:
            if self.options.texture_scale != Options.texture_scale_medium:
                self.display_restart_dialog()
            self.options.texture_scale = Options.texture_scale_medium
            self.setTextureScale()
        else:
            self.options.texture = Options.texture_medium

    def texture_high_button_function(self):
        self.fade_button(self.texture_low_button)
        self.fade_button(self.texture_medium_button)
        self.highlight_button(self.texture_high_button)
        self.fade_button(self.texture_maximum_button)
        if self.options.texture_scale_mode:
            if self.options.texture_scale != Options.texture_scale_high:
                self.display_restart_dialog()
            self.options.texture_scale = Options.texture_scale_high
            self.setTextureScale()
        else:
            self.options.texture = Options.texture_high

    def texture_maximum_button_function(self):
        self.fade_button(self.texture_low_button)
        self.fade_button(self.texture_medium_button)
        self.fade_button(self.texture_high_button)
        self.highlight_button(self.texture_maximum_button)
        if self.options.texture_scale_mode:
            if self.options.texture_scale != Options.texture_scale_maximum:
                self.display_restart_dialog()
            self.options.texture_scale = Options.texture_scale_maximum
            self.setTextureScale()
        else:
            self.options.texture = Options.texture_scale_maximum

    def texture_compression_button_function(self):
        self.display_restart_dialog()
        if self.options.textureCompression:
            self.options.textureCompression = 0
        else:
            self.options.textureCompression = 1
        if self.options.textureCompression:
            self.highlight_button(self.texture_compression_button)
        else:
            self.fade_button(self.texture_compression_button)

    def texture_compression_button_display(self):
        if self.options.textureCompression:
            self.highlight_button(self.texture_compression_button)
        else:
            self.fade_button(self.texture_compression_button)

    def character_low_button_function(self):
        self.highlight_button(self.character_low_button)
        self.fade_button(self.character_medium_button)
        self.fade_button(self.character_high_button)
        level = Options.option_low
        self.options.setRuntimeAvatarDetailLevel(
            self.options.character_detail_level)
        self.options.character_detail_level = level
        self.options.setRuntimeAvatarDetailLevel(level)

    def character_medium_button_function(self):
        self.fade_button(self.character_low_button)
        self.highlight_button(self.character_medium_button)
        self.fade_button(self.character_high_button)
        level = Options.option_medium
        self.options.character_detail_level = level
        self.options.setRuntimeAvatarDetailLevel(level)

    def character_high_button_function(self):
        self.fade_button(self.character_low_button)
        self.fade_button(self.character_medium_button)
        self.highlight_button(self.character_high_button)
        level = Options.option_high
        self.options.character_detail_level = level
        self.options.setRuntimeAvatarDetailLevel(level)

    def terrain_low_button_function(self):
        self.highlight_button(self.terrain_low_button)
        self.fade_button(self.terrain_medium_button)
        self.fade_button(self.terrain_high_button)
        level = Options.option_low
        self.options.terrain_detail_level = level
        self.options.setRuntimeGridDetailLevel(level)

    def terrain_medium_button_function(self):
        self.fade_button(self.terrain_low_button)
        self.highlight_button(self.terrain_medium_button)
        self.fade_button(self.terrain_high_button)
        level = Options.option_medium
        self.options.terrain_detail_level = level
        self.options.setRuntimeGridDetailLevel(level)

    def terrain_high_button_function(self):
        self.fade_button(self.terrain_low_button)
        self.fade_button(self.terrain_medium_button)
        self.highlight_button(self.terrain_high_button)
        level = Options.option_high
        self.options.terrain_detail_level = level
        self.options.setRuntimeGridDetailLevel(level)

    def aggressive_memory_button_function(self):
        self.highlight_button(self.aggressive_memory_button)
        self.fade_button(self.default_memory_button)
        self.options.memory = 1
        self.setLowMemory()

    def default_memory_button_function(self):
        self.fade_button(self.aggressive_memory_button)
        self.highlight_button(self.default_memory_button)
        self.options.memory = 0
        self.setLowMemory()

    def setLowMemory(self):
        try:
            base.setLowMemory(self.options.memory)
        except:
            pass

    def off_ship_vis_button_function(self):
        self.highlight_button(self.off_ship_vis_button)
        self.fade_button(self.low_ship_vis_button)
        self.fade_button(self.high_ship_vis_button)
        self.options.ocean_visibility = 0
        if not base.overrideShipVisibility:
            base.shipsVisibleFromIsland = 0
            messenger.send('ship_vis_change', [0])

    def low_ship_vis_button_function(self):
        self.fade_button(self.off_ship_vis_button)
        self.highlight_button(self.low_ship_vis_button)
        self.fade_button(self.high_ship_vis_button)
        self.options.ocean_visibility = 1
        if not base.overrideShipVisibility:
            base.shipsVisibleFromIsland = 1
            messenger.send('ship_vis_change', [1])

    def high_ship_vis_button_function(self):
        self.fade_button(self.off_ship_vis_button)
        self.fade_button(self.low_ship_vis_button)
        self.highlight_button(self.high_ship_vis_button)
        self.options.ocean_visibility = 2
        if not base.overrideShipVisibility:
            base.shipsVisibleFromIsland = 2
            messenger.send('ship_vis_change', [2])

    def sound_off_button_function(self):
        self.options.sound = 0
        self.fade_button(self.sound_on_button)
        self.highlight_button(self.sound_off_button)
        base.enableSoundEffects(False)
        self.update()

    def sound_on_button_function(self):
        self.options.sound = 1
        self.highlight_button(self.sound_on_button)
        self.fade_button(self.sound_off_button)
        base.enableSoundEffects(True)
        self.update()

    def music_off_button_function(self):
        self.options.music = 0
        self.fade_button(self.music_on_button)
        self.highlight_button(self.music_off_button)
        base.enableMusic(False)
        self.update()

    def music_on_button_function(self):
        self.options.music = 1
        self.highlight_button(self.music_on_button)
        self.fade_button(self.music_off_button)
        base.enableMusic(True)
        self.update()

    def mouse_look_off_button_function(self):
        self.options.mouse_look = 0
        self.fade_button(self.mouse_look_on_button)
        self.highlight_button(self.mouse_look_off_button)
        self.update()

    def mouse_look_on_button_function(self):
        self.options.mouse_look = 1
        self.highlight_button(self.mouse_look_on_button)
        self.fade_button(self.mouse_look_off_button)
        self.update()

    def cpu_frequency_warning_off_button_function(self):
        self.options.cpu_frequency_warning = 0
        self.fade_button(self.cpu_frequency_warning_on_button)
        self.highlight_button(self.cpu_frequency_warning_off_button)
        self.update()

    def cpu_frequency_warning_on_button_function(self):
        self.options.cpu_frequency_warning = 1
        self.highlight_button(self.cpu_frequency_warning_on_button)
        self.fade_button(self.cpu_frequency_warning_off_button)
        self.update()

    def open_key_mappings_page(self):
        self.controlsFrame = BorderFrame(
            parent=self,
            relief=None,
            frameSize=(0, self.width - 0.15, 0,
                       PiratesGuiGlobals.TextScaleLarge * 2.5),
            pos=(0.08, 0,
                 self.height - 0.15 - PiratesGuiGlobals.TextScaleLarge * 2.5))
        return

    def gamma_off_button_function(self):
        self.options.gamma_enable = 0
        self.fade_button(self.gamma_on_button)
        self.highlight_button(self.gamma_off_button)
        if base.win and base.win.getGsg():
            base.win.getGsg().restoreGamma()
        self.update()

    def gamma_on_button_function(self):
        self.options.gamma_enable = 1
        self.highlight_button(self.gamma_on_button)
        self.fade_button(self.gamma_off_button)
        if base.win and base.win.getGsg():
            if self.options.gamma_enable:
                base.win.getGsg().setGamma(
                    self.options.optionsGammaToGamma(self.options.gamma))
        self.update()

    def hdr_off_button_function(self):
        if self.options.hdr != 0:
            self.display_restart_dialog()
        self.options.hdr = 0
        self.fade_button(self.hdr_on_button)
        self.highlight_button(self.hdr_off_button)
        self.update()

    def hdr_on_button_function(self):
        if self.options.hdr != 1:
            self.display_restart_dialog()
        self.options.hdr = 1
        self.highlight_button(self.hdr_on_button)
        self.fade_button(self.hdr_off_button)
        self.update()

    def delete(self):
        pass

    def set_options(self, change_display, restore=False):
        if self.gui:
            self.gui.set_options(change_display)
            return
        if change_display:
            self.set_display(self.options, base.pipe, self.options.getWidth(),
                             self.options.getHeight())
        self.set_fullscreen_button2(self.options.fullscreen)
        if base.inAdFrame:
            self.windowed_resolution_button_function(None, restore)
            self.fullscreen_resolution_button_function(None, restore)
        self.initDisplayButtons()
        if self.options.reflection == 0:
            self.reflection_off_button_function()
        if self.options.reflection == 1:
            self.reflection_sky_button_function()
        if self.options.reflection == 2:
            self.reflection_default_button_function()
        if self.options.reflection == 3:
            self.reflection_all_button_function()
        if self.options.shader:
            self.shader_on_button_function()
        else:
            self.shader_off_button_function()
        if self.options.shadow:
            self.shadow_button_function()
        else:
            self.simple_shadow_button_function()
        if self.options.special_effects == Options.SpecialEffectsLow:
            self.special_effects_low_button_function()
        if self.options.special_effects == Options.SpecialEffectsMedium:
            self.special_effects_medium_button_function()
        if self.options.special_effects == Options.SpecialEffectsHigh:
            self.special_effects_high_button_function()
        if self.options.texture_scale_mode:
            if self.options.texture_scale == Options.texture_scale_low:
                self.texture_low_button_function()
            if self.options.texture_scale == Options.texture_scale_medium:
                self.texture_medium_button_function()
            if self.options.texture_scale == Options.texture_scale_high:
                self.texture_high_button_function()
            if self.texture_maximum_button and self.options.texture_scale == Options.texture_scale_maximum:
                self.texture_maximum_button_function()
        else:
            if self.options.texture == Options.texture_low:
                self.texture_low_button_function()
            if self.options.texture == Options.texture_medium:
                self.texture_medium_button_function()
            if self.options.texture == Options.texture_high:
                self.texture_high_button_function()
            if self.options.texture == Options.texture_maximum or self.options.texture > Options.texture_high:
                self.texture_maximum_button_function()
        self.texture_compression_button_display()
        if self.options.character_detail_level == Options.option_low:
            self.character_low_button_function()
        if self.options.character_detail_level == Options.option_medium:
            self.character_medium_button_function()
        if self.options.character_detail_level == Options.option_high:
            self.character_high_button_function()
        if self.options.terrain_detail_level == Options.option_low:
            self.terrain_low_button_function()
        if self.options.terrain_detail_level == Options.option_medium:
            self.terrain_medium_button_function()
        if self.options.terrain_detail_level == Options.option_high:
            self.terrain_high_button_function()
        if self.options.memory == 1:
            self.aggressive_memory_button_function()
        if self.options.memory == 0:
            self.default_memory_button_function()
        if self.enable_ship_visibility:
            if self.options.ocean_visibility == 0:
                self.off_ship_vis_button_function()
            elif self.options.ocean_visibility == 1:
                self.low_ship_vis_button_function()
            elif self.options.ocean_visibility == 2:
                self.high_ship_vis_button_function()
        if self.options.sound:
            self.sound_on_button_function()
        else:
            self.sound_off_button_function()
        self.sound_volume_slider['value'] = self.options.sound_volume
        if self.options.music:
            self.music_on_button_function()
        else:
            self.music_off_button_function()
        self.music_volume_slider['value'] = self.options.music_volume
        if self.options.mouse_look == 1:
            self.mouse_look_on_button_function()
        else:
            self.mouse_look_off_button_function()
        self.gui_scale_slider['value'] = self.options.gui_scale
        if base.config.GetBool('want-cpu-frequency-warning', 0):
            if self.options.cpu_frequency_warning == 1:
                self.cpu_frequency_warning_on_button_function()
            else:
                self.cpu_frequency_warning_off_button_function()
        if self.options.gamma_enable == 1:
            self.gamma_on_button_function()
        else:
            self.gamma_off_button_function()
        self.gamma_slider['value'] = self.options.gamma
        if self.enable_hdr:
            if self.options.hdr == 1:
                self.hdr_on_button_function()
            else:
                self.hdr_off_button_function()
        self.update()
        return

    def update(self):
        self.options.options_to_config()

    def isHidden(self):
        if self.gui:
            return self.gui.isHidden()
        else:
            return NodePath.isHidden(self)

    def show(self):
        self.restore_options = copy.copy(self.options)
        if self.gui:
            self.gui.show()
        else:
            BorderFrame.show(self)
        messenger.send('GameOptionsShown')

    def hide(self, log=True):
        self.delete_dialogs()
        if self.gui:
            self.gui.hide()
        else:
            BorderFrame.hide(self)
        if log:
            self.options.log('User Closed Options')
        messenger.send('GameOptionsHidden')

    @classmethod
    def width_to_resolution_id(self, width):
        id = 1
        index = 0
        total_resolutions = len(base.resolution_table)
        while index < total_resolutions:
            if width == base.resolution_table[index][0]:
                id = index
                break
            index += 1

        return id

    def system_information_to_settings(self):
        debug = False
        pipe = base.pipe
        di = pipe.getDisplayInformation()
        if di.getDisplayState() == DisplayInformation.DSSuccess:
            total_display_modes = di.getTotalDisplayModes()
            if debug:
                print 'maximum window width', di.getMaximumWindowWidth()
                print 'maximum window height', di.getMaximumWindowHeight()
                print 'bits per pixel', di.getWindowBitsPerPixel()
                print 'total_display_modes', total_display_modes
            index = 0
            widscreen = 0
            while index < total_display_modes:
                if debug:
                    print 'W', di.getDisplayModeWidth(
                        index), 'H', di.getDisplayModeHeight(
                            index), 'BPP', di.getDisplayModeBitsPerPixel(
                                index), 'RR', di.getDisplayModeRefreshRate(
                                    index
                                ), 'FS', di.getDisplayModeFullscreenOnly(index)
                aspect_ratio = di.getDisplayModeHeight(
                    index) * 10000 / di.getDisplayModeWidth(index)
                if aspect_ratio == 7500:
                    pass
                else:
                    if aspect_ratio == 5625:
                        pass
                index += 1

            size = di.getVideoMemory()
            if size == 0:
                size = di.getTextureMemory()
            if debug:
                print 'shader_model', di.getShaderModel()
                print 'video_memory', di.getVideoMemory()
                print 'texture_memory', di.getTextureMemory()
            mb = 1024 * 1024
            if size <= 0:
                pass
            elif size <= 32 * mb:
                pass
            elif size <= 64 * mb:
                pass
            elif size <= 96 * mb:
                pass
            elif size <= 128 * mb:
                pass
            elif size <= 256 * mb:
                pass
            elif size <= 512 * mb:
                pass
            elif size <= 768 * mb:
                pass
            elif size <= 1024 * mb:
                pass
            elif size > 1024 * mb:
                pass
        if debug:
            print 'physical_memory', di.getPhysicalMemory()
            print 'available_physical_memory', di.getAvailablePhysicalMemory()

    def set_display(self, options, pipe, width, height):
        state = False
        if self.debug:
            print 'SET DISPLAY'
        if base.inAdFrame:
            if self.display_identifier >= 0:
                embedded.setWindowMode(self.display_identifier)
                m = embedded.getAtWindowModeDef(self.display_identifier)
                if m:
                    properties = WindowProperties()
                    properties.setSize(m['want_size_x'], m['want_size_y'])
                    properties.setOrigin(m['want_loc_x'], m['want_loc_y'])
                    properties.setFullscreen(0)
                    if base.win:
                        current_properties = base.win.getProperties()
                    else:
                        current_properties = WindowProperties.getDefault()
                    new_properties = WindowProperties(current_properties)
                    new_properties.addProperties(properties)
                    base.win.requestProperties(new_properties)
                    base.graphicsEngine.renderFrame()
            state = True
        else:
            fullscreen = options.fullscreen_runtime
            self.current_pipe = base.pipe
            self.current_properties = WindowProperties(base.win.getProperties())
            if self.debug:
                print 'CURRENT X SIZE', self.current_properties.getXSize()
                print 'CURRENT Y SIZE', self.current_properties.getYSize()
                print 'CURRENT FULLSCREEN', self.current_properties.getFullscreen(
                )
            if self.current_properties.getFullscreen(
            ) == fullscreen and self.current_properties.getXSize(
            ) == width and self.current_properties.getYSize() == height:
                if self.debug:
                    print 'NO DISPLAY CHANGE REQUIRED'
                state = True
            else:
                properties = WindowProperties()
                properties.setSize(width, height)
                properties.setFullscreen(fullscreen)
                if self.resetDisplayProperties(pipe, properties):
                    if self.debug:
                        print 'DISPLAY CHANGE SET'
                    properties = base.win.getProperties()
                    if self.debug:
                        print 'X SIZE', properties.getXSize()
                        print 'Y SIZE', properties.getYSize()
                        print 'FULLSCREEN', properties.getFullscreen()
                    if properties.getFullscreen(
                    ) == fullscreen and properties.getXSize(
                    ) == width and properties.getYSize() == height:
                        if self.debug:
                            print 'DISPLAY CHANGE VERIFIED'
                        state = True
                    else:
                        if self.debug:
                            print 'VERIFY DISPLAY CHANGE FAILED, RESTORING PREVIOUS DISPLAY'
                        self.restore_display_properties()
                else:
                    if self.debug:
                        print 'DISPLAY CHANGE FAILED'
                        print 'BEFORE RESTORE'
                    self.restore_display_properties()
                    if self.debug:
                        print 'AFTER RESTORE'
                base.graphicsEngine.renderFrame()
                base.graphicsEngine.renderFrame()
        if state:
            self.current_options = copy.copy(self.options)
        return state

    def setNonPaid(self):
        for button in self.windowed_resolutions_button_array[2:]:
            button.hide()

        for button in self.fullscreen_resolutions_button_array:
            button.hide()

    def setPaid(self):
        for button in self.windowed_resolutions_button_array[2:]:
            button.show()

        for button in self.fullscreen_resolutions_button_array:
            button.show()

    def initDisplayButtons(self):
        self.inAdFrame = base.inAdFrame
        if self.inAdFrame:
            self.setNonPaid()
            windowed_index = self.options.resolution
        else:
            windowed_index = self.resolutionToIndex(
                self.options.window_width, self.options.window_height, False)
            self.setPaid()
        fullscreen_index = self.resolutionToIndex(
            self.options.fullscreen_width, self.options.fullscreen_height,
            False)
        for i in xrange(len(self.windowed_resolutions_button_array)):
            if i == windowed_index:
                self.highlight_button(self.windowed_resolutions_button_array[i])
            else:
                self.fade_button(self.windowed_resolutions_button_array[i])

        for i in xrange(len(self.fullscreen_resolutions_button_array)):
            if base.inAdFrame:
                self.inactive_button(
                    self.fullscreen_resolutions_button_array[i])
            elif i == fullscreen_index:
                self.highlight_button(
                    self.fullscreen_resolutions_button_array[i])
            else:
                self.fade_button(self.fullscreen_resolutions_button_array[i])

    def windowed_resolution_button_function(self, button, restore=False):
        index = 0
        total_resolutions = len(self.windowed_resolutions_button_array)
        while index < total_resolutions:
            b = self.windowed_resolutions_button_array[index]
            self.fade_button(b)
            index += 1

        if button:
            if self.debug:
                print 'windowed_resolution_button_function', button.identifier
                print base.windowed_resolution_table[button.identifier]
            index = 0
            while index < total_resolutions:
                b = self.windowed_resolutions_button_array[index]
                if index == button.identifier:
                    if base.inAdFrame:
                        if index > 1:
                            index = 0
                        if self.options.fullscreen_runtime:
                            self.inactive_highlight_button(b)
                        else:
                            self.highlight_button(b)
                            self.display_identifier = button.identifier
                            if restore == False:
                                self.set_display(
                                    self.options, base.pipe,
                                    base.windowed_resolution_table[
                                        button.identifier][0],
                                    base.windowed_resolution_table[
                                        button.identifier][1])
                        if base.hasEmbedded:
                            self.options.resolution = index
                    else:
                        if self.options.fullscreen_runtime:
                            self.inactive_highlight_button(b)
                        else:
                            self.highlight_button(b)
                            if restore == False:
                                self.set_display(
                                    self.options, base.pipe,
                                    base.windowed_resolution_table[
                                        button.identifier][0],
                                    base.windowed_resolution_table[
                                        button.identifier][1])
                        self.options.window_width = base.windowed_resolution_table[
                            button.identifier][0]
                        self.options.window_height = base.windowed_resolution_table[
                            button.identifier][1]
                index += 1

        else:
            if base.inAdFrame:
                total_modes = embedded.getCountWindowModes()
                current_mode = embedded.getCurrentWindowModeDef()
                for button_index in range(total_modes):
                    m = embedded.getAtWindowModeDef(button_index)
                    if current_mode['want_size_x'] == m['want_size_x'] and current_mode['want_size_y'] == m['want_size_y']:
                        b = self.windowed_resolutions_button_array[button_index]
                        self.highlight_button(b)

    def fullscreen_resolution_button_function(self, button, restore=False):
        index = 0
        total_resolutions = len(self.fullscreen_resolutions_button_array)
        while index < total_resolutions:
            b = self.fullscreen_resolutions_button_array[index]
            if base.inAdFrame:
                self.inactive_button(b)
            else:
                self.fade_button(b)
            index += 1

        if base.inAdFrame:
            pass
        else:
            if button:
                if self.debug:
                    print 'fullscreen_resolution_button_function', button.identifier
                    print base.fullscreen_resolution_table[button.identifier]
                index = 0
                while index < total_resolutions:
                    b = self.fullscreen_resolutions_button_array[index]
                    if index == button.identifier:
                        if self.options.fullscreen_runtime:
                            self.highlight_button(b)
                            if restore == False:
                                self.set_display(
                                    self.options, base.pipe,
                                    base.fullscreen_resolution_table[
                                        button.identifier][0],
                                    base.fullscreen_resolution_table[
                                        button.identifier][1])
                        else:
                            self.inactive_highlight_button(b)
                        self.options.fullscreen_width = base.fullscreen_resolution_table[
                            button.identifier][0]
                        self.options.fullscreen_height = base.fullscreen_resolution_table[
                            button.identifier][1]
                    index += 1

    def resolutionToIndex(self, width, height, fullscreen):
        resolution_index = -1
        if fullscreen:
            resolution_table = base.fullscreen_resolution_table
        else:
            resolution_table = base.windowed_resolution_table
        if resolution_table:
            index = 0
            total_resolutions = len(resolution_table)
            while index < total_resolutions:
                if width == resolution_table[index][0] and height == resolution_table[index][1]:
                    resolution_index = index
                    break
                index += 1

        return resolution_index

    def disableButton(self, button):
        c = 0.5
        button['state'] = DGG.DISABLED
        button['text_fg'] = (c, c, c, 1.0)

    def setTextureScale(self):
        if False:
            config_variable = ConfigVariableDouble('texture-scale', 1.0)
            value = self.options.texture_scale
            if value <= 0.0:
                value = 1.0
            if value >= 1.0:
                value = 1.0
            config_variable.setValue(value)

    def updateShipVisibility(self):
        if self.enable_ship_visibility:
            if self.options.ocean_visibility == 0:
                self.off_ship_vis_button_function()
            elif self.options.ocean_visibility == 1:
                self.low_ship_vis_button_function()
            elif self.options.ocean_visibility == 2:
                self.high_ship_vis_button_function()

    def __loadFeedbackPanel(self):
        from pirates.piratesgui import FeedbackPanel
        self.close_button_function()
        FeedbackPanel.FeedbackPanel()


# okay decompiling .\pirates\piratesgui\GameOptions.pyc
