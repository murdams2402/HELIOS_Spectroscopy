import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import peak_widths
from utils import Voigt, gaussian, lorenzian
from numpy import sqrt, log
# from uncertainties import ufloat

import plot_config
import pandas as pd
import numpy as np

from plot_data import plot_data
import plot_config

from datetime import datetime
from simple_spectrometer import get_background_noise, get_snapshot

integration_time = 2000
path = 'Spectrum_data/'

print("Acquiring background noise ... \n ")
start, end = get_background_noise(integration_time)
background = pd.read_table(path + 'background_noise_spectrum_raw_data.txt', sep=" ", names=["wavelegnth", "intensiy"], skiprows=2)

# print("Specify valid wavelength range [1 - 2048 nm]: \n")
# start = int(input("Start: "))
# end = int(input("End: "))
# print("\n")

starting_time = datetime.now()

data = pd.DataFrame(columns=["pressure", "moment", "wavelength", "intensiy"])

pressure = 1
moments = []
moments.append(starting_time)

show = True

while pressure > 1e-8:
    pressure = float(input("Enter actual pressure value [mbar]: p = "))
    now = datetime.now()
    dt_string = now.strftime("%d:%m:%y_%H-%M-%S")

    # Getting data: measuring plasma spectrum 
    get_snapshot(integration_time=integration_time, 
                 name=f"doppler_broadening_data_pressure={pressure}mbar_time=" + dt_string, 
                 start=start, 
                 end=end)
    
    # Importing data 
    brut = pd.read_table(path + f"doppler_broadening_data_pressure={pressure}mbar_time=" + dt_string + "_spectrum_raw_data.txt", 
                         sep=" ", 
                         names=["wavelength", "intensiy"], 
                         skiprows=2)
    raw = [(pressure, now, lambda_, I) for lambda_, I in zip(brut['wavelength'], brut["intensiy"])]
    data_ = pd.DataFrame(raw, columns=["pressure", "moment", "wavelength", "intensiy"])
    data_["intensiy"] = data_["intensiy"] - background["intensiy"] # background["intensiy"][start-1:end+1]
    data = pd.concat([data, data_])

    moments.append(now)

    if show:
        plot_data(data_["wavelength"], data_["intensiy"], 
                  x_label=r"$\lambda$", y_label="Intensity", 
                  title=f"{pressure} mbar", show=False)

    stop = input("Continue pressure measurments? Y/N :")
    if stop == 'N':
        break

if show :
    plt.show()

# Analysing the data : fitting broadening with Gaussian / Lorenzian / Voigt function
#                      and determining gas temperature
# FWHM_Gauss = []
# FWHM_Lorenzian = []
# FWHM_Voigt = []
# FWHM_Voigt_estimation = []
# for p in data["pressure"]:
#     starting_points = []    
#     # The FWHM of a Lorenzian is two times it's parameter b = \gamma (see function definition in utils.py)
#     popt_Lorenzian, covopt_Lorenzian = curve_fit(lorenzian, 
#                                              data[data["pressure"] == p]["intensiy"], 
#                                              p0=starting_points)
#     FWHM_Lorenzian.append(2*popt_Lorenzian[1])

#     starting_points = []
#     # The FWHM of a Gaussian is equal to FWHM = sigma*sqrt( 8*ln(2) )
#     popt_Gauss, covopt_Gauss = curve_fit(gaussian, 
#                                          data[data["pressure"] == p]["intensiy"], 
#                                          p0=starting_points)
#     sigma = 1/sqrt(2*popt_Gauss[2])
#     Delta_lambda = sigma*sqrt(8*log(2))
#     FWHM_Gauss.append(Delta_lambda)
    
#     starting_points = []
#     # The FWHM of the Voigt profile function is determined numerically
#     popt_Voigt, covopt_Voigt = curve_fit(Voigt, 
#                                          data[data["pressure"] == p]["intensiy"], 
#                                          p0=starting_points)
#     FWHM_Voigt.append()
#     # However there is an approximation, which we can use as 4th estimation for the temperature
#     FWHM_Voigt_estimation.append(0.5346*2*popt_Lorenzian[1] + sqrt(0.2166*(4*popt_Lorenzian[1]*popt_Lorenzian[1]) + Delta_lambda*Delta_lambda))
    
#     # indices of peakes
#     peaks = []
#     # Using scipy's function that retreaves the FWHM of the specified peaks
#     widths, _ = peak_widths(x=data[data["pressure"] == p]["intensiy"], peaks=peaks )
