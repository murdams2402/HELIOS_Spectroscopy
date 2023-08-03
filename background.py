from plot_data import plot_data
from save_data import save_spectrum_data
import seabreeze
seabreeze.use('cseabreeze')
from seabreeze.spectrometers import list_devices, Spectrometer
import matplotlib.pyplot as plt

from seabreeze.spectrometers import Spectrometer
spec = Spectrometer.from_first_available()

from datetime import datetime

from time import time

# import seabreeze.spectrometers as sb
# from seabreeze.spectrometers import Spectrometer
# spec = Spectrometer.from_first_available()

spec.integration_time_micros(20000)

plt.ion()
plt.figure(figsize=(18,8))
# manager = plt.get_current_fig_manager()
# manager.full_screen_toggle()  
start_time = time()
t = 0
try:
    while t < 7201:
        wavelengths, intensities = spec.spectrum()
        plt.plot(wavelengths,intensities, color='b')
        plt.xlabel(r"$\lambda \rm \ [nm]$")
        plt.ylabel(r"$\rm Intensity \ [a.u.]$")
        plt.grid(True)
        plt.pause(1)
        plt.cla()

        if int(t) % 900 == 0:
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%Hh%Mmin%Ss")     
            name = spec.model + '_' + dt_string
            save_spectrum_data(name, intensities, wavelengths[0], save_path='Background_data/')
        t = time() - start_time
except KeyboardInterrupt:
 # Exit on CTRL-C
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%Hh%Mmin%Ss")     
    name = spec.model + '_' + dt_string

    # save_spectrum_data(name, filtered_data, start, save_path='Spectrum_data/')
    plt.savefig('Spectrum_figures/' + name + 'spectrum.png')
        # plt.savefig(name + "_spectrum" + '.eps')
    pass
    
