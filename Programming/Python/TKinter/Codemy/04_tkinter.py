#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Tk, Label, Button, Entry
from tkinter.constants import W

root = Tk()

# Function for the Button
def myClick():
    myLabel1 = Label(root, text= myEntry.get())
    myLabel1.grid(row=2, column=0)


# Button Widget
myButton = Button(root, text="Enter your name", padx=50, pady=15, command=myClick, fg="white", bg="blue")

myEntry = Entry(root, width=15, bg="White", fg="Black")
myEntry.get()
myEntry.insert(0, "Enter your name here")

# Palce it on a grid
myEntry.grid(row=0, column=0)
myButton.grid(row=1, column=0)

# Loop
root.mainloop()