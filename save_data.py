import os.path

def save_spectrum_data(name, data, wavelength, save_path=""):
    file_name = name + "_spectrum_raw_data.txt"
    completeName = os.path.join(save_path, file_name) 

    file = open(completeName, 'w')
    file.write(name + " " + "spectrum")
    file.write('\n')
    file.write("Wavelength [nm] // Intensity [u.a.] \n")

    for intensity, w in zip(data, wavelength):
        file.write(str(w) + " " + str(intensity))
        file.write('\n')
    file.close()

    return completeName