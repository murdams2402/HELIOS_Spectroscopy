import tkinter as tk
from tkinter import *

window = Tk()
text = tk.Label(text="Helios Spectrometer", background="#34A2FE")
text.pack(fill=tk.BOTH)

def frame(root, side):
   w = Frame(root)
   w.pack(side=side, expand=YES, fill=BOTH)
   return w
def button(root, side, text, command=None):
   w = Button(root, text=text, command=command)
   w.pack(side=side, expand=YES, fill=BOTH)
   return w

window.mainloop()