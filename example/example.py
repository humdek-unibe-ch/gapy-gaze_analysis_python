#!/usr/bin/python3

import gazepy
import csv

if __name__ == "__main__":
    params = gazepy.getFilterParameterDefault()

    params.gap.max_gap_length = 0
    params.noise.mid_idx = 0
    params.saccade.velocity_threshold = 25
    h = gazepy.Gazepy(params)
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
        h.update(float(row[5]), float(row[6]), float(row[7]), float(row[2]), float(row[3]), float(row[4]), float(row[8]), int(row[9]), str(row[10]))
        fixation = h.fixationFilter()
        if fixation is not None:
            fixations.append(fixation)
            print('f:', fixation.first_sample.timestamp, '(' + str(fixation.duration) + '):', fixation.point[0], fixation.point[1], fixation.point[2])
        saccade = h.saccadeFilter()
        if saccade is not None:
            saccades.append(saccade)
            print('s:', saccade.first_sample.timestamp, '(' + str(saccade.last_sample.timestamp - saccade.first_sample.timestamp) + '):', saccade.first_sample.point[0], saccade.first_sample.point[1], saccade.first_sample.point[2], '->', saccade.last_sample.point[0], saccade.last_sample.point[1], saccade.last_sample.point[2])
        h.cleanup()
