from numpy import exp, convolve
from parse import *

def gaussian(x, a, b, c):
    return a*exp(-(x-b)*(x-b)*c)

def lorenzian(x, b):
    return 1/(b + x*x)

def Voigt(x, a, b):
    f = gaussian(x, 1, 0, a)
    g = lorenzian(x, b)
    return convolve(f, g)