from numpy import exp, convolve
from math import pi
from parse import *

def gaussian(x, a, b, c):
    return a*exp(-(x-b)*(x-b)*c)

def lorenzian(x, x0, b):
    return (1/pi)*b/(b*b + (x-x0)*(x-x0))

def Voigt(x, x0, a, b, A):
    f = gaussian(x, 1, x0, a)
    g = lorenzian(x, x0, b)
    return convolve(f, g)