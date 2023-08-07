import plot_config 
import matplotlib.pyplot as plt


def plot_data(x, y, x_label, y_label, title="", show=True):
    plt.figure
    plt.title(title)
    plt.plot(x, y)
    plt.xlabel(rf"{x_label}")
    plt.ylabel(rf"{y_label}")
    plt.grid(True)
    if show : plt.show()