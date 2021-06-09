#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:00:19 2021

@author: Rodrigo
"""

from tkinter import StringVar, Tk, Label, Button, Entry, filedialog, OptionMenu

import numpy as np
import matplotlib.pyplot as plt

root = Tk()
root.title("Matplotlib GUI")
root.geometry("400x200")

# Function for the Button
def myClick():
    myLabel1 = Label(root, text= clicked.get())
    myLabel1.grid(row=2, column=0)

def graph():
    house_prices = np.random.normal(20000, 25000, 5000)
    plt.hist(house_prices.flatten(), bins=50)
    plt.show()


# Button Widget
myButton = Button(root, text="Show selection", padx=50, pady=15, command=graph, fg="white", bg="blue")


# Palce it on a grid
myButton.grid(row=0, column=0)

# Loop
root.mainloop()