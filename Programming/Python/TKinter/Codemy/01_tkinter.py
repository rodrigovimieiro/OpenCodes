#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:00:19 2021

@author: Rodrigo
"""

from tkinter import Tk, Label

root = Tk()

# Label Widget
myLabel = Label(root, text= "Hello")

# Showing on screen
myLabel.pack()

# Loop
root.mainloop()