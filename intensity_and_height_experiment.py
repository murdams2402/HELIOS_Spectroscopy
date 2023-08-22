import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import get_files_and_params
from scipy.signal import find_peaks
import plot_config

filtered_data = pd.DataFrame(columns=["model", "shot", "gas", "height", "RF power", "massflow", "coil current", "wavelength", "intensity"])
peaks = pd.DataFrame(columns=["model", "shot", "gas", "height", "RF power", "massflow", "coil current", "wavelength", "intensity", "normalized intensity"])

## Opening background noise data file
file_name = 'shot=0_gas=Background_height=80_RF=0.0W_massflow=0_coils=0.0A_HR4000_spectrum_raw_data.txt'
background = pd.read_table(f"Background_data/{file_name}", 
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)



dir = "Spectrum_data/Intensity_experiment_2"
files = get_files_and_params(dir, format="shot={shot}_gas={gas}_height={height}_RF={RF_power}W_massflow={mass}_coils={coils}A_{model}_spectrum_raw_data.txt")
#     (Example of file names)             shot=165_gas=Ne_hight=60_RF=243.0W_massflow=8000_coils=0.0A_HR4000_spectrum_raw_data.txt
#                                         shot=82_gas=Ne_height=40_RF=249.0W_massflow=8000_coils=100.0A_HR4000_spectrum_raw_data.txt

for  file in files:
        file_name = file["name"]
        
        ## Opening acquired spectrum
        spectrum = pd.read_table(f"{dir}/{file_name}", 
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)
        
        
        ## Filtering data (taking out the background noise)
        temp = [(file["model"], int(file["shot"]), file["gas"], int(file["height"]), float(file["RF_power"]), int(file["mass"]), float(file["coils"]), w, I-b) for w, I, b in zip(spectrum["wavelength"], spectrum["intensity"], background["intensity"])]
        temp = pd.DataFrame(temp, 
                            columns=["model", "shot", "gas", "height", "RF power", "massflow", "coil current", "wavelength", "intensity"])
        filtered_data = pd.concat([filtered_data, temp])

        ## Isolating the spectrum's peaks
        max_peaks = spectrum.max()
        max_max_peak = max_peaks.max()
        peaks_info = find_peaks(x=spectrum["intensity"], height=[960, max_peaks["intensity"]])
        peaks_ = spectrum.filter(items=peaks_info[0], axis=0)

        bck_temp = background.filter(items=peaks_info[0], axis=0)
        temp = [(file["model"], int(file["shot"]), file["gas"], int(file["height"]), float(file["RF_power"]), int(file["mass"]), float(file["coils"]), w, I-b, (I-b)/(max_max_peak-b)) for w, I, b in zip(peaks_["wavelength"], peaks_["intensity"], bck_temp["intensity"])]
        temp = pd.DataFrame(temp, columns=["model", "shot", "gas", "height", "RF power", "massflow", "coil current", "wavelength", "intensity", "normalized intensity"])
        peaks = pd.concat([peaks, temp])




currents = [0.0, 50, 80.1, 100.0]
gases = filtered_data["gas"].drop_duplicates()
heights = [35, 40, 50, 70, 80, 90, 110]
RF_power = filtered_data["RF power"].drop_duplicates()
peak_wavelengths = peaks["wavelength"].drop_duplicates() 

show_spectra = True

for gas in gases:
    temp = filtered_data[filtered_data["gas"]==gas]
    # fig, axs = plt.subplots(2, 2)
    # i, j = 0, 0
    for I in currents:
        #######################################################
        # Ploting all different spectrums
        if show_spectra:
            plt.figure()
            # axs[i, j].set_title(rf"{gas}: $ I = {I}\pm 0.4 \rm\ A$")
            plt.title(rf"{gas}: $ I = {I}\pm 0.4 \rm\ A$")
            for file in files:
                coils = float(file["coils"])
                if abs(coils - I) < 0.5 : 
                    shot = int(file["shot"])
                    plt.plot(temp[temp["shot"]==shot]["wavelength"],
                            temp[temp["shot"] == shot]["intensity"])
                    # axs[i, j].plot(temp[temp["shot"]==shot]["wavelength"],
                    #          temp[temp["shot"] == shot]["intensity"])
            # match i, j:
            #     case 0,0:
            #         j += 1
            #     case 0, 1:
            #         i = 1
            #         j = 0
            #     case 1, 0:
            #         j = 1
        # for ax in axs.flat:
        #     ax.set(ylabel=r"$\rm Intensity \ [a.u.]$")
            plt.xlabel(r"$\lambda \rm \ [nm]$")
            plt.ylabel(r"$\rm Intensity \ [a.u.]$")
            plt.grid(True)

        #######################################################
        # Ploting 
        
        peaks_temp = peaks[(peaks["gas"] == gas) & (abs(peaks["coil current"] - I) < 0.5) & (abs(peaks["RF power"] - 250) < 10)]
        plt.figure()
        plt.title(rf"{gas}: $ I = {I}\pm 0.4 \rm\ A$")
        for l in peak_wavelengths:
            plt.scatter(peaks_temp[abs(peaks_temp["wavelength"] - l) < 0.5]["height"],
                        peaks_temp[abs(peaks_temp["wavelength"] - l) < 0.5]["normalized intensity"])
        plt.xlabel(r"$ z \rm \ [mm]$")
        plt.ylabel(r"$\rm Intensity \ [a.u.]$")
        plt.grid(True)


show_relative_int = False

if show_relative_int:
    for height in heights:
        for gas in gases:
            temp = peaks[(peaks["gas"]==gas) & (peaks["height"] == height)]
            # temp = temp[temp["height"] == height]
            plt.figure()
            plt.title(rf"{gas}")
            for l in peak_wavelengths:
                plt.scatter(temp[temp["wavelength"] == l]["coil current"],
                            temp[temp["wavelength"] == l]["normalized intensity"])   
            plt.xlabel(r"$I \rm\ [A]$")
            plt.ylabel(r"$\rm Intensity \ [a.u.]$")
            plt.grid(True)      





plt.show()