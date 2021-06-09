#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:00:19 2021

@author: Rodrigo
"""

from tkinter import StringVar, Tk, Label, Button, Entry, filedialog, OptionMenu

root = Tk()

# Function for the Button
def myClick():
    myLabel1 = Label(root, text= clicked.get())
    myLabel1.grid(row=2, column=0)

options = [str(x) for x in range(10)]

clicked = StringVar()
clicked.set(options[5])

# Button Widget
myButton = Button(root, text="Show selection", padx=50, pady=15, command=myClick, fg="white", bg="blue")

# Drop Down Boxes
drop = OptionMenu(root, clicked, *options)


# Palce it on a grid
myButton.grid(row=0, column=0)
drop.grid(row=1, column=0)


# Loop
root.mainloop()