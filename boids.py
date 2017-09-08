#!/usr/bin/env python3

"""
Implementing Craig Reynold's Boids...
Boids: Simulating a flock.
Boids model created by Craig Reynolds for realistic-looking simulating the flock behavior of birds.
"""

import sys
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial.distance import squareform, pdist, cdist
from numpy.linalg import norm

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

# the width and height of simulation window on the screen
width, height = 640, 480


class Boids:
    def __init__(self, N):
        """initialize the represents Boids simulation"""
        self.pos = [width / 2.0, height / 2.0] + 10 * np.random.rand(2 * N).reshape(N, 2)
        # normalized random velocities
        angles = 2 * math.pi * np.random.rand(N)
        self.vel = np.array(list(zip(np.sin(angles), np.cos(angles))))
        self.N = N
        # minimum distance of approach
        self.min_dist = 25.0
        # maximum magnitude of velocities calculated by 'rules'
        self.max_rule_vel = 0.03
        # maximum maginitude of the final velocity
        self.max_vel = 2.0

    def tick(self, frame_num, pts, beak):
        """update the simulation by one time step. """
        # get pairwise distances
        self.dist_matrix = squareform(pdist(self.pos))
        # apply rules:
        self.vel += self.apply_rules()
        self.limit(self.vel, self.max_vel)
        self.pos += self.vel
        self.apply_bc()

        # update data
        pts.set_data(
            self.pos.reshape(2 * self.N)[::2],
            self.pos.reshape(2 * self.N)[1::2],
        )
        vec = self.pos + 10 * self.vel / self.max_vel
        beak.set_data(vec.reshape(2 * self.N)[::2], vec.reshape(2 * self.N)[1::2])

    def apply_bc(self):
        """apply boundary conditions"""
        delta_r = 2.0
        for coord in self.pos:
            if coord[0] > width + delta_r:
                coord[0] = -delta_r
            if coord[0] < -delta_r:
                coord[0] = width + delta_r
            if coord[1] > height + delta_r:
                coord[1] = -delta_r
            if coord[1] < -delta_r:
                coord[1] = height + delta_r

    def limit_vec(self, vec, max_val):
        """limit the magnitide of the 2D vector"""
        mag = norm(vec)
        if mag > max_val:
            vec[0], vec[1] = vec[0] * max_val / mag, vec[1] * max_val / mag

    def limit(self, x, max_val):
        for vec in x:
            self.limit_vec(vec, max_val)

    def apply_rules(self):
        D = self.dist_matrix < 25.0
        vel = self.pos * D.sum(axis=1).reshape(self.N, 1) - D.dot(self.pos)
        self.limit(vel, self.max_rule_vel)

        # distance
        D = self.dist_matrix < 50

        # apply rule #2: Aligment
        vel2 = D.dot(self.vel)
        self.limit(vel2, self.max_rule_vel)
        vel += vel2

        # apply rule #3
        vel3 = D.dot(self.pos) - self.pos
        self.limit(vel3, self.max_rule_vel)
        vel += vel3
        return vel

    def buttom_press(self, event):
        # left-click to add a boid
        if event.button is 1:
            self.pos = np.concatenate((
                self.pos, np.array([[event.xdata, event.ydata]])), axis=0)
            angles = 2 * math.pi * np.random.rand(1)
            v = np.array(list(zip(np.sin(angles), np.cos(angles))))
            self.vel = np.concatenate((self.vel, v), axis=0)
            self.N += 1
        # right-click to scatter boids
        elif event.button is 3:
            # add scattering velocity
            self.vel += 0.1 * (self.pos - np.array([[event.xdata, event.ydata]]))


def tick_all(frame_num, pts, beak, boids):
    boids.tick(frame_num, pts, beak)
    return pts, beak


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    # add
    parser.add_argument('--num-boids', dest='N', required=False)
    args = parser.parse_args()

    N = 100
    if args.N:
        N = int(args.N)

    boids = Boids(N)
    fig = plt.figure()
    ax = plt.axes(xlim=(0, width), ylim=(0, height))

    pts, = ax.plot([], [], markersize=10, c='k', marker='o', ls='None')
    beak, = ax.plot([], [], markersize=4, c='r', marker='o', ls='None')
    anim = animation.FuncAnimation(fig, tick_all, fargs=(pts, beak, boids), interval=50)

    cud = fig.canvas.mpl_connect('button_press_event', boids.buttom_press)

    plt.show()


if __name__ == '__main__':
    main()
