import math
from typing import Dict, List, Tuple
from panda3d.core import LVecBase2f, LVecBase3f, LVecBase4f, LPoint2f, LPoint3f, NodePath, PerlinNoise3, ClockObject


class SeaPatchRoot:
    """
    Root class for managing sea patch properties, waves, and calculations.
    """

    # Enums
    class WaveTarget:
        WTZ = 0
        WTU = 1
        WTV = 2

    class WaveFunction:
        WFSin = 0
        WFNoise = 1
    
    @staticmethod
    def WTZ():
        return WaveTarget.WTZ

    @staticmethod
    def WTU():
        return WaveTarget.WTU

    @staticmethod
    def WTV():
        return WaveTarget.WTV

    @staticmethod
    def WFSin():
        return WaveFunction.WFSin
    
    def WFNoise():
        return WaveFunction.WFNoise

    def __init__(self):
        self.m_waves = []
        self.m_flat_wells = {}
        self.resetEnvironment()
        self.resetProperties()
        self.m_high_color = LVecBase4f(0.2, 0.4, 0.6, 1)
        self.m_low_color = LVecBase4f(0.2, 0.4, 0.6, 1)
        self.m_mid_color = LVecBase4f(0.2, 0.4, 0.6, 1)
        self.m_noise = PerlinNoise3()

    def resetEnvironment(self):
        self.m_anchor = NodePath()
        self.m_center = NodePath()
        self.setSeaLevel(0.0)
        self.enable()
        self.animateHeight(True)
        self.animateUv(True)

    def resetProperties(self):
        self.m_speed = LVecBase2f(0, 0)
        self.setRadius(100)
        self.setThreshold(80)
        self.m_uv_scale = LVecBase2f(36, 36)
        self.m_uv_speed = LVecBase2f(0, 0)
        self.m_uv_offset = LVecBase2f(0, 0)
        self.m_uv_scale_adjustment = LVecBase2f(0, 0)
        self.setNormalDamper(1.0)
        self.setHeightDamper(0.5)
        self.m_amplitude_scale = 0.0

    def assignEnvironmentFrom(self, other):
        self.setOverallSpeed(other.getOverallSpeed())
        self.setAnchor(other.getAnchor())
        self.setCenter(other.getCenter())
        self.setNormalDamper(other.getNormalDamper())
        self.setHeightDamper(other.getHeightDamper())
        self.setUvSpeed(other.getUvSpeed())
        self.setUvScale(other.getUvScale())
        self.setSeaLevel(other.getSeaLevel())
        self.animateHeight(other.getAnimateHeight())
        self.animateUv(other.getAnimateUv())
        self.setRadius(other.getRadius())
        self.setThreshold(other.getThreshold())

    def enable(self):
        self.m_enabled = True

    def disable(self):
        self.m_enabled = False

    def isEnabled(self):
        return self.m_enabled

    def setAnchor(self, anchor: NodePath):
        self.m_anchor = anchor

    def getAnchor(self):
        return self.m_anchor

    def setCenter(self, center: NodePath):
        self.m_center = center

    def getCenter(self):
        return self.m_center

    def setSeaLevel(self, seaLevel: float):
        self.m_sea_level = seaLevel

    def getSeaLevel(self):
        return self.m_sea_level

    def animateHeight(self, animateHeight: bool):
        self.m_animate_height = animateHeight

    def getAnimateHeight(self):
        return self.m_animate_height

    def animateUv(self, animateUv: bool):
        self.m_animate_uv = animateUv

    def getAnimateUv(self):
        return self.m_animate_uv

    def setOverallSpeed(self, speed: float):
        current_time = ClockObject.get_global_clock().get_frame_time()
        current_phase = self.m_speed[0] * current_time + self.m_speed[1]
        self.m_speed = LVecBase2f(speed, current_phase - current_time * speed)

    def getOverallSpeed(self):
        return self.m_speed[0]

    def setUvSpeed(self, uvSpeed: LVecBase2f):
        old_uv_speed = self.m_uv_speed
        current_time = ClockObject.get_global_clock().get_frame_time()
        time_based_offset = old_uv_speed * current_time
        accumulated_offset = time_based_offset + self.m_uv_offset
        self.m_uv_speed = uvSpeed
        self.m_uv_offset = old_uv_speed - self.m_uv_speed * accumulated_offset[0]

    def getUvSpeed(self):
        return self.m_uv_speed

    def setUvScale(self, uvScale: LVecBase2f):
        if self.m_center.is_empty() or self.m_anchor.is_empty():
            self.m_uv_scale = uvScale
            return

        scale_factor = self.m_center.get_scale(self.m_anchor)
        inverse_old_scale = LVecBase2f(scale_factor[0] / self.m_uv_scale[0], scale_factor[1] / self.m_uv_scale[1])
        current_time = ClockObject.get_global_clock().get_frame_time()
        time_scaled_factor = inverse_old_scale * current_time
        accumulated_offset = time_scaled_factor + self.m_uv_offset
        combined_factor = inverse_old_scale + accumulated_offset
        stored_factor = combined_factor
        self.m_uv_scale = uvScale
        inverse_new_scale = LVecBase2f(scale_factor[0] / self.m_uv_scale[0], scale_factor[1] / self.m_uv_scale[1])
        adjusted_factor = stored_factor - inverse_new_scale
        adjusted_offset = adjusted_factor
        time_adjusted = adjusted_offset * current_time
        final_adjusted = adjusted_offset - time_adjusted
        self.m_uv_scale_adjustment = final_adjusted

    def getUvScale(self):
        return self.m_uv_scale

    def getUvOffset(self):
        return self.m_uv_offset

    def setRadius(self, radius: float):
        self.m_radius = radius
        self.m_radius2 = radius * radius

    def getRadius(self):
        return self.m_radius

    def setThreshold(self, threshold: float):
        self.m_threshold = threshold
        self.m_threshold2 = threshold * threshold

    def getThreshold(self):
        return self.m_threshold

    def setLowColor(self, lowColor: LVecBase4f):
        self.m_low_color = lowColor
        self.m_mid_color = (self.m_high_color + self.m_low_color) / 2.0

    def getLowColor(self):
        return self.m_low_color

    def setHighColor(self, highColor: LVecBase4f):
        self.m_high_color = highColor
        self.m_mid_color = (self.m_high_color + self.m_low_color) / 2.0

    def getHighColor(self):
        return self.m_high_color

    def getMidColor(self):
        return self.m_mid_color

    def getNumWaves(self):
        return len(self.m_waves)

    def clearWaves(self):
        self.m_waves = []

    def allocateWave(self, index: int):
        while len(self.m_waves) <= index:
            wave = {
                'm_enabled': False,
                'm_target': self.WaveTarget.WTZ,
                'm_function': self.WaveFunction.WFSin,
                'm_choppy_k': 1,
                'm_direction': LVecBase2f(0, 0),
                'm_direction_transformed': LVecBase2f(0, 0),
                'm_speed': LVecBase2f(0, 0),
                'm_amplitude': 1,
                'm_length': 0
            }
            self.m_waves.append(wave)

    def removeWave(self, index: int):
        if 0 <= index < len(self.m_waves):
            del self.m_waves[index]
        self.computeAmplitudeScale()

    def enableWave(self, index: int):
        self.allocateWave(index)
        self.m_waves[index]['m_enabled'] = True
        self.computeAmplitudeScale()

    def disableWave(self, index: int):
        self.allocateWave(index)
        self.m_waves[index]['m_enabled'] = False
        self.computeAmplitudeScale()

    def isWaveEnabled(self, index: int):
        self.allocateWave(index)
        return self.m_waves[index]['m_enabled']

    def setWaveTarget(self, index: int, target):
        self.allocateWave(index)
        self.m_waves[index]['m_target'] = target

    def getWaveTarget(self, index: int):
        return self.m_waves[index]['m_target']

    def setWaveFunc(self, index: int, function):
        self.allocateWave(index)
        self.m_waves[index]['m_function'] = function

    def getWaveFunction(self, index: int):
        return self.m_waves[index]['m_function']

    def setChoppyK(self, index: int, choppyK: int):
        self.allocateWave(index)
        self.m_waves[index]['m_choppy_k'] = choppyK

    def getChoppyK(self, index: int):
        return self.m_waves[index]['m_choppy_k']

    def setWaveLength(self, index: int, length: float):
        self.allocateWave(index)
        wave = self.m_waves[index]
        wave['m_length'] = length
        wave['m_direction_transformed'] = wave['m_direction'] * 2 * math.pi / wave['m_length']

    def getWaveLength(self, index: int):
        return self.m_waves[index]['m_length']

    def setWaveDirection(self, index: int, direction: LVecBase2f):
        self.allocateWave(index)
        wave = self.m_waves[index]
        wave['m_direction'] = direction
        wave['m_direction_transformed'] = wave['m_direction'] * 2 * math.pi / wave['m_length']

    def getWaveDirection(self, index: int):
        return self.m_waves[index]['m_direction']

    def setWaveSpeed(self, index: int, speed: float):
        self.allocateWave(index)
        wave = self.m_waves[index]
        root_time = self.getRootT()
        current_phase = wave['m_speed'][0] * root_time + wave['m_speed'][1]
        wave['m_speed'] = LVecBase2f(speed, current_phase - root_time * speed)

    def getWaveSpeed(self, index: int):
        return self.m_waves[index]['m_speed'][0]

    def setWaveAmplitude(self, index: int, amplitude: float):
        self.allocateWave(index)
        self.m_waves[index]['m_amplitude'] = amplitude
        self.computeAmplitudeScale()

    def getWaveAmplitude(self, index: int):
        return self.m_waves[index]['m_amplitude']

    def setNormalDamper(self, normalDamper: float):
        self.m_normal_damper = normalDamper

    def getNormalDamper(self):
        return self.m_normal_damper

    def setHeightDamper(self, heightDamper: float):
        self.m_height_damper = heightDamper

    def getHeightDamper(self):
        return self.m_height_damper

    def computeAmplitudeScale(self):
        total_amplitude = 0
        for wave in self.m_waves:
            if wave['m_enabled']:
                total_amplitude += wave['m_amplitude']
        if total_amplitude:
            self.m_amplitude_scale = 1.0 / (2 * total_amplitude)
        else:
            self.m_amplitude_scale = 0.0

    def getRootT(self):
        t = ClockObject.get_global_clock().get_frame_time()
        return self.m_speed[0] * t + self.m_speed[1]

    def addFlatWell(self, name: str, nodePath: NodePath, x: float, y: float, a6: float, a7: float):
        well_data = {}
        center_point = LPoint3f(x, y, 0)
        well_data['p'] = self.m_anchor.get_relative_point(nodePath, center_point)
        scale_x = self.m_anchor.get_sx(nodePath)
        outer_radius = max(0.0, a7)
        inner_radius = max(0.0, a6)
        scaled_inner = inner_radius * scale_x
        scaled_outer = scale_x * outer_radius
        outer_squared = scaled_outer * scaled_outer
        well_data['a'] = scaled_inner * scaled_inner
        well_data['b'] = outer_squared
        well_data['c'] = outer_squared - well_data['a']
        self.m_flat_wells[name] = well_data

    def removeFlatWell(self, name: str):
        if name in self.m_flat_wells:
            del self.m_flat_wells[name]

    def calcFlatWellScale(self, x: float, y: float):
        scale = 1.0
        for well in self.m_flat_wells.values():
            diff_vector = LVecBase2f(y - well['p'][1], x - well['p'][0])
            distance_squared = diff_vector.length_squared()
            if well['b'] < distance_squared:
                continue
            if well['a'] > distance_squared:
                return 0
            interpolation_ratio = (distance_squared - well['a']) / well['c']
            scale = min(scale, interpolation_ratio)
        return scale

    def calcHeight(self, x: float, y: float, dist2: float):
        result = self.getSeaLevel()
        well_scale = self.calcFlatWellScale(x, y)
        if self.m_animate_height and self.m_radius2 > dist2 and well_scale:
            root_time = self.getRootT()
            height_offset = 0.0
            for wave in self.m_waves:
                if not (wave['m_enabled'] and wave['m_target'] == self.WaveTarget.WTZ):
                    continue
                if wave['m_function'] == self.WaveFunction.WFNoise:
                    noise_position = LVecBase3f(x / wave['m_length'], y / wave['m_length'],
                                               wave['m_speed'][0] * root_time + wave['m_speed'][1])
                    wave_value = self.m_noise.noise(noise_position)
                else:
                    direction_dot = (wave['m_direction_transformed'][0] * x +
                                   wave['m_direction_transformed'][1] * y)
                    phase = wave['m_speed'][0] * root_time + wave['m_speed'][1]
                    wave_value = math.sin(direction_dot + phase) * 0.5 + 0.5
                if wave['m_choppy_k'] > 1:
                    wave_value = pow(wave_value, wave['m_choppy_k'])
                height_offset += (wave_value - 0.5) * wave['m_amplitude']
            if self.m_threshold2 < dist2:
                distance = math.sqrt(dist2 + 0.001)
                threshold_diff = distance - self.m_threshold
                height_offset -= threshold_diff * height_offset / (self.m_radius - self.m_threshold)
            result += height_offset * well_scale
        return result

    def calcFilteredHeight(self, x: float, y: float, min_length: float, dist2: float):
        result = self.getSeaLevel()
        well_scale = self.calcFlatWellScale(x, y)
        if self.m_animate_height and self.m_radius2 > dist2 and well_scale:
            root_time = self.getRootT()
            height_offset = 0.0
            for wave in self.m_waves:
                if not (wave['m_enabled'] and wave['m_target'] == self.WaveTarget.WTZ and
                        wave['m_function'] == self.WaveFunction.WFSin and
                        wave['m_length'] > min_length):
                    continue
                direction_dot = (wave['m_direction_transformed'][0] * x +
                               wave['m_direction_transformed'][1] * y)
                phase = wave['m_speed'][0] * root_time + wave['m_speed'][1]
                wave_value = math.sin(direction_dot + phase) * 0.5 + 0.5
                if wave['m_choppy_k'] > 1:
                    wave_value = pow(wave_value, wave['m_choppy_k'])
                height_offset += (wave_value - 0.5) * wave['m_amplitude']
            if self.m_threshold2 < dist2:
                distance = math.sqrt(dist2 + 0.001)
                threshold_diff = distance - self.m_threshold
                height_offset -= threshold_diff * height_offset / (self.m_radius - self.m_threshold)
            result += height_offset * well_scale
        return result

    def calcHeightForMass(self, x: float, y: float, dist2: float, mass: float, area: float):
        return self.calcHeight(x, y, dist2) * self.m_height_damper - (mass / area)

    def calc_normal(self, height: float, x: float, y: float, dist2: float):
        offset_y1 = y + 0.2
        offset_x1 = x - 0.3
        offset_y2 = y - 0.1
        offset_x2 = x - 0.3
        height1 = self.calc_height(offset_x1, offset_y1, dist2)
        height2 = self.calc_height(offset_x2, offset_y2, dist2)
        point1 = LVecBase3f(offset_x1, offset_y1, height1)
        point2 = LVecBase3f(offset_x2, offset_y2, height2)
        center_point = LVecBase3f(x, y, height)
        vec1 = point1 - center_point
        vec2 = point2 - center_point
        normal = vec1.cross(vec2)
        normal.normalize()
        return normal

    def calcNormalForMass(self, height: float, x: float, y: float, dist2: float, mass: float, area: float):
        offset_y1 = y + 0.2
        offset_x1 = x - 0.3
        offset_y2 = y - 0.1
        offset_x2 = x - 0.3
        height1 = self.calcHeightForMass(offset_x1, offset_y1, dist2, mass, area)
        height2 = self.calcHeightForMass(offset_x2, offset_y2, dist2, mass, area)
        adjusted_height1 = height1 - (height1 - height) * self.m_normal_damper
        adjusted_height2 = height2 - (height2 - height) * self.m_normal_damper
        point1 = LVecBase3f(offset_x1, offset_y1, adjusted_height1)
        point2 = LVecBase3f(offset_x2, offset_y2, adjusted_height2)
        center_point = LVecBase3f(x, y, height)
        vec1 = point1 - center_point
        vec2 = point2 - center_point
        normal = vec2.cross(vec1)
        normal.normalize()
        return normal

    def calcUv(self, x: float, y: float, dist2: float):
        base_uv = LPoint2f(x / self.m_uv_scale[0], y / self.m_uv_scale[1])
        result = base_uv + self.getUvOffset()
        if self.m_animate_uv and self.m_radius2 > dist2:
            root_time = self.getRootT()
            for wave in self.m_waves:
                if wave['m_enabled'] and (wave['m_target'] == self.WaveTarget.WTU or
                                          wave['m_target'] == self.WaveTarget.WTV):
                    if wave['m_function'] == self.WaveFunction.WFNoise:
                        noise_position = LPoint3f(x / wave['m_length'], y / wave['m_length'],
                                                 wave['m_speed'][0] * root_time + wave['m_speed'][1])
                        wave_value = self.m_noise.noise(noise_position)
                    else:
                        direction_dot = (wave['m_direction_transformed'][0] * x +
                                       wave['m_direction_transformed'][1] * y)
                        phase = wave['m_speed'][0] * root_time + wave['m_speed'][1]
                        wave_value = math.sin(direction_dot + phase) * 0.5 + 0.5
                    displacement = wave['m_amplitude'] * wave_value
                    if wave['m_target'] == self.WaveTarget.WTU:
                        result[0] += displacement
                    else:
                        result[1] += displacement
        return result

    def calcColor(self, height: float, x: float, y: float):
        normalized_height = (height - self.m_sea_level) * self.m_amplitude_scale + 0.5
        if normalized_height <= 0.0:
            normalized_height = 0.0
        elif normalized_height >= 1.0:
            normalized_height = 1.0
        return self.m_low_color + (self.m_high_color - self.m_low_color) * (1.0 - normalized_height)