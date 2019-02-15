import numpy as np


def identity(n):
    return n


def bias(n):
    return 1


def sig(n):
    return 1 / (1 + np.exp(-n))