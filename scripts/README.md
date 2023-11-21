# 3d Gaze Analysis

The goal of this repo is to compute gaze fixations in 3d space with the following approach:

1. Static situation: Find gaze rays that point in the same direction. This is done by computing the angles of each gaze ray in a sliding window with respect to the average gaze ray in the sliding window.
2. Dynamic situation: Find gaze ray intersection points (nearest points) of consecutive gaze rays in a sliding window and compute the dispersion of each point with the center of mass of all points.

TODO: The static situation is currently position-agnostic. This could lead to false fixation detections where a subject moves but keeps its gaze direction constant (gaze rays are parallel).
