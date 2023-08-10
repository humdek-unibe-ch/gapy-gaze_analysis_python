#!/usr/bin/python3

from ctypes import *
import pathlib

class GapyFilterParameterGap(Structure):
    _fields_ = [
            ("max_gap_length", c_double),
            ("sample_period", c_double)
    ]

class GapyFilterParameterNoise(Structure):
    _fields_ = [
            ("type", c_uint),
            ("mid_idx", c_uint)
    ]

class GapyFilterParameterSaccade(Structure):
    _fields_ = [
            ("velocity_threshold", c_float)
    ]

class GapyFilterParameterFixation(Structure):
    _fields_ = [
            ("duration_threshold", c_double),
            ("dispersion_threshold", c_float)
    ]

class GapyFilterParameter(Structure):
    _fields_ = [
            ("is_heap", c_bool),
            ("gap", GapyFilterParameterGap),
            ("noise", GapyFilterParameterNoise),
            ("saccade", GapyFilterParameterSaccade),
            ("fixation", GapyFilterParameterFixation)
    ]

class GapySample(Structure):
    _fields_ = [
            ("is_heap", c_bool),
            ("point", c_float * 3),
            ("origin", c_float * 3),
            ("timestamp", c_double)
    ]

class GapyFixation(Structure):
    _fields_ = [
            ("is_heap", c_bool),
            ("point", c_float * 3),
            ("duration", c_double),
            ("timestamp", c_double)
    ]

class GapySaccade(Structure):
    _fields_ = [
            ("is_heap", c_bool),
            ("point_start", c_float * 3),
            ("point_dest", c_float * 3),
            ("duration", c_double),
            ("timestamp", c_double)
    ]

class GapyLib():
    def __init__(self):
        # load dynamic library
        libname = pathlib.Path().absolute() / "gac/build/lib/libgac.so"
        self.gac = CDLL(libname)

        # define function interfaces
        self.gac.gac_get_filter_parameter.restype = c_bool
        self.gac.gac_get_filter_parameter.argtypes = [c_void_p, POINTER(GapyFilterParameter)]
        self.gac.gac_get_filter_parameter_default.restype = c_bool
        self.gac.gac_get_filter_parameter_default.argtypes = [POINTER(GapyFilterParameter)]
        self.gac.gac_create.restype = c_void_p
        self.gac.gac_create.argtypes = [POINTER(GapyFilterParameter)]
        self.gac.gac_destroy.argtypes = [c_void_p]
        self.gac.gac_filter_fixation_create.restype = c_void_p
        self.gac.gac_filter_fixation_create.argtypes = [c_double, c_double]
        self.gac.gac_filter_fixation_destroy.argtypes = [c_void_p]
        self.gac.gac_filter_fixation.restype = c_bool
        self.gac.gac_filter_fixation.argtypes = [c_void_p, POINTER(GapySample), POINTER(GapyFixation)]
        self.gac.gac_filter_gap_create.restype = c_void_p
        self.gac.gac_filter_gap_create.argtypes = [c_double, c_double]
        self.gac.gac_filter_gap_destroy.argtypes = [c_void_p]
        self.gac.gac_filter_gap.restype = c_uint
        self.gac.gac_filter_gap.argtypes = [c_void_p, c_void_p, POINTER(GapySample)]
        self.gac.gac_filter_noise_create.restype = c_void_p
        self.gac.gac_filter_noise_create.argtypes = [c_uint, c_uint]
        self.gac.gac_filter_noise_destroy.argtypes = [c_void_p]
        self.gac.gac_filter_noise.restype = POINTER(GapySample)
        self.gac.gac_filter_noise.argtypes = [c_void_p, POINTER(GapySample)]
        self.gac.gac_filter_saccade_create.restype = c_void_p
        self.gac.gac_filter_saccade_create.argtypes = [c_float]
        self.gac.gac_filter_saccade_destroy.argtypes = [c_void_p]
        self.gac.gac_filter_saccade.restype = c_bool
        self.gac.gac_filter_saccade.argtypes = [c_void_p, POINTER(GapySample), POINTER(GapySaccade)]
        self.gac.gac_queue_clear.restype = c_bool
        self.gac.gac_queue_clear.argtypes = [c_void_p]
        self.gac.gac_queue_create.restype = c_void_p
        self.gac.gac_queue_create.argtypes = [c_uint]
        self.gac.gac_queue_destroy.argtypes = [c_void_p]
        self.gac.gac_queue_remove.argtypes = [c_void_p]
        self.gac.gac_sample_window_cleanup.restype = c_bool
        self.gac.gac_sample_window_cleanup.argtypes = [c_void_p]
        self.gac.gac_sample_window_fixation_filter.restype = c_bool
        self.gac.gac_sample_window_fixation_filter.argtypes = [c_void_p, POINTER(GapyFixation)]
        self.gac.gac_sample_window_saccade_filter.restype = c_bool
        self.gac.gac_sample_window_saccade_filter.argtypes = [c_void_p, POINTER(GapySaccade)]
        self.gac.gac_sample_window_update.argtypes = [c_void_p, c_float, c_float, c_float, c_float, c_float, c_float, c_double]

    def getFilterParameterDefault(self):
        params = GapyFilterParameter()
        if self.gac.gac_get_filter_parameter_default(byref(params)):
            return params
        else:
            return None

class Gapy():

    def __init__(self, lib, params=None):
        self.gac = lib.gac
        self.h = self.__create(params)

    def __del__(self):
        self.__destroy()

    def __create(self, params=None):
        if params is None:
            params = gapyGetFilterParameterDefault()
        return self.gac.gac_create(byref(params))

    def __destroy(self):
        self.gac.gac_destroy(self.h)

    def getFilterParameter(self):
        if self.gac.gac_get_filter_parameter(self.h, byref(params)):
            return params
        else:
            return None

    def cleanup(self):
        self.gac.gac_sample_window_cleanup(self.h)

    def fixationFilter(self):
        fixation = GapyFixation()
        if self.gac.gac_sample_window_fixation_filter(self.h, byref(fixation)):
            return fixation
        else:
            return None

    def saccadeFilter(self):
        saccade = GapySaccade()
        if self.gac.gac_sample_window_saccade_filter(self.h, byref(saccade)):
            return saccade
        else:
            return None

    def update(self, sample):
        self.gac.gac_sample_window_update(self.h,
                sample.origin[0], sample.origin[1], sample.origin[2],
                sample.point[0], sample.point[1], sample.point[2],
                sample.timestamp)

    def update(self, ox, oy, oz, px, py, pz, timestamp):
        self.gac.gac_sample_window_update(self.h, ox, oy, oz, px, py, pz, timestamp)

class GapyFilterFixation():

    def __init__(self, lib, dispersion_threshold, duration_threshold):
        self.gac = lib.gac
        self.f = self.__create(dispersion_threshold, duration_threshold)

    def __del__(self):
        self.__destroy()

    def __create(self, dispersion_threshold, duration_threshold):
        return self.gac.gac_filter_fixation_create(dispersion_threshold, duration_threshold)

    def __destroy(self):
        self.gac.gac_filter_fixation_destroy(self.f)

    def filter(self, sample):
        fixation = GapyFixation()
        if self.gac.gac_filter_fixation(self.f, sample, fixation):
            return fixation
        else:
            return None

class GapyFilterGap():

    def __init__(self, lib, max_gap_length, sample_period):
        self.gac = lib.gac
        self.f = self.__create(max_gap_length, sample_period)

    def __del__(self):
        self.__destroy()

    def __create(self, max_gap_length, sample_period):
        return self.gac.gac_filter_gap_create(max_gap_length, sample_period)

    def __destroy(self):
        self.gac.gac_filter_gap_destroy(self.f)

    def filter(self, samples, sample):
        return self.gac.gac_filter_gap(self.f, samples, sample)

class GapyFilterNoise():

    def __init__(self, lib, mid_idx):
        self.gac = lib.gac
        self.f = self.__create(mid_idx)

    def __del__(self):
        self.__destroy()

    def __create(self, mid_idx):
        return self.gac.gac_filter_noise_create(0, mid_idx)

    def __destroy(self):
        self.gac.gac_filter_noise_destroy(self.f)

    def filter(self, sample):
        return self.gac.gac_filter_noise(self.f, sample)

class GapyFilterSaccade():

    def __init__(self, lib, velocity_threshold):
        self.gac = lib.gac
        self.f = self.__create(velocity_threshold)

    def __del__(self):
        self.__destroy()

    def __create(self, velocity_threshold):
        return self.gac.gac_filter_saccade_create(velocity_threshold)

    def __destroy(self):
        self.gac.gac_filter_saccade_destroy(self.f)

    def filter(self, sample):
        saccade = GapySaccade()
        if self.gac.gac_filter_saccade(self.f, sample, saccade):
            return saccade
        else:
            return None

class GapyQueue():

    def __init__(self, lib, length):
        self.gac = lib.gac
        self.item_type = item_type
        self.q = self.__create(length)

    def __del__(self):
        self.__destroy()

    def __create(length):
        return self.gac.gac_queue_create(length)

    def __destroy(self):
        self.gac.gac_queue_destroy(self.q)

    def clear(self):
        return self.gac.gac_queue_clear(self.q)

    def remove(self):
        self.gac.gac_queue_remove(self.q)


if __name__ == "__main__":
    lib = GapyLib()
    params = lib.getFilterParameterDefault()
    print(params.gap.max_gap_length)

    params.gap.max_gap_length = 1
    h = Gapy(lib, params)
    params = h.getFilterParameter()
    print(params.gap.max_gap_length)
