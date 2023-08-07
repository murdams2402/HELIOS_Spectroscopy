from master import  get_snapshot, get_snapshot_raw
import pandas as pd
import matplotlib.pyplot as plt

# Opening background noise
background = pd.read_table("Background_data/HR4000_03_08_2023_13h58min08s_spectrum_raw_data.txt",
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)


data = pd.DataFrame(columns=[ "file_name", "pressure", "wavelength", "intensity"])

while True:
    pressure = float(input("Enter pressure [mbar] = "))
    fullname = get_snapshot(path='Spectrum_data/Temperature_experiment/',
                            name=f"{pressure}")

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
for filename in data["file_name"]:
    plt.plot(data["wavelength"],data["intensity"])
    plt.xlabel(r"$\lambda \rm \ [nm]$")
    plt.ylabel(r"$\rm Intensity \ [a.u.]$")
    plt.grid(True)  
plt.show()        