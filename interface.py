import tkinter as tk
from tkinter import *
import subprocess
import os
import signal
import sys

# Global variable to store the subprocess object
running_process = None

def launch_script():
    global running_process
    # script_path = "C:/Users/Administrator/Desktop/HELIOS_Spectroscopy/launch.py"
    script_path = "/Users/Mur/Desktop/EPFL/SummerInTheLab/Spectrometer/OceanOptics_Interface/HELIOS_Spectroscopy/launch.py"
    # user_input = entry.get()

    running_process = subprocess.Popen(["python", script_path], 
                                              shell=True)

   #  if user_input.strip():
   #       # Launch script with user input as an argument
   #       running_process = subprocess.Popen(["python ", script_path], 
   #                                            shell=True)
   #       # running_process = subprocess.Popen(["python", script_path, user_input], 
   #       #                                    capture_output=True, 
   #       #                                    check=False)
   #  else:
   #      print("Input is empty. Please provide a valid input.")
   #      pass

   #  running_process = subprocess.Popen(["python", script_path], 
   #                                     shell=True)
    # Get user input from Entry widget
    """ user_input = entry.get()
    
  # Check if the input is not empty or whitespace
    if user_input.strip():
         # Launch script with user input as an argument
         running_process = subprocess.Popen(["python", script_path, user_input], shell=True)
    else:
        # print("Input is empty. Please provide a valid input.")
        pass """
    # running_process.terminate()

def stop_script():
   global running_process
   if running_process:
        if os.name == "nt": # Checking is running on Windows
            running_process.send_signal(signal.CTRL_C_EVENT) # sends Ctrl+C
        else :
            running_process.terminate()
        running_process = None


window = Tk()
# Disable automatic resizing of the window by widgets
window.pack_propagate(False)

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


title = tk.Label(text="Helios Spectrometer", 
                background="#FFA500", 
                font=("Helvetica", 40),
                fg="black")
title.pack(fill=tk.BOTH)
# title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
# title.grid(row=0, column=0, columnspan=10, padx=30, pady=30)


# root = tk.Tk()
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
# launch_button.place(relx=0.7, rely=0.7, anchor=tk.W)
# launch_button.grid(row=1, column=0, padx=10)


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
# stop_button.place(relx=0.7, rely=0.7, anchor=tk.E)
# stop_button.grid(row=1, column=1, padx=10)

description_label = tk.Label(window, 
                             text="Click the buttons bellow to launch or stop the spectrometer:",
                             font=("Helvetica", 20))
description_label.pack(pady=20)
# description_label.place(relx=0.7, rely=0.7, anchor=tk.CENTER)
# description_label.grid(row=2, column=0, columnspan=2, padx=20, pady=20)


# Load the image
image = PhotoImage(file="Images/background.PNG") 
# Resize the image using subsample
resized_image = image.subsample(4, 4)
# Create a label to display the image
image_label = tk.Label(window, image=resized_image)
image_label.pack()
# image_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Create an Entry widget for user input
entry_label = Label(window, text="Enter intergration time [micro seconds]: ")
entry_label.pack()
entry = tk.Entry(window)
entry.pack()

# def frame(root, side):
#    w = Frame(root)
#    w.pack(side=side, expand=YES, fill=BOTH)
#    return w
# def button(root, side, text, command=None):
#    w = Button(root, text=text, command=command)
#    w.pack(side=side, expand=YES, fill=BOTH)
#    return w

window.mainloop()