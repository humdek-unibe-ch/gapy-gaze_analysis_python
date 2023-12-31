# `gazepy`: Python Bindings for `libgac`

This repository holds a python package which implements the bindings to the gaze analysis library [gac](http://phhum-a209-cp.unibe.ch:10012/LIB/LIB-gaze_analysis_c).

Note that this library is experimental and rather slow compared to the C library.

## Quick Start

Install the library:
```sh
pip install release/gazepy-<version>.tar.gz
```
where `<version>` stands for a chosen package version.

In a python script, load the package and prepare the gaze handler:

```py
import gazepy

h = gazepy.Gazepy()
```

In order to parse gaze data for fixations and saccades and perform noise and gap filtering **loop** over the gaze data and call the following functions for each sample:
```py
# add a sample to the sliding window and filter the sample
h.update(float(origin_x), float(origin_y), float(origin_z), float(point_x), float(point_y), float(point_z), float(timestamp), int(trial_id), str(label))

# parse for fixations
fixation = h.fixationFilter()
if fixation is not None:
    pass # modify to store the detected fixation

# parse for saccades
saccade = h.saccadeFilter()
if saccade is not None:
    pass # modify to store the detected saccade

# cleanup the sliding window
h.cleanup()
```

The gaze handler can be configured through parameters:

```py
# get the default parameters
params = gazepy.getFilterParameterDefault()

# change the default parameters
params.gap.max_gap_length = 0
params.noise.mid_idx = 0
params.saccade.velocity_threshold = 25
# pass the updated parameter object to the gaze handler constructor
h = gazepy.Gazepy(params)
```

## Create a Python Package

To create the package bundle simply run `python3 -m build`.
