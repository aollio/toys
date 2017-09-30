#!/usr/bin/env python3
"""
Run Conway's Game of Life simulation.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

ON = 255
OFF = 0
vals = [ON, OFF]


def add_glider(i, j, grid):
    """ add a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i + 3, j:j + 3] = glider


def random_grid(length):
    """ return a grid of N * N random values """
    return np.random.choice(vals, length ** 2, p=[0.2, 0.8]).reshape(length, length)


def update(frame_num, img, grid, length):
    new_grid = grid.copy()
    for i in range(length):
        for j in range(length):
            # compute 8 neighbors sum using boundary conditions
            total = int(
                (
                    grid[i, (j - 1) % length] + grid[i, (j + 1) % length] +
                    grid[(i - 1) % length, j] + grid[(i + 1) % length, j] +
                    grid[(i - 1) % length, (j - 1) % length] + grid[(i - 1) % length, (j + 1) % length] +
                    grid[(i + 1) % length, (j - 1) % length] + grid[(i + 1) % length, (j + 1) % length]
                ) / 255
            )
            if grid[i, j] == ON:
                if not 1 < total < 4:
                    new_grid[i, j] = OFF
            else:
                if total == 3:
                    new_grid[i, j] = ON

    # update data
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    # add argument
    parser.add_argument('-l', '--grid-length', dest='length', required=False, help='the playground length')
    parser.add_argument('--mov-file', dest='mov_file', required=False)
    parser.add_argument('-i', '--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    args = parser.parse_args()

    # set grid size
    length = 100
    if args.length and int(length) > 8:
        length = int(args.length)

    # set animation update interval
    update_interval = 16
    if args.interval:
        update_interval = int(args.interval)

    # declare grid
    grid = np.array([])
    # check if 'glider' demo flag is special
    if args.glider:
        grid = np.zeros(length * length).reshape(length, length)
        add_glider(1, 1, grid)
    else:
        # populate grid with random on/off - more off than on
        grid = random_grid(length)

    # set up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    anim = animation.FuncAnimation(fig, update, fargs=(img, grid, length,),
                                   frames=10, interval=update_interval, save_count=50)

    # number of frames?
    # set output file
    if args.mov_file:
        anim.save(args.mov_file, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


if __name__ == '__main__':
    main()
