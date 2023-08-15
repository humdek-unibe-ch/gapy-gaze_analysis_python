#!/usr/bin/python3

import gazepy
import csv

if __name__ == "__main__":
    lib = gazepy.GazepyLib()
    params = lib.getFilterParameterDefault()

    params.gap.max_gap_length = 0
    params.noise.mid_idx = 0
    params.saccade.velocity_threshold = 25
    h = gazepy.Gazepy(lib, params)
    fixations = []
    saccades = []
    rows = []

    with open('sample2.csv') as csvfile:
        data = csv.reader(csvfile)
        is_first = True
        for row in data:
            if is_first:
                is_first = False
            else:
                rows.append(row)

    for row in rows:
        h.update(float(row[3]), float(row[4]), float(row[5]), float(row[0]), float(row[1]), float(row[2]), float(row[6]))
        fixation = h.fixationFilter()
        if fixation is not None:
            fixations.append(fixation)
        #     print('f:', fixation.timestamp, '(' + str(fixation.duration) + '):', fixation.point[0], fixation.point[1], fixation.point[2])
        saccade = h.saccadeFilter()
        if saccade is not None:
            saccades.append(saccade)
        #     print('s:', saccade.timestamp, '(' + str(saccade.duration) + '):', saccade.point_start[0], saccade.point_start[1], saccade.point_start[2], '->', saccade.point_dest[0], saccade.point_dest[1], saccade.point_dest[2])
        h.cleanup()
