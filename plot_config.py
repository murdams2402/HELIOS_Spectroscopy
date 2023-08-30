import matplotlib.pyplot as plt
import matplotlib as mpl

### This simple code allows to change the interpreter of the mpl and plt figures to
###     LaTeX interpreter and make hight quality graphs ;)

mpl.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["font.family"] = "serif"
plt.rcParams["figure.autolayout"] = True
mpl.rcParams.update({"font.size": 20})