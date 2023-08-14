from plot_data import plot_data
from save_data import save_spectrum_data
import seabreeze
seabreeze.use('cseabreeze')
# seabreeze.use('pyseabreeze')
from seabreeze.spectrometers import list_devices, Spectrometer
import matplotlib.pyplot as plt

#from seabreeze.spectrometers import Spectrometer


from datetime import datetime




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
        plt.figure(figsize=(9,7))

    try :
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

    except KeyboardInterrupt:
        # Closing connection with spectrometer
        spec.close()
        pass

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
