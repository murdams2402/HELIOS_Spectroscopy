# HELIOS_Spectroscopy
## Introduction and easy launching
This code is destined to the automatation of the OcenView (OceanOptics) spectrometer added to the HELIOS experiment of the Swiss Plasma Center (SPC). Using the open-source SEABREEZE python library, this 100% python code allows an easy visualisation of HELIOS' cold plasma spectra via a kinimal user-friendly interface. 

In order to run the simplified user interface, simply run the `interface.py` python scritp from your terminal. 

> [!IMPORTANT]
>Note that it is necessary to install [python](https://www.python.org/downloads/) (3.10 or 3.11) beforehand as well as the [SEABREEZE](https://github.com/ap--/python-seabreeze#changes) python library, as well as [pyusb](https://pypi.org/project/pyusb/) and [libusb](https://pypi.org/project/libusb/). 

Once python is downloaded on your computer, open a terminal and run the following script:

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

## Spectral analysis codes