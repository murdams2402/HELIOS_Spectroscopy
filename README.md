# HELIOS_Spectroscopy
## Introduction and easy launching
This code is destined to the automatation of the OceanInsight (OceanOptics) spectrometer added to the HELIOS experiment of the Swiss Plasma Center (SPC). Using the open-source SEABREEZE python library, this 100% python code allows an easy visualisation of HELIOS' cold plasma spectra via a minimalistic user-friendly interface. 

In order to run the simplified user interface, simply run the `interface.py` python scritp from your terminal. 

> [!IMPORTANT]
> Note that it is necessary to install [python](https://www.python.org/downloads/) (3.10 or 3.11) beforehand as well as the [SEABREEZE](https://github.com/ap--/python-seabreeze#changes) python library, as well as [pyusb](https://pypi.org/project/pyusb/) and [libusb](https://pypi.org/project/libusb/). 

Once python is downloaded on your computer, open a terminal and enter the following line on your terminal:

```
git clone https://github.com/murdams2402/HELIOS_Spectroscopy.git
```

Once the file is imported, open the `HELIOS_Spectroscopy` folder and launch `interface.py` by typing :
```
python interface.py
# or the following 
python3 interface.py
``` 
 Once the code is launched, a long window should appear, such as the one below: 

![Image of the user interface](/Images/interface.png)

In order to visualise the spectrum, click once on the `Launch Spectrometer` button. If nothing happens, make sure that your spectrometer is properly connected to your computer.

## Spectral analysis scripts

Some of the codes you may find in this repository have nothing to do with the actual implementation of the interface. In fact, they are usefull for some qualitative spectral analysis and data acquiremnets from the spectra seen by the OceanInsight spectrometers. Feel free to use these codes by changing the plots, taking more raw data measurments, etc. The scripts used to acquire data are the following 
* `background.py`
* `intensities.py`
* `line_ratio.py`

and the ones used to analyse the data are the following

* `doppler_broadening.py`
* `intensity_and_height_experiment.py`
* `light_profile.py`
* `line_ratio_analysis.py`
* `temperature.py`

> [!NOTE]
> When analysing data, the `.gitignore` file will not you to add any JupyterNotebook file to the repository. 

## Data and figures

In this repository, in addition to the interface and analysis python scripts, you will also find examples of raw spectrum data in the `Spectrum_data` & `Background_data` files and some figures in the `Spectrum_figures` that allow a visualisation of the spectrums, line-ratio plots or background noise.