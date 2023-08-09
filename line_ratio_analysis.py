import pandas as pd
import matplotlib.pyplot as plt
from utils import get_files_and_params
from scipy.constants import c, k, h, e


if __name__ == '__main__':
    data = pd.DataFrame(columns=[ "file_name", "pressure", "peak wavelength", "peak intensity", "FWHM Doppler", "temperature"])
    dir = "Spectrum_data/Line_ratio"
    files = get_files_and_params(dir, format="gas={gas}_shot={shot}_power={power}W_HR4000_spectrum_raw_data.txt")
    