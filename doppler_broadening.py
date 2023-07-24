import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from utils import Voigt
from uncertainties import ufloat

import plot_config
import pandas as pd

from datetime import datetime
from simple_spectrometer import get_background_noise, get_snapshot

integration_time = 4000

print("Acquiring background noise ... \n ")
get_background_noise(integration_time)

now = datetime.now()
dt_string = now.strftime("%d:%m:%Y_%H-%M-%S")

print("Specify valid wavelength range [1 - 2048 nm]: \n")
start = int(input("Start: "))
end = int(input("End: "))
print("\n")

starting_time = datetime.now()

pressure = 1
while pressure > 1e-8:
    pressure = input("Enter pressure value [mbar]: p = ")
    now = datetime.now()
    get_snapshot(integration_time=integration_time, name=now, start=start, end=end)
    stop = input("Continue? Y/N :")
    if stop == 'Y':
        break

# Impprting data 
file = input("Enter spectrum data file name (relative file path): ")
data = pd.read_table(file, sep=" ", names=["wavelegnth", "intensiy"], skiprows=2)

# 