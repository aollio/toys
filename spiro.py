#!/usr/bin/env python3

"""
The spirographs implemented by turtle. Smart turtle.
This program draws Spirographs using the Turtle module.
When run with no arguments, this program draws random Spirographs.

Terminology:
    R: radius of outer circle.
    r: radius of inner circle.
    l: ratio of hole distance to r.

"""

import random
import turtle
from turtle import Turtle
from fractions import gcd
import argparse

import math

from datetime import datetime

import sys
from PIL import Image


class Spiro:
    def __init__(self, xc, yc, col, R, r, l):
        self.turtle = Turtle()
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
        for i in range(0, int(360 * self.n_rot + 1), self.step):
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
            spiro.set_parameters(*rparams)
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
            # self.restart()
            pass
        turtle.ontimer(self.update, self.delta_t)

    def toggle_turtles(self):
        for sprio in self.spiros:
            if sprio.turtle.isvisible():
                sprio.turtle.isvisible()
            else:
                sprio.turtle.showturtle()


def save_drawing():
    """save drawing as PNG files"""
    turtle.hideturtle()
    # generate unique file name
    date_str = (datetime.now()).strftime('%d%b%Y-%H%M%S')
    file_name = 'spiro-' + date_str
    print('saving drawing to %s.eps/png' % file_name)
    # get the tkinter canvas
    canvas = turtle.getcanvas()
    # saving the drawing as a postscript image
    canvas.postscript(file=file_name + '.eps')
    # use the Pillow module to convert the postscript image file to PNG
    img = Image.open(file_name + '.eps')
    img.save(file_name + '.png', 'png')
    # show the turtle cursor
    turtle.showturtle()


def main():
    # use sys.argv if needed

    # create parser
    parser = argparse.ArgumentParser(description=__doc__)

    # add expected arguments
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help='The three arguments in sparams: R, r, l. ')

    parser.add_argument('-c', '--count', dest='count', default=random.randint(3, 10), required=False,
                        help='The count of spirographs.', type=int)

    # parse args
    args = parser.parse_args()
    turtle.setup(width=0.8)
    turtle.shape('turtle')
    # set title
    turtle.title('Spirographs! ')
    # add the key handler to save our drawings
    turtle.onkey(save_drawing, 's')
    turtle.onkey(sys.exit, 'q')

    # hide the main turtle cursor
    turtle.hideturtle()

    print('generating spirograph')
    print("key: 's', save image")
    print("key: 'q', quit application")
    print("key: 't', toggle_turtles")
    print("key: 'space', restart all turtles")

    if args.sparams:
        params = [float(x) for x in args.sparams]
        # draw the Spirograph with the given parameters
        col = 0.0, 0.0, 0.0
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        count = args.count
        # create the animator object
        spiro_anim = SpiroAnimator(count)
        # add a key handler to toggle the turtle cursor
        turtle.onkey(spiro_anim.toggle_turtles, 't')
        # add a key handler to restart the animation
        turtle.onkey(spiro_anim.restart, 'space')

    # start listening
    turtle.listen()
    turtle.mainloop()


if __name__ == '__main__':
    main()
