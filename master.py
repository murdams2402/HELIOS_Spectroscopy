from plot_data import plot_data
from save_data import save_spectrum_data
import seabreeze

seabreeze.use('cseabreeze')
### If the code bugs, maybe change the line above to the line below (cseabreeze to pyseabreeze)
# seabreeze.use('pyseabreeze')

from seabreeze.spectrometers import list_devices, Spectrometer
import matplotlib.pyplot as plt

#from seabreeze.spectrometers import Spectrometer


from datetime import datetime


### This code manages the communiocation between the computer and the spectrometer. Make sure you've
###     downloaded pyusb, libsub and the seabreeze python libraries in order to allow the 
###     communication to be allowed.



def get_spectrometer():
    spec = Spectrometer.from_first_available()
    return spec

def get_snapshot_raw(int_time=2000):
    spec = get_spectrometer()
    spec.integration_time_micros(int_time)
    wavelengths, intensities = spec.spectrum()
    spec.close()
    return wavelengths, intensities

def get_snapshot(int_time=2000, path='Spectrum_data/', name=''):
    # Opening the spectrometer
    spec = get_spectrometer()
    spec.integration_time_micros(int_time)
    # Acquireing data
    wavelengths, intensities = spec.spectrum()
    # Saving the data in the folder
    dt_string = '' #now.strftime("%d_%m_%Y_%Hh%Mmin%Ss")     
    name += spec.model # + '_' + dt_string
    # Closing connection with spectrometer
    spec.close()
    # Saving data and returning the file's full name
    return save_spectrum_data(name, intensities, wavelengths, save_path=path)


def acquire_live_data(int_time=2000, show=False, save=False, path='Spectrum_data/'):
    spec = get_spectrometer()
    spec.integration_time_micros(int_time)
    
    if show:
        plt.ion()
        # plt.figure(figsize=(9,7))
        fig, ax = plt.subplots(figsize=(10,7.5))
        # plt.rcParams["figure.figsize"] = [9.00, 6.50]
        # im = plt.imread("/Users/Mur/Desktop/EPFL/SummerInTheLab/Spectrometer/OceanOptics_Interface/HELIOS_Spectroscopy/Images/visible-light-spectrum.jpg")
        # newax = fig.add_axes([0.09, 0.65, 0.4, 0.4], anchor='NW')
        # newax.imshow(im)
        # newax.axis('off')
    try :
        while True:
            wavelengths, intensities = spec.spectrum()
            filter = wavelengths > 200 # nm
            filtered_wavelengths = wavelengths[filter]
            filtered_intensities = intensities[filter]
            if show:
                ax.plot(filtered_wavelengths, filtered_intensities, color='b')
                plt.xlabel(r"$\lambda \rm \ [nm]$")
                plt.ylabel(r"$\rm Intensity \ [a.u.]$")
                ax.grid(True)
                plt.pause(0.6)
                ax.cla()
            
            if save:
                dt_string = now.strftime("%d_%m_%Y_%Hh%Mmin%Ss")     
                name = spec.model + '_' + dt_string
                _ = save_spectrum_data(name, intensities, wavelengths, save_path=path)
                plt.savefig('Spectrum_figures/' + name + 'spectrum.png')

    except KeyboardInterrupt:
        # Closing connection with spectrometer
        spec.close()
        # raise KeyboardInterrupt




def acquire_live_data_inf_loop(int_time=2000, show=False, save=False, path='Spectrum_data/'):
    spec = get_spectrometer()
    spec.integration_time_micros(int_time)
    
    if show:
        plt.ion()
        plt.figure(figsize=(9,7))


    while True:
        wavelengths, intensities = spec.spectrum()
        if show:
            plt.plot(wavelengths,intensities, color='b')
            plt.xlabel(r"$\lambda \rm \ [nm]$")
            plt.ylabel(r"$\rm Intensity \ [a.u.]$")
            plt.grid(True)
            plt.pause(1.5)
            plt.cla()
        
        if save:
            dt_string = now.strftime("%d_%m_%Y_%Hh%Mmin%Ss")     
            name = spec.model + '_' + dt_string
            _ = save_spectrum_data(name, intensities, wavelengths, save_path=path)
            plt.savefig('Spectrum_figures/' + name + 'spectrum.png')




if __name__ == '__main__':

    spec = Spectrometer.from_first_available()
    # import seabreeze.spectrometers as sb
    # from seabreeze.spectrometers import Spectrometer
    # spec = Spectrometer.from_first_available()
    print(spec.model)
    spec.integration_time_micros(20000)

    show = True

    plt.ion()
    plt.figure(figsize=(18,8))
    # manager = plt.get_current_fig_manager()
    # manager.full_screen_toggle()  

    try:
        while True:
            if show:
                wavelengths, intensities = spec.spectrum()
                plt.plot(wavelengths,intensities, color='b')
                plt.xlabel(r"$\lambda \rm \ [nm]$")
                plt.ylabel(r"$\rm Intensity \ [a.u.]$")
                plt.grid(True)
                plt.pause(1)
                plt.cla()
    except KeyboardInterrupt:
    # Exit on CTRL-C
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%Hh%Mmin%Ss")     
        # name = spec.model() + '_' + dt_string
        name = spec.model + '_' + dt_string

        # save_spectrum_data(name, filtered_data, start, save_path='Spectrum_data/')
        if show: 
            plt.savefig('Spectrum_figures/' + name + 'spectrum.png')
            # plt.savefig(name + "_spectrum" + '.eps')
        pass
        _ =  save_spectrum_data(name, intensities, wavelengths, save_path='Spectrum_data/')
        
        
        #raise KeyboardInterrupt
