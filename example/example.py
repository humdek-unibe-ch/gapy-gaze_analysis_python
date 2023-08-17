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

    with open('sample.csv') as csvfile:
        data = csv.reader(csvfile)
        is_first = True
        for row in data:
            if is_first:
                is_first = False
            else:
                rows.append(row)

    for row in rows:
        h.updateWithScreen(float(row[5]), float(row[6]), float(row[7]),
                float(row[2]), float(row[3]), float(row[4]),
                float(row[0]), float(row[1]),
                float(row[8]), int(row[9]), row[10])
        fixation = h.fixationFilter()
        if fixation is not None:
            fixations.append(fixation)
            print(fixation.first_sample.timestamp,
                    f'fixation({fixation.first_sample.label.decode()}, {fixation.first_sample.trial_id}):',
                    f'[{fixation.screen_point[0]}, {fixation.screen_point[1]}]',
                    f'[{fixation.point[0]}, {fixation.point[1]}, {fixation.point[2]}],',
                    fixation.duration)
        saccade = h.saccadeFilter()
        if saccade is not None:
            saccades.append(saccade)
            print(saccade.first_sample.timestamp,
                    f'saccade({saccade.first_sample.label.decode()}, {saccade.first_sample.trial_id}):',
                    f'[{saccade.first_sample.screen_point[0]}, {saccade.first_sample.screen_point[1]}]',
                    f'[{saccade.first_sample.point[0]}, {saccade.first_sample.point[1]}, {saccade.first_sample.point[2]}]',
                    '->',
                    f'[{saccade.last_sample.screen_point[0]}, {saccade.last_sample.screen_point[1]}]',
                    f'[{saccade.last_sample.point[0]}, {saccade.last_sample.point[1]}, {saccade.last_sample.point[2]}],',
                    saccade.last_sample.timestamp - saccade.first_sample.timestamp)
        h.cleanup()
