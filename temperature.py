from master import  get_snapshot, get_snapshot_raw
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_files_and_params
from scipy.constants import c, k
m_Ne = 3.3509e-26 # kg
from numpy import log, sqrt, absolute
from utils import Voigt, gaussian, lorenzian
from scipy.optimize import curve_fit

from scipy.signal import peak_widths, find_peaks

# Opening background noise
background = pd.read_table("Background_data/HR4000_03_08_2023_13h58min08s_spectrum_raw_data.txt",
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)

def acquire_spectra(gas="Neon_"):
    data = pd.DataFrame(columns=[ "file_name", "pressure", "wavelength", "intensity"])

    while True:
        pressure = float(input("Enter pressure [mbar] = "))
        fullname = get_snapshot(path='Spectrum_data/Temperature_experiment/',
                                name=gas+f"pressure={pressure}_")

        # Importing data 
        brut = pd.read_table(fullname, 
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)
        raw = [(fullname, pressure, w, I) for w, I in zip(brut['wavelength'], brut["intensity"])]
        data_ = pd.DataFrame(raw, columns=[ "file_name", "pressure", "wavelength", "intensity"])
        # Filtering data
        data_["intensity"] = data_["intensity"] # - background["intensiy"] # background["intensiy"][start-1:end+1]
        
        data = pd.concat([data, data_])

        stop = input("Continue measurments? Y/N :")
        if stop == 'N':
            break


    plt.figure(figsize=(8,6))
    for file_name in data["file_name"]:
        plt.plot(data["file_name"==file_name]["wavelength"],data["file_name"==file_name]["intensity"])
        plt.xlabel(r"$\lambda \rm \ [nm]$")
        plt.ylabel(r"$\rm Intensity \ [a.u.]$")
        plt.grid(True)  
    plt.show()        


delta_lambda = 0.26962647198209 # [nm]
Delta_Lamda_Apparatus = 1 # [nm] Apparatus-linked broadening : FWHM for HR4000

if __name__ == '__main__':
    temperature = pd.DataFrame(columns=[ "file_name", "pressure", "peak wavelength", "FWHM Doppler", "temperature"])
    dir = "Spectrum_data/Temperature_experiment"
    files = get_files_and_params(dir, format="Neon_pressure={pressure}_HR4000_spectrum_raw_data.txt")
    plt.figure(figsize=(8,6))
    raw = pd.DataFrame(columns=[ "file_name", "pressure", "wavelength", "frequency", "intensity"])
    for file in files:
        file_name = file["name"]
        p = file["pressure"]
        data = pd.read_table(f"{dir}/{file_name}", 
                            sep=" ", 
                            names=["wavelength", "intensity"], 
                            skiprows=2)
        
        temp = [(file_name, p, w, c/(w*1e-9), I) for w, I in zip(data["wavelength"], data["intensity"])]
        temp = pd.DataFrame(temp, columns=[ "file_name", "pressure", "wavelength", "frequency", "intensity"])
        raw = pd.concat([raw, temp])

        max_peaks = data.max()
        # print(max_peaks["intensity"])

        data["frequency"] = c/(data["wavelength"]*1e-9)

        plt.plot(data["wavelength"],data["intensity"])
        plt.xlabel(r"$\lambda \rm \ [nm]$")
        plt.ylabel(r"$\rm Intensity \ [a.u.]$")
        plt.grid(True)

        # plt.plot(data["frequency"],data["intensity"])
        # plt.xlabel(r"$\nu \rm \ [Hz]$")
        # plt.ylabel(r"$\rm Intensity \ [a.u.]$")
        # plt.grid(True)

        # Using scipy's function that retreaves the FWHM of the specified peaks
        peaks_ = find_peaks(x=data["intensity"], height=[1000, max_peaks["intensity"]])
        widths = peak_widths(x=data["intensity"], peaks=peaks_[0], rel_height=0.5)
        wavelengths = data.filter(items=peaks_[0], axis=0)
        
        # Computing the FWHM of each peak
        Delta_Lamda_doppler = [ sqrt(absolute((fwhm*delta_lambda)*(fwhm*delta_lambda) - Delta_Lamda_Apparatus*Delta_Lamda_Apparatus)) for fwhm in widths[0]]
        Tg = [ ((delta/l0)*(delta/l0))*(c*c*m_Ne)/(8*k*log(2)) for delta, l0 in zip(Delta_Lamda_doppler, wavelengths["wavelength"])]
        
        # Saving data for later analysis
        brut = [(file_name, p, peak, wdth, tg) for wdth, peak, tg in zip(Delta_Lamda_doppler, wavelengths["wavelength"], Tg)]
        temperature_ = pd.DataFrame(brut, columns=[ "file_name", "pressure", "peak wavelength", "FWHM Doppler", "temperature"])
        temperature = pd.concat([temperature, temperature_])
    # plt.show()


    # plt.figure(figsize=(8,6))
    # for file in temperature["file_name"]:
    #         plt.scatter(temperature[temperature["file_name"]== file]["pressure"], temperature[temperature["file_name"]== file]["temperature"])
    #         plt.xlabel(r"$p \rm \ [mbar]$")
    #         plt.ylabel(r"$\rm T \ [?]$")
    #         plt.grid(True)
    # plt.show()

    show = True
    if show :
        plt.figure(figsize=(8,6))
        for peak in temperature["peak wavelength"]:
                plt.scatter(x=temperature[temperature["peak wavelength"]== peak]["pressure"], y=temperature[temperature["peak wavelength"]== peak]["temperature"])
                plt.xlabel(r"$p \rm \ [mbar]$")
                plt.ylabel(r"$\rm T \ [K]$")
                plt.grid(True)
        plt.show()

    ##################################################################################################
    # Trying an analysis "by hand"
    window = [[584.6, 587], [624, 628], [646, 652.6], [690, 697], [700, 708]] # [639, 645]

    for i in range(0, len(window)):
        filtered_raw = raw[ (raw["wavelength"] >= window[i][0]) & (raw["wavelength"] <= window[i][1]) ]
        # print(filtered_raw)

        FWHM_Gauss = pd.DataFrame(columns=["pressure", "FWHM", "temperature"])
        FWHM_Lorenzian = []

        # print(filtered_raw["file_name"])

        plt.figure(figsize=(8,6))
        for file in files:
            file_name = file["name"]

            plt.plot(filtered_raw[filtered_raw["file_name"] == file_name]["wavelength"],filtered_raw[filtered_raw["file_name"] == file_name]["intensity"])
            plt.xlabel(r"$\lambda \rm \ [nm]$")
            plt.ylabel(r"$\rm Intensity \ [a.u.]$")
            plt.grid(True)

            x0 = absolute(window[i][1] + window[i][0])*0.5
            max_peak = filtered_raw[filtered_raw["file_name"] == file_name]["intensity"].max()
            
            # The FWHM of a Gaussian is equal to FWHM = sigma*sqrt( 8*ln(2) )
            starting_points = [max_peak, x0, 0.5]
            popt_Gauss, covopt_Gauss = curve_fit(gaussian, 
                                                filtered_raw[filtered_raw["file_name"] == file_name]["wavelength"],
                                                filtered_raw[filtered_raw["file_name"] == file_name]["intensity"],
                                                p0=starting_points)
            sigma = 1/sqrt(2*popt_Gauss[2])
            fwhm_gauss = sigma*sqrt(8*log(2))
            doppler_fwhm = sqrt(fwhm_gauss*fwhm_gauss - Delta_Lamda_Apparatus*Delta_Lamda_Apparatus)
            temp__ = pd.DataFrame([(file["pressure"], fwhm_gauss, ((doppler_fwhm/popt_Gauss[1])*(doppler_fwhm/popt_Gauss[1]))*(c*c*m_Ne)/(8*k*log(2)) )], columns=["pressure", "FWHM", "temperature"])
            FWHM_Gauss = pd.concat([FWHM_Gauss, temp__])
            


            # # The FWHM of a Lorenzian is two times it's parameter b = \gamma (see function definition in utils.py)
            # starting_points = [x0, max_peak*0.5]
            # popt_Lorenzian, covopt_Lorenzian = curve_fit(lorenzian, 
            #                                         filtered_raw[filtered_raw["file_name"] == file_name]["wavelength"],
            #                                     filtered_raw[filtered_raw["file_name"] == file_name]["intensity"],
            #                                     p0=starting_points)
            # FWHM_Lorenzian.append(2*popt_Lorenzian[1])
            

            # break
        plt.show()


        plt.figure(figsize=(8,6))
        # print(FWHM_Gauss)
        plt.plot(FWHM_Gauss["pressure"],FWHM_Gauss["temperature"])
        plt.xlabel(r"$ p \rm \ [mbar]$")
        plt.ylabel(r"$\rm T \ \rm [K]$")
        plt.grid(True)
        plt.show()

    # plt.show()
