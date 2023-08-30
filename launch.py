from master import acquire_live_data, acquire_live_data_inf_loop


### This code must be the simplest possible. A single function runs the whole spectrometer
###     Change the intergration time here depending on the spectrometer you are using
###     I suggest :
###                     - USB2000+ --> 2000 micro.s
###                     - HR4000   --> 4000 micro.s

acquire_live_data(show=True, save=False, int_time=4000)
# acquire_live_data_inf_loop(show=True, save=False)