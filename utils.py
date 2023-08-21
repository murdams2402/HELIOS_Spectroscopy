from numpy import exp, convolve
from math import pi
from parse import *
import os

def gaussian(x, a, b, c):
    return a*exp(-(x-b)*(x-b)*c)

def lorenzian(x, x0, b):
    return (1/pi)*b/(b*b + (x-x0)*(x-x0))

def Voigt(x, x0, a, b, A):
    f = gaussian(x, 1, x0, a)
    g = lorenzian(x, x0, b)
    return convolve(f, g)


def get_files_and_params(dir, format):
    """
    Get all files in dir and extract params from their names.
    returns [
    {
        "name": <file_name>,
        "param1": <param1>,
        ...
    }
    ]
    """ 
    files = os.listdir(dir)
    files_and_params = []
    for file in files:
        # get params from file name
        if file != '.DS_Store':
            params = parse(format, file).named
            files_and_params.append({
                "name": file,
                **params
            })
    return files_and_params