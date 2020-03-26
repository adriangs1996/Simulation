"""
Continuos Random Variables Generator.
"""

from numpy.random import random
from math import log


def exponential(rate, size=None):
    if size is None:
        u = random()
        return -1 / rate * log(u)
    else:
        return [-1 / rate * log(random()) for _ in range(size)]


def normal(m, sd, size=None):
    # Una variable aleatoria X~N(u,s^2) se puede
    # normalizar con el cambio de variable
    # Z = (X - u) / s, por tanto nos basta
    # generar una normal en (0, 1) y aplicar
    # el cambio de variable X = u + sZ
    if size is None:
        while True:
            Y1, Y2 = exponential(1), exponential(1)
            if Y2 >= ((Y1 - 1)**2) / 2:
                if random() <= 1 / 2:
                    return Y1 * sd + m
                else:
                    return -(Y1 * sd + m)
    else:
        samples = []
        while len(samples) < size:
            Y1, Y2 = exponential(1), exponential(1)
            if Y2 >= ((Y1 - 1)**2) / 2:
                if random() <= 1 / 2:
                    samples.append(Y1 * sd + m)
                else:
                    samples.append(-(Y1 * sd + m))
        return samples
