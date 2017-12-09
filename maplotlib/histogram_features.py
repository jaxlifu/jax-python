#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

np.random.seed(19680801)


def main():
    mu = 100
    sigma = 15
    x = mu + sigma * np.random.randn(437)

    num_bins = 50

    fig, ax = plt.subplots()

    n, bins, patches = ax.hist(x, num_bins, normed=1)
    y = mlab.normpdf(bins,mu,sigma)
    ax.plot(bins,y,'--')
    ax.set_xlabel('Smarts')
    ax.set_ylabel('Probability density')
    ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

    fig.tight_layout()
    plt.show()
    pass


if __name__ == '__main__':
    main()
