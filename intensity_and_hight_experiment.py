import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import get_files_and_params
import plot_config

data = pd.DataFrame(columns=["model", "shot", "gas", "height", "RF power", "massflow", "coil current", "wavelength", "intensity"])
filtered_data = data

## Opening background noise data file
file_name = 'shot=0_gas=Background_height=80_RF=0.0W_massflow=0_coils=0.0A_HR4000_spectrum_raw_data.txt'
background = pd.read_table(f"Background_data/{file_name}", 
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)



dir = "Spectrum_data/Intensity_experiment_2"
files = get_files_and_params(dir, format="shot={shot}_gas={gas}_height={height}_RF={RF_power}W_massflow={mass}_coils={coils}A_{model}_spectrum_raw_data.txt")
#                                         shot=165_gas=Ne_hight=60_RF=243.0W_massflow=8000_coils=0.0A_HR4000_spectrum_raw_data.txt
#                                         shot=82_gas=Ne_height=40_RF=249.0W_massflow=8000_coils=100.0A_HR4000_spectrum_raw_data.txt

for  file in files:
        file_name = file["name"]
        
        ## Opening acquired spectrum
        spectrum = pd.read_table(f"{dir}/{file_name}", 
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)
        temp = [(file["model"], int(file["shot"]), file["gas"], int(file["height"]), float(file["RF_power"]), int(file["mass"]), float(file["coils"]), w, I) for w, I in zip(spectrum["wavelength"], spectrum["intensity"])]
        temp = pd.DataFrame(temp, 
                            columns=["model", "shot", "gas", "height", "RF power", "massflow", "coil current", "wavelength", "intensity"])
        data = pd.concat([data, temp])
        
        ## Filtering data (taking out the background noise)
        temp = [(file["model"], int(file["shot"]), file["gas"], int(file["height"]), float(file["RF_power"]), int(file["mass"]), float(file["coils"]), w, I-b) for w, I, b in zip(spectrum["wavelength"], spectrum["intensity"], background["intensity"])]
        temp = pd.DataFrame(temp, 
                            columns=["model", "shot", "gas", "height", "RF power", "massflow", "coil current", "wavelength", "intensity"])
        filtered_data = pd.concat([filtered_data, temp])




currents = [0.0, 50, 80.1, 100.0]
gases = ['Ne', 'Ar']

for gas in gases:
    temp = data[data["gas"]==gas]
    for I in currents:
        plt.figure()
        plt.title(rf"{gas}: $ I = {I}\pm 0.4 \rm\ A$")
        for file in files:
            coils = float(file["coils"])
            if abs(coils - I) < 0.5 : 
                shot = int(file["shot"])
                plt.plot(temp[temp["shot"]==shot]["wavelength"],
                         temp[temp["shot"] == shot]["intensity"])
        plt.xlabel(r"$\lambda \rm \ [nm]$")
        plt.ylabel(r"$\rm Intensity \ [a.u.]$")
        plt.grid(True)


plt.show()