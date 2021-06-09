#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Tk, Label, Button, Entry, filedialog

root = Tk()

# Function for the Button
def myClick():
    root.filename = filedialog.askopenfilename(initialdir="/~", 
                                    title="Select a file",
                                    filetypes=(("png files","*.png"),("all files", "*.*")))
    myLabel1 = Label(root, text= root.filename)
    myLabel1.grid(row=2, column=0)


# Button Widget
myButton = Button(root, text="Open a file", padx=50, pady=15, command=myClick, fg="white", bg="blue")

# Palce it on a grid
myButton.grid(row=0, column=0)

# Loop
root.mainloop()