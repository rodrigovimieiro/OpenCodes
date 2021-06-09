#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Canvas, StringVar, Tk, Label, Button, Entry, filedialog, OptionMenu

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
root.title("Canvas Matplotlib GUI")
root.geometry("500x600")

# Function for the Button
def graph():
    house_prices = np.random.normal(20000, 25000, 5000)
    plot = fig.add_subplot(111)
    plot.hist(house_prices.flatten(), bins=50)
    fig.canvas.draw()
   

# Button Widget
myButton = Button(root, text="Plot histogram", padx=50, pady=15, command=graph, fg="white", bg="blue")

# Canvas Widget
fig = plt.figure(figsize=(5,5))
figCanvas = FigureCanvasTkAgg(fig, root)
myCanvas = figCanvas.get_tk_widget()

# Palce it on a grid
myButton.grid(row=0, column=0)
myCanvas.grid(row=1, column=0)

# Loop
root.mainloop()