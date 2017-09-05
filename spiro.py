#!/usr/bin/env python3

"""
The spirographs implemented by turtle. Smart turtle
"""

import random
import turtle
from turtle import Turtle
from fractions import gcd
import argparse

import math


class Spiro:
    def __init__(self, xc, yc, col, R, r, l):
        self.turtle = turtle.Turtle()
        # set the cursor shape
        self.turtle.shape('turtle')
        # set the step in degrees
        self.step = 5
        # set the drawing complete flag
        self.drawing_complete = False

        # set parameters
        self.set_parameters(xc, yc, col, R, r, l)

        # initalize the drawing
        self.restart()

    def set_parameters(self, xc, yc, col, R, r, l):
        # Spirograph parameters
        self.xc = xc
        self.yc = yc
        self.col = col
        self.R = R
        self.r = r
        self.l = l

        # reduce r/R to its smallest form by dividing with the GCD
        gcd_val = gcd(self.r, self.R)
        self.n_rot = self.r // gcd_val
        # get ratio of radii
        self.k = r / float(R)

        self.turtle.color(*col)
        # store the current angle
        self.a = 0

    def restart(self):
        # set the flag
        self.drawing_complete = False
        # show the turtle
        self.turtle.showturtle()
        # go to the first point
        self.turtle.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R * ((1 - k) * math.cos(a) + 1 * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) - 1 * k * math.sin((1 - k) * a / k))
        self.turtle.setpos(self.xc + x, self.yc + y)
        self.turtle.down()

    def draw(self):
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360 * self.n_rot + 1, self.step):
            a = math.radians(i)
            x = R * ((1 - k) * math.cos(a) + 1 * k * math.cos((1 - k) * a / k))
            y = R * ((1 - k) * math.sin(a) - 1 * k * math.sin((1 - k) * a / k))
            self.turtle.setpos(self.xc + x, self.yc + y)
        self.turtle.hideturtle()

    def update(self):
        # skip the rest of the steps if done
        if self.drawing_complete:
            return

        # increment the angle
        self.a += self.step
        # draw a step
        R, k, l = self.R, self.k, self.l
        a = math.radians(self.a)
        x = R * ((1 - k) * math.cos(a) + 1 * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) - 1 * k * math.sin((1 - k) * a / k))
        self.turtle.setpos(self.xc + x, self.yc + y)

        # if drawing is complete, set the flag
        if self.a >= 360 * self.n_rot:
            self.drawing_complete = True
            # drawing is now done so hide the turtle cursor
            self.turtle.hideturtle()

    def clear(self):
        self.turtle.clear()


class SpiroAnimator:
    def __init__(self, count):
        # set the timer value in milliseconds
        self.delta_t = 10
        # get the window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        # create the Spiro objects
        self.spiros = []
        for i in range(count):
            # generate random parameters
            rparams = self.gen_random_params()
            # set the spiro parameters
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
        # call timer
        turtle.ontimer(self.update, self.delta_t)

    def gen_random_params(self):
        # generate random parameters
        width, height = self.width, self.height
        R = random.randint(50, min(width, height) // 4)
        r = random.randint(10, 9 * R // 20)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width // 2 + 50, width // 2 - 50)
        yc = random.randint(-height // 2 + 50, height // 2 - 50)
        col = (random.random(), random.random(), random.random())
        return xc, yc, col, R, r, l

    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams = self.gen_random_params()
            # set the spiro parameters
            spiro.setparams(*rparams)
            #  restart drawing
            spiro.restart()

    def update(self):
        # update all spiro
        n_complete = 0
        for spiro in self.spiros:
            spiro.update()
            if spiro.drawing_complete:
                n_complete += 1
        if n_complete == len(self.spiros):
            self.restart()
        turtle.ontimer(self.update, self.delta_t)

    def toggle_turtles(self):
        for sprio in self.spiros:
            if sprio.turtle.isvisible():
                sprio.turtle.isvisible()
            else:
                sprio.turtle.showturtle()


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-c', '--count', dest='count', default=1, required=False,
                        help='the count of spirographs, should be in 1 - 4', type=int)

    args = parser.parse_args()
    turtle.setup(width=0.8)
    turtle.shape('turtle')
    turtle.title('Spirographs! ')
    turtle.hideturtle()

    count = 1
    if args.count and 0 < args.count < 5:
        count = args.count
    spiro_anim = SpiroAnimator(count)
    turtle.onkey(spiro_anim.toggle_turtles, 't')

    turtle.mainloop()


if __name__ == '__main__':
    main()
