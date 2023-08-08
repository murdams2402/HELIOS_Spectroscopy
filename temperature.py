from master import  get_snapshot, get_snapshot_raw
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_files_and_params
from scipy.constants import c, k
m_Ne = 3.3509e-26 # kg
from numpy import log, sqrt

from scipy.signal import peak_widths, find_peaks

# Opening background noise
background = pd.read_table("Background_data/HR4000_03_08_2023_13h58min08s_spectrum_raw_data.txt",
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)

def acquire_spectra(gas="Neon_"):
    data = pd.DataFrame(columns=[ "file_name", "pressure", "wavelength", "intensity"])

    while True:
        pressure = float(input("Enter pressure [mbar] = "))
        fullname = get_snapshot(path='Spectrum_data/Temperature_experiment/',
                                name=gas+f"pressure={pressure}_")

        # Importing data 
        brut = pd.read_table(fullname, 
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)
        raw = [(fullname, pressure, w, I) for w, I in zip(brut['wavelength'], brut["intensity"])]
        data_ = pd.DataFrame(raw, columns=[ "file_name", "pressure", "wavelength", "intensity"])
        # Filtering data
        data_["intensity"] = data_["intensity"] # - background["intensiy"] # background["intensiy"][start-1:end+1]
        
        data = pd.concat([data, data_])

        stop = input("Continue measurments? Y/N :")
        if stop == 'N':
            break


    plt.figure(figsize=(8,6))
    for file_name in data["file_name"]:
        plt.plot(data["file_name"==file_name]["wavelength"],data["file_name"==file_name]["intensity"])
        plt.xlabel(r"$\lambda \rm \ [nm]$")
        plt.ylabel(r"$\rm Intensity \ [a.u.]$")
        plt.grid(True)  
    plt.show()        

temperature = pd.DataFrame(columns=[ "file_name", "pressure", "peak wavelength", "FWHM Doppler", "temperature"])
delta_lambda = 0.26962647198209 # [nm]
Delta_Lamda_Apparatus = 0.03 # [nm] for HR4000
if __name__ == '__main__':
    dir = "Spectrum_data/Temperature_experiment"
    files = get_files_and_params(dir, format="Neon_pressure={pressure}_HR4000_spectrum_raw_data.txt")
    plt.figure(figsize=(8,6))
    for file in files:
        file_name = file["name"]
        p = file["pressure"]
        data = pd.read_table(f"{dir}/{file_name}", 
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)
        
        max_peaks = data.max()
        # print(max_peaks["intensity"])

        plt.plot(data["wavelength"],data["intensity"])
        plt.xlabel(r"$\lambda \rm \ [nm]$")
        plt.ylabel(r"$\rm Intensity \ [a.u.]$")
        plt.grid(True)

        # Using scipy's function that retreaves the FWHM of the specified peaks
        peaks_ = find_peaks(x=data["intensity"], height=[1000, max_peaks["intensity"]])
        widths = peak_widths(x=data["intensity"], peaks=peaks_[0])
        wavelengths = data.filter(items=peaks_[0], axis=0)
        # print(wavelengths)
        Delta_Lamda_doppler = [ sqrt((fwhm*delta_lambda)*(fwhm*delta_lambda) - Delta_Lamda_Apparatus*Delta_Lamda_Apparatus) for fwhm in widths[0]]
        Tg = [ ((delta/l0)**2)*(c*c*m_Ne)/(8*k*log(2)) for delta, l0 in zip(Delta_Lamda_doppler, wavelengths["wavelength"])]
        # print(Tg)
        # Saving data for later analysis
        brut = [(file_name, p, peak, wdth, tg) for wdth, peak, tg in zip(Delta_Lamda_doppler, wavelengths["wavelength"], Tg)]
        temperature_ = pd.DataFrame(brut, columns=[ "file_name", "pressure", "peak wavelength", "FWHM Doppler", "temperature"])
        temperature = pd.concat([temperature, temperature_])
    plt.show()


# plt.figure(figsize=(8,6))
# for file in temperature["file_name"]:
#         plt.scatter(temperature[temperature["file_name"]== file]["pressure"], temperature[temperature["file_name"]== file]["temperature"])
#         plt.xlabel(r"$p \rm \ [mbar]$")
#         plt.ylabel(r"$\rm T \ [?]$")
#         plt.grid(True)
# plt.show()

plt.figure(figsize=(8,6))
for peak in temperature["peak wavelength"]:
        plt.scatter(x=temperature[temperature["peak wavelength"]== peak]["pressure"], y=temperature[temperature["peak wavelength"]== peak]["temperature"])
        plt.xlabel(r"$p \rm \ [mbar]$")
        plt.ylabel(r"$\rm T \ [?]$")
        plt.grid(True)
plt.show()