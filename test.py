from plot_data import plot_data
import seabreeze
seabreeze.use('cseabreeze')
from seabreeze.spectrometers import list_devices, Spectrometer

from seabreeze.spectrometers import Spectrometer
spec = Spectrometer.from_first_available()


# import seabreeze.spectrometers as sb
# from seabreeze.spectrometers import Spectrometer
# spec = Spectrometer.from_first_available()
spec
spec.integration_time_micros(20000)
wavelengths, intensities = spec.spectrum()
plot_data(wavelengths, intensities, rf"$\lambda [\rm nm]$", "Intensity [a.u.]")
