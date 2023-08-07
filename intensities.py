from master import  get_snapshot, get_snapshot_raw
import pandas as pd

from scipy.signal import find_peaks

#print("Acquiring background noise, please turn the plasma off ... \n ")
#W, I = get_snapshot_raw()
#background = pd.DataFrame([(w, i) for w, i in zip(W, I)],
#                          columns=["wavelength", "intensiy"])
#print("Done!\n")

data = pd.DataFrame(columns=["shot", "file_name" "depth", "wavelength", "intensity"])

while True:
    shot = int(input("Enter shot number of measurment = "))
    depth = int(input("Enter depth [mm] = "))
    fullname = get_snapshot(path='Spectrum_data/Intensity_experiment/',name=f"{shot}")

    # Importing data 
    brut = pd.read_table(fullname, 
                         sep=" ", 
                         names=["wavelength", "intensity"], 
                         skiprows=2)
    raw = [(shot, fullname, w, I) for w, I in zip(brut['wavelength'], brut["intensity"])]
    data_ = pd.DataFrame(raw, columns=["shot", "file_name" "depth", "wavelength", "intensity"])
    
    # peaks, _ = find_peaks(data_["intensity"])
    #data_["peaks"] = peaks

    # Filtering data
    data_["intensity"] = data_["intensity"] # - background["intensiy"] # background["intensiy"][start-1:end+1]
    data = pd.concat([data, data_])


    stop = input("Continue measurments? Y/N :")
    if stop == 'N':
        break