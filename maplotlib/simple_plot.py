#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


def main():
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    fig, ax = plt.subplots()
    ax.plot(t, s)
    ax.set(xlabel='time(s)', ylabel='voltage (mV)',
           title='About as sample as it gets,floks')
    ax.grid()
    fig.savefig('test.png')
    plt.show()
    pass


if __name__ == '__main__':
    main()
