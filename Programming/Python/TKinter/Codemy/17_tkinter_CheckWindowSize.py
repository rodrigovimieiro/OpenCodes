#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Checkbutton, StringVar, Tk, Label, Button, Entry, filedialog, OptionMenu, IntVar

root = Tk()

var = IntVar()

def show():
    myLabel = Label(root, text=root.winfo_geometry())

    myLabel.pack()
    return


myButton = Button(root, text="Check info", command=show)

myButton.pack()

# Loop
root.mainloop()