from master import  get_snapshot, get_snapshot_raw
import pandas as pd

from scipy.signal import find_peaks

print("Acquiring background noise, please turn the plasma off ... \n ")
W, I = get_snapshot_raw()
background = pd.DataFrame([(w, i) for w, i in zip(W, I)],
                          columns=["wavelength", "intensiy"])
print("Done!\n")

data = pd.DataFrame(columns=["shot", "file_name" "depth", "wavelength", "intensiy", "peaks"])

while True:
    shot = int(input("Enter shot number of measurment = "))
    depth = int(input("Enter depth [mm] = "))
    fullname = get_snapshot(name=f"{shot}")

    # Importing data 
    brut = pd.read_table(fullname, 
                         sep=" ", 
                         names=["wavelength", "intensiy"], 
                         skiprows=2)
    raw = [(shot, fullname, w, I) for w, I in zip(brut['wavelength'], brut["intensiy"])]
    data_ = pd.DataFrame(raw, columns=["shot", "file_name" "depth", "wavelength", "intensiy"])
    
    peaks, _ = find_peaks(data_["intesity"])
    data_["peaks"] = peaks

    # Filtering data
    data_["intensiy"] = data_["intensiy"] - background["intensiy"] # background["intensiy"][start-1:end+1]
    data = pd.concat([data, data_])


    stop = input("Continue measurments? Y/N :")
    if stop == 'N':
        break