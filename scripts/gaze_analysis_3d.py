#!/usr/bin/python3

import pandas as pd
import numpy as np
import quaternionic
import csv

def q_dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w

def quaternion_mean(qs):
    # Number of quaternions to average
    M = qs.shape[0]
    A = np.zeros(shape=(4,4))

    for i in range(0,M):
        q = qs[i,:]
        # multiply q with its transposed version q' and add A
        A = np.outer(q,q) + A

    # scale
    A = (1.0/M)*A
    # compute eigenvalues and -vectors
    eigenValues, eigenVectors = np.linalg.eig(A)
    # Sort by largest eigenvalue
    eigenVectors = eigenVectors[:,eigenValues.argsort()[::-1]]
    # return the real part of the largest eigenvector (has only real part)
    return quaternionic.array(eigenVectors[:,0]).normalized

def quaternion_mean_approx(qs):
    avg = quaternionic.array([0, 0, 0, 0])
    is_first = True
    for q in qs:
        if is_first == False and q_dot(q, qs[0]) < 0:
            q = -q
        avg += q
        is_first = False

    return avg.normalized

def dispersion_static(qs):
    q_mean = quaternion_mean_approx(qs)
    q_mean_conj = np.conj(q_mean)
    q0 = q_mean_conj * qs
    angle = 2 * np.arccos(q0.w)
    return (np.max(angle) - np.min(angle), q_mean)

def shortest_distance(p1, p2, n):
    return abs(np.sum((p2 - p1) * n, axis=1) / np.linalg.norm(n, axis=1))

def nearest_points(p1, p2, d1, d2, n):
    n2 = np.cross(d2, n)
    n1 = np.cross(d1, n)

    s1 = np.sum((p2 - p1) * n2, axis=1) / np.sum(d1 * n2, axis=1)
    s1 = np.broadcast_to(s1, (3, len(s1))).transpose()
    c1 = p1 + s1 * d1

    s2 = np.sum((p1 - p2) * n1, axis=1) / np.sum(d2 * n1, axis=1)
    s2 = np.broadcast_to(s2, (3, len(s2))).transpose()
    c2 = p2 + s2 * d2

    return (c1, c2)

def dispersion_dynamic(p, qs):
    nx = np.array([1, 0, 0])
    d = qs.rotate(nx)
    d1 = d[:-1]
    d2 = d[1:]
    p1 = p[:-1]
    p2 = p[1:]
    n = np.cross(d1, d2)
    c1, c2 = nearest_points(p1, p2, d1, d2, n)
    c = (c1 + c2) / 2
    dist = np.linalg.norm(c - p2, axis=1)
    dist = np.broadcast_to(dist, (3, len(dist))).transpose()
    c_norm = c * dist
    cx = c_norm[:, 0]
    cy = c_norm[:, 1]
    cz = c_norm[:, 2]
    dispersion = np.linalg.norm(np.array([cx.max() - cx.min(), cy.max() - cy.min(), cz.max() - cz.min()]))

    return (dispersion, c.mean(axis=0))


if __name__ == "__main__":
    dispersion_threashold = np.deg2rad(0.5)
    dispersion_threashold_mm = np.sqrt(2 * (1 - np.cos(dispersion_threashold)))
    duration_threashold = 50
    sample_period = 1000/120
    df = pd.read_csv('samples/sample.csv')
    pos = df[['pos.x', 'pos.y', 'pos.z']].to_numpy()
    ori = df[['ori.qw', 'ori.qx', 'ori.qy', 'ori.qz']].to_numpy()
    q = quaternionic.array(ori).normalized

    start_s = 0
    start_d = 0
    stop_s = 0
    stop_d = 0
    duration_s = 0
    duration_d = 0
    is_collecting_s = False
    is_collecting_d = False
    idx = 0
    while(idx < len(ori)):
        stop_s += 1
        stop_d += 1
        duration_s += sample_period
        duration_d += sample_period
        if duration_s >= duration_threashold:
            dispersion, q_mean = dispersion_static(q[start_s:stop_s])

            if dispersion <= dispersion_threashold:
                is_collecting_s = True
            elif is_collecting_s == True:
                pos_mean = pos[start_s:stop_s].mean(axis=0)
                print(f'static fixation detected: {duration_s}, {q_mean}, {pos_mean}')
                is_collecting_s = False
                start_s = stop_s
                duration_s = 0
            else:
                start_s += 1

        if duration_d >= duration_threashold:
            dispersion, c_mean = dispersion_dynamic(pos[start_d:stop_d], q[start_d:stop_d])

            if dispersion <= dispersion_threashold_mm:
                is_collecting_d = True
            elif is_collecting_d == True:
                print(f'dynamic fixation detected: {duration_d}, {c_mean}')
                is_collecting_d = False
                start_d = stop_d
                duration_d = 0
            else:
                start_d += 1
        idx += 1

