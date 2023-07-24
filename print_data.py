
def save_spectrum_data(model_name, data, start):
    file_name = model_name + "_spectrum_raw_data.txt"
    with open(file_name, 'w') as file:
        file.write(model_name + " " + "spectrum")
        file.write('\n')
        file.write("Wavelength [nm] // Intensity [u.a.] \n")
        i=start
        for line in data:
            file.write(str(i) + " " + str(line))
            file.write('\n')
            i += 1
    file.close()