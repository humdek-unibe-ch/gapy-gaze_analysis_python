#!/usr/bin/python3

from ctypes import *
import pathlib

libname = pathlib.Path().absolute() / "gac/build/lib/libgac.so"
gac = CDLL(libname)

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

gac.gac_get_filter_parameter.restype = c_bool
gac.gac_get_filter_parameter.argtypes = [c_void_p, POINTER(GapyFilterParameter)]
def gapyGetFilterParameter(h):
    if gac.gac_get_filter_parameter(h, byref(params)):
        return params
    else:
        return None

gac.gac_get_filter_parameter_default.restype = c_bool
gac.gac_get_filter_parameter_default.argtypes = [POINTER(GapyFilterParameter)]
def gapyGetFilterParameterDefault():
    params = GapyFilterParameter()
    if gac.gac_get_filter_parameter_default(byref(params)):
        return params
    else:
        return None

gac.gac_create.restype = c_void_p
gac.gac_create.argtypes = [POINTER(GapyFilterParameter)]
def gapyCreate(params=None):
    if params is None:
        params = gapyGetFilterParameterDefault()
    return gac.gac_create(byref(params))

gac.gac_destroy.argtypes = [c_void_p]
def gapyDestroy(h):
    gac.gac_destroy(h)

gac.gac_filter_fixation_create.restype = c_void_p
gac.gac_filter_fixation_create.argtypes = [c_double, c_double]
def gapyFilterFixationCreate(dispersion_threshold, duration_threshold):
    return gac.gac_filter_fixation_create(dispersion_threshold, duration_threshold)

gac.gac_filter_fixation_destroy.argtypes = [c_void_p]
def gapyFilterFixationDestroy(f):
    gac.gac_filter_fixation_destroy(f)

gac.gac_filter_fixation.restype = c_bool
gac.gac_filter_fixation.argtypes = [c_void_p, POINTER(GapySample), POINTER(GapyFixation)]
def gapyFilterFixation(f, sample):
    fixation = GapyFixation()
    if gac.gac_filter_fixation(f, sample, fixation):
        return fixation
    else:
        return None

gac.gac_filter_gap_create.restype = c_void_p
gac.gac_filter_gap_create.argtypes = [c_double, c_double]
def gapyFilterGapCreate(max_gap_length, sample_period):
    return gac.gac_filter_gap_create(max_gap_length, sample_period)

gac.gac_filter_gap_destroy.argtypes = [c_void_p]
def gapyFilterGapDestroy(f):
    gac.gac_filter_gap_destroy(f)

gac.gac_filter_gap.restype = c_uint
gac.gac_filter_gap.argtypes = [c_void_p, c_void_p, POINTER(GapySample)]
def gapyFilterGap(f, samples, sample):
    return gac.gac_filter_gap(f, samples, sample)

gac.gac_filter_noise_create.restype = c_void_p
gac.gac_filter_noise_create.argtypes = [c_uint, c_uint]
def gapyFilterNoiseCreate(mid_idx):
    return gac.gac_filter_noise_create(0, mid_idx)

gac.gac_filter_noise_destroy.argtypes = [c_void_p]
def gapyFilterNoiseDestroy(f):
    gac.gac_filter_noise_destroy(f)

gac.gac_filter_noise.restype = POINTER(GapySample)
gac.gac_filter_noise.argtypes = [c_void_p, POINTER(GapySample)]
def gapyFilterNoise(f, sample):
    return gac.gac_filter_noise(f, sample)

gac.gac_filter_saccade_create.restype = c_void_p
gac.gac_filter_saccade_create.argtypes = [c_float]
def gapyFilterSaccadeCreate(velocity_threshold):
    return gac.gac_filter_saccade_create(velocity_threshold)

gac.gac_filter_saccade_destroy.argtypes = [c_void_p]
def gapyFilterSaccadeDestroy(f):
    gac.gac_filter_saccade_destroy(f)

gac.gac_filter_saccade.restype = c_bool
gac.gac_filter_saccade.argtypes = [c_void_p, POINTER(GapySample), POINTER(GapySaccade)]
def gapyFilterSaccade(f, sample):
    saccade = GapySaccade()
    if gac.gac_filter_saccade(f, sample, saccade):
        return saccade
    else:
        return None

gac.gac_queue_clear.restype = c_bool
gac.gac_queue_clear.argtypes = [c_void_p]
def gapyQueueClear(q):
    return gac.gac_queue_clear(q)

gac.gac_queue_create.restype = c_void_p
gac.gac_queue_create.argtypes = [c_uint]
def gapyQueueCreate(length):
    return gac.gac_queue_create(length)

gac.gac_queue_destroy.argtypes = [c_void_p]
def gapyQueueDestroy(q):
    gac.gac_queue_destroy(q)

gac.gac_queue_remove.argtypes = [c_void_p]
def gapyQueueRemove(q):
    gac.gac_queue_remove(q)

gac.gac_sample_window_cleanup.restype = c_bool
gac.gac_sample_window_cleanup.argtypes = [c_void_p]
def gac_sample_window_cleanup(h):
    gac.gac_sample_window_cleanup(h)

gac.gac_sample_window_fixation_filter.restype = c_bool
gac.gac_sample_window_fixation_filter.argtypes = [c_void_p, POINTER(GapyFixation)]
def gac_sample_window_fixation_filter(h):
    fixation = GapyFixation()
    if gac.gac_sample_window_fixation_filter(h, byref(fixation)):
        return fixation
    else:
        return None

gac.gac_sample_window_saccade_filter.restype = c_bool
gac.gac_sample_window_saccade_filter.argtypes = [c_void_p, POINTER(GapySaccade)]
def gac_sample_window_saccade_filter(h):
    saccade = GapySaccade()
    if gac.gac_sample_window_saccade_filter(h, byref(saccade)):
        return saccade
    else:
        return None

gac.gac_sample_window_update.argtypes = [c_void_p, c_float, c_float, c_float, c_float, c_float, c_float, c_double]
def gac_sample_window_update(h, ox, oy, oz, px, py, pz, timestamp):
    gac.gac_sample_window_update(h, ox, oy, oz, px, py, pz, timestamp)


if __name__ == "__main__":
    params = gapyGetFilterParameterDefault()
    params.gap.max_gap_length = 1
    h = gapyCreate(params)
    params = gapyGetFilterParameter(h)
    gapyDestroy(h)
