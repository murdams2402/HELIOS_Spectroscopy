from master import acquire_live_data, acquire_live_data_inf_loop
""" import sys
import getopt
argv = sys.argv[1:]
optons, args = getopt.getopt(argv, "") """

# import sys

# from simple_spectrometer import acquire
# acquire(show=True, verbose=True, integration_time=4500)
# int_time = int(input())
# print(sys.argv)
acquire_live_data(show=True, save=False, int_time=4000)
# acquire_live_data_inf_loop(show=True, save=False)