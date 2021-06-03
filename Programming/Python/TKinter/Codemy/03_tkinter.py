#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Tk, Label, Button

root = Tk()

# Function for the Button
def myClick():
    myLabel1 = Label(root, text= "Look! I Clicked")
    myLabel1.grid(row=0, column=0)


# Button Widget
myButton = Button(root, text="Click me", padx=50, pady=15, command=myClick, fg="white", bg="blue")

# Palce it on a grid
myButton.grid(row=1, column=5)

# Loop
root.mainloop()