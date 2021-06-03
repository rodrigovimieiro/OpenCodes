#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Tk, Label

root = Tk()

# Label Widget
myLabel1 = Label(root, text= "Hello")
myLabel2 = Label(root, text= "Hello World")

# Palce it on a grid
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=5)

# Loop
root.mainloop()