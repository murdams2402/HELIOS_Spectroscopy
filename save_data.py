import os.path

def save_spectrum_data(model_name, data, start, save_path=""):
    file_name = model_name + "_spectrum_raw_data.txt"
    completeName = os.path.join(save_path, file_name) 

    file = open(completeName, 'w')
    file.write(model_name + " " + "spectrum")
    file.write('\n')
    file.write("Wavelength [nm] // Intensity [u.a.] \n")
    i=start
    for line in data:
        file.write(str(i) + " " + str(line))
        file.write('\n')
        i += 1
    file.close()