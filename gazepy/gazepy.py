"""
Python bindings for the C library libgac.
"""

from ctypes import *
import platform
import os

class GazepyFilterParameterGap(Structure):
    """
    The paramters to configure the gap filter.
    """
    _fields_ = [
            ("max_gap_length", c_double),
            ("sample_period", c_double)
    ]

class GazepyFilterParameterNoise(Structure):
    """
    The paramters to configure the noise filter.
    """
    _fields_ = [
            ("type", c_uint),
            ("mid_idx", c_uint)
    ]

class GazepyFilterParameterSaccade(Structure):
    """
    The paramters to configure the saccade filter.
    """
    _fields_ = [
            ("velocity_threshold", c_float)
    ]

class GazepyFilterParameterFixation(Structure):
    """
    The paramters to configure the fixation filter.
    """
    _fields_ = [
            ("duration_threshold", c_double),
            ("dispersion_threshold", c_float)
    ]

class GazepyFilterParameter(Structure):
    """
    The filter parameter structure holding all parameters used to configure the
    filters.
    """
    _fields_ = [
            ("is_heap", c_bool),
            ("gap", GazepyFilterParameterGap),
            ("noise", GazepyFilterParameterNoise),
            ("saccade", GazepyFilterParameterSaccade),
            ("fixation", GazepyFilterParameterFixation)
    ]

class GazepySample(Structure):
    """
    A data sample to be passed to gaze analysis filters.
    """
    _fields_ = [
            ("is_heap", c_bool),
            ("trial_id", c_uint),
            ("screen_point", c_float * 2),
            ("point", c_float * 3),
            ("origin", c_float * 3),
            ("timestamp", c_double),
            ("label", c_wchar_p)
    ]

class GazepyFixation(Structure):
    """
    A fixation data structure.
    """
    _fields_ = [
            ("is_heap", c_bool),
            ("screen_point", c_float * 2),
            ("point", c_float * 3),
            ("duration", c_double),
            ("first_sample", GazepySample)
    ]

    def __del__(self):
        gazepy_lib.gac.gac_fixation_destroy(byref(self))


class GazepySaccade(Structure):
    """
    A saccade data structure.
    """
    _fields_ = [
            ("is_heap", c_bool),
            ("first_sample", GazepySample),
            ("last_sample", GazepySample)
    ]

    def __del__(self):
        gazepy_lib.gac.gac_saccade_destroy(byref(self))

class GazepyLib():
    """
    Loads libgac and defines the function interfaces.
    """
    def __init__(self):
        # load dynamic library
        # libname = pathlib.Path().absolute() / "bin/libgac.so"
        libname = os.path.abspath( os.path.dirname(__file__)) + "/bin/libgac"
        if platform.uname()[0] == "Windows":
            libname += ".dll"
        else:
            libname += ".so"
        self.gac = cdll.LoadLibrary(libname)

        # define function interfaces
        self.gac.gac_get_filter_parameter.restype = c_bool
        self.gac.gac_get_filter_parameter.argtypes = [c_void_p, POINTER(GazepyFilterParameter)]
        self.gac.gac_get_filter_parameter_default.restype = c_bool
        self.gac.gac_get_filter_parameter_default.argtypes = [POINTER(GazepyFilterParameter)]
        self.gac.gac_create.restype = c_void_p
        self.gac.gac_create.argtypes = [POINTER(GazepyFilterParameter)]
        self.gac.gac_destroy.argtypes = [c_void_p]
        self.gac.gac_filter_fixation_create.restype = c_void_p
        self.gac.gac_filter_fixation_create.argtypes = [c_double, c_double]
        self.gac.gac_filter_fixation_destroy.argtypes = [c_void_p]
        self.gac.gac_filter_fixation.restype = c_bool
        self.gac.gac_filter_fixation.argtypes = [c_void_p, POINTER(GazepySample), POINTER(GazepyFixation)]
        self.gac.gac_filter_gap_create.restype = c_void_p
        self.gac.gac_filter_gap_create.argtypes = [c_double, c_double]
        self.gac.gac_filter_gap_destroy.argtypes = [c_void_p]
        self.gac.gac_filter_gap.restype = c_uint
        self.gac.gac_filter_gap.argtypes = [c_void_p, c_void_p, POINTER(GazepySample)]
        self.gac.gac_filter_noise_create.restype = c_void_p
        self.gac.gac_filter_noise_create.argtypes = [c_uint, c_uint]
        self.gac.gac_filter_noise_destroy.argtypes = [c_void_p]
        self.gac.gac_filter_noise.restype = POINTER(GazepySample)
        self.gac.gac_filter_noise.argtypes = [c_void_p, POINTER(GazepySample)]
        self.gac.gac_filter_saccade_create.restype = c_void_p
        self.gac.gac_filter_saccade_create.argtypes = [c_float]
        self.gac.gac_filter_saccade_destroy.argtypes = [c_void_p]
        self.gac.gac_filter_saccade.restype = c_bool
        self.gac.gac_filter_saccade.argtypes = [c_void_p, POINTER(GazepySample), POINTER(GazepySaccade)]
        self.gac.gac_queue_clear.restype = c_bool
        self.gac.gac_queue_clear.argtypes = [c_void_p]
        self.gac.gac_queue_create.restype = c_void_p
        self.gac.gac_queue_create.argtypes = [c_uint]
        self.gac.gac_queue_destroy.argtypes = [c_void_p]
        self.gac.gac_queue_grow.restype = c_bool
        self.gac.gac_queue_grow.argtypes = [c_void_p, c_uint]
        self.gac.gac_queue_push.restype = c_bool
        self.gac.gac_queue_push.argtypes = [c_void_p, c_void_p]
        self.gac.gac_queue_pop.restype = c_bool
        self.gac.gac_queue_pop.argtypes = [c_void_p, POINTER(c_void_p)]
        self.gac.gac_queue_remove.argtypes = [c_void_p]
        self.gac.gac_sample_window_cleanup.restype = c_bool
        self.gac.gac_sample_window_cleanup.argtypes = [c_void_p]
        self.gac.gac_sample_window_fixation_filter.restype = c_bool
        self.gac.gac_sample_window_fixation_filter.argtypes = [c_void_p, POINTER(GazepyFixation)]
        self.gac.gac_sample_window_saccade_filter.restype = c_bool
        self.gac.gac_sample_window_saccade_filter.argtypes = [c_void_p, POINTER(GazepySaccade)]
        self.gac.gac_sample_window_update.restype = c_uint
        self.gac.gac_sample_window_update.argtypes = [c_void_p, c_float, c_float, c_float, c_float, c_float, c_float, c_double, c_uint, c_wchar_p]
        self.gac.gac_sample_destroy.argtypes = [POINTER(GazepySample)]
        self.gac.gac_fixation_destroy.argtypes = [POINTER(GazepyFixation)]
        self.gac.gac_saccade_destroy.argtypes = [POINTER(GazepySaccade)]

    def getFilterParameterDefault(self):
        """
        Get the default filter parameters which are used to configure the
        gaze analysis filters.

        Returns
        -------
        GazepyFilterParameter, None
            the parameter structure or None on failure
        """
        params = GazepyFilterParameter()
        if self.gac.gac_get_filter_parameter_default(byref(params)):
            return params
        else:
            return None

class Gazepy():
    """
    The gaze analysis handler. This handler maintains its own sample window
    and is therefore easier to use than the individual filter handlers.
    All filters can be configures through the filter parameter structure.
    To parse for fixations and saccades use the methods fixationFilter() and
    saccadeFilter(), respectively.
    """

    def __init__(self, params=None):
        """
        Parameters
        ----------
        params: GazepyFilterParameter, optional
            a filter parameter object configuring the gaze analysis filters.
        """
        self.gac = gazepy_lib.gac
        self.h = self.__create(params)

    def __del__(self):
        self.__destroy()

    def __create(self, params=None):
        if params is None:
            return self.gac.gac_create(None)
        else:
            return self.gac.gac_create(byref(params))

    def __destroy(self):
        self.gac.gac_destroy(self.h)

    def getFilterParameter(self):
        """
        Get the filter parameters used to configure the gaze analysis filter.

        Returns
        -------
        GazepyFilterParameter, None
            the parameter structure or None on failure
        """
        params = GazepyFilterParameter()
        if self.gac.gac_get_filter_parameter(self.h, byref(params)):
            return params
        else:
            return None

    def cleanup(self):
        """
        Remove all unused samples from the sample window. Samples which are
        still in use by filters are left in the sample window.
        """
        self.gac.gac_sample_window_cleanup(self.h)

    def fixationFilter(self):
        """
        Check for a fixation in the curren sample window. Call this method
        after each update() call to parse the gaze samples for fixations.

        Returns
        -------
        GazepyFixation, None
            If a fixation was detected a fixation structure is returned. If
            no fixation was detected or a fixation is still ongoing, None is
            returned.
        """
        fixation = GazepyFixation()
        if self.gac.gac_sample_window_fixation_filter(self.h, byref(fixation)):
            return fixation
        else:
            return None

    def saccadeFilter(self):
        """
        Check for a saccade in the curren sample window. Call this method
        after each update() call to parse the gaze samples for saccades.

        Returns
        -------
        GazepySaccade, None
            If a saccade was detected a sacade structure is returned. If
            no saccade was detected or a saccade is still ongoing, None is
            returned.
        """
        saccade = GazepySaccade()
        if self.gac.gac_sample_window_saccade_filter(self.h, byref(saccade)):
            return saccade
        else:
            return None

    def update(self, ox, oy, oz, px, py, pz, timestamp, trial_id, label):
        """
        Update the sample window with a new gaze sample.

        Parameters
        ----------
        ox: float
            the x coordiante of the gaze origin.
        oy: float
            the y coordiante of the gaze origin.
        oz: float
            the z coordiante of the gaze origin.
        px: float
            the x coordiante of the gaze point.
        py: float
            the y coordiante of the gaze point.
        pz: float
            the z coordiante of the gaze point.
        timestamp: float
            the timestamp of the gaze sample in milliseconds.
        trial_id: int
            the ID of the ongoing trial.
        label: string
            an arbitrary string to annotate a sample.

        Returns
        -------
        int
            the number of samples added to the sample window.
        """
        self.gac.gac_sample_window_update(self.h, ox, oy, oz, px, py, pz, timestamp, trial_id, label)

class GazepyFilterFixation():
    """
    The fixation filter handler. Use this if only fixation parsing on the raw
    data is required. Otherwise use the class Gazepy instead.
    """

    def __init__(self, dispersion_threshold, duration_threshold):
        """
        Parameters
        ----------
        dispersion_threshold: float
            the dispersion threshold in degrees.
        duration_threashold: float
            the duration threshold in milliseconds.
        """
        self.gac = gazepy_lib.gac
        self.f = self.__create(dispersion_threshold, duration_threshold)

    def __del__(self):
        self.__destroy()

    def __create(self, dispersion_threshold, duration_threshold):
        return self.gac.gac_filter_fixation_create(dispersion_threshold, duration_threshold)

    def __destroy(self):
        self.gac.gac_filter_fixation_destroy(self.f)

    def filter(self, sample):
        """
        Parse for fixations. This handler maintains its own sample window.
        There is no need for removing samples from the window as this is done
        internally.

        Parameters
        ----------
        sample: GazepySample
            a sample structure with the new sample data.

        Returns
        -------
        GazepyFixation, None
            If a fixation was detected a fixation structure is returned. If
            no fixation was detected or a fixation is still ongoing, None is
            returned.
        """
        fixation = GazepyFixation()
        if self.gac.gac_filter_fixation(self.f, sample, fixation):
            return fixation
        else:
            return None

class GazepyFilterGap():
    """
    The gap filter handler. Use this if only gap filling on the raw data is
    required. Otherwise use the class Gazepy instead.
    """

    def __init__(self, max_gap_length, sample_period):
        """
        Parameters
        ----------
        max_gap_length: float
            the maximal gap length in milliseconds to fil-in samples. Larger
            gaps are ignored. If set to 0 the filter is disabled.
        """
        self.gac = gazepy_lib.gac
        self.f = self.__create(max_gap_length, sample_period)

    def __del__(self):
        self.__destroy()

    def __create(self, max_gap_length, sample_period):
        return self.gac.gac_filter_gap_create(max_gap_length, sample_period)

    def __destroy(self):
        self.gac.gac_filter_gap_destroy(self.f)

    def filter(self, samples, sample):
        """
        Fill in gaps between the last sample and the current sample through
        interpolation. The number of samples to be filled in depends on the sample
        period.  To avoid filling up large gaps the gap filling is limited to
        a maximal gap length (in milliseconds).  The sample passed to the function
        is added as well.

        Parameters
        ----------
        samples: GazepyQueue
            the sample list to fill in.
        sample: GazepySample
            the new gaze sample to add to the sample list

        Returns
        -------
        int
            the number of samples added to the sample window.
        """
        return self.gac.gac_filter_gap(self.f, samples, sample)

class GazepyFilterNoise():
    """
    The noise filter handler. Use this if only noise filtering on the raw data
    is required. Otherwise use the class Gazepy instead.
    """

    def __init__(self, mid_idx):
        """
        mid_idx: int
            the middle index of the window. This is used to compute the length
            of the window: window_length = mid_idx * 2 + 1. If set to 0 the
            filter is disabled.
        """
        self.gac = gazepy_lib.gac
        self.f = self.__create(mid_idx)

    def __del__(self):
        self.__destroy()

    def __create(self, mid_idx):
        return self.gac.gac_filter_noise_create(0, mid_idx)

    def __destroy(self):
        self.gac.gac_filter_noise_destroy(self.f)

    def filter(self, sample):
        """
        A noise filter. The filter consecutively collects samples into a window
        and returns a filtered value when the window is full, otherwise None is
        returned. The filter maintains its own sample window.

        Parameters
        ----------
        sample: GazepySample
            the new gaze sample to add to the filter window.

        Returns
        -------
        GazepySample, None
            if the filter window is filled the averaged gaze sample is returned,
            othrewise None.
        """
        return self.gac.gac_filter_noise(self.f, sample)

class GazepyFilterSaccade():
    """
    The saccade filter handler. Use this if only saccade parsing on the raw
    data is required. Otherwise use the class Gazepy instead.
    """

    def __init__(self, velocity_threshold):
        """
        Parameters
        ----------
        velocity_threshold: float
            the velocity threshold in degrees per second.
        """
        self.gac = gazepy_lib.gac
        self.f = self.__create(velocity_threshold)

    def __del__(self):
        self.__destroy()

    def __create(self, velocity_threshold):
        return self.gac.gac_filter_saccade_create(velocity_threshold)

    def __destroy(self):
        self.gac.gac_filter_saccade_destroy(self.f)

    def filter(self, sample):
        """
        Parse for saccades. This handler maintains its own sample window.
        There is no need for removing samples from the window as this is done
        internally.

        Parameters
        ----------
        sample: GazepySample
            a sample structure with the new sample data.

        Returns
        -------
        GazepySaccade, None
            If a saccade was detected a saccade structure is returned. If
            no saccade was detected or a saccade is still ongoing, None is
            returned.
        """
        saccade = GazepySaccade()
        if self.gac.gac_filter_saccade(self.f, sample, saccade):
            return saccade
        else:
            return None

class GazepyQueue():
    """
    A queue which grows dynamically in size.
    """

    def __init__(self, length):
        """
        Parameters
        ----------
        length: int
            the initial length of the queue.
        """
        self.gac = gazepy_lib.gac
        self.item_type = item_type
        self.q = self.__create(length)

    def __del__(self):
        self.__destroy()

    def __create(length):
        return self.gac.gac_queue_create(length)

    def __destroy(self):
        self.gac.gac_queue_destroy(self.q)

    def clear(self):
        """
        Remove all items from the queue.

        Returns
        -------
        bool
            True on success, False on failure.
        """
        return self.gac.gac_queue_clear(self.q)

    def grow(self, count):
        """
        Manually grow the queue length.

        Parameters
        ----------
        count: int
            the number of spaces to add to the queue.
        """
        return self.gac.gac_queue_grow(self.q, count)

    def pop(self):
        """
        Remove a sample from the queue tail and return it.

        Returns
        -------
        any, None
            the date sample from the queue tail or None.
        """
        klass = globals()[class_name]
        instance = klass()
        if self.gac.gac_queue_pop(self.q, byref(instance)):
            return instance
        else:
            return None

    def push(self, data):
        """
        Add a sample to the queue head.

        Parameters
        ----------
        data: any
            the data sample to add to the queue head.

        Returns
        -------
        bool
            True on success, False otherwise
        """
        return self.gac.gac_queue_push(self.q, data)

    def remove(self):
        """
        Remove a sample from the queue tail.
        """
        self.gac.gac_queue_remove(self.q)

gazepy_lib = GazepyLib()

def getFilterParameterDefault():
    return gazepy_lib.getFilterParameterDefault()

def sampleDestroy(sample):
    gazepy_lib.gac.gac_sample_destroy(byref(sample))
