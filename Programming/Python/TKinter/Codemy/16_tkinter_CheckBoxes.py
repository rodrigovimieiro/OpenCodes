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
    myLabel = Label(root, text=var.get())

    myLabel.pack()
    return

c = Checkbutton(root, text= "Check this box", variable=var)

c.pack()


myButton = Button(root, text="Show selection", command=show)

myButton.pack()

# Loop
root.mainloop()