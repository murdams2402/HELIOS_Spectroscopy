import tkinter as tk
from tkinter import *
import subprocess
import os
import signal
import sys

### This code manages the python interface. Follow the instructions commented below
###     such that the interface works on the computer you are running it on.


# Global variable to store the subprocess object
running_process = None

def launch_script():
    global running_process
    ### Use these lines if running on Windows
    # script_path = rf"C:\Users\Administrator\Desktop\HELIOS_Spectroscopy\launch.py"
    # running_process = subprocess.Popen(["python", script_path], 
    #                                         shell=True)

    ### Use these lines if running on MacOS
    script_path = "/Users/Mur/Desktop/EPFL/SummerInTheLab/Spectrometer/OceanOptics_Interface/HELIOS_Spectroscopy/launch.py"
    running_process = subprocess.Popen(["/usr/local/bin/python3 " + script_path], 
                                              shell=True)
    


def stop_script():
   global running_process
   if running_process is not None:
        if os.name == "nt": # Checking is running on Windows
            running_process.send_signal(signal.CTRL_C_EVENT) # sends Ctrl+C
            running_process.send_signal(signal.CTRL_C_EVENT) # sends Ctrl+C
            running_process.send_signal(signal.CTRL_C_EVENT) # sends Ctrl+C
            running_process.send_signal(signal.CTRL_C_EVENT) # sends Ctrl+C
            running_process.send_signal(signal.CTRL_C_EVENT) # sends Ctrl+C
            
        else :
            running_process.terminate()
        running_process = None


window = Tk()
# Disable automatic resizing of the window by widgets
window.pack_propagate(False)

## Neglect this part
# ##########################
# # Adding an image in the background

# # Load the image
# background_image = PhotoImage(file="Images/background.PNG")  

# # Create a canvas to display the image as background
# canvas = tk.Canvas(window, width=background_image.width(), height=background_image.height())
# canvas.pack()

# # Display the image on the canvas
# canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
# ##########################


def stop_program():
    stop_script()
    window.quit()

# Set the window size
window_width = 1400
window_height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Setting the title 
title = tk.Label(text="Helios Spectrometer", 
                background="#FFA500", 
                font=("Helvetica", 40),
                fg="black")
title.pack(fill=tk.BOTH)

# Defining the launch button
launch_button = tk.Button(window, 
                          text="Launch Spectrometer", 
                          font=("Helvetica", 20),
                          command=launch_script,
                          width=20, 
                          height=2,
                          background="green",
                          fg="black",
                          relief=tk.RAISED)
launch_button.pack(padx=10, pady=20, side=tk.LEFT)


# Defining the stop button
stop_button=  tk.Button(window, 
                          text="Stop Spectrometer", 
                          font=("Helvetica", 20),
                          command=stop_script,
                          width=20, 
                          height=2,
                          background="red",
                          fg="black",
                          relief=tk.RAISED)
stop_button.pack(padx=10, pady=20, side=tk.RIGHT)


description_label = tk.Label(window, 
                             text="Click the buttons bellow to launch or stop the spectrometer:",
                             font=("Helvetica", 20))
description_label.pack(pady=20)



# Loading an image of HELIOS for the interface (the placement is automatic)
image = PhotoImage(file="/Users/Mur/Desktop/EPFL/SummerInTheLab/Spectrometer/OceanOptics_Interface/HELIOS_Spectroscopy/Images/background.PNG")
### Use this line if using Windows
# image = PhotoImage(file=rf"C:\Users\Administrator\Desktop\HELIOS_Spectroscopy\Images\background.PNG")  

# Resize the image using subsample
resized_image = image.subsample(4, 4)
# Create a label to display the image
image_label = tk.Label(window, image=resized_image)
image_label.pack()
# image_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


window.mainloop()