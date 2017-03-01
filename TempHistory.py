from Queue import Queue
from threading import Thread

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

import time

import thread

LIMIT = 50

class TempHistory():
    def __init__(self, plot_vars=None):
        self.queue = Queue(1)
        self.tdata = []
        self.ydata = []
        if plot_vars is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.fig, self.ax = plot_vars
        self.star_animation()

    def getPlotVars(self):
        return self.fig, self.ax

    def star_animation(self):
        self.ax.set_xlim(0, LIMIT)
        self.ax.set_ylim(0, 40)
        self.line, = self.ax.plot(self.tdata, self.ydata)
        self.ani = animation.FuncAnimation(self.fig, self.update, self.data_gen, blit=True)
        # plt.show()

    def add_value(self, value):
        v = int(value)
        self.queue.put(v)

    def update(self, data):
        t, y = data
        if len(self.ydata) >= LIMIT:
            self.ydata.pop(0)
        else:
            self.tdata.append(t)

        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,

    def data_generator(self):
        t = 0
        while True:
            # time.sleep(0.001)
            t += 1
            y = self.queue.get()
            yield t, y

    def data_gen(self):
        t = 0
        y = 0
        while True:
            t += 1
            y = random.randint(1,35)
            yield t,y



# tt = TempHistory()
# def run(tt):
#     while(True):
#         tt.add_value(random.randint(35,38))
# t = thread.start_new(run, (tt,))
# print 'hi'
# tt.star_animation()



