import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from utils import Voigt
from uncertainties import ufloat

# import plot_config

import pandas as pd

from simple_spectrometer import get_background_noise

get_background_noise()

# Impprting data 
file = input("Enter spectrum data file name (relative file path): ")
data = pd.read_table(file, sep=" ", names=["wavelegnth", "intensiy"], skiprows=2)

# 