import matplotlib.pyplot as plt
import pandas as pd
import plot_config
from utils import get_files_and_params

from scipy.integrate import trapezoid
from scipy.signal import find_peaks

dir = "Spectrum_data/Intensity_experiment"
files = get_files_and_params(dir, format="{shot}HR4000_spectrum_raw_data.txt")

# # print(files)
# plt.figure(figsize=(8,6))

# background = pd.read_table("Background_data/HR4000_03_08_2023_14h28min08s_spectrum_raw_data.txt",
#                             sep=" ", 
#                             names=["wavelength", "intensity"], 
#                             skiprows=2)

# plt.plot(background["wavelength"],background["intensity"])
# # plt.show()

depth = 23
delta_x = 195.74304201014752 - 195.47341553816543

peaks = pd.DataFrame(columns=["shot", "depth", "wavelength", "intensity", "normalized intensity"])

area = pd.DataFrame(columns=["shot", "depth", "area under full curve"])

plt.figure(figsize=(8,6))
for file in files:
        if int(file["shot"]) > 129 :
            file_name = file["name"]
            spectrum = pd.read_table(f"{dir}/{file_name}", 
                                sep=" ", 
                                names=["wavelength", "intensity"], 
                                skiprows=2)
            plt.plot(spectrum["wavelength"], spectrum["intensity"])

            # Getting every interesting peak
            max_peaks = spectrum.max()
            max_max_peak = max_peaks.max()
            peaks_info = find_peaks(x=spectrum["intensity"], height=[1000, max_peaks["intensity"]])
            peaks_ = spectrum.filter(items=peaks_info[0], axis=0)

            temp = [(file["shot"], depth, w, I, I/max_max_peak) for w, I in zip(peaks_["wavelength"], peaks_["intensity"])]
            temp = pd.DataFrame(temp, columns=["shot", "depth", "wavelength", "intensity", "normalized intensity"])
            peaks = pd.concat([peaks, temp])

            I = trapezoid(spectrum["intensity"], spectrum["wavelength"], dx=delta_x)
            temp = pd.DataFrame([(file["shot"], depth, I)], columns=["shot", "depth", "area under full curve"])
            area = pd.concat([area, temp])

            depth += 5

plt.xlabel(r"$\lambda \rm \ [nm]$")
plt.ylabel(r"$\rm Intensity \ [a.u.]$")
plt.grid(True)      
# plt.show()

# peaks = peaks.sort_values("power")
peak_wavelengths = peaks["wavelength"].drop_duplicates()
peak_wavelengths = peak_wavelengths.sort_values()

plt.figure()
l_max = peak_wavelengths[11]
plt.scatter(peaks[peaks["wavelength"] == l_max]["depth"], peaks[peaks["wavelength"] == l_max]["intensity"])
plt.xlabel(r"$ d \rm \ [mm]$")
plt.ylabel(r"$\rm Intensity \ [a.u.]$")
plt.grid(True)      


plt.figure()
for l in peak_wavelengths :
    plt.scatter(peaks[peaks["wavelength"] == l]["depth"], peaks[peaks["wavelength"] == l]["normalized intensity"])
plt.xlabel(r"$ d \rm \ [mm]$")
plt.ylabel(r"$\rm Normalized Intensity $")
plt.grid(True)  


plt.figure()
plt.scatter(area["depth"], area["area under full curve"])
plt.xlabel(r"$ d \rm \ [mm]$")
plt.ylabel(r"$\rm Area\ under\ spectrum \ [a.u.]$")
plt.grid(True)  

plt.show()