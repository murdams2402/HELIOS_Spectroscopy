import matplotlib.pyplot as plt
import pandas as pd
import plot_config
from utils import get_files_and_params

dir = "Spectrum_data/Intensity_experiment"
files = get_files_and_params(dir, format="{shot}HR4000_spectrum_raw_data.txt")


# print(files)
plt.figure(figsize=(8,6))

background = pd.read_table("Background_data/HR4000_03_08_2023_13h58min08s_spectrum_raw_data.txt",
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)

plt.plot(background["wavelength"],background["intensity"])
plt.show()

plt.figure(figsize=(8,6))
for file in files:
    file_name = file["name"]
    data = pd.read_table(f"{dir}/{file_name}", 
                         sep=" ", 
                         names=["wavelength", "intensity"], 
                         skiprows=2)

    plt.plot(data["wavelength"],data["intensity"])
    plt.xlabel(r"$\lambda \rm \ [nm]$")
    plt.ylabel(r"$\rm Intensity \ [a.u.]$")
    plt.grid(True)
    
plt.show()