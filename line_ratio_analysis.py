import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from utils import get_files_and_params
from scipy.constants import c, k, h, e

import plot_config
from scipy.signal import find_peaks

if __name__ == '__main__':
    data = pd.DataFrame(columns=["model", "gas", "shot", "power", "wavelength", "intensity"])
    dir = "Spectrum_data/Line_ratio"
    files = get_files_and_params(dir, format="gas={gas}_shot={shot}_power={power}W_{model}_spectrum_raw_data.txt")
    peaks = data

    for  file in files:
        file_name = file["name"]
        
        # Opening acquired spectrum
        spectrum = pd.read_table(f"{dir}/{file_name}", 
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)
        temp = [(file["model"], file["gas"], file["shot"], file["power"], w, I) for w, I in zip(spectrum["wavelength"], spectrum["intensity"])]
        temp = pd.DataFrame(temp, columns=["model", "gas", "shot", "power", "wavelength", "intensity"])
        data = pd.concat([data, temp])
        
        # Picking the spectrum peaks
        max_peaks = spectrum.max()
        peaks_info = find_peaks(x=spectrum["intensity"], height=[1000, max_peaks["intensity"]])
        # peaks_info[1].get("peak_heights")
        peaks_ = spectrum.filter(items=peaks_info[0], axis=0)
        temp = [(file["model"], file["gas"], file["shot"], file["power"], w, I) for w, I in zip(peaks_["wavelength"], peaks_["intensity"])]
        temp = pd.DataFrame(temp, columns=["model", "gas", "shot", "power", "wavelength", "intensity"])
        peaks = pd.concat([peaks, temp])
    
    
    plt.figure()
    for file in files:
        shot = file["shot"]
        plt.plot(data[data["shot"]==shot]["wavelength"],data[data["shot"] == shot]["intensity"])
    plt.xlabel(r"$\lambda \rm \ [nm]$")
    plt.ylabel(r"$\rm Intensity \ [a.u.]$")
    plt.grid(True)
    # plt.show()


    plt.figure()
    for file in files:
        shot = file["shot"]
        plt.scatter(peaks[peaks["shot"]==shot]["wavelength"],peaks[peaks["shot"] == shot]["intensity"])
    plt.xlabel(r"$\lambda \rm \ [nm]$")
    plt.ylabel(r"$\rm Intensity \ [a.u.]$")
    plt.grid(True)
    
    # plt.show() 

    mpl.rcParams.update({"font.size": 15})

    peak_wavelengths = peaks["wavelength"].drop_duplicates() 
    # print(peak_wavelengths)
    sorted = peaks.sort_values("power")
    plt.figure()
    for l in peak_wavelengths:
        plt.scatter(sorted[sorted["wavelength"] == l]["power"],sorted[sorted["wavelength"] == l]["intensity"])
    plt.xlabel(r"$ \rm Power \ [W]$")
    plt.ylabel(r"$\rm Intensity \ [a.u.]$")
    plt.grid(True)
    plt.show() 